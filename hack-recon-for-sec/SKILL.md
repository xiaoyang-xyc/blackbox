---
name: recon-for-sec
description: >-
  Entry P1 category router for reconnaissance and methodology. Use when mapping
  scope, discovering assets, fingerprinting technology, building endpoint
  inventory, and choosing the first high-value security testing path.
---

# Recon and Methodology Router

This is the starting router for new targets and unknown attack surfaces.

## When to Use

- You just received a new target and do not yet know what to test first
- You need to begin with asset discovery, tech fingerprinting, endpoint inventory, and test-route planning
- You want to build follow-up testing on structured methodology instead of random payload enumeration

## Skill Map

- [Recon and Methodology](../hack-recon-and-methodology/SKILL.md)
- [Insecure Source Code Management](../hack-insecure-source-code-management/SKILL.md) — .git/.svn/.hg exposure detection
- [Dependency Confusion](../hack-dependency-confusion/SKILL.md) — Supply chain reconnaissance for internal package names

## Recommended Flow

1. First confirm in-scope assets and target type
2. Then perform asset discovery, port/service identification, technology fingerprinting, and endpoint collection
3. Route based on collected findings to [api-sec](../hack-api-sec/SKILL.md), [auth-sec](../hack-auth-sec/SKILL.md), [injection-checking](../hack-injection-checking/SKILL.md), or [business-logic-vuln](../hack-business-logic-vuln/SKILL.md)