---
name: web-spa-recon
description: SPA 前端侦察——从 Vue/React 单页应用提取真实 API 攻击面。识别 SPA fallback、拉取 JS chunk 提取接口定义/baseURL/staging 地址、区分 AUTH/未授权端点、挖掘认证接口面（登录/SSO/OAuth）。当目标是现代前后端分离站点时使用。
version: 1.0.0
platforms: [windows, linux]
metadata:
  hermes:
    tags: [recon, spa, frontend, api, javascript, web]
---

# SPA 前端侦察（Web 单页应用攻击面提取）

> 现代站点（Vue/React/ElementUI 等）后端 API 全隐藏在 JS bundle 里——侦察的核心是拆 JS。

## 触发条件
- 目标返回单页应用（title 如 xxx-front、SPA 结构、index.html 引用 webpack chunk）
- 需要找 API 端点/隐藏接口/未授权面

## 工作流

### 1. 识别 SPA 与 SPA fallback
- 首页 HTML：`<div id="app">` + `/static/js/runtime.*.js` / `chunk-vendors.*.js` → Vue；`main.*.js` → React
- **SPA fallback 识别（关键坑）**：history 模式路由下，任何未匹配路径都返回 index.html（HTTP 200 + `Content-Type: text/html` + 固定字节数，如 4307）
  - 探测端点必须看 Content-Type / 响应大小，不能只看状态码——`/api`、`/v2/api-docs` 返回 200 可能是 fallback 不是真实接口
  - 真实后端 API 返回 `application/json`

### 2. 拉取 JS 提取接口定义
```bash
# 从 index.html 提取 JS 路径
# 优先拉大 chunk（chunk-common/vendors），接口定义集中在那里
curl -s http://TARGET/static/js/chunk-common.HASH.js -o common.js
```
grep 模式（PowerShell 注意转义）：
| 模式 | 提取内容 |
|---|---|
| `baseURL:"..."` | 后端地址、**staging/开发环境地址**（重要！） |
| `["get",\`${BASE_URL}/path\`]` 或 `["post",...]` | 接口定义：方法 + 路径 + 是否需认证（`!1`=否 `!0`=是）+ 配置 |
| `uploadImgUrl=`/`uploadFileUrl=` | 上传接口（高危面） |
| `http(s)://域名` | 第三方/外包域名线索 |
| `login\|captcha\|verify\|ssoToken\|pku\|oauth` 上下文 | 认证接口面 |

- 接口路径常为动态模板拼接（`${n.Ir}/admin/...`），用宽松正则提取
- 懒加载路由的接口可能在按需 chunk 里，先提 `webpackChunk` 清单

### 3. 端点批量探测分类
对提取的接口做轻量 GET（只读，RoE 内）：
```
分类规则：
- 含统一未登录 code（如 10001）→ AUTH（已鉴权，跳过或走认证面）
- 404 / Not Found → 不存在
- 返回 JSON 数据 / 200 + 长度 > 100 → DATA!（未授权候选，深挖）
- 其他 → 单独看响应
```
- 所有 /admin/ 等业务前缀通常统一鉴权；**认证前缀（/uc/、/auth/、/login、/sso）无认证可达**是正常设计——验证码绕过、SSO token 校验、OAuth 配置泄露在这里挖
- 未授权接口金矿：`/export`、`/download`、`/list`、`/look`、`/addressbook`、`/user/data` 类

### 4. 高价值线索
- **staging 地址泄露**：生产前端 baseURL 写死测试环境（如 xxx.stg.开发商.com）——确认可达性记录为信息泄露；⚠️ 第三方域名可能不在授权范围，深入测试前确认 scope
- **OAuth 客户端配置无认证直出**（如 /uc/home/pku_login）：appId + submitUrl + redirectUrl——关注回调是否 HTTP 明文
- **系统版本**：接口响应常带 `sys_version` 字段（信息泄露 + 漏洞匹配用）
- 外包开发商域名（itknown.com 之类）→ 供应链线索

## 坑位
- crt.sh 常被限流（返回空/0 bytes）→ 换 certspotter / hackertarget API
- PowerShell 正则转义地狱：JS 提取用单引号包裹模式，`${` 要转义或用 char 拼接
- 大 JS（700KB+）用 Get-Content -Raw 一次性读再正则，别逐行
- 探测请求保持轻量（30-50 个/轮），全 AUTH 就转认证面，别硬枚举
