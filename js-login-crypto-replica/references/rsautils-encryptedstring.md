# RSAUtils.encryptedString 逐字节等价（David Shapiro 经典 JS RSA）

来源：某高校 CAS（cas.example.edu，正方智慧校园）raw/js_security.js + raw/js_cas.js，2026-08-11 复刻验证（Node 金标准逐字节一致，含多块）。

## JS 原逻辑（checkForm → encryptedString）

```js
var reversedPwd = password.split("").reverse().join("");   // ① 密码先反转
var encrypedPwd = RSAUtils.encryptedString(key, reversedPwd); // ② 再 RSA
```

`encryptedString(key, s)`：
1. `a[i] = s.charCodeAt(i)` 字符码数组（UTF-16 code unit；ASCII 密码即字节值）
2. `while (a.length % key.chunkSize != 0) a[i++] = 0;` 零填充到 chunk 边界
3. `chunkSize = 2 * biHighIndex(modulus)`；modulus 按 4 hex 字符从尾部组 16-bit digit（小端序）；biHighIndex = 最高非零 digit 下标
4. 每 chunk：`block.digits[j] = a[k] + (a[k+1] << 8)` 小端 16-bit 打包 → `crypt = barrett.powMod(block, e)`
5. 输出 `biToHex(crypt)`：从最高非零 digit 向下、每 digit 4 位小写 hex（= minimal lowercase hex），各 chunk 用**单空格**拼接

## Python 等价（stdlib only）

```python
def encrypt_password(plaintext, modulus_hex, exponent_hex):
    n, e = int(modulus_hex, 16), int(exponent_hex, 16)
    digits = (len(modulus_hex) + 3) // 4          # modulus 的 16-bit digit 数
    hi = max(i for i in range(digits) if ((n >> (16 * i)) & 0xFFFF) != 0)
    chunk_size = 2 * hi                          # 1024-bit → 126（不是 128！）
    a = [ord(c) for c in plaintext[::-1]]
    while len(a) % chunk_size:
        a.append(0)
    out = []
    for i in range(0, len(a), chunk_size):
        block = 0
        for j in range(0, chunk_size, 2):
            k = i + j
            block |= (a[k] + (a[k + 1] << 8)) << (16 * (j // 2))
        out.append(format(pow(block, e, n), 'x'))
    return " ".join(out)
```

## 正方 CAS 链要点

- 公钥：`POST /cas/v1/getPubKey` → `{modulus, exponent}`，存 `localStorage['cas_modulus']` / `cas_exponent`
- 无 OAEP、无随机盐 → **确定性输出**（同明文+同 key = 同密文），弱填充
- OTP 登录（手机/邮箱/APP 验证码）同 reverse+RSA 模式（checkSmsForm/checkEmailForm/checkAppForm）
- 无 `pwdDefaultEncryptSalt` → 非 Apereo，自定义平台
- 相关端点：`GET /cas/kaptcha`（图形验证码）、`GET /cas/getKaptchaStatus`（验证码开关）

## Node 金标准 harness（先于 Python 生成对照）

```js
const fs = require('fs');
global.window = global;                 // js_security.js 是 IIFE (function(window){...})(window)
eval(fs.readFileSync('raw/js_security.js', 'utf8'));
const key = RSAUtils.getKeyPair(exponent, '', modulus);   // d 传空串
console.log(RSAUtils.encryptedString(key, pwd.split('').reverse().join('')));
```

- 测试密钥：`cryptography` 生成 1024-bit RSA，modulus/exponent/d/p/q 存 test_rsa_key.json（含私钥，仅测试用）
- 私钥回解验证：`pow(int(c,16), d, n).to_bytes(chunk_size, 'little')` == 反转明文.encode() + b'\x00' * 填充
  - ⚠️ 别用 `while m:` 逐字节剥 —— 大整数高位零 = 字节串尾部零填充，会被剥掉误报 FAIL
- 多块测试：≥126 字符密码（如 'A'*200 → 2 chunks，chunk 数 = ceil(填充后长/126)）
