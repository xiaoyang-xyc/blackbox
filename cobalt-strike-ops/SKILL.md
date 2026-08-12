---
name: cobalt-strike-ops
description: Cobalt Strike 部署/启动/运维。触发：装 CS、Team Server 起不来、客户端连不上。
---

# Cobalt Strike 部署与运维（雷姆实战版）

课堂/授权环境 C2 工具。**仅限课堂靶场/授权环境使用**（司法实践认定 CS 属"专门用于侵入计算机信息系统的程序"）。

## 架构铁律

- **Team Server 只能跑 Linux**（teamserver 脚本 + TeamServerImage，Windows 不支持）
- **Client 任意平台**（Java GUI，连 Team Server 端口）
- 每个包自带 `cobaltstrike.auth`（512B）：**Client/Server 的 auth 必须一致**（md5 核对），不一致握手直接失败

## 本机已知部署（2026-08-11 验证通过）

- 安装包：微信备份 `D:\backup\微信文件备份\2026-07\cs4.9.zip` → 解压到 `D:\tools\cobaltstrike\cs4.9\`（Client/Server 分离目录）
- Kali 侧：`~/cobaltstrike/Server/`（teamserver + TeamServerImage + .cobaltstrike.beacon_keys + cobaltstrike.store）
- 本机客户端：`D:\tools\cobaltstrike\cs4.9\Client\`，启动脚本 `D:\tools\cobaltstrike\启动CS客户端.bat`
- Kali 重启脚本：`~/cobaltstrike/start.sh`（nohup sudo ./teamserver ...）
- **Pwn3rs 培训版端口 = 33000**（非官方默认 50050，teamserver 脚本里 `-Dcobaltstrike.server_port=33000`，部署后先看脚本确认）

## 部署步骤（完整流程）

1. 解压：`unzip -o cs4.9.zip` → 得到 Client/ + Server/ 两目录
2. 传 Server 到 Kali：`scp -r Server kali2026:~/cobaltstrike/`
3. **chmod +x**（scp 后 TeamServerImage/teamserver 可能丢执行位，直接跑报"权限不够"）：`chmod +x TeamServerImage teamserver`
4. 启动（root 必需）：`nohup sudo ./teamserver <KaliIP> '<password>' > ~/cobaltstrike/teamserver.log 2>&1 &`
5. 验证：日志出现 `[+] Team server is up on 0.0.0.0:33000` + `ss -tlnp | grep 33000`
6. 本机客户端（Java 11+ 必需）：`java -XX:+AggressiveHeap -jar cobaltstrike-client.jar`
7. GUI 连接：host=KaliIP:33000，user/pass 填启动时参数；首次连接**点接受证书指纹**

## 坑位清单（全部实测）

| 坑 | 现象 | 解法 |
|---|---|---|
| TeamServerImage 无执行权限 | `./teamserver: 行 47: ./TeamServerImage: 权限不够` | `chmod +x TeamServerImage` |
| 本机 Java 8 | CS 4.9 客户端拒绝/异常 | 需 Java 11+；本机用 `C:\Program Files\Microsoft\jdk-11.0.16.101-hotspot\bin\java.exe` |
| 缺 `-XX:+AggressiveHeap` | 客户端打印 "Use the Cobalt Strike launcher. Don't click the .jar file!" | 启动命令加 `-XX:+AggressiveHeap` |
| agscript 无头模式 | Kali 侧日志 `Remote host terminated the handshake`（auth phase） | **正常现象**——无头模式无法交互确认服务端证书指纹，握手被客户端掐断；GUI 点接受即可。验证连接用 GUI 而非 agscript |
| 端口不是 50050 | 客户端连不上 | 培训定制版看 teamserver 脚本里的 `server_port`（Pwn3rs 版=33000） |
| auth 不匹配 | 连接被拒 | `md5sum Client/cobaltstrike.auth Server/cobaltstrike.auth` 必须一致 |

## 验证命令速查

```bash
# Kali 侧
sudo ss -tlnp | grep 33000              # 端口监听
tail -20 ~/cobaltstrike/teamserver.log  # 启动日志
# 本机侧
timeout 8 bash -c 'echo > /dev/tcp/192.0.2.137/33000' && echo TCP_OK  # 连通性
```

## 客户端启动脚本模板（Windows bat）

```bat
@echo off
cd /d D:\tools\cobaltstrike\cs4.9\Client
"C:\Program Files\Microsoft\jdk-11.0.16.101-hotspot\bin\java.exe" -XX:+AggressiveHeap -jar cobaltstrike-client.jar
pause
```

## 上传文件姿势（CS 没有拖拽上传）

- Beacon 会话控制台：`upload C:\path\to\file.exe`（传到目标机当前目录）
- File Browser 面板有上传按钮（文件选择器），不走拖拽
- 哥哥如果问"为什么不能拖文件进 CS 窗口"——CS 本来就不支持拖拽，用 upload 命令
