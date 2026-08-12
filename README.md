# blackbox

黑盒安全测试技能集（Black-box Security Testing Skills）

AI Agent 使用的黑盒渗透 / 外部攻击面测试技能合集。每个技能一个独立目录，含 `SKILL.md` 与 `references/`。

## 技能清单

| 技能 | 说明 |
|------|------|
| [rem-execution-boost](./rem-execution-boost/) | 雷姆执行增强模式——改编自 gpt-5.6-instruct v45 破甲提示词机制，去毒化后适配 Hermes Agent，用于授权渗透场景下提升 Agent 执行力与任务推进韧性 |

## 安装

方式一（Hermes CLI）：

```bash
hermes skills install <技能目录路径>
```

方式二（手动）：将技能目录复制到 Hermes skills 目录（如 `~/AppData/Local/hermes/skills/pentest/`），开新会话生效。

## 声明

本仓库所有内容仅供**授权范围内**的安全测试、本地靶场练习与安全研究使用。对未授权目标的主动测试行为与作者无关。
