---
name: src-hunter
description: 实战 SRC / 众测 / Bug bounty 漏洞挖掘工作流 skill。包含：5 阶段方法论（intake → recon → enum → hunt → report）、19 个攻击类 playbook（SQLi/XSS/RCE/SSRF/IDOR/CSRF/Path Traversal/F…
argument-hint: "<target-or-program-or-phase>"
level: 2
---

# SRC Hunter — 实战漏洞挖掘工作流

这是一个**带强制 checkpoint 的工作流**,不是参考手册。每个阶段有 MUST 输出,未通过不进下一阶段。详细 payload / playbook / H1 案例**按需 Read**,不准凭记忆生成。

数据规模、目录树、工具索引见 `README.md`,本文件只管"做什么 / 何时做 / 何时去读哪个文件"。

---

## 触发条件

命中任一即进入:
- "src 挖洞 / 漏洞赏金 / bug bounty / 众测 / hackerone / Security Response Center"
- "如何挖 / 怎么测 / 怎么打 + 某目标 / 某接口 / 某参数"
- "WAF 绕过 / 任意账号 / 任意修改 / 密码重置 / 未授权访问 / 默认凭据"
- 用户给一个 URL / API endpoint / APK 让你测

**不应触发**:纯白盒源码审计 → `code-audit` skill;漏洞修复问答 → 通用对话;CTF → 通用对话。

---

## 反幻觉硬约束(全程适用)

1. **不准凭记忆出 payload**。要给 SQLi/RCE/SSRF/XSS 任何 payload 前,先 Read 对应 `references/playbooks/<type>.md`(或 `<type>/00-index.md` + 具体子文件,见下表)。Phase 4 的 payload 必须能在文件里查到出处。
2. **不准编造案例编号**。引用 H1/WooYun 案例前必须 Read `references/h1-reports/by-weakness/` 下的实际文件。说不出文件路径就别引。
3. **无证据不下结论**。无 HTTP 包/截图/视频时只能写"待验证 / 假设",不写"已确认 / 发现漏洞"。
4. **出 scope 吹哨**。任何时候发现要测的资产不在 Phase 1 已确认的 in-scope 列表 → 一句话提示超 scope 风险，由哥哥裁决是否继续（2026-08-08 新模式），不擅自停手。
5. **疑似漏洞过三审**。发现疑似漏洞后，按 `vuln-verify-pipeline` 快速三审（真假 / 数据 / 可复现）逐一排除，未过三审不得定级、不得提交。
6. **"已提交/已收录"断言必须核对本地文件**。汇报项目提交状态（已提交/收录/受理/驳回）前，先核对本地证据目录（`~/.claude/evidence/` 下的提交单 txt/md 与截图）是否真实存在。记忆中的状态可能把"准备态"误记为"已提交态"（诗路云教训 2026-08-04：Hindsight 曾有"已提交补天 Company/65453 收录确认"错误记录，实际提交单从未生成、补天从未提交）。**提交单文件不存在 = 未提交，一切以本地文件为准**；引用记忆中的状态时同步给出证据文件路径。

---

## Phase 1 · Intake(接单)

**进入条件**:用户首次给出目标 / 程序名 / URL。

**MUST 输出 checkpoint**(四项缺一不进 Phase 2,缺什么向用户问什么,不要假设):

- [ ] **In-scope**:可测域名 / IP 段 / app / endpoint(逐条列)
- [ ] **Out-of-scope**:禁测项(逐条列)
- [ ] **规则**:payout tier / disclosure window / safe-harbor / 测试 header(如 `X-Bug-Bounty:<handle>`)
- [ ] **时间盒**:6h / 单日 / HVV / 月度

**仅当用户问"哪个最值得先测"** → Read `references/methodology/05-srctimebox-priority.md`。

---

## Phase 2 · Recon(被动侦察)

**进入条件**:Phase 1 checkpoint 四项全过。

**禁止**:任何主动发包(端口扫描 / 路径爆破 / payload 测试)。

**MUST 输出**:不发包给目标得到的资产清单 + 历史信息,来源 ≥3 种:
- CT 日志(crt.sh / Censys)
- Wayback / CommonCrawl 历史快照
- GitHub dorks(`org:target` + `password|api_key|SECRET|.env`)
- FOFA / Shodan favicon hash
- SecurityTrails / DNS 历史
- ASN / IP 段(bgp.he.net)

**数据预筛(Phase 3 前做一次;Phase 5 提交前重做)**:
- [ ] 抽 3-5 条样本数据(电话 / 邮箱 / 单号 / 姓名)搜公网(搜索引擎 / 第三方站点 / 目标官网)
- [ ] **有一条搜得到 → 整个洞可能不成立** → 标注"疑似公开数据",回 Phase 4 换攻击面或降级
- [ ] 判断功能设计意图:数据是"服务你"(栏目,零认证是设计使然)还是"关于你"(涉他 PII)?
- [ ] 参考记忆 `public-data-vs-vulnerability` — GetCall 教训:公开业务数据不是漏洞,提交前搜公网

---

## Phase 3 · Enum(主动探测)

**进入条件**:Phase 2 资产清单非空。

**MUST 输出**:活资产矩阵——`域 → 端口 → 服务 → 指纹 → JS endpoint`。

**条件触发 Read**(命中就必读,不命中不读):

| 命中信号 | MUST Read |
|---|---|
| 指纹含 `weaver/seeyon/tongda/landray/yongyou/kingdee/hikvision/dahua` | `references/dictionaries/chinese-srcfingerprints.md` + `references/dictionaries/default-credentials-cn.md` |
| 资产含 银行 / 支付 / 网银 / 第三方支付聚合 | `references/industry/banking-finance.md` |
| 资产含 运营商 / BOSS / 网管 / 物联网卡 | `references/industry/telecom-isp.md` |

---

## Phase 4 · Hunt(漏洞探测)

**进入条件**:Phase 3 矩阵 ≥1 个候选目标。

**🔴 强制 checkpoint(未通过阻塞 Phase 4 主体)**:
- [ ] 为每个候选目标从上表选定了 1 个 playbook
- [ ] **已 Read 该 playbook 文件**(目录型 playbook:00-index.md + 路由到的子文件,两步 Read 未完成不算)
- [ ] 输出中给出 **playbook 文件路径 + 一句摘要**(证明真读,不是凭记忆)
- [ ] 计划使用的每个 payload 都能在已 Read 的文件里查到出处

**未通过 → 停在 checkpoint, Read 再继续。Playbook 未读 = 不出 payload。**

**强制流程(每个候选目标走一遍)**:
1. 看目标信号,从下表选 1 个 playbook
2. **Read 该 playbook 文件**(不准跳过、不准凭记忆替代)→ 完成后输出标注 `✔ playbook 已读: <文件路径>`
3. 按 playbook 的"参数频率表"挑入口
4. 按 playbook 的"payload 库"探测——payload 来自文件,不来自训练记忆
5. 被 WAF 拦 → Read `references/methodology/02-bypass-toolkit.md` 决策树
6. 命中后立即保存 HTTP 包 / 截图 → 进 Phase 5 候选
7. **命中后立即过快速三审（vuln-verify-pipeline）**：正常请求对比 + 数据预筛 + 复现确认，三审通过才列为候选漏洞

| 入口信号 | MUST Read |
|---|---|
| Actuator / Swagger / 默认端口 / 弱密码 | `references/playbooks/unauth-access.md` |
| .git / .svn / .env / heapdump / 路径列举 | `references/playbooks/info-disclosure.md` |
| 用户态 ID 可遍历 / 任意 X 越权 | `references/playbooks/arbitrary-x-authz.md` |
| 密码重置 / 支付 / 验证码 / 订单 / 提现 | `references/playbooks/logic-flaws/00-index.md` |
| OAuth / SAML / JWT / redirect_uri | `references/playbooks/oauth-saml-jwt/00-index.md` |
| REST API / BOLA / Mass Assignment / 速率 | `references/playbooks/api-rest/00-index.md` |
| 任何用户输入进 DB | `references/playbooks/sqli.md` |
| 反序列化 / SSTI / XXE / 原型链 / 框架 RCE | `references/playbooks/rce/00-index.md` |
| URL 入参 / 缓存 / Host 注入 | `references/playbooks/ssrf-cache-host/00-index.md` |
| 文件路径入参 / LFI / RFI | `references/playbooks/path-traversal/00-index.md` |
| 上传点 + 解析漏洞 | `references/playbooks/file-upload/00-index.md` |
| 用户输入回显到 HTML / JS | `references/playbooks/xss/00-index.md` |
| 反代 + Content-Length / TE | `references/playbooks/http-smuggling.md` |
| GraphQL endpoint / introspection | `references/playbooks/graphql.md` |
| 并发 / TOCTOU | `references/playbooks/race-conditions.md` |
| ReDoS / 资源不限速 / 算法爆炸 | `references/playbooks/dos.md` |
| APK / IPA / 移动端 | `references/playbooks/mobile.md` |
| LLM agent / prompt 入口 / 工具调用 | `references/playbooks/llm-prompt-injection/00-index.md` |
| 已拿到 shell / 凭据 / 内网 | `references/playbooks/intranet-postexp/00-index.md` |

**两步 Read 模式(已拆分的 playbook)**:目录形式的 playbook(`rce/` / `oauth-saml-jwt/` / `ssrf-cache-host/` / `api-rest/` / `logic-flaws/` / `file-upload/` / `path-traversal/` / `xss/` / `llm-prompt-injection/` / `intranet-postexp/`)第一步只 Read `00-index.md`——它含**子文件路由表**和通用方法论。**不要把 00-index 当 payload 库用**,据子文件路由定位到具体场景后**再 Read 对应子文件**(如 `rce/14-ssti.md` / `oauth-saml-jwt/12-jwt.md`)。单文件形式的 playbook(`sqli.md` / `xxx.md`)直接 Read 即可。

**通用方法论**(仅在卡壳时 Read,不要预加载):
- 不知道下一步打什么 → `references/methodology/01-attack-priority.md`
- 被 WAF / EDR 拦 → `references/methodology/02-bypass-toolkit.md`
- 怀疑自己幻觉 / 想检查证据链 → `references/methodology/03-evidence-discipline.md`
- 找不到漏洞点 → `references/methodology/04-control-gap-hunting.md`

---

## 🧠 联动（记忆 ↔ 技能 ↔ Kali，2026-08-07 建立）
本技能执行时联动以下资源（不孤立挖洞）：
- **联动总索引**：`D:\tools\sec-kb\notes\README-技能记忆Kali联动总索引.md`
- **学习笔记**：`D:\tools\sec-kb\notes\` 58 份（H1 2369 案例全量补读 / playbook-payload / 默认凭据字典 / 时间盒优先级 / 控制缺口探针表 / RedTeamNotes 全量）
- **Kali 工具**：KaliMCP 29 工具（subfinder/nuclei/sqlmap/netexec 等）
- **流程**：目标 → 查联动索引 → playbook → 笔记 → 工具 → 证据 → 报告

## Phase 5 · Report(提交)

**进入条件**:Phase 4 至少一个 finding 已具备可重现 HTTP 包 / 截图 / 视频。

**MUST 流程**(顺序执行):
1. **对每个 finding 过 `vuln-verify-pipeline` 三审**（快速三审 + 终审定级），未过不提交
2. Read `references/compliance.md` 核对合规红线(不准跳)
3. Read `references/templates/report-submission.md` 取模板
4. 三段式输出:
   - **标题**:≤80 字,精确到 endpoint + 漏洞类型
   - **重现步骤**:每步可执行,带 HTTP 包 / curl / 截图
   - **影响 + 修复建议**:CVSS 4.0 vector + 业务影响段

---

## MCP 工具集成

默认 `mcp__jshook__search_tools` + `mcp__jshook__activate_tools` 按需激活(~3K token)。完整索引仅在用户问"用什么工具 / Burp / Frida / adb"时 Read:`references/tools/mcp-jshook.md`。

## 2026-08-01 实战优化

今日教训(GetCall 埋葬 + oidc redirect_uri bypass + WAF 绕过未用)固化为**强制规则**,同 Phase checkpoint:

1. **Phase 4 强制 checkpoint(血泪)**:每个候选目标出 payload 前 Read 对应 playbook 文件并在输出标注路径。之前跳过 Read 直接出 payload,导致 payload 凭记忆、漏变体。**Playbook 未读 = 不出 payload。**
2. **数据预筛(GetCall 教训)**:提交前抽 3-5 条样本数据搜公网,有一条搜得到整个洞可能不成立。区分"服务你"(栏目,零认证是设计使然)vs"关于你"(涉他 PII)。参考记忆 `public-data-vs-vulnerability`。
3. **WAF 绕再弃**:目标有 WAF → 试 `web-app-security` §3 绕过技术(HTTP 走私 / 竞态条件 / 缓存投毒)再放弃,不准直接降级为"低危"。
4. **OAuth redirect_uri**:见 `api-security-testing` §2.4,逐条测前缀绕过 / @欺骗 / 隐式流 / PKCE / state。

**验证联动**:这些规则同步根 CLAUDE.md"漏洞验证清单"第 6-9 条,Phase 5 提交前逐条核对。完整三审流水线见 `vuln-verify-pipeline` skill（快速三审 + 硬性拒绝规则）。