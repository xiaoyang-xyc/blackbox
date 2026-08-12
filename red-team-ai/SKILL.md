---
name: red-team-ai
description: AI驱动的红队实战指南 — 基于《Redefining Hacking》作者Omar Santos(DEF CON Red Team Village联合创始人)方法论。覆盖AI辅助侦察、智能漏洞利用、C2隐蔽通道、后渗透、AD攻击、RAG漏洞挖掘。
user-invocable: true
---

# Red Team AI — AI驱动的红队实战

> 基于 Omar Santos《红队实战指南：AI驱动的渗透测试、红队评估和漏洞挖掘》(2026)

## 路由

| 任务 | 调用 |
|------|------|
| AI辅助信息收集 | → §1 Recon |
| 智能漏洞利用 | → §2 Exploit |
| C2与隐蔽通道 | → §3 C2 |
| AD域攻击 | → §4 AD |
| 后渗透 | → §5 Post-Exploit |
| RAG漏洞挖掘 | → §6 RAG |

---

## §1 AI 辅助侦察

### 1.1 智能子域名发现
```bash
# AI增强的子域名枚举
subfinder -d target.com -o subs.txt
# 用 LLM 分析子域名模式，生成变体
for word in $(cat wordlist.txt); do
  echo "${word}.target.com" >> custom.txt
done
# 批量存活检测
httpx -l all_subs.txt -o live.txt -silent
```

### 1.2 AI 指纹识别
- 用 LLM 分析响应头/HTML 识别技术栈
- 自动匹配 CVE 数据库
- 生成针对性攻击计划

### 1.3 关键检查清单
```
□ /actuator/health → Spring Boot
□ /druid/index.html → 阿里 Druid
□ rememberMe=deleteMe → Shiro
□ /swagger-ui.html → API 文档
□ Server 头 → 版本泄露
□ .git/HEAD → 源码泄露
□ .env → 配置泄露
```

---

## §2 智能漏洞利用

### 2.1 AI 辅助 Payload 生成
- 根据目标技术栈自动生成定制 Payload
- WAF 绕过变体自动生成
- Unicode/Hex/Base64 多编码组合

### 2.2 框架漏洞速查
| 框架 | 检测 | 利用 |
|------|------|------|
| Shiro | `rememberMe=deleteMe` | ysoserial |
| Fastjson | DNSLog + `@type` | JNDI 注入 |
| Spring Boot | `/actuator/env` | SpEL 注入 |
| Ruoyi | `/common/upload` | 文件上传 CVE |
| ThinkPHP | 指纹 + 版本 | 5.x RCE |

### 2.3 漏洞优先级（按成功率）
```
1. 信息泄露（20%） → 2. 未授权访问（18%）
3. XSS（15%）     → 4. SQL 注入（12%）
5. SSRF（10%）    → 6. RCE（8%）
```

---

## §3 C2 隐蔽通道

### 3.1 C2 协议选择
| 协议 | 隐蔽性 | 适用场景 |
|------|--------|---------|
| HTTPS | 中 | 通用 |
| DNS Tunnel | 高 | 严格出网限制 |
| WebSocket | 高 | 长连接 |
| MCP 协议 | 极高 | 伪装 AI API 流量 |
| ICMP | 中 | 特殊环境 |

### 3.2 免杀技术
```
□ ETW Patching
□ API Unhooking
□ DLL 反射加载
□ Process Hollowing
□ Parent PID Spoofing
□ Syscall 直调
□ OLLVM 混淆
□ memfd_create 内存执行
```

---

## §4 AD 域攻击

### 4.1 攻击路径
```
初始入口 → 本地提权 → 域枚举 →
  BloodHound 路径分析 → Kerberoasting →
  AS-REP Roasting → DCSync → 域控
```

### 4.2 关键命令
```powershell
# 域枚举
net group "Domain Admins" /domain
# BloodHound 采集
SharpHound.exe -c All
# Kerberoasting
Rubeus.exe kerberoast
# DCSync
mimikatz # lsadump::dcsync /domain:corp.local /user:Administrator
```

---

## §5 后渗透

### 5.1 持久化
```
□ 计划任务 (schtasks)
□ WMI 事件订阅
□ 注册表 Run 键
□ Windows 服务
□ DLL 劫持
□ SSH authorized_keys (Linux)
□ crontab (Linux)
```

### 5.2 横向移动
```
□ PSRemoting / WinRM
□ WMI 远程执行
□ PsExec
□ RDP
□ SSH 密钥信任链
□ 云助手 (阿里云 ECS RunCommand)
```

---

## §6 RAG 漏洞挖掘

### 6.1 RAG 流程
```
目标代码/文档 → 嵌入模型 → 向量数据库 →
  检索相关漏洞模式 → LLM 生成测试用例 →
  自动化验证 → 报告生成
```

### 6.2 实战应用
- 将 CVE 数据库嵌入到向量库
- 根据目标指纹检索相关历史漏洞
- AI 自动生成验证 POC
- 自动编写渗透测试报告

---

> **参考**: 《红队实战指南：AI驱动的渗透测试、红队评估和漏洞挖掘》Omar Santos 等 (2026)
> **MITRE ATT&CK**: T1595-T1210-T1078-T1003
