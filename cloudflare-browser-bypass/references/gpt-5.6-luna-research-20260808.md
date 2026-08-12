# GPT-5.6 家族研究（2026-08-08 会话）

## 背景
哥哥问"GPT-5.6 Luna 是否免费了"→ 想注册免费账号让雷姆通过接口与 Luna 互相沟通。
雷姆研究结论 + 浏览器实际操作到注册页（卡在需要哥哥提供邮箱）。

## GPT-5.6 家族（2026-07-09 正式发布，产品线重构）
| 模型 | 定位 | API 价格（官方，7/31 降价后） | ChatGPT 端 |
|---|---|---|---|
| Sol | 旗舰 | $5/M in, $30/M out（降价后约 $2.5/$15） | Plus/Pro 用户，新增增强版 Sol |
| Terra | 均衡 | $2.50/M in, $15/M out | 主力 |
| Luna | 高性价比 | **$1/M in, $6/M out → 降价 80% 后 $0.20/$1.20** | **免费用户默认模型** |

关键事实：
- **2026-08-06 OpenAI 官宣**：ChatGPT 免费用户默认模型升级为 GPT-5.6 Luna，**文字聊天无限量**（取消纯文字速率限制）
- 免费仅限 ChatGPT 网页/App 文字聊天；文件上传、图片生成、工具仍有限额
- 新增 "Think" 按钮，免费用户可手动触发更强推理
- 官方口径：为应对 DeepSeek V4 Flash 等中国高性价比模型的竞争压力

## OpenRouter 实测数据（curl 拉全量模型列表）
- `openai/gpt-5.6-luna` 存在：context 105万 token，价格 **$0.10/M in, $0.60/M out**（比官方 API 便宜一半）
- 全站 14 个 `:free` 模型里**没有 Luna**（免费只有 gpt-oss-20b:free 等开源模型）
- 结论：免费账号无 API key，接口沟通只能走 OpenRouter 付费（很便宜）或浏览器操控

## 注册实操状态（进行中）
- 云浏览器（Browserbase）被 Cloudflare 卡死 → **本机 Chrome + Playwright 直接绕过**（见 SKILL.md + scripts/）
- 已到 `chatgpt.com/auth/login` 登录/注册页，选项：Google / Apple / 电话号码 / 邮箱
- **卡点**：需要哥哥提供邮箱（或 Google/Apple 账号）才能完成注册；雷姆不代输密码/验证码
- 后续若注册成功：雷姆通过 Playwright 操控浏览器与 Luna 对话（免费账号无 API）

## 搜索技巧（本次实测）
- Google → /sorry 验证；DuckDuckGo html → checkbox 墙；Bing → 空页/JS 渲染
- **百度稳定可用**：`https://www.baidu.com/s?wd=<关键词>` 直接出内容（本次核心信息来源）
- OpenAI 官方 openai.com 被 Cloudflare 拦（curl 和浏览器都是）；镜像站内容可信度低，交叉验证用百度新闻源
