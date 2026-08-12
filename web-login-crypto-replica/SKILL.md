---
name: web-login-crypto-replica
description: "登录自动化需复刻 JS 加密链（RSAUtils/CAS）时用：node 跑真 JS 逐字节验证 Python 复刻。"
version: 1.0.0
author: hermes-curator
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [login-automation, crypto, rsa, cas, sso, node-oracle, python-replica]
---

# 网页登录加密链 Python 复刻（node 真 JS 金标准验证）

做登录面自动化（CAS/正方智慧校园等 SSO）前，必须先把前端提交密码前的加密链复刻成 Python。
本技能是**通用工作流**；某高校 CAS 的具体 RSAUtils 链细节见 `references/rsa-utils-david-shapiro.md`。

## 何时用

- 登录自动化/爆破/凭证枚举需要构造 `password=` 加密值
- 目标登录页 JS 里有 RSAUtils / encryptedString / setMaxDigits / getPubKey 等老式 RSA 痕迹
- 任何"把浏览器端 JS 加密行为搬到 Python"的任务

## 工作流（7 步）

1. **抓证据**：登录页 HTML + 相关 JS（通常 `js_security.js`/`js_common.js`/`js_cas.js`，也可能内联）落盘 `raw/`。定位提交前对 password 的变换（reverse? md5? RSA? AES?）与公钥来源（如 `POST /cas/v1/getPubKey` → localStorage `cas_modulus`/`cas_exponent`）。
2. **建自包含目录**：`mkdir -p <workdir> && git init -q`，证据复制进 `<workdir>/evidence/` —— 子代理沙箱（codex workspace-write / opencode）读外部目录受限，证据必须先入目录。
3. **写 Python 复刻**（stdlib only）：大数 RSA 直接用 `pow(m, e, n)`，setMaxDigits/BigInt 都不需要；逐函数对照 JS 源码（biFromHex、biHighIndex、biToHex、digitToHex、encryptedString 每个都要复刻到位，别只复刻"数学等价"——输出格式怪癖全在那些函数里）。
4. **金标准验证（关键，不可省）**：写 `oracle.js`，node 直接 eval 生产 JS（`global.window = {}; eval(code)` —— 老式文件多是 `})(window)` IIFE，`window` shim 即可跑；文件自带 `setMaxDigits(130)` 不用管）。用真 JS 加密同一输入，与 Python 输出**逐字节对比**。oracle 模板见 references/。
5. **本地自测**（不联网）：本地生成固定 1024-bit 测试 RSA 密钥（含私钥，仅测试用，勿用真实会话公钥）→ 结构检查（hex 串/分块数/每块长度）+ 私钥回解 roundtrip（反向验证明文）+ oracle 对比 → 输出落 `selftest-output.txt`。
6. **README.md**：用法 + 加密链说明 + 下轮登录自动化接入方式（公钥获取 → 加密 → POST /cas/login 字段：execution token、_eventId、kaptcha 等）。
7. **收编**：若 codex/子代理代写，产物必须过第 4 步 oracle 才收编；`git add -A` 前先写 `.gitignore`（`__pycache__/`、`*.pyc`），自测会重建 pycache。

## 通用坑

- **老式 JS RSA 输出格式怪癖**：chunkSize = 2*biHighIndex(modulus)（1024-bit 是 **126 不是 128**）；块内 16-bit digit 小端组装（`digit = a[k] + (a[k+1]<<8)`）；每 digit 输出 **4 位小写 hex**（digitToHex 零填充）；多块用**单空格**连接。详见 references/。
- **非 ASCII 密码在老 RSAUtils 下天然损坏**：charCodeAt>255 溢出 16-bit digit 数学，m≥n，**服务端自己也解不开**——复刻只保证 ASCII（现实密码字符集）逐字节一致；非 ASCII 连真 JS 都因 float64 舍入无法精确复刻，别在这上面耗时间，README 里注明即可。
- **公钥每次会话动态获取**：`POST /cas/v1/getPubKey` → `{modulus, exponent}`；自动化时每次登录前刷新，勿复用 localStorage 缓存旧值（静态 key 风险=字典枚举）。
- 字符码数组用 `[ord(c) for c in s]`（等价 JS charCodeAt/UTF-16 code unit），**不是** `s.encode('utf-8')` 字节（非 ASCII 会差）。
- Windows Git Bash：调原生 python.exe 传 `C:/...` 原生路径，MSYS `/c/...` 路径会变 `C:\c\...`。

## 相关技能

- `claude-codex-pi-executors`（user-owned）：派 codex 写复刻代码的调用姿势与坑（pty/export/sandbox/trusted dir/写后不退出）
- `edu-higher-ed-platform-recon`：教育行业平台指纹/侦察（本技能是其登录面利用的下游）
