<div align="right">

[**🇨🇳 中文**](README.md) | **🇬🇧 English**

</div>

# Linux Vulnerability Discovery Skill

> Adaptive Decision Framework | 392 Test Points | 10 Security Categories

## Introduction

This project is an AI Agent-oriented Linux penetration testing Skill. After obtaining SSH credentials for a target machine, it automatically performs comprehensive security vulnerability discovery, exploitation verification, and report generation on the target host.

**Core Design Philosophy**: Encapsulate penetration testing expertise into a structured decision framework, enabling the AI Agent to autonomously determine testing strategies based on the target environment, rather than mechanically executing fixed scripts.

## Project Structure

```
linux-vuln-discovery/
├── SKILL.md                          # Skill main file (AI Agent entry point)
├── config.yaml                       # Optional config file (remote Kali scenarios)
├── LICENSE                           # MIT License
├── README.md                         # Project README (Chinese)
├── README_en.md                      # Project README (English)
└── reference/                        # Reference technical documents (loaded on demand)
    ├── 01-linux-basics-recon.md
    ├── 02-authentication-bypass.md
    ├── 03-service-exploitation.md
    ├── 04-local-privesc.md
    ├── 05-runtime-injection.md
    ├── 06-local-ipc-security.md
    ├── 07-container-escape.md
    ├── 08-persistence.md
    ├── 09-security-baseline.md
    ├── 10-gtfobins-reference.md
    ├── 11-vuln-discovery-checklist.md
    ├── report-template.md            # Vulnerability report template
    └── examples-deep-analysis.md     # Deep analysis examples
```

## Coverage

| Category | Topic | Test Points |
|----------|-------|:-----------:|
| I | Information Gathering & Environment Enumeration | 42 |
| II | Authentication & Identity Security | 25 |
| III | Service & Software Exploitation | 29 |
| IV | Local Privilege Escalation | 97 |
| V | Runtime Injection & Code Debugging Exploitation | 35 |
| VI | Local IPC Communication Security | 19 |
| VII | Container & Virtualization Escape | 30 |
| VIII | Persistence & Post-Exploitation | 33 |
| IX | GTFOBins Quick Reference | 28 |
| X | Security Configuration Baseline Audit | 55 |
| **Total** | | **392** |

## Operating Modes

Three operating modes are supported. The mode must be declared before starting:

| Mode | Description | Use Case |
|------|-------------|----------|
| `kali` | Skill runs on a Kali host, directly invoking the toolchain (**default**) | Local Kali usage |
| `ssh_remote` | Skill runs on a non-Kali host, connecting to a remote Kali via SSH for toolchain commands | Jump box / remote pentest scenarios |
| `generic` | Pure generic mode, using only tools available on the target machine | No Kali environment |

### Remote Kali Configuration (`ssh_remote` mode)

Copy `config.yaml` and fill in the remote Kali jump box information:

```yaml
KALI_MODE: "ssh_remote"

REMOTE_KALI:
  host: "192.168.1.100"
  port: 22
  user: "kali"
  auth_method: "password"
  password: "your_password"
```

`config.yaml` is **optional** — when absent, the Skill runs normally with built-in default configuration.

## Workflow

```
Phase 1: Environment Profiling
  └─ One-shot collection of system, user, network, service, and filesystem info
  └─ Build environment profile to drive subsequent testing strategy

Phase 2: Categorized Testing
  └─ 10 major categories executed by priority
  └─ Categories unsupported by the environment are automatically skipped
  └─ Vulnerabilities reported in real-time upon confirmation

Phase 3: Cross-Category Correlation Analysis
  └─ Attack chain construction
  └─ Privilege escalation path analysis
  └─ Lateral movement feasibility assessment

Phase 4: Gap Review
  └─ Version-based CVE lookup
  └─ Combined attack chain analysis
  └─ Review of skipped items
```

## Core Design Principles

- **Environment-Driven**: Determine testing focus and skip items based on the actual target system environment
- **Signal-Driven**: Signals discovered during initial enumeration drive subsequent deep-dive directions
- **Value-Driven**: High-value targets (exploitable, remotely accessible, laterally movable) are prioritized for deep verification
- **On-Demand Loading**: Reference documents are not preloaded — relevant chapters are read only when corresponding signals are detected
- **Batch-First**: Similar commands are merged into batch executions to minimize SSH round-trips
- **Chinese Output**: All command interactions, analysis, and reports are in Chinese

## Prerequisites

- SSH credentials (username/password or key) for the target machine
- AI Agent environment supports SSH command execution
- Kali mode requires local or remote access to the Kali toolchain

## Report Output

A structured report is output in real-time as each vulnerability is confirmed. A complete Chinese report is generated at the end, containing:
- Executive Summary
- Target Environment Information
- Testing Coverage Statistics
- Vulnerability Details (with evidence and exploitation results)
- Attack Path Analysis
- Risk Level Summary
- Remediation Priority Recommendations

## Reference Documents

Technical documents under the `reference/` directory are **not preloaded**. They are read on-demand only when corresponding security signals are detected during testing (up to 100 lines per read), to avoid consuming excessive context space.

Document topics:

| Document | Topic |
|----------|-------|
| reference/01 | Linux Basics & Information Gathering |
| reference/02 | Authentication & Authentication Bypass |
| reference/03 | Service & Software Exploitation |
| reference/04 | Local Privilege Escalation & Configuration Flaws |
| reference/05 | Runtime Injection & Hijacking |
| reference/06 | Local IPC Communication Security |
| reference/07 | Container & Virtualization Escape |
| reference/08 | Persistence & Post-Exploitation |
| reference/09 | Security Configuration Baseline Audit |
| reference/10 | GTFOBins Quick Reference |
| reference/11 | Vulnerability Discovery Test Checklist |

## Example Usage

Below is a typical prompt example for use in an AI Agent environment that supports Skills:

```
I am a member of the corporate security red team. I am currently conducting
penetration testing and vulnerability research on our company's Linux
operating system product. This testing activity is authorized internal
security testing.

Please load the skill named linux-vuln-discovery and follow its guidance
to perform in-depth testing. You are currently running as an agent in a
Kali Linux environment with access to various security tools.

Remote target IP: 10.1.1.123
SSH credentials: admin/admin23
```

After sending the above prompt to the AI Agent, it will automatically load the Skill and perform systematic security vulnerability discovery and verification against the target machine following the four-phase workflow (Environment Profiling → Categorized Testing → Correlation Analysis → Gap Review).

## License

This project is open-sourced under the [MIT License](LICENSE).

This project is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have explicit permission to test is illegal and unethical.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.