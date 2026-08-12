---
name: js-login-crypto-replica
description: "复刻登录页 JS 加密链为 Python 等价实现。触发：写登录加密脚本/encryptedString/登录自动化。"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [crypto, rsa, js, login-automation, python-replica, cas, pentest]
---

# JS 登录加密链复刻（JS → Python）

## When to Use

- 登录面自动化前需要把登录页 JS 里的客户端加密（reverse→RSA、AES、MD5、自定义混淆）用 Python 等价复刻
- 手里有登录页引用的 JS 证据文件（security.js / common.js / 主题 cas.js），要写 `encrypt_password` 类接口
- 典型目标：正方/泛微等校园 CAS（reverse→RSA + getPubKey 动态公钥）、各类 SRC 登录表单

场景：SRC/渗透登录面自动化需要 Python 复刻登录页客户端加密（正方/泛微等校园 CAS 的 reverse→RSA、AES、MD5、自定义混淆）。输入：登录页 HTML + 引用的 JS 证据文件（security.js / common.js / 主题 cas.js 等）。2026-08-11 某高校 CAS 实战验证：Python 复刻与真实 JS 输出**逐字节一致**。

## 五步工作流

1. **提取加密链**（grep JS 证据）：`grep -n "encryptedString|RSAUtils|setMaxDigits|chunkSize|reversedPwd|password|putRsa|getPubKey"` 定位 submit handler（checkForm 类）→ 确认：变换顺序（先 reverse 再 RSA？）、padding、输出格式（hex 串 / 空格分块）、公钥来源（POST getPubKey → localStorage）。`pwdDefaultEncryptSalt` 变量存在与否 → 判断是否 Apereo CAS（存在=是；不存在=自定义平台，如正方）
2. **金标准先行**：Node 直接跑原始 JS 拿 ground truth（IIFE shim 见 Pitfalls），**先于 Python 实现生成对照输出** —— 最硬的验证锚点
3. **Python 复刻**：stdlib only；大数 RSA 用 `pow(block, e, n)`；接口固定 `encrypt_password(plaintext_password, modulus_hex, exponent_hex) -> str` + CLI `python xxx.py <pwd> <modulus_hex> <exponent_hex>`
4. **验证矩阵**（selftest.py 模式，全本地不联网）：
   - 输出格式：空格分隔的小写 hex 块
   - chunk 数学：块数 = 填充后长度/chunkSize，chunkSize 从 modulus 位数推出
   - 私钥回解：有私钥时逐块 `pow(int(c,16), d, n)`，**定长 `to_bytes(chunk_size,'little')`** 后 == 反转+零填充明文
   - **与 Node 真实 JS 输出逐字节比对**：短密码（单块）+ 长密码 ≥ chunkSize（多块）各一次
5. **落盘**：selftest-output.txt + README.md（用法 + 链说明 + 下轮自动化怎么用），git commit

## Pitfalls

- **RSAUtils chunkSize = 2*biHighIndex(modulus)：1024-bit 公钥 = 126，不是 128**（David Shapiro 经典实现怪癖，必须复刻；错 2 字节全盘皆输）
- 输出 hex 是最小长度：biToHex 从最高非零 16-bit digit 向下、每 digit 4 位小写 hex、高位零 digit 省略 = Python `format(int,'x')`
- 私钥回解**别用** `while m: out.append(m&0xFF)` —— 会剥掉明文尾部零填充，误报 FAIL；用 `m.to_bytes(chunk_size, 'little')`
- JS IIFE shim：`global.window = global; eval(fs.readFileSync('xxx.js','utf8'))` 后直接调 `RSAUtils.getKeyPair(e,'',n)` + `encryptedString`；文件可能带 UTF-8 BOM（codex PowerShell 写盘产物），字节比对前注意
- 公钥会话级动态：POST `/cas/v1/getPubKey` → `{modulus, exponent}` → localStorage `cas_modulus`/`cas_exponent`；自动化每次刷新，勿复用旧 key
- 测试密钥本地生成即可（cryptography lib 1024-bit RSA），无需联网；侦察报告（cas-recon.md 类）通常没记样例公钥
- 时间盒纪律：15min 内先出复刻 + 金标准比对，验证通过即收工

## 派 codex 复刻（可选）

- 证据文件先复制进**自包含工作目录**（codex 沙箱读外部目录受限），`git init` 后 `codex exec --skip-git-repo-check --sandbox workspace-write "<English prompt>"`（pty=true；trusted-directory 坑详见 claude-codex-pi-executors 技能，user-owned 勿改）
- 提示词给精确算法步骤（reverse → char codes → chunkSize → 小端 16-bit 打包 → pow → minimal hex → 空格拼接），codex 复刻成功率最高
- codex 跑的同时**并行**：生成测试 RSA 密钥 + 写 Node 金标准 harness
- **codex 写完交付文件后常自我迭代不退出（10min+，会读父代中途放入的文件继续折腾）——独立验证通过即 `process kill`，kill 后重跑一次最终验证锁定产物**（防它 kill 前又改文件）

## 参考

- `references/rsautils-encryptedstring.md` — RSAUtils.encryptedString 逐字节等价细节 + 正方 CAS 链 + Node 金标准 harness 模板
