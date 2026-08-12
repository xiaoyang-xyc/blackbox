---
name: jwt-static-key-bruteforce
description: JWT HS256 静态密钥离线爆破。触发：真 token + 白盒已知派生规则，本地爆破静态 key。
version: 1.0.0
author: hermes-curator
license: internal
metadata:
  tags: [jwt, hs256, bruteforce, offline, shirojwt, dolyw]
  related_skills: [jwt-oauth-token-attacks, unified-pentest]
---

# JWT 静态密钥离线爆破（HS256 弱密钥扩大爆破）

> 适用：白盒/源码已拿到 JWT 密钥派生规则后，本地离线爆破静态 key（零触网，合规）。
> 典型场景：dolyw/ShiroJwt 系教程骨架二开（国内 SRC 高频目标），派生规则 `secret = account + 静态配置值`。

## When to Use（触发条件）

- 有真实 JWT（含签名）+ 源码/白盒确认了密钥派生规则（`secret = X + 静态值` 形态）
- 教程/默认密钥已被生产改掉（伪造 token 签名无效实测确认）
- 需要离线爆破静态 key → 任意账号伪造（顶配危害）

## 1. 先读源码确认派生规则（最重要的一步，决定爆破目标形态）

dolyw/ShiroJwt（com/wang/util/JwtUtil.java）实测确认：
- `secret = account + Base64ConvertUtil.decode(encryptJWTKey)`（sign 与 verify 同源同式）
- 配置（application.yml / config.properties）里 `encryptJWTKey` 存的是 **Base64 字符串**，代码先解码再拼接
- 教程默认：`encryptJWTKey=U0JBUElKV1RkV2FuZzkyNjQ1NA==` → 解码后 `SBAPIJWTdWang926454`
- **含义**：爆破目标是「解码后的明文 key」；命中后报告可顺带给出配置值 = base64(明文)。
  教程默认值常被改掉，但「配置存 Base64」这个习惯常被二开保留——品牌词测明文形态即可，不用测其 base64（因为解码后才进 secret）。

## 2. 本地验证器（重算签名，零联网）

```python
import hmac, hashlib, base64, json
real = open('user-jwt.txt').read().strip()
H, P, S = real.split('.')
acc = json.loads(base64.urlsafe_b64decode(P + '=='))['account']  # 必须从 payload 提取——派生用的就是它
TGT = base64.urlsafe_b64decode(S + '==')
MSG = f'{H}.{P}'.encode()
# 候选 key k：对 (acc+k, k+acc, k) 三结构逐一 hmac.new(v, MSG, hashlib.sha256).digest() == TGT
```

- **自检**：教程默认 key 必须**不**匹配（证明生产改过 + 验证器无误报）。匹配了反而要怀疑验证逻辑。
- 结构三变体：`account+key`（教程原配，最可能）/ `key+account` / `纯key`。顺序按概率排，命中即停。

## 3. 候选生成配方（2026-08 shiluyun 实战验证）

1. **定制小字典先行**（单进程秒级跑完，命中就免开 Pool）：
   - 品牌全拼/简拼：shiluyun / sly / lingdayun / lingda / ldy / wsydt / hangzhou / hz / 0571 / 科技类后缀 keji/tech
   - × 后缀：年份 2015-2026、123、123456、@123、!、!@#、888、666、520、1314、168、8888、6666、5201314、123123、9527、10086、10010…
   - × 首字母大写 / 全大写；前缀变体（123+词、2024+词、0571+词）
   - **中文原文**（如 诗路云/灵答/微商一点通）：java-jwt 的 HMAC256(String) 用 UTF-8 bytes，Python `encode('utf-8')` 直接可测，别跳过
   - 教程默认值系（SBAPIJWT / dWang926454 / 作者名 dolyw）、账号本身 + 后缀
   - 创始人/作者名未知 → 跳过，别瞎编
2. **rockyou 截断策略**（预算受限时）：
   - 前 5M 词 × 全规则（原样 + 12 年份 + 9 符号数字 + 首字母大写 + 全大写 = 24 变体/词）
   - 剩余词 × 高价值规则（原样 + 年份 + @123 + 123 = 15 变体/词）
   - 每词用 set 去重（大写与原样碰撞），跳过空串
3. **命中输出**：`jwt-key-cracked.txt` 写 `static_key=<明文>` + `config_value_b64=<base64>` + `account=<账号>`，并本地重算签名确认一次。

## 4. Windows 多进程坑（实战实测，必踩）

- `multiprocessing.Pool` 在 Windows 是 **spawn** 模式：~40s 启动延迟，第一条进度线的 rate 会显示 0.01M/s 的假象 → **不要据此杀任务**，等第二条进度线再判断速率是否恢复。
- **计数单位陷阱**：worker 里 `n += len(variants)` 数的是「变体数」，每变体 ×3 结构 = 3 次 HMAC。台账要报 HMAC 数（×3），否则覆盖量虚报 3 倍、和历史轮口径对不上。
- 速率参考：i9-13980HX、24 进程、纯 Python hmac ≈ 2.4M HMAC/s；14.34M 词 × 24/15 规则 × 3 结构 ≈ 7.8 亿 HMAC ≈ 5.5 分钟。
- deadline 用 argv 传入，主循环 `elapsed > deadline` → `pool.terminate()` 后**如实报已跑量**（未跑完不算命中）。
- 进度打印：`imap_unordered` + 每 ~8s 一次，输出 词数/hmacs/rate/耗时 四要素。

## 5. 台账口径

本轮覆盖 = 定制字典条数 + Σ(词数 × 规则数 × 3 结构)；速度 = ΣHMAC / 总秒数。
**累计口径必须与历史轮一致**（如历史「43M」= 14.34M 词 × 3 结构 = 43M 次 HMAC，不是 43M 词）。

## 6. 未命中后的下一步方向（别再无限扩规则）

1. GitHub 代码搜索该厂牌/品牌词 + `encryptJWTKey|jwt|secret` 反搜真实配置值（二开常把配置提交进公开仓库）
2. 前端 JS 产物 / 子域名 / 历史泄露源里捞配置片段
3. 对 encryptJWTKey 直接爆破其 **Base64 字符串形态**（防「配置里存了非 base64 的怪串」）
4. dolyw/ShiroJwt 衍生项目常见二开 key 清单

## 参考脚本

可复用骨架：`D:\tools\audit\shiluyun\jwt_crack_t5.py`（定制字典先行 + rockyou 前 5M 全规则/剩余高价值规则 + 3 结构 + deadline 参数 + 进度台账，Windows 24 进程实测 ~2.4M HMAC/s）。
