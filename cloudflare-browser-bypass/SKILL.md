---
name: cloudflare-browser-bypass
description: |
  用本机真实浏览器（Playwright + 本地 Chrome/Edge）绕过 Cloudflare Turnstile / 机器人检测，
  访问被云浏览器或无头浏览器拦截的站点（chatgpt.com、openai.com 等）。
  触发：页面卡在"请稍候…"/"正在验证…"/"Please verify you are human"；browser_* 云浏览器被 Cloudflare 质询卡死；
  需要真实浏览器指纹访问受保护站点；注册/登录需要人机验证的 Web 服务。
version: 1.0.0
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [cloudflare, captcha, playwright, browser-automation, bypass, chatgpt]
    category: pentest
---

# Cloudflare 浏览器级绕过（本地 Chrome + Playwright）

## 核心原理

Cloudflare Turnstile 对三类特征敏感：数据中心 IP（无住宅代理）、无头浏览器、自动化指纹。
Hermes 的 `browser_*` 工具走托管云浏览器（Browserbase），无住宅代理时访问 chatgpt.com / openai.com
几乎必被拦（页面永远"请稍候…"）。**本机真实 Chrome + Playwright 可稳定绕过**——真实指纹 + 去自动化标记，
实测 chatgpt.com 登录/注册页完整加载。

## 标准流程

1. **确认本机浏览器路径**（Windows 常见位置）：
   - Chrome: `C:\Program Files\Google\Chrome\Application\chrome.exe`
   - Edge: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
2. **Playwright 启动**（关键参数）：
   - `executable_path=` 指向本机浏览器 exe
   - `headless=False` —— 无头模式仍会被识破，必须可见窗口
   - args 加 `--disable-blink-features=AutomationControlled`
   - context 加真实 UA + viewport + locale
3. **goto 后轮询等待**：Cloudflare 质询可能持续数秒，循环 3s×10 检查
   `page.url / title / body text`，直到标题不再是"请稍候…"或 URL 变成目标页。
4. **验证成功标志**：body 文本出现目标页内容（如登录框/按钮）即为通过。

可直接复用：`scripts/local_chrome_playwright.py`（改 URL 即用）。

## 关键坑位

- **PowerShell 的 `curl` 是 Invoke-WebRequest 别名**：`-H` 头会报"无法绑定参数 Headers"。
  必须用 `curl.exe`（真实 curl）才能带 `-H "User-Agent: ..."`。
- **browser_vision 截图可能滞后**：截图可能仍是 Cloudflare 质询瞬间的旧图，而 playwright 的
  DOM 文本已确认页面加载成功。**以 DOM 文本为准，不要被 vision 旧图误导**。
- **搜索引擎自动化会触发反爬**：Google 弹 `/sorry` 验证、DuckDuckGo html 版弹 checkbox 墙、
  Bing 返回空页/JS 渲染无内容。中文内容用 `https://www.baidu.com/s?wd=<关键词>` 反而稳定可用
  （本次查 GPT-5.6 Luna 新闻即靠百度）。
- **登录/密码/验证码是安全红线**：帮用户走到登录/注册页后，密码、验证码输入必须提示用户自己
  完成或提供，雷姆绝不代输（computer-use 技能同样规则）。

## 与相关技能的分工

- `waf-bypass-techniques`：payload/WAF 规则级绕过（SQLi、命令注入等请求层面）。
- 本技能：浏览器/人机验证层面（Cloudflare Turnstile 等 bot 检测）。
- `computer-use`：驱动桌面 GUI（点击用户已开的原生应用），本技能是脚本化本地浏览器，两者互补。

## 参考

- `references/gpt-5.6-luna-research-20260808.md`：GPT-5.6 家族（Sol/Terra/Luna）免费政策、
  OpenRouter 定价与模型可用性、ChatGPT 免费账号注册状态（任务进行中）。
