"""本地 Chrome + Playwright 绕过 Cloudflare 质询的标准模板（实测可用）。

用法:
    python local_chrome_playwright.py <url> [--keep-open]

把 URL 换成目标站点即可。默认启动可见 Chrome 窗口，轮询等待 Cloudflare 质询通过，
打印页面标题/URL/正文前 300 字，并截图到 TEMP\cloudflare_bypass.png。

依赖: pip install playwright  (python -m playwright install chromium 非必需，
      因为本模板直接复用本机 Chrome，无需下载 Playwright 自带浏览器)
"""
import asyncio
import sys
from playwright.async_api import async_playwright

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_browser():
    import os
    for p in CHROME_PATHS + EDGE_PATHS:
        if os.path.exists(p):
            return p
    raise SystemExit("未找到本机 Chrome/Edge，请手动指定 executable_path")


async def main(url: str, keep_open: bool = False):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=find_browser(),
            headless=False,  # 必须可见窗口，无头会被识破
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
            ],
        )
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
        )
        page = await ctx.new_page()
        try:
            await page.goto(url, timeout=45000, wait_until="domcontentloaded")
        except Exception as e:
            print("goto err:", e)

        # 轮询等待 Cloudflare 质询通过（最长 ~30s）
        passed = False
        for i in range(10):
            await page.wait_for_timeout(3000)
            title = await page.title()
            url_now = page.url
            text = ""
            try:
                text = (await page.inner_text("body"))[:300]
            except Exception:
                pass
            print(f"[{i}] url={url_now} title={title!r} text={text[:100]!r}")
            if "请稍候" not in title and "just a moment" not in title.lower() and title.strip():
                passed = True
                break

        print("PASSED" if passed else "STILL BLOCKED", "| final url:", page.url)
        await page.screenshot(path=r"C:\Users\user\AppData\Local\Temp\cloudflare_bypass.png")
        print("screenshot -> C:\\Users\\18270\\AppData\\Local\\Temp\\cloudflare_bypass.png")

        if keep_open:
            # 保持窗口开着，供用户手动完成登录/验证码等操作（雷姆不代输密码）
            print("窗口保持打开，用户可手动操作。Ctrl+C 退出。")
            try:
                while True:
                    await page.wait_for_timeout(5000)
            except asyncio.CancelledError:
                pass
        await browser.close()


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://chatgpt.com/auth/login"
    keep = "--keep-open" in sys.argv
    asyncio.run(main(target, keep))
