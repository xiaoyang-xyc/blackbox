# openEuler安全配置基线 v1.0

## 1 初始部署
## 1.1 文件系统
### 1.1.1 禁止存在无属主或属组的文件或目录

**检查方法：**

查找无属主或属组的文件，无返回表示正常：

```bash
# find `df -l | sed -n '2,$p' | awk '{print $6}' ` -xdev -nouser 2>/dev/null
# find `df -l | sed -n '2,$p' | awk '{print $6}' ` -xdev -nogroup 2>/dev/null
```

### 1.1.2 禁止存在空链接文件

**检查方法：**

查找空链接文件：

```bash
# find ./ -type l -follow
```

排除特定目录搜索：

```bash
# find / -path /var -prune -o -path /run -prune -o -path /proc -prune -o -path /sys -prune -o -path /dev -prune -o -type l -follow
```

仅搜索当前分区：

```bash
# find / -xdev -type l -follow
```

### 1.1.3 禁止存在隐藏的可执行文件

**检查方法：**

查找可执行隐藏文件（无返回为正常）：

```bash
# find / -type f -name "\.*" -perm /+x
```

### 1.1.4 确保全局可写目录已设置sticky位

**检查方法：**

查找全局可写且无粘滞位的目录：

```bash
# find ./ -type d -perm -0002 -a ! -perm -1000
```

### 1.1.5 确保UMASK配置正确

**检查方法：**

- 检查配置文件UMASK值：

  ```bash
  # grep -i "^umask" /etc/bashrc ~/.bashrc
  ```
  
- root用户创建文件确认权限：

  ```bash
  # touch test
  # ll test
  
  
  # mkdir testdir
  # ll -d testdir
  ```
  
- 普通用户创建文件确认权限：

  ```bash
  $ touch test
  $ ll test
  
  $ mkdir testdir
  $ ll -d testdir
  ```

### 1.1.6 禁止存在全局可写的文件

**检查方法：**

使用如下命令在根目录下进行搜索（已排除了“/sys”、“/proc”这两个目录），返回全局可写文件列表，如果返回为空，表示无全局可写文件：

```bash
# find / -path /proc -prune -o -path /sys -prune -o -type f -perm -0002 -exec ls -lg {} \;
```

仅搜索当前分区：

```bash
# find / -xdev -type f -perm -0002 -exec ls -lg {} \;
```

### 1.1.7 确保移除不需要的文件系统挂载支持

**检查方法：**

使用命令检查文件系统（如 cramfs）挂载是否被禁用：

- 输出 `install /bin/true`：已禁止挂载
- 输出 `insmod .../cramfs.ko`：未禁止，显示路径

```bash
# modprobe -n -v cramfs | grep -E '(cramfs|install)'
```

无回显时检查模块是否已加载：

```bash
# lsmod | grep cramfs
```

### 1.1.8 确保无需修改的分区以只读方式挂载

**检查方法：**

检查分区是否只读挂载：

```bash
# mount | grep "\/root\/readonly" | grep "\<ro\>"
```

### 1.1.9 确保无需挂载设备的分区以nodev方式挂载

**检查方法：**

检查未设置nodev的挂载点：

```bash
# mount | grep -v "nodev" | awk -F " " '{print $3}'
```

### 1.1.10 确保无可执行文件的分区以noexec方式挂载

**检查方法：**

检查noexec挂载：

```bash
# mount | grep "\/root\/noexec" | grep "noexec"
```

### 1.1.11 确保可移动设备分区以noexec、nodev方式挂载

**检查方法：**

检查可移动设备noexec、nodev挂载：

```bash
# mount | grep "\/dev\/vda"
```

### 1.1.12 确保无需SUID/SGID的分区以nosuid方式挂载

**检查方法：**

检查未以nosuid方式挂载的分区：

```bash
# mount | grep -v "nosuid"
```

### 1.1.13 确保删除文件不必要的SUID和SGID位

**检查方法：**

可使用如下命令查找系统中的SUID和SGID文件：

```bash
# find / -type f \( -perm -4000 -o -perm -2000 \) -exec ls -l {} \;
```

### 1.1.14 确保关键文件、目录权限最小化

**检查方法：**

查看文件权限：

```bash
# ls -l test
```

### 1.1.15 确保用户可打开文件数量配置正确

**检查方法：**

* 当前软限制：

  ```bash
  # ulimit -Sn
  ```
  
* 当前硬限制：

  ```bash
  # ulimit -Hn
  ```

### 1.1.16 确保软、硬链接文件保护配置正确

**检查方法：**

检查软硬链接保护（返回1表示已启用）：

```bash
# sysctl fs.protected_symlinks
# sysctl fs.protected_hardlinks
```

### 1.1.17 避免使用USB存储

**检查方法：**

使用命令检查 USB 存储设备禁用状态：

- 输出 `install /bin/true`：已禁止
- 输出 `insmod .../usb-storage.ko.xz`：未禁止，显示路径

```bash
# modprobe -n -v usb-storage
```

### 1.1.18 应当分区管理硬盘数据

**检查方法：**

检查目录挂载情况：

```bash
# df | grep -iE "/boot|/tmp|/home|/var|/usr"
```

### 1.1.19 确保LD_LIBRARY_PATH变量定义正确

**检查方法：**

* 检查各配置文件中是否永久设置了 LD_LIBRARY_PATH，涉及文件包括：

  - `/etc/profile`
  - `~/.bashrc`
  - `~/.bash_profile`（用户家目录下的文件，每个用户均有，检查时不可遗漏）
  
  检查内容：profile 中的 LD_LIBRARY_PATH 设置。
  
  ```bash
  # grep "LD_LIBRARY_PATH" /etc/profile ~/.bashrc ~/.bash_profile
  ```
  
* 检查当前用户上下文中是否设置了 `LD_LIBRARY_PATH`：

  - 打印为空：未设置
  - 打印路径：已设置，显示当前值
  
  ```bash
  # echo $LD_LIBRARY_PATH
  ```

### 1.1.20 确保用户PATH变量被严格定义

**检查方法：**

检查root PATH：
```bash
# echo $PATH
```

普通用户PATH示例：
```bash
# echo $PATH
```

### 1.2.1 禁止安装FTP客户端

**检查方法：**

检查FTP是否安装：

```bash
# rpm -q "ftp"
```

### 1.2.2 禁止安装TFTP客户端

**检查方法：**

可检查是否安装了TFTP软件，如果命令返回“package tftp is not installed”，表示未安装：

```bash
# rpm -q "tftp"
```

### 1.2.3 禁止安装Telnet客户端

**检查方法：**

可检查是否安装了Telnet客户端软件，如果命令返回“package telnet is not installed”，表示未安装：

```bash
# rpm -q "telnet"
```

### 1.2.4 禁止安装不安全的SNMP协议版本

**检查方法：** 

可检查snmp是否安装：
```bash
# rpm -qa | grep -E "net-snmp-[0-9]"
```

### 1.2.5 禁止安装python2

**检查方法：**

可检查python2是否安装：
```bash
# rpm -qa | grep "python2-"
```

### 1.2.6 确保yum源配置GPG校验

**检查方法：**

检查GPG公钥：

```bash
# rpm -qa gpg-pubkey*
```

检查repo源配置文件中是否包含有“gpgcheck=1”字段，如果有多个配置文件，则每个配置文件都应该设置该字段：

```bash
# grep -iE "^gpgcheck[ ]*=[ ]*1" /etc/yum.repos.d/ -rn
```

检查repo gpgkey配置：

```bash
# grep -iE "^gpgkey" /etc/yum.repos.d/ -rn
```

### 1.2.7 禁止启用debug-shell服务

**检查方法：**

检查服务是否禁用：
```bash
# systemctl is-enabled debug-shell
```

### 1.2.8 禁止安装rsync服务

**检查方法：**

步骤1：

检查rsync是否安装：

```bash
# rpm -qa | grep "rsync"
```

步骤2：

若已安装，检查服务是否禁用：

```bash
# systemctl is-enabled rsyncd
```

### 1.2.9 禁止安装avahi服务

**检查方法：**

检查avahi是否安装：
```bash
# rpm -qa | grep "avahi"
```

检查avahi服务：

```bash
# systemctl is-enabled avahi-daemon
```

### 1.2.10 禁止安装LDAP服务

**检查方法：**

检查openldap-servers是否安装：

```bash
# rpm -qa | grep "openldap-servers"
```

### 1.2.11 禁止安装打印服务

**检查方法：**

检查CUPS是否安装：
```bash
# rpm -qa cups
```

### 1.2.12 禁止安装NIS服务端

**检查方法：**

检查ypserv是否安装：
```bash
# rpm -qa | grep "ypserv"
```

### 1.2.13 禁止安装NIS客户端

**检查方法：**

检查ypbind是否安装：
```bash
# rpm -qa | grep "ypbind"
```

### 1.2.14 禁止安装LDAP客户端

**检查方法：**

检查openldap-clients是否安装：

```bash
# rpm -qa | grep "openldap-clients"
```

### 1.2.15 禁止安装网络嗅探类工具

**检查方法：**

扫描网络嗅探工具：

* 检查指定 RPM 包是否安装（包名由用户根据实际场景确定）：

  - 返回为空：未安装
  - 返回列表：已安装

  ```bash
  # rpm -qa | grep -iE "^(wireshark-|netcat-|tcpdump-|nmap-|ethereal-)"
  ```

* 检查指定命令是否安装（命令名由用户根据实际场景确定）：

  - 返回为空：未安装
  - 返回列表：已安装
  
  ```bash
  # files=`find / -type f \( -name "wireshark" -o -name  "netcat" -o -name "tcpdump" -o -name "nmap" -o  -name "ethereal" \) 2>/dev/null`;for f in $files;do if [ -n "$f" ];then file $f | grep -i "ELF" ;fi;done
  ```

### 1.2.16 禁止安装调测类工具

**检查方法：**

扫描调测工具：

* 检查指定 RPM 包是否安装（包名由用户按需指定）：

  - 无输出：未安装
  - 有输出：已安装，并列出包名

  ```bash
  # rpm -qa | grep -iE "^strace-|^gdb-|^perf-|^binutils-extra|^appict|^kmem_analyzer_tools"
  ```

* 检查指定命令是否安装（命令名由用户按需指定）：

  - 无输出：未安装
  - 有输出：已安装，并列出命令名
  
  ```bash
  # find / -type f \( -name "gdb" -o -name  "perf" -o -name "strace" -o -name "readelf" \)
  ```

### 1.2.17 禁止安装开发编译类工具

**检查方法：**

扫描开发编译工具：

* 检查指定的 RPM 包是否已安装（包名由用户按需指定）：

  - 无输出：未安装
  - 有输出：已安装并显示包名

  ```bash
  # rpm -qa | grep -iE "^(gcc-|cpp-|mcpp-|flex-|cmake-|make-|rpm-build-|binutils-extra|elfutils-extra|llvm-|rpcgen-|gcc-c++|libtool)"
  ```

* 检查指定命令是否已安装（命令名由用户按需指定）：

  - 无输出：未安装
  - 有输出：已安装并显示命令名
  
  ```bash
  # files=`find / -type f \( -name "gcc" -o -name "g++" -o -name "c++" -o -name  "cpp" -o -name "mcpp" -o -name "flex" -o -name "lex" -o -name  "cmake" -o -name "make" -o -name "rpmbuild" -o  -name "ld" -o -name "ar" -o -name "llc" -o -name "rpcgen" -o -name "libtool" -o -name "javac" -o -name "objdump" -o -name "eu-objdump" -o -name "eu-readelf" -o -name "nm" \) 2> /dev/null`; for f in $files; do if [ -n "$f" ]; then file $f | grep -i "ELF"; fi; done
  ```

### 1.2.18 避免安装X Window系统

**检查方法：**

检查X Window组件：

```bash
# rpm -qa "xorg-x11"
```

### 1.2.19 避免安装HTTP服务

**检查方法：**

可检查是否安装了httpd客户端软件，如果命令返回“package httpd is not installed”，表示未安装：

```bash
# rpm -q "httpd"
```

### 1.2.20 避免安装samba服务

**检查方法：**

可检查是否安装了samba软件，如果命令返回“package samba is not installed”，表示未安装：

```bash
# rpm -q "samba"
```

### 1.2.21 避免启用DNS服务

**检查方法：**

检查服务是否禁用：
```bash
# systemctl is-enabled named
```

### 1.2.22 避免启用NFS服务

**检查方法：**

检查服务是否禁用：
```bash
# systemctl is-enabled nfs-server
```

### 1.2.23 避免启用RPC服务

**检查方法：**

检查服务是否禁用：
```bash
# systemctl is-enabled rpcbind
```

### 1.2.24 避免启用DHCP服务

**检查方法：**

检查服务是否禁用：
```bash
# systemctl is-enabled dhcpd
```

### 2.1.1 禁止无需登录的账号设置登录能力

**检查方法：** 

确认不可登录账号已设置nologin/false或锁定：

- 检查/etc/passwd文件中非登录账号是否都已经被设置正确，命令执行后会列出所有设置了禁止登录的账号，可根据业务场景对这些账号进行比对：

  ```bash
  # cat /etc/passwd | grep "\/sbin\/nologin\|\/bin\/false" | awk -F ":" '{print $1}'
  ```

- 检查/etc/passwd文件中所有允许登录的账号，命令执行后会列出所有允许登录的账号，可根据业务场景对这些账号进行比对：

  ```bash
  # cat /etc/passwd | grep -v "\/sbin\/nologin\|\/bin\/false" | awk -F ":" '{print $1}'
  ```

- 如下命令执行后会列出所有口令被锁定的账号，可根据业务场景对这些账号进行比对：

  ```bash
  # cat /etc/passwd | awk -F ":" '{print $1}' | xargs -I '{}' passwd -S '{}' | awk '($2=="L" || $2=="LK") {print $1}' 
  ```

- 如下命令执行后会列出所有口令未被锁定的账号，可根据业务场景对这些账号进行比对：

  ```bash
  # cat /etc/passwd | awk -F ":" '{print $1}' | xargs -I '{}' passwd -S '{}' | awk '($2!="L" && $2!="LK") {print $1}'
  ```

### 2.1.2 禁止存在不使用的账号

**检查方法：**

查找系统所有账号：

```bash
# cat /etc/passwd | awk  -F ":" '{print $1}'  
```

按照以下步骤进行查询和判断：

- 在未部署业务的平台上，使用上述命令获取所有账号信息；
- 在完整部署业务的平台上，使用上述命令获取所有账号信息；
- 对比两者返回结果，对差异部分进行分析，是否符合业务设计。

### 2.1.3 确保不同账号初始分配不同的组ID

**检查方法：**

检查账号组ID唯一性：

```bash
# cat /etc/passwd | awk -F ":" '{a[$4]++}END{for(i in a){if(a[i]!=1 && i!=0){print i, a[i]}}}'
1003 2
```

### 2.1.4 禁止存在UID为0的非root账号

**检查方法：**

检查UID=0的非root账号：

```bash
# cat /etc/passwd | awk -F ":" '{if($1!="root" && $3==0){print $1, $3}}'
test 0
```

### 2.1.5 确保账号、组及口令文件权限正确

**检查方法：**

检查文件权限：

```bash
# ll /etc/passwd
# ll /etc/shadow
# ll /etc/group
# ll /etc/gshadow
# ll /etc/passwd-
# ll /etc/shadow-
# ll /etc/group-
# ll /etc/gshadow-
```

### 2.1.6 确保账号拥有自己的Home目录

**检查方法：**

检查Home目录存在及属主：

```bash
#!/bin/bash  
grep -E -v '^(halt|sync|shutdown)' "/etc/passwd" | awk -F ":" '($7 != "/bin/false" && $7 != "/sbin/nologin" && $7 != "/usr/sbin/nologin") {print $1 " " $6}' | while read name home;
do
    if [ ! -d "$home" ]; then
        echo "No home folder \"$home\" of \"$name\"."
    else
            owner=`ls -l -d $home | awk -F " " '{print $3}'`
        if [ "$owner" != "$name" ]; then
            echo "\"$home\" is owned by $owner, not \"$name\"."
        fi
    fi
done
```

### 2.1.7 确保/etc/passwd中的组都存在

**检查方法：**

检查用户组设置：

```bash
#!/bin/bash
grep -E -v '^(halt|sync|shutdown)' "/etc/passwd" | awk -F ":" '($7 != "/bin/false" && $7 != "/sbin/nologin") {print $4}' | while read group;
do
    grep -q -P "^.*?:[^:]*:$group:" "/etc/group"
    if [ $? -ne 0 ]; then
        echo "Group $group not found"
    fi
done
```

### 2.1.8 确保UID唯一

**检查方法：**

检查UID唯一性：

```bash
# cat /etc/passwd | awk -F ":" '{a[$3]++}END{for(i in a){if(a[i]!=1){print i, a[i]}}}'
```

### 2.1.9 确保账号名唯一

**检查方法：**

检查账号名唯一性：

```bash
# cat /etc/passwd | awk -F ":" '{a[$1]++}END{for(i in a){if(a[i]!=1){print i, a[i]}}}'
```

### 2.1.10 确保GID唯一

**检查方法：**

检查GID唯一性：

```bash
# cat /etc/group | awk -F ":" '{a[$3]++}END{for(i in a){if(a[i]!=1){print i, a[i]}}}'
```

### 2.1.11 确保组名唯一

**检查方法：**

检查组名唯一性：

```bash
# cat /etc/group | awk -F ":" '{a[$1]++}END{for(i in a){if(a[i]!=1){print i, a[i]}}}'
```

### 2.1.12 应当正确设置账号有效期

**检查方法：**

检查账号过期时间设置：

检查账号过期时间：

```bash
# cat /etc/shadow | grep "test" | awk -F ":" '{if($8!=""){print $8}}'
```

### 2.1.13 避免Home目录下存在.forward文件

**检查方法：**

使用如下脚本进行检查，如果无返回输出，则表示所有Home目录下无“.forward”文件：

```bash
#!/bin/bash  
grep -E -v '^(halt|sync|shutdown)' "/etc/passwd" | awk -F ":" '($7 != "/bin/false" && $7 != "/sbin/nologin") {print $6}' | while read home;
do
    if [ -d "$home" ]; then
        find $home -name ".forward"
    fi
done
```

### 2.1.14 避免Home目录下存在.netrc文件

**检查方法：**

使用如下脚本进行检查，如果无返回输出，则表示所有Home目录下无“.netrc”文件：

```bash
#!/bin/bash
grep -E -v '^(halt|sync|shutdown)' "/etc/passwd" | awk -F ":" '($7 != "/bin/false" && $7 != "/sbin/nologin") {print $6}' | while read home;
do
    if [ -d "$home" ]; then
        find $home -name ".netrc"
    fi
done
```

### 2.2.1 确保口令复杂度设置正确

**检查方法：**

方法1：
- /etc/pam.d/system-auth和/etc/pam.d/password-auth分别提供该功能项的配置，不同应用程序或者服务对应的配置项，需根据各自include的配置文件而定：

  ```bash
  # grep system-auth /etc/pam.d/ -r
  
  ```
  
- 在/etc/pam.d/system-auth文件中检查“设置口令复杂度”的配置情况：

  ```bash
  # grep pam_pwquality /etc/pam.d/system-auth
  password    requisite     pam_pwquality.so minlen=8 minclass=3 enforce_for_root try_first_pass local_users_only retry=3 dcredit=0 ucredit=0 lcredit=0 ocredit=0
  ```

方法2：
- 在/etc/security/pwquality.conf文件中检查“设置口令复杂度”的配置情况：

  ```bash
  #cat /etc/security/pwquality.conf
  ```

### 2.2.2 禁止使用历史口令

**检查方法：**

- 在/etc/pam.d/system-auth文件中检查“禁用历史口令”的配置情况，检查配置remember值是否不小于5：

  ```bash
  # grep pam_pwhistory /etc/pam.d/system-auth
  ```
  
- 在/etc/pam.d/password-auth文件中检查“禁用历史口令”的配置情况，检查配置remember值是否不小于5：

  ```bash
  # grep pam_pwhistory /etc/pam.d/password-auth
  ```

### 2.2.3 确保用户修改自身口令时需验证旧口令

**检查方法：**

- root账号更改口令情况如下：

  ```bash
  # passwd
  ```
  
- 普通账号（如test）更改口令：

  ```bash
  $ passwd
  ```

### 2.2.4 确保口令中不包含账号字符串

**检查方法：**

- /etc/pam.d/system-auth和/etc/pam.d/password-auth分别提供该功能项的配置，不同应用程序或者服务对应的配置项，需根据各自include的配置文件而定：

  ```bash
  # grep system-auth /etc/pam.d/ -r
  ```
  
- 在/etc/pam.d/system-auth文件中检查“口令中不包含账号字符串”的配置情况，不应包含“usercheck=0”字段：

  ```bash
  # grep pam_pwquality /etc/pam.d/system-auth
  ```

### 2.2.5 确保口令使用强Hash算法加密

**检查方法：**

- /etc/pam.d/system-auth和/etc/pam.d/password-auth分别提供该功能项的配置，不同应用程序或者服务对应的配置项，需根据各自include的配置文件而定：

  ```bash
  # grep system-auth /etc/pam.d/ -r
  ```
  
- 在/etc/pam.d/system-auth文件中检查“口令使用强Hash算法加密”的配置情况：

  ```bash
  # grep sha512 /etc/pam.d/system-auth
  ```

### 2.2.6 确保弱口令字典设置正确

**检查方法：**

方法1：
- /etc/pam.d/system-auth和/etc/pam.d/password-auth分别提供该功能项的配置，不同应用程序或者服务对应的配置项，需根据各自include的配置文件而定：

  ```bash
  # grep system-auth /etc/pam.d/ -r
  ```
  
- 在/etc/pam.d/system-auth文件中检查“设置弱口令字典”的配置情况：

  ```bash
  # grep pam_pwquality /etc/pam.d/system-auth
  ```
  - 使用如下命令，导出字典库到文件dictionary.txt中：

  ```bash
  # cracklib-unpacker /usr/share/cracklib/pw_dict > dictionary.txt
  ```

方法2：
- 在/etc/security/pwquality.conf文件中检查“弱口令字典”的配置情况：

  ```bash
  # grep -rnR "dictcheck" /etc/security/pwquality.conf
  ```
  ### 2.2.7 确保口令有效期设置正确

**检查方法：**

- 检查/etc/login.defs文件中是否已经配置相关字段：

  ```bash
  # grep ^PASS_MAX_DAYS /etc/login.defs 
  # grep ^PASS_WARN_AGE /etc/login.defs 
  # grep ^PASS_MIN_DAYS /etc/login.defs
  ```
  
- 检查/etc/shadow文件中指定账号的配置是否正确：

  ```bash
  # grep ^test: /etc/shadow 
  ```

### 2.2.8 禁止空口令登录

**检查方法：**

检查SSH空口令登录：

```bash
# grep ^PermitEmptyPasswords /etc/ssh/sshd_config | grep no
```

### 2.2.9 确保Grub已设置口令保护

**检查方法：**

UEFI模式下：

方法1：

- 查看grub.cfg配置文件是否存在password_pbkdf2相关配置：

  ```bash
  # grep password_pbkdf2 /boot/efi/EFI/openEuler/grub.cfg
  ```
  
- GRUB2_PASSWORD是定义在user.cfg文件中的口令密文，“xxxx”表示密文内容：

  ```bash
  # cat /boot/efi/EFI/openEuler/user.cfg
  ```

方法2：

- 查看grub.cfg配置文件是否存在password_pbkdf2相关配置：

  ```bash
  # grep grub.pbkdf2.sha512.10000 /boot/efi/EFI/openEuler/grub.cfg
  ```

legecy模式下：

方法1：

- 查看grub.cfg配置文件是否存在password_pbkdf2相关配置：

  ```bash
  # grep password_pbkdf2 /boot/grub2/grub.cfg
  ```
  
- GRUB2_PASSWORD是定义在user.cfg文件中的口令密文，“xxxx”表示密文内容：

  ```bash
  # cat /boot/grub2/user.cfg
  ```

方法2：

- 查看grub.cfg配置文件是否存在password_pbkdf2相关配置：

  ```bash
  # grep grub.pbkdf2.sha512.10000 /boot/grub2/grub.cfg
  ```

### 2.2.10 确保单用户模式已设置口令保护

**检查方法：**

检查rescue/emergency登录方式：

```bash
# grep /systemd-sulogin-shell /usr/lib/systemd/system/rescue.service
# grep /systemd-sulogin-shell /usr/lib/systemd/system/emergency.service
```

### 2.2.11 确保账号在首次登录时强制修改口令

**检查方法：**

检查/etc/shadow文件中指定账号的配置是否正确：

```bash
# grep ^test: /etc/shadow 
```

此处，以冒号“:”分割的第3个字段，如果是0，表示此账号对应口令已被强制设置为过期。

### 2.3.1 确保登录失败一定次数后锁定账号

**检查方法：**

- /etc/pam.d/system-auth和/etc/pam.d/password-auth分别提供该功能项的配置，不同应用程序或者服务对应的配置项，需根据各自include的配置文件而定：

  ```bash
  # grep system-auth /etc/pam.d/ -r
  ```
  
- 在/etc/pam.d/system-auth文件中检查“连续失败登录次数”的配置情况：

  ```bash
  # grep deny /etc/pam.d/system-auth
  ```
  
- 在/etc/pam.d/system-auth文件中检查“锁定时间”的配置情况：

  ```bash
  # grep unlock_time /etc/pam.d/system-auth
  ```

### 2.3.2 确保会话超时时间设置正确

**检查方法：**

```bash
# grep "^export TMOUT" /etc/profile
```

### 2.3.3 确保Warning Banners包含合理的信息

**检查方法：**

* 通过cat命令，查看/etc/motd、/etc/issue、/etc/issue.net三个文件中警告信息是否合理，是否存在系统版本、应用服务器类型、功能等信息；

* 通过ll命令查看/etc/motd、/etc/issue、/etc/issue.net三个文件权限是否为644；

### 2.3.4 应当正确配置Banner路径

**检查方法：**

使用grep命令查看配置，如果返回为空，表示未配置：

```bash
# grep -i "^Banner" /etc/ssh/sshd_config
```

### 2.4.1 限制历史命令记录数量

**检查方法：**

1. 查看环境变量 HISTSIZE 设置的值：

  ```bash
  # echo $HISTSIZE
  ```

2. 检查HISTSIZE值：

  ```bash
  # grep -iP "^HISTSIZE" /etc/profile
  ```
### 2.4.2 应当启用enforce模式

**检查方法：**

检查SELinux运行模式：

```bash
# getenforce
```

检查SELinux默认模式：

```bash
# grep "^SELINUX=" /etc/selinux/config
```

### 2.4.3 应当正确配置SELinux策略

**检查方法：**

运行以下命令查看当前系统策略，建议配置为targeted：

```bash
# sestatus | grep 'Loaded policy name'
```

检查SELinux异常拒绝：

```bash
# grep avc /var/log/audit/audit.log*
```

### 2.4.4 确保su受限使用

**检查方法：**

检查su wheel限制：

```bash
# grep pam_wheel.so /etc/pam.d/su | grep required
```

### 2.4.5 确保普通用户通过sudo运行特权程序

**检查方法：**

检查sudo配置：

```bash
# grep "(root)" /etc/sudoers
```

说明：示例中“/bin/ping”为可以使用sudo执行的程序。实际上，具体的程序由用户根据业务场景进行配置。

### 2.4.6 确保sudoers不能配置低权限用户可写的脚本

**检查方法：**

检查sudo特权程序写权限：

```bash
# grep "(root)" /etc/sudoers
# ll /bin/xxx.sh
```

### 2.4.7 确保普通用户不能借助pkexec配置提权root

**检查方法：**

检查pkexec权限：

```bash
# cat /etc/polkit-1/rules.d/50-default.rules
```

### 2.4.8 确保su命令继承用户环境变量不会引入提权

**检查方法：**

检查ALWAYS_SET_PATH：

```bash
# cat /etc/login.defs | grep ALWAYS_SET_PATH=yes
```

### 2.4.9 避免root用户本地接入系统

**检查方法：**

* 检查/etc/pam.d/system-auth文件中是否添加了account类型的pam_access.so模块，且该模块必须在sufficient控制行之前加载：

  ```bash
  # cat /etc/pam.d/system-auth
  ```
  
* 并且，检查/etc/security/access.conf文件中是否设置对root用户登录tty1的限制：

  ```bash
  # grep "^\-:root" /etc/security/access.conf
  ```

* 使用串口尝试登录root账号，确认是否拒绝登录。如果拒绝登录，串口打印信息如下：

  ```bash
    localhost login: root
  Password:
  Permission denied 
  ```

### 2.4.10 避免使用标签为unconfined_service_t的程序

**检查方法：**

检查unconfined_service_t进程：

```bash
# ps -eZ | grep unconfined_service_t
```

### 2.5.1 应当启用IMA度量

**检查方法：**

* 首先确认当前内核启动参数中是否配置了integrity=1，如果查不到该参数，则说明IMA没有开启：

  ```bash
  # cat /proc/cmdline | grep integrity=1
  ```
  
* 确认IMA开启后，查看/sys/kernel/security/ima/runtime_measurement_count文件中存储的度量记录数，如果该值大于1，则表示已配置IMA度量策略：

  ```bash
  # cat /sys/kernel/security/ima/runtime_measurements_count
  ```

### 2.5.2 应当启用aide入侵检测

**检查方法：**

* 检查是否安装了aide软件包（如果返回-bash: aide: command not found，表示未安装）：

  ```bash
  # aide --version
  ```
  
* 检查/etc/aide.conf文件中是否已经配置需要监控的文件或目录，举例仅表示默认配置监控目录中的/boot目录，用户若自行配置了需要监控的文件或目录，则确认相应的文件或目录已配置即可：

  ```bash
  # grep boot /etc/aide.conf | grep NORMAL
  ```
  
* 检查是否存在基准数据库：

  ```bash
  # ls /var/lib/aide/aide.db.gz
  ```

### 2.6.1 应当启用haveged服务

**检查方法：**

检查环境中haveged服务是否处于正常运行状态：

```bash
# systemctl is-active haveged
```

### 2.6.2 应当设置全局加解密策略配置不低于DEFAULT

**检查方法：**

检查是否配置LEGACY模式：

```bash
# cat /etc/crypto-policies/config | grep "LEGACY"
```

亦可通过如下方式检查当前配置的模式：

```bash
# cat /etc/crypto-policies/config | grep -v "^#"
```

### 3.1.1 避免使用不常见网络服务

**检查方法：**

- 使用 modprobe 检查 sctp 模块：

  - 输出 `install /bin/true`：已禁止
  - 输出 `insmod .../sctp.ko`：未禁止，同时显示 ko 路径
  - 输出 `modprobe: FATAL: Module sctp not found ...`：模块不存在，无需处理
  
  ```bash
  # modprobe -n -v sctp
  ```
  
- 使用 modprobe 检查 tipc 模块：

  - 输出 `install /bin/true`：已禁止
  - 输出 `insmod .../tipc.ko`：未禁止，显示路径（可能附带依赖 ko，如 udp_tunnel、ip6_udp_tunnel，忽略即可）
  - 输出 `modprobe: FATAL: Module tipc not found ...`：模块不存在，无需处理
  
  ```bash
  # modprobe -n -v tipc
  ```

### 3.1.2 避免使用无线网络

**检查方法：**

检查无线网络：

```bash
# nmcli radio all
```

### 3.2.1 应当启用firewalld服务

**检查方法：**

检查firewalld启用：

```bash
# service firewalld status 2>&1 | grep Active
# service iptables status 2>&1 | grep Active
# service nftables status 2>&1 | grep Active
```

### 3.2.2 应当配置正确的默认区域

**检查方法：**

使用firewall-cmd命令查询默认区域配置：

```bash
# firewall-cmd --get-default-zone
```

### 3.2.3 应当确保网络接口绑定正确区域

**检查方法：**

检查各个区域配置的接口情况：

```bash
# firewall-cmd --get-active-zones
```

### 3.2.4 避免开启不必要的服务和端口

**检查方法：**

检查firewalld区域配置：

```bash
# for zone in $(firewall-cmd --get-active-zones | grep -v "^[[:space:]]"); do firewall-cmd --list-all --zone=$zone; done
```

### 3.2.5 应当启用iptables服务

**检查方法：**

检查iptables启用：

```bash
# service iptables status 2>&1 | grep Active
# service firewalld status 2>&1 | grep Active
# service nftables status 2>&1 | grep Active
```

检查ip6tables服务是否已经启用：

```bash
# service ip6tables status 2>&1 | grep Active
```

### 3.2.6 应当正确配置iptables默认拒绝策略

**检查方法：**

检查IPv4默认拒绝策略：

```bash
# iptables -L | grep -E "INPUT|OUTPUT|FORWARD"
```

检查IPv6默认拒绝策略：

```bash
# ip6tables -L | grep -E "INPUT|OUTPUT|FORWARD"
```

### 3.2.7 应当正确配置iptables loopback策略

**检查方法：**

检查IPv4回环地址策略：

```bash
# iptables -L INPUT -v -n
# iptables -L OUTPUT -v -n
```

检查IPv6回环地址策略：

```bash
# ip6tables -L INPUT -v -n
# ip6tables -L OUTPUT -v -n
```

### 3.2.8 应当正确配置iptables INPUT策略

**检查方法：**

检查INPUT链策略：

```bash
# iptables -L INPUT -v -n
```

检查IPv6：

```bash
# ip6tables -L INPUT -v -n
```

### 3.2.9 应当正确配置iptables OUTPUT策略

**检查方法：**

检查OUTPUT链策略：

```bash
# iptables -L OUTPUT -v -n
```

检查IPv6：

```bash
# ip6tables -L OUTPUT -v -n
```

### 3.2.10 应当正确配置iptables INPUT、OUTPUT关联策略

**检查方法**检查方法：**

检查INPUT和OUTPUT链是否配置了关联策略：

```bash
# iptables -L
```

检查IPv6：

```bash
# ip6tables -L
```

### 3.2.11 应当启用nftables服务

**检查方法：**

检查nftables启用：

```bash
# service nftables status 2>&1 | grep Active
# service firewalld status 2>&1 | grep Active
# service iptables status 2>&1 | grep Active
```

### 3.2.12 应当配置nftables默认拒绝策略

**检查方法：**

检查nftables DROP策略：

```bash
# nft list ruleset
```

### 3.2.13 应当配置nftables loopback策略

**检查方法：**

查看回环地址策略：

- input链：lo 设备 ACCEPT；非 lo 且源地址 127.0.0.0/8 DROP
- output链：源地址 127.0.0.0/8 ACCEPT

IPv4配置：

```bash
# nft list ruleset
```

IPv6配置：

```bash
# nft list ruleset
```

### 3.2.14 应当正确配置nftables input策略

**检查方法：**

检查nftables input策略：

```bash
# nft list chain inet test input
```

### 3.2.15 应当正确配置nftables output策略

**检查方法：**

检查nftables output策略：

```bash
# nft list chain inet test output
```

### 3.2.16 应当正确配置nftables input、output关联策略

**检查方法**检查方法：**

检查input和output链是否配置了关联策略：

```bash
# nft list ruleset
```

### 3.3.1 确保SSH服务版本配置正确

**检查方法：**

通过如下命令，查看返回是否为2：

```bash
# grep "^Protocol" /etc/ssh/sshd_config
```

### 3.3.2 确保SSH服务认证方式配置正确

**检查方法：**

检查SSH关键配置项：tion和PubkeyAuthentication至少有一个为yes：

```bash
# grep "^PasswordAuthentication\|^PubkeyAuthentication\|^ChallengeResponseAuthentication\|^IgnoreRhosts\|^HostbasedAuthentication" /etc/ssh/sshd_config
```

### 3.3.3 确保SSH密钥交换算法配置正确

**检查方法：**

检查SSH密钥交换算法：

```bash
# grep ^KexAlgorithms /etc/ssh/sshd_config
```

### 3.3.4 确保用户认证密钥算法配置正确

**检查方法：**

通过如下方法检查配置：

```bash
# grep "^PubkeyAcceptedKeyTypes" /etc/ssh/sshd_config
```

### 3.3.5 确保PAM认证使能

**检查方法：**

使用grep命令查看配置：

```bash
# grep -i "^UsePAM" /etc/ssh/sshd_config
```

### 3.3.6 确保SSH服务MACs算法配置正确

**检查方法：**

使用grep命令查看配置，如果返回为空，表示未配置：

```bash
# grep -i "^MACs" /etc/ssh/sshd_config
```

### 3.3.7 确保SSH服务密码算法配置正确

**检查方法：**

使用grep命令查看配置，如果返回为空，表示未配置：

```bash
# grep -i "^Ciphers" /etc/ssh/sshd_config
```

### 3.3.8 禁止SSH服务配置加密算法覆盖策略

**检查方法：**

检查 `/etc/sysconfig/sshd` 中 `CRYPTO_POLICY=`：

- 为空或被注释：未配置加密算法覆盖策略
- 有值：已配置

```bash
# grep "^\s*CRYPTO_POLICY=" /etc/sysconfig/sshd | cut -d "=" -f 2-
'-oCiphers=aes256-ctr,aes192-ctr,aes128-ctr -oMACS=hmac-sha2-512,hmac-sha2-256'
```

### 3.3.9 确保禁用root用户通过SSH登录

**检查方法：**

检查SSH PermitRootLogin：

 ```bash
 # sshd -T -C user=root -C host="$(hostname)" -C addr="$(grep $(hostname) /etc/hosts | awk '{print $1}')" | grep permitrootlogin
 # grep -Ei '^\s*PermitRootLogin\s+yes' /etc/ssh/sshd_config
 ```

### 3.3.10 应当正确配置SSH服务日志级别

**检查方法：**

检查日志级别：

```bash
# grep -i "^LogLevel" /etc/ssh/sshd_config
```

### 3.3.11 应当正确配置SSH服务接口

**检查方法：**

检查监听地址配置：

```bash
# grep -i "^ListenAddress" /etc/ssh/sshd_config
```

### 3.3.12 应当正确配置SSH并发未认证连接数

**检查方法：**

使用grep命令查看配置，如果返回为空，表示未配置：

```bash
# grep -i "^MaxStartups" /etc/ssh/sshd_config
```

### 3.3.13 应当正确配置单个SSH连接允许的并发会话数

**检查方法：**

使用grep命令查看配置，如果返回为空，表示未配置：

```bash
# grep -i "^MaxSessions" /etc/ssh/sshd_config
```

### 3.3.14 禁止使用X11 Forwarding

**检查方法：**

使用grep命令查看配置：

```bash
# grep -i "^X11Forwarding" /etc/ssh/sshd_config
```

### 3.3.15 应当正确配置MaxAuthTries

**检查方法：**

使用grep命令查看配置，如果返回为空，表示未配置：

```bash
# grep -i "^MaxAuthTries" /etc/ssh/sshd_config
```

### 3.3.16 禁止使用PermitUserEnvironment

**检查方法：**

使用grep命令查看配置：

```bash
# grep -i "^PermitUserEnvironment" /etc/ssh/sshd_config
```

### 3.3.17 应当正确配置LoginGraceTime

**检查方法：**

使用grep命令查看配置：

```bash
# grep -i "^LoginGraceTime" /etc/ssh/sshd_config
```

### 3.3.18 禁止SSH服务预设置authorized_keys

**检查方法：**

检查authorized_keys预配置：

```bash
# find /home/ /root/ -name authorized_keys 
```

### 3.3.19 禁止SSH服务预设置known_hosts

**检查方法：**

检查known_hosts预配置：

```bash
# find /home/ /root/ -name known_hosts 
```

### 3.3.20 禁止SSH服务配置弃用的选项

**检查方法：**

检查SSH配置兼容性：

```bash
# sshd -t
```

### 3.3.21 确保禁用SSH的TCP转发功能

**检查方法：**

检查SSH allowtcpforwarding：

```bash
# sshd -T -C user=root -C host="$(hostname)" -C addr="$(grep $(hostname) /etc/hosts | awk '{print $1}')" | grep allowtcpforwarding
# grep -Ei '^\s*AllowTcpForwarding\s+yes\b' /etc/ssh/sshd_config
```

### 3.3.22 应当正确配置认证黑白名单

**检查方法：**

检查配置项：

```bash
# grep "^AllowUsers\|^AllowGroups\|^DenyUsers\|^DenyGroups" /etc/ssh/sshd_config
```

### 3.4.1 确保crontab执行的脚本非属主用户不可写

**检查方法：**

检查crontab脚本写权限：

```bash
# ls /etc/crontab
  *  *  *  *  * user-name  /bin/xxx.sh
# ll /bin/xxx.sh
```

### 3.4.2 确保cron守护进程正常启用

**检查方法**检查方法：**

执行以下命令来确定 cron 守护进程是否正常启用：

```bash
# systemctl is-enabled crond
```

如结果为enabled，则视为通过此项检查。

### 3.4.3 确保at、cron配置正确

**检查方法：**

* 首先要确保系统中cron服务已经启用：

  ```bash
  # systemctl is-enabled crond
  ```

  请确认返回结果是enabled。

* 确认/etc/crontab文件和/etc/cron.hourly、/etc/cron.daily、/etc/cron.weekly、/etc/cron.monthly、/etc/cron.d目录的UID和GID都是0，且不允许group和other用户访问：  

  ```bash
  # stat /etc/crontab
  ```
  
* 确认黑名单文件/etc/cron.deny和/etc/at.deny不存在，确认白名单文件/etc/cron.allow和/etc/at.allow设置了正确的权限，即UID和GID都是0，且不允许group和other用户访问：

  ```bash
  # stat /etc/cron.allow
  ```

### 3.5.1 确保内核ASLR已启用

**检查方法：**

输入以下命令并检查相应的命令返回是否为2：

```bash
# cat /proc/sys/kernel/randomize_va_space
```

### 3.5.2 确保dmesg访问权限配置正确

**检查方法：**

检查/etc/sysctl.conf文件中是否已经配置相关字段，“kernel.dmesg_restrict=1”表示已经设置dmesg的访问限制：

```bash
# grep kernel.dmesg_restrict /etc/sysctl.conf
```

### 3.5.3 确保正确配置内核参数kptr_restrict

**检查方法：**

输入以下命令并检查相应的命令返回值是否为1：

```bash
# sysctl kernel.kptr_restrict
```

### 3.5.4 确保内核SMAP已启用

**检查方法：**

检查CPU是否支持SMAP：
```bash
# cat /proc/cpuinfo | grep "smap"
```

检查SMAP启动参数：

```bash
# cat /proc/cmdline | grep -i "nosmap"
```

### 3.5.5 确保内核SMEP已启用

**检查方法：**

检查CPU是否支持SMEP：
```bash
# cat /proc/cpuinfo | grep "smep"
```

检查SMEP启动参数：

```bash
# cat /proc/cmdline | grep -i "nosmep"
```

### 3.5.6 禁止系统响应ICMP广播报文

**检查方法：**

检查内核参数icmp_echo_ignore_broadcasts（应为1）：

```bash
# sysctl net.ipv4.icmp_echo_ignore_broadcasts
```

```bash
# grep "net.ipv4.icmp_echo_ignore_broadcasts" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.7 禁止接收ICMP重定向报文

**检查方法：**

检查内核参数（应为0）：

```bash
# sysctl net.ipv4.conf.all.accept_redirects && sysctl net.ipv6.conf.all.accept_redirects && sysctl net.ipv4.conf.all.secure_redirects && sysctl net.ipv4.conf.default.secure_redirects
```

```bash
# grep "net.ipv4.conf.all.accept_redirects" /etc/sysctl.conf /etc/sysctl.d/*
# grep "net.ipv6.conf.all.accept_redirects" /etc/sysctl.conf /etc/sysctl.d/*
# grep "net.ipv4.conf.all.secure_redirects" /etc/sysctl.conf /etc/sysctl.d/*
# grep "net.ipv4.conf.default.secure_redirects" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.8 禁止转发ICMP重定向报文

**检查方法：**

检查内核参数send_redirects（应为1）：

```bash
# sysctl net.ipv4.conf.all.send_redirects
# sysctl net.ipv4.conf.default.send_redirects
```

```bash
# grep "net.ipv4.conf.all.send_redirects" /etc/sysctl.conf /etc/sysctl.d/*
# grep "net.ipv4.conf.default.send_redirects" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.9 应当忽略所有ICMP请求

**检查方法：**

检查内核参数icmp_echo_ignore_all（应为1）：

```bash
# sysctl net.ipv4.icmp_echo_ignore_all
```

```bash
# grep "net.ipv4.icmp_echo_ignore_all" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.10 确保丢弃伪造的ICMP报文，不记录日志

**检查方法：**

检查内核参数icmp_ignore_bogus_error_responses（应为1）：

```bash
# sysctl net.ipv4.icmp_ignore_bogus_error_responses
```

```bash
# grep "net.ipv4.icmp_ignore_bogus_error_responses" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.11 确保反向地址过滤已启用

**检查方法：**

检查内核参数rp_filter（应为1）：

```bash
# sysctl net.ipv4.conf.all.rp_filter
# sysctl net.ipv4.conf.default.rp_filter
```

```bash
# grep "net.ipv4.conf.all.rp_filter" /etc/sysctl.conf /etc/sysctl.d/*
# grep "net.ipv4.conf.default.rp_filter" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.12 禁止IP转发

**检查方法：**

检查内核参数ip_forward（应为0）：

```bash
# sysctl net.ipv4.ip_forward
# sysctl net.ipv6.conf.all.forwarding
```

```bash
# grep -E -s "^\s*net\.ipv4\.ip_forward\s*=\s*1" /etc/sysctl.conf /etc/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /run/sysctl.d/*.conf
无任何输出
# grep -E -s "^\s*net\.ipv6\.conf\.all\.forwarding\s*=\s*1" /etc/sysctl.conf /etc/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /run/sysctl.d/*.conf
无任何输出
```

### 3.5.13 禁止报文源路由

**检查方法：**

检查内核参数（应为0）：

```bash
# sysctl net.ipv4.conf.all.accept_source_route
# sysctl net.ipv4.conf.default.accept_source_route
# sysctl net.ipv6.conf.all.accept_source_route
# sysctl net.ipv6.conf.default.accept_source_route
```

### 3.5.14 确保TCP-SYN cookie保护已启用

**检查方法：**

检查内核参数tcp_syncookies（应为1）：

```bash
# sysctl net.ipv4.tcp_syncookies
```

```bash
# grep "^net.ipv4.tcp_syncookies" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.15 应当记录仿冒、源路由以及重定向报文日志

**检查方法：**

检查内核参数log_martians（应为1）：

```bash
# sysctl net.ipv4.conf.all.log_martians
# sysctl net.ipv4.conf.default.log_martians
```

```bash
# grep "^net.ipv4.conf.all.log_martians" /etc/sysctl.conf /etc/sysctl.d/*
# grep "^net.ipv4.conf.default.log_martians" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.16 避免开启tcp_timestamps

**检查方法：**

检查内核参数tcp_timestamps（应为0）：

```bash
# sysctl net.ipv4.tcp_timestamps
```

```bash
# grep "^net.ipv4.tcp_timestamps" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.17 确保TIME_WAIT TCP协议等待时间已配置

**检查方法：**

检查内核参数tcp_fin_timeout：

```bash
# sysctl net.ipv4.tcp_fin_timeout
```
```bash
# grep "^net.ipv4.tcp_fin_timeout" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.18 应当正确配置SYN_RECV状态队列数量

**检查方法：**

检查内核参数tcp_fin_timeout：

```bash
# sysctl net.ipv4.tcp_max_syn_backlog
```

```bash
# grep "^net.ipv4.tcp_max_syn_backlog" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.19 禁止使用ARP代理

**检查方法：**

检查内核参数proxy_arp（应为1）：

```bash
# sysctl net.ipv4.conf.all.proxy_arp
# sysctl net.ipv4.conf.default.proxy_arp
```

```bash
# grep "^net.ipv4.conf.all.proxy_arp" /etc/sysctl.conf /etc/sysctl.d/*
# grep "^net.ipv4.conf.default.proxy_arp" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.20 确保core dump配置正确

**检查方法：**

* 禁用场景的检查方法：

  输入以下命令并检查相应的命令返回：

  ```bash
  # ulimit -c
  ```
  
  或者检查文件/etc/security/limits.conf，是否包含配置行“* hard core 0”。
  
* 限制场景的检查方法：

  检查core dump目录限制：
  
  ```bash
  #!/bin/bash  
  core_path=$(sysctl kernel.core_pattern | awk -F"^[[:space:]]*kernel.core_pattern[[:space:]]*=[[:space:]]*" '{print $2}')
  [[ "${core_path}" =~ ^/.+ ]] || { echo "kernel.core_pattern[${core_path}] must be started with /"; exit 1; }
  core_dir=$(dirname "${core_path}")
  [[ -d "${core_dir}" ]] || { echo "kernel.core_pattern dir[${core_dir}] not exist"; exit 1; }
  rights_digit=$(stat -c%a "${core_dir}")
  [[ "${rights_digit}" =~ ^700$ || "${rights_digit}" =~ ^1770$ || "${rights_digit}" =~ ^1777$ ]] || { echo "rights[${rights_digit}] of dir[${core_dir}] not safe, must be 700 or 1770 or 1777"; exit 1; }
  exit 0
  ```

### 3.5.21 禁止使用SysRq键

**检查方法：**

检查内核参数sysrq（应为0）：

```bash
# cat /proc/sys/kernel/sysrq
```

```bash
# grep "^kernel.sysrq" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.22 应当正确配置内核参数ptrace_scope

**检查方法：**

检查内核参数log_martians：

```bash
# sysctl kernel.yama.ptrace_scope
```

```bash
# grep "^kernel.yama.ptrace_scope" /etc/sysctl.conf /etc/sysctl.d/*
```

### 3.5.23 应当启用seccomp

**检查方法：**

确定进程PID：
```bash
# ps -aux | grep "test_seccomp" 
```

根据PID查询进程seccomp状态：

- 返回值 0：未开启
- 1：STRICT 模式
- 2：FILTER 模式

```bash
# cat /proc/[pid]/status | grep "Seccomp"
```

### 3.6.1 应当正确配置ntpd服务

**检查方法：**

- 检查ntpd服务是否启动，Active字段返回“active (running)”表示服务已经启动，返回“inactive (dead)”表示未启动：

  ```bash
  # service ntpd status 2>&1 | grep Active
  ```
  
- 通过grep命令查看/etc/ntp.conf中restrict的配置，获取ntp权限控制配置：

  ```bash
  # grep "^restrict" /etc/ntp.conf 
  ```
  
- 通过grep命令查看/etc/ntp.conf中server|pool的配置（<IP or domain name>表示具体的服务器IP或域名），获取ntp服务器配置：

  ```bash
  # grep -E "^(server|pool)" /etc/ntp.conf
  ```

### 3.6.2 应当正确配置chronyd服务

**检查方法：**

- 使用grep命令查看/etc/chrony.conf文件中是否正确配置了授时服务器地址：

  ```bash
  # grep "^server\|^pool" /etc/chrony.conf
  ```
  
- 使用ps命令查看是否已启动chronyd服务，如果返回“/usr/sbin/chronyd”进程，表示已经启动：

  ```bash
  # ps -ef | grep chronyd
  ```

### 4.1.1 确保auditd审计已启用

**检查方法**检查方法：**

检查auditd默认状态：

```bash
# systemctl is-enabled auditd.service
```
检查auditd运行状态：
```bash
# systemctl status auditd.service | grep active
```

### 4.1.2 确保审计日志rotate已启用

**检查方法：**

使用如下命令检查当前配置：

```bash
# grep -iE "max_log_file_action|num_logs" /etc/audit/auditd.conf
```

### 4.1.3 应当配置登录审计规则

**检查方法：**

通过执行如下指令，检查用户登录的审计规则：

```bash
# auditctl -l | grep -iE "lastlog"
```

### 4.1.4 应当配置账号信息修改审计规则

**检查方法：**

通过如下命令，检查修改账号信息的审计规则：

```bash
# auditctl -l | grep -iE "passwd|group|shadow"
```

### 4.1.5 应当配置提权命令审计规则

**检查方法：**

使用如下脚本检查提权命令的审计规则：

```bash
#!/bin/bash
array=`find / -xdev -type f \( -perm -4000 -o -perm -2000 \) | awk '{print $1}'`
for element in ${array[@]}
do
    ret=`auditctl -l | grep "$element "`
    if [ $? -ne 0 ]; then
        echo "$element not set"
    else
        echo $ret
    fi
done
```

如果系统中提权命令已经配置audit策略，则该脚本执行后打印出对应策略行，如果未配置，则打印出“\<file path> not set”字样，如下：

```bash
# sh check.sh
```

### 4.1.6 应当配置内核模块变更审计规则

**检查方法：**

如果是32位系统，检查内核模块变更的审计规则：

```bash
# auditctl -l | grep -iE "insmod|rmmod|modprobe|init_module|delete_module"
```
如果是64位系统，还需有如下配置：

```bash
-a always,exit -F arch=b64 -S init_module,delete_module -F key=module
```

### 4.1.7 应当配置管理员特权操作审计规则

**检查方法：**

检查sudo操作审计规则：

```bash
# auditctl -l | grep -iE "sudo\.log"
```

### 4.1.8 应当在启动阶段启用auditd

**检查方法：**

执行如下命令，查看内核启动参数中是否已经添加“audit=1”：

```bash
# cat /proc/cmdline | grep "audit=1"
```

### 4.1.9 应当正确配置audit_backlog_limit

**检查方法：**

执行如下命令，查看内核启动参数中是否已经添加“audit_backlog_limit=\<size\>”：

```bash
# cat /proc/cmdline | grep "audit_backlog_limit"
```

### 4.1.10 避免使用auditctl设置auditd规则

**检查方法：**

通过grep命令，检查/etc/audit/rules.d/目录下是否存在特定的rules文件，包含有“-e 2”字段：

```bash
# grep "-e 2" /etc/audit/rules.d/*.rules
```

### 4.1.11 确保日志大小限制配置正确

**检查方法：**

检查当前配置：

```bash
# grep "^max_log_file" /etc/audit/auditd.conf
```

### 4.1.12 应当正确配置硬盘空间阈值

**检查方法：**

检查auditd.conf配置：

```bash
# cat /etc/audit/auditd.conf | grep -iE "space_left|space_left_action|admin_space_left|admin_space_left_action|disk_full_action|disk_error_action"
```

### 4.1.13 应当配置sudoers审计规则

**检查方法：**

检查sudoers审计规则：

```bash
# auditctl -l | grep "sudoers"
```

### 4.1.14 应当配置会话审计规则

**检查方法：**

检查登录文件审计规则：

```bash
# auditctl -l | grep -iE "utmp|wtmp|btmp"
```

### 4.1.15 应当配置时间修改审计规则

**检查方法：**

如果是32位系统，检查配置：

```bash
# auditctl -l | grep -iE "adjtimex|settimeofday|clock_settime|localtime"
-a always,exit -F arch=b32 -S stime,settimeofday,adjtimex,clock_settime -F key=time
-w /etc/localtime -p wa -k time
```
如果是64位系统，还需有如下配置：

```bash
-a always,exit -F arch=b64 -S settimeofday,adjtimex,clock_settime -F key=time
```

### 4.1.16 应当配置SELinux审计规则

**检查方法：**

检查selinux相关审计配置：

```bash
# auditctl -l | grep -iE "selinux"
```

### 4.1.17 应当配置网络环境审计规则

**检查方法：**

如果是32位系统，检查配置：

```bash
# auditctl -l | grep -iE "setdomainname|sethostname|hosts|issue"
-a always,exit -F arch=b32 -S sethostname,setdomainname -F key=hostnet
-w /etc/hosts -p wa -k hostnet
-w /etc/issue -p wa -k hostnet
-w /etc/issue.net -p wa -k hostnet
```

如果是64位系统，还需有如下配置：
```bash
-a always,exit -F arch=b64 -S sethostname,setdomainname -F key=hostnet
```

### 4.1.18 应当配置文件访问控制权限审计规则

**检查方法：**

如果是32位系统，检查配置：

```bash
# auditctl -l | grep -iE "chmod|chown|setxattr|exattr"
-a always,exit -F arch=b32 -S chmod,fchmod,fchmodat -F auid>=1000 -F auid!=-1 -F key=fileperm
-a always,exit -F arch=b32 -S chown,fchown,lchown,fchownat -F auid>=1000 -F auid!=-1 -F key=fileperm
-a always,exit -F arch=b32 -S setxattr,lsetxattr,fsetxattr,removexattr,lremovexattr,fremovexattr -F auid>=1000 -F auid!=-1 -F key=fileperm
```
如果是64位系统，还需有如下配置：

```bash
-a always,exit -F arch=b64 -S chmod,fchmod,fchmodat -F auid>=1000 -F auid!=-1 -F key=fileperm
-a always,exit -F arch=b64 -S chown,fchown,lchown,fchownat -F auid>=1000 -F auid!=-1 -F key=fileperm
-a always,exit -F arch=b64 -S setxattr,lsetxattr,fsetxattr,removexattr,lremovexattr,fremovexattr -F auid>=1000 -F auid!=-1 -F key=fileperm
```

### 4.1.19 应当配置文件访问失败审计规则

**检查方法：**

如果是32位系统，检查配置：

```bash
# auditctl -l | grep -iE "EACCES|EPERM"
-a always,exit -F arch=b32 -S open,truncate,ftruncate,creat,openat -F exit=-EACCES -F auid>=1000 -F auid!=-1 -F key=fileaccess
-a always,exit -F arch=b32 -S open,truncate,ftruncate,creat,openat -F exit=-EPERM -F auid>=1000 -F auid!=-1 -F key=fileaccess
```
如果是64位系统，还需有如下配置：

```bash
-a always,exit -F arch=b64 -S open,truncate,ftruncate,creat,openat -F exit=-EACCES -F auid>=1000 -F auid!=-1 -F key=fileaccess
-a always,exit -F arch=b64 -S open,truncate,ftruncate,creat,openat -F exit=-EPERM -F auid>=1000 -F auid!=-1 -F key=fileaccess
```

### 4.1.20 应当配置文件删除审计规则

**检查方法：**

如果是32位系统，检查配置：

```bash
# auditctl -l | grep -iE "unlink|unlinkat|rename|renameat"
-a always,exit -F arch=b32 -S rename,unlink,unlinkat,renameat -F auid>=1000 -F auid!=-1 -F key=filedelete
```
如果是64位系统，还需有如下配置：

```bash
-a always,exit -F arch=b64 -S rename,unlink,unlinkat,renameat -F auid>=1000 -F auid!=-1 -F key=filedelete
```

### 4.1.21 应当配置文件系统挂载审计规则

**检查方法：**

如果是32位系统，检查配置：

```bash
# auditctl -l | grep -iE "mount"
-a always,exit -F arch=b32 -S mount -F auid>=1000 -F auid!=-1 -F key=mount
```
如果是64位系统，还需有如下配置：

```bash
-a always,exit -F arch=b64 -S mount -F auid>=1000 -F auid!=-1 -F key=mount
```

### 4.2.1 确保rsyslog服务已启用

**检查方法：**

- 执行如下命令，查看rsyslog.service服务默认状态是否为enable

  ```bash
  # systemctl is-enabled rsyslog.service
  ```
  
- 执行如下命令，查看rsyslog.service服务是否已经启动成功：

  ```bash
  # systemctl status rsyslog.service | grep Active
  ```

### 4.2.2 确保系统认证相关事件日志已记录

**检查方法：**

检查rsyslog auth配置：

```bash
# grep auth /etc/rsyslog.conf | grep -v "^#"
```

### 4.2.3 确保cron服务日志已记录

**检查方法：**

检查rsyslog配置：

```bash
# grep /var/log/cron /etc/rsyslog.conf
```

### 4.2.4 应当正确配置rsyslog默认文件权限

**检查方法：**

检查 `/etc/rsyslog.conf` 及 `/etc/rsyslog.d/*.conf` 中 `FileCreateMode` 配置：

- 若未配置或值不为 `0600`，则日志文件存在泄露或被篡改风险，需修复权限。

```bash
# grep ^\$FileCreateMode /etc/rsyslog.conf /etc/rsyslog.d/*.conf
```

### 4.2.5 应当正确配置各服务日志记录

**检查方法：**

检查rsyslog记录规则：

```bash
# grep \/var\/log /etc/rsyslog.conf /etc/rsyslog.d/*.conf
```

### 4.2.6 确保rsyslog转储journald日志已配置

**检查方法：**

检查rsyslog配置：

```bash
# grep imjournal /etc/rsyslog.conf
```

### 4.2.7 确保rsyslog日志rotate已配置

**检查方法：**

检查/etc/logrotate.d/rsyslog文件中是否已经配置相关字段，此处“/var/log/*”是/etc/rsyslog.conf文件中配置的rsyslog日志输出路径，两者需要匹配一致：

```bash
# cat /etc/logrotate.d/rsyslog | grep -iE "\/var\/log|maxage|\<rotate\>|compress|size"
```

### 4.2.8 应当配置远程日志服务器

**检查方法：**

检查rsyslog.d配置：

```bash
# grep -irE "^*.*@*:[0-9]+$" /etc/rsyslog.d/*.conf
```

### 4.2.9 应当仅在指定的日志主机上接受远程rsyslog消息

**检查方法：**

检查rsyslog配置文件：

* 检查TCP配置：

  ```bash
  # grep ^\$ModLoad /etc/rsyslog.conf /etc/rsyslog.d/*.conf | grep imtcp
  # grep ^\$InputTCPServerRun /etc/rsyslog.conf /etc/rsyslog.d/*.conf
  ```
  
* 检查UDP配置：

  ```bash
  # grep ^\$ModLoad /etc/rsyslog.conf /etc/rsyslog.d/*.conf | grep imudp
  # grep ^\$InputUDPServerRun /etc/rsyslog.conf /etc/rsyslog.d/*.conf
  ```

