# David Shapiro RSAUtils 登录加密链复刻明细（某高校 CAS 2026-08-11 实战）

来源：`C:\Users\user\agent-pentest\example-edu\cas-crypto\`（证据 evidence/js_security.js、js_common.js、js_cas.js + cas-recon.md）。
该实现（1998-era，无 OAEP、零字节填充、**确定性输出**）在中国高校 CAS/正方智慧校园栈里非常常见，遇到同名函数直接套本文件。

## 加密链

```
password -> reverse -> RSAUtils.encryptedString(key, reversed)
key = {modulus, exponent} hex，每次会话 POST /cas/v1/getPubKey 获取
      -> localStorage['cas_modulus'] / ['cas_exponent']（js_common.js putRsa/generateRsaKey）
```

## encryptedString 逐字节复刻要点（Python）

```python
def encrypt_password(pwd, modulus_hex, exponent_hex):
    a = [ord(c) for c in pwd[::-1]]          # charCodeAt = ord（UTF-16 code unit），非 utf-8 字节！
    chunk_size = 2 * bi_high_index(modulus_hex)   # 1024-bit 公钥 -> 126（不是 128！）
    while len(a) % chunk_size: a.append(0)   # 零字节填充到 chunkSize 整数倍
    n, e = int(modulus_hex, 16), int(exponent_hex, 16)
    blocks = []
    for i in range(0, len(a), chunk_size):
        m = 0
        for j in range(chunk_size // 2):     # 小端 16-bit digit 组装
            digit = a[i+2*j] + (a[i+2*j+1] << 8)   # block.digits[j] = a[k] + (a[k+1]<<8)
            m |= digit << (16 * j)
        blocks.append(bi_to_hex(pow(m, e, n)))
    return " ".join(blocks)                  # 块间单空格（JS 是 join(" ")）
```

- `bi_high_index`：modulus hex 从尾部按 4 hex 字符一组解析成 16-bit 小端 digit（biFromHex），返回最高非零 digit 下标；完整 1024-bit 模数 → 64 digits → high index 63 → chunkSize 126。
- `bi_to_hex`（= biToHex）：从最高非零 digit 向下，每 digit 用 digitToHex 输出 **4 位小写 hex**（零填充），即整数的"最小小写 hex 但每 digit 定宽"；零值返回 "0000"。
- digitToHex 实现（本文件版本是 4 位定宽版，别用旧版 1-4 位变长版）：
  `''.join(hexchars[n>>(4*(3-i)) & 0xf] for i in range(4))` 或 format(d, '04x')。
- 私钥回解验证：`m = pow(c, d, n)`，m 按 16-bit 小端拆字节 `(m & 0xFFFF).to_bytes(2,'little')`，拼接后 rstrip(b'\x00') == reversed plaintext。

## 非 ASCII 密码：平台自身损坏（实测，别修）

charCodeAt > 255 时 `a[k] + (a[k+1]<<8)` 溢出 16-bit digit，m 可 ≥ n，私钥回解对不上——
**真 JS 自己也解不开**（服务端同理），且 JS float64 舍入导致 Python 无法与真 JS 逐字节对齐。
结论：ASCII（现实密码字符集）逐字节一致即可；非 ASCII 在 README 注明"平台不支持"，不投入。

## node 金标准 oracle（验证 Python 复刻）

```js
// oracle.js —— 用生产 JS 加密，与 Python 输出逐字节对比
const fs = require('fs');
global.window = {};                       // 老式文件是 (function($w){...})(window) IIFE
eval(fs.readFileSync('evidence/js_security.js', 'utf8'));  // 自带 setMaxDigits(130)
const RSAUtils = window.RSAUtils;
const [modulus, exponent, reversedPwd] = process.argv.slice(2);
const key = RSAUtils.getKeyPair(exponent, '', modulus);
console.log('chunkSize=' + key.chunkSize);
console.log('cipher=' + RSAUtils.encryptedString(key, reversedPwd));
// 用法：node oracle.js <modulus_hex> <exponent_hex> <已反转密码>；输出与 python 版比对
```

注意：该 JS 文件带 UTF-8 BOM + CRLF——git 提交后 diff 会显示 BOM 行变化（无害，注意即可）。

## 自测结构（selftest.py 模式）

- 本地生成固定 1024-bit 测试密钥（Miller-Rabin 纯 Python 即可），模数/指数/私钥常量内嵌 → 完全离线可复现
- 用例：任务样例密码（如 "Test@123456"）、200 字符（触发 2 块）
- 每用例三项断言：① 块结构（每块 4*(high_index+1) 位小写 hex）② 私钥回解 roundtrip ③ node oracle 逐字节相等
- 输出 tee 到 selftest-output.txt

## 某高校 CAS 登录面（下轮自动化接入）

- `POST /cas/v1/getPubKey` → `{"modulus": ..., "exponent": ...}`（contentType: application/json）
- `POST /cas/login` 需 execution（UUID+HS512 JWT flow token）、_eventId=submit、type=zhmm、kaptcha（按 getKaptchaStatus 条件出现）
- 平台：非 Apereo，正方智慧校园定制 CAS（无 pwdDefaultEncryptSalt 变量；Tengine 反代；iPlanetDirectoryProCAS cookie 遗留）
