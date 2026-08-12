---
name: web-frontend-recon
description: 前端 JS 侦察与 API 面提取方法——SPA fallback 识别、webpack chunk 接口提取、统一鉴权特征识别、OAuth/SSO 配置泄露侦察、外包 staging 环境发现。当目标为 Vue/React SPA 或需要从 JS 挖 API 端点/隐藏配置时加载。
version: 1.0.0
platforms: [windows, linux]
metadata:
  hermes:
    tags: [recon, frontend, js, api, spa, web]
---

# 前端 JS 侦察（Web 目标金矿）

> 前端代码是攻击面的说明书——API 端点、隐藏配置、外包环境地址全在里面。
> 实战来源：北大生科 OA（newoa.bio.pku.edu.cn）侦察（2026-08-04）。

## 触发条件
- 目标是 Vue/React SPA（页面源码是 `#app` + 大量 JS chunk）
- 需要快速拿到完整 API 端点清单
- 目录扫描全 404/全 200 分不清真假
- 找 OAuth/SSO 配置、外包商 staging 环境

## 工作流

### 1. 识别 SPA 与 JS 清单
```
curl 首页 → 抓 <script src> 全部 .js 路径
```
- 特征：`<div id="app">` + 一堆 `/static/js/chunk-*.js`
- 重点拉取：`chunk-common.*.js`、`chunk-vendors.*.js`（常 500KB-1MB，接口全在这）、`index.*.js`（路由+初始化）

### 2. SPA fallback 识别（防误报铁律）
- Vue Router history 模式：**所有未匹配路径都返回 index.html**（HTTP 200 + text/html + 固定字节数）
- 探测 `/api`、`/v2/api-docs`、`/actuator` 全 200 ≠ 接口存在！
- **判定方法**：`curl -sI` 看 Content-Type + size
  - text/html + 固定 size（如 4307）= fallback（假 200）
  - application/json = 真实后端 API ✅
- 真实 API 的特征：错误 JSON 如 `{"code":10001,"error":"未登录..."}`
- **直连被 fallback 挡 → 代理路径可打真 API**（2026-08-07 iclass 实证）：`iclass.scu.edu.cn/teachplatform/api/...` 直连返回 SPA 首页 HTML（200 假象），但走 webvpn 代理 `https://https-{host}-{port}.webvpn.edu.cn` 同路径返回真实 JSON。判断"API 不可达"前先试代理前缀
- **notoken 命名惯例**：Java 后端接口名自带 `notoken`（如 `/ky/km/kmKnowledgeMap/notoken/list`）= 开发标记免认证，扫描时优先测这类路径，往往直出业务数据

### 3. webpack chunk 提取 API 端点
```powershell
# 模板字符串拼接模式（最常见）
[regex]::Matches($js, '\$\{n\.Ir\}(/[a-zA-Z0-9_\-/]{2,80})')
# 双引号字面量
[regex]::Matches($js, '["''](/admin/[a-zA-Z0-9_\-/]{2,80})["'']')
# axios 调用
[regex]::Matches($js, '(?:get|post|put|delete)\("([^"]{3,60})"')
```
- 接口定义格式：`login:["post",`${n.Ir}/uc/home/login`,!1,{...}]` → 方法+URL+选项
- **baseURL 配置**（金矿）：`baseURL:"http://xxx.stg.外包商.com"` —— dev/staging 环境地址直接泄露
- upload 接口：`/admin/upload/{img,file,import}` 常为独立鉴权点

### 4. 统一鉴权特征识别
- 未登录响应：`{"code":10001,"error":"未登录或登录已失效！"}` → 全接口统一鉴权中间件
- 批量探测分类法：
  | 标签 | 判断 |
  |---|---|
  | AUTH | 命中统一鉴权码（10001 等） |
  | BADREQ | 41001 / bad Request（接口存在但参数错） |
  | ERR500 | 500/出现错误（接口存在，可能缺参） |
  | **DATA-200!** | code 200 = **未授权可达 = 金矿** |
- 未授权可达的模块（如 /uc/home/*）单独深挖：验证码逻辑、OAuth 配置、SSO token 处理

### 5. OAuth/SSO 配置侦察
- 找 `/uc/*`、`/sso/*`、`/oauth/*`、`/authorize`、`/login` 相关接口
- 无认证 POST 配置接口可能直出：appId、submitUrl（IAM 端点）、redirectUrl
- **关注点**：redirectUrl 是否 HTTP 明文（授权码可被中间人截获）；appId 是否可枚举
- pku 类 IAM token 接口：畸形/数组/超长 token 测试返回差异（41001 bad Request 是特征）

### 6. 外包 staging 环境（延伸攻击面）
- 生产前端 baseURL 泄露 `stg.外包商.com` → DNS 解析 + HTTP 状态确认
- ⚠️ **范围红线**：外包商域名不在甲方授权域内！只记录为信息泄露发现，深入测试需用户确认授权
- 测试环境通常：防护弱、测试数据、调试接口——若确认在范围内是高价值目标

## 陷阱
- crt.sh 常被限流（返回空/JSON 解析失败）→ certspotter（免费限 100 条左右）+ hackertarget hostsearch 多源合并
- PowerShell 复杂命令里 `$matches` 在 Invoke-Expression 包装下可能 null → 用 write_file 落 .ps1 或拆小命令
- 大 JS 文件用 curl 落盘再正则（727KB 直接管道处理易崩）
- 前端路由 ≠ API 端点（/admin、/user 是 Vue route，真实 API 是 /admin/xxx 带后端逻辑）——先分清
- 版本泄露：`sys_version` 等字段随错误响应带出，可用于已知漏洞匹配
- **分类树/树形接口参数类型坑**（2026-08-07 小北实证）：`loadTreeRoot?pcode=` 根用**空串**（`pcode=` 后跟空格让 urllib 编码）成功返回 27 节点，但展开子节点用**雪花 key** 报"不存在"，必须用 **code**（如 B25）——树接口的 pcode 是 code 不是 key。卡住时逐个换参数类型
- **搜索/列表接口超时 ≠ 不存在**：searchDoc/listDraft 全超时（后端慢/需内部服务），但下载接口（downloadKmDoc）缺 docId 报 500 参数错误、ID 无效报 404——用报错结构区分"参数格式对但 ID 无效" vs "路径不存在"

## 参考案例
- 北大 newoa.bio：chunk-common 727KB 提取 300+ 接口 → 全 AUTH 统一鉴权 → uc/ 模块未授权面 → pku_login 直出 OAuth 配置 → baseURL 泄露 stg.itknown.com（外包 staging 存活）

## 3D/WebGL 站点资产侦察（2026-08-08 pinchen.me 实证）
Three.js/R3F 站点（模型房间/虚拟展厅）的资产侦察要点：
- **模型 URL 定位**：搜 chunk 里 `assets/room`、`\.glb`、`useGLTF` 引用——原站模型名可能很朴素（pinchen.me 的完整房间就是 `n="/assets/room/desk.glb"`，与功能名无关）；先信原站模型，别急着自建
- **单行混淆 chunk 提取**：webpack chunk 常是单行超长 JS（read_file 显示 0 行、Select-String 失灵）→ 用 Python `re.finditer` 搜关键词 + 截 ±200 字符上下文
- **纹理/贴图映射表**：原站常在 chunk 存 `{mesh名:"组名"}` 映射（desk_lamp:"group1", whiteboard:"group3", book1:"books", Vinyl_1:"vinyl"），纹理 URL 模式 `/assets/room/textures/{组}/{名}.webp`——组目录可枚举（12 组），但文件名映射常在被混淆的独立模块（猜 URL 全 404 就放弃，用组级纯色近似）
- **GLB materials=0 ≠ 模型坏**：原站 GLB 常无材质，靠 JS 运行时按组贴图/着色——还原时按映射表给 mesh 上近似色即可
- **大坐标系陷阱**：Sketchfab 场景单位巨大（desk.glb 包围盒 153×63×231），固定相机坐标会站进模型内部——加载后必须 Box3 动态适配相机
- **DRACO 解码**：原站 `setDRACOLoader` + `/assets/draco/`——抓模型时注意是 draco 压缩的
