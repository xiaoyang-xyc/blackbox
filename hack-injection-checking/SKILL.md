---
name: injection-checking
description: >-
  Entry P1 category router for injection testing. Use when routing between XSS,
  SQLi, SSRF, XXE, SSTI, command injection, and NoSQL injection workflows based
  on how attacker-controlled input is consumed.
---

# Injection Testing Router

This is the routing entry point when input reaches a dangerous interpreter or execution environment.

After confirming this is an injection-class issue, use it to decide whether it is mainly browser context, database, template engine, server-side requests, XML parsing, or system commands.

## When to Use

- Input reaches HTML, JS, SQL, templates, URL fetchers, XML parsers, or shell
- You have not yet decided whether to start with XSS, SQLi, SSRF, XXE, SSTI, CMDi, or NoSQL
- You need to choose the correct deep-topic skill based on input flow

## Skill Map

- [XSS Cross Site Scripting](../hack-xss-cross-site-scripting/SKILL.md)
- [SQLi SQL Injection](../hack-sqli-sql-injection/SKILL.md)
- [SSRF Server Side Request Forgery](../hack-ssrf-server-side-request-forgery/SKILL.md)
- [XXE XML External Entity](../hack-xxe-xml-external-entity/SKILL.md)
- [SSTI Server Side Template Injection](../hack-ssti-server-side-template-injection/SKILL.md)
- [CMDi Command Injection](../hack-cmdi-command-injection/SKILL.md)
- NoSQL Injection
- [Deserialization Insecure](../hack-deserialization-insecure/SKILL.md)
- [JNDI Injection](../hack-jndi-injection/SKILL.md)
- [Expression Language Injection](../hack-expression-language-injection/SKILL.md)
- [CRLF Injection](../hack-crlf-injection/SKILL.md)
- [Extra Injection Types (SSI, LDAP, XPath)](./EXTRA_INJECTION_TYPES.md)
- [Request Smuggling](../hack-request-smuggling/SKILL.md)
- [Prototype Pollution](../hack-prototype-pollution/SKILL.md)
- [Type Juggling](../hack-type-juggling/SKILL.md)
- [HTTP Parameter Pollution](../hack-http-parameter-pollution/SKILL.md)
- [XSLT Injection](../hack-xslt-injection/SKILL.md)
- [CSV Formula Injection](../hack-csv-formula-injection/SKILL.md)

## Recommended Flow

1. First identify the final sink of the input
2. Then choose the topic skill that best matches that interpreter
3. Small payload samples and quick triage are merged into each main skill; no extra payload router is needed

## Related Categories

- [file-access-vuln](../hack-file-access-vuln/SKILL.md)