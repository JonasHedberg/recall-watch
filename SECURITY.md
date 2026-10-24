# Security Policy

## Reporting a vulnerability

Use GitHub's **Report a vulnerability** private reporting feature when enabled. Do not disclose live exploit details or secrets in public issues. If private reporting is not enabled, contact the repository maintainer through GitHub and request a private channel before sharing sensitive details.

## Supported versions

There are **no production-supported releases** yet. Version 0.3.0b1 is an unreleased development candidate.

## Security boundaries

- Use only curated, fixed official government HTTPS endpoints; never accept arbitrary remote URLs from users.
- Apply request timeouts, response size limits, safe XML parsing and bounded data retention.
- Never execute remote notice content, use dynamic code evaluation or expose credentials.
- Treat source text as untrusted; extracted batch and product details may be incomplete.
- Treat an absence of notices as **unknown**, not proof of safety.

## Incident handling

The maintainer assesses reports, coordinates remediation, documents affected versions and publishes advisory information where appropriate. No fixed response-time guarantee is offered.
