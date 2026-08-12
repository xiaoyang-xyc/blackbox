---
name: api-sec
description: >-
  Entry P1 category router for API security. Use when choosing between API
  recon, authorization, token abuse, and hidden-parameter workflows before any
  deeper API topic skill.
---

# API Security Router

This is the routing entry point for API security testing.

Use this skill first to decide whether the API issue is mostly recon/docs, object authorization, token trust, or GraphQL/hidden parameters, then route to a deeper topic skill.

## When to Use

- The target exposes REST APIs, mobile backends, or GraphQL endpoints
- You need to define API testing order before going into specific topics
- You want to handle object authorization, JWT, GraphQL, and hidden fields as separate tracks

## Skill Map

- [API Recon and Docs](../hack-api-recon-and-docs/SKILL.md): OpenAPI, Swagger, version drift, hidden documentation
- [API Authorization and BOLA](../hack-api-authorization-and-bola/SKILL.md): BOLA, BFLA, method abuse, hidden writable fields
- [API Auth and JWT Abuse](../hack-api-auth-and-jwt-abuse/SKILL.md): bearer token, header trust, claim abuse, rate-limit bypass
- [GraphQL and Hidden Parameters](../hack-graphql-and-hidden-parameters/SKILL.md): introspection, batching, undocumented fields, hidden parameters

## Quick Triage

| Observation | Route |
|---|---|
| Swagger or OpenAPI is present | [api-recon-and-docs](../hack-api-recon-and-docs/SKILL.md) |
| IDs appear in URL, JSON, headers, or GraphQL args | [api-authorization-and-bola](../hack-api-authorization-and-bola/SKILL.md) |
| JWT token visible in traffic | [api-auth-and-jwt-abuse](../hack-api-auth-and-jwt-abuse/SKILL.md) |
| `/graphql` or batched JSON arrays are present | [graphql-and-hidden-parameters](../hack-graphql-and-hidden-parameters/SKILL.md) |
| Registration, login, or profile updates accept extra fields | [api-authorization-and-bola](../hack-api-authorization-and-bola/SKILL.md) then [api-auth-and-jwt-abuse](../hack-api-auth-and-jwt-abuse/SKILL.md) |

## Recommended Flow

1. Start with exposed endpoints and documentation assets
2. Then evaluate object-level and function-level authorization
3. Then evaluate token, header, signature, and rate-limit boundaries
4. If GraphQL or complex JSON is present, continue with hidden fields and schema abuse

## Related Categories

- [auth-sec](../hack-auth-sec/SKILL.md)
- [business-logic-vuln](../hack-business-logic-vuln/SKILL.md)
- [recon-for-sec](../hack-recon-for-sec/SKILL.md)