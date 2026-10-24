# Security Policy

## Supported versions

| Version | Security status |
| --- | --- |
| `0.3.0b1` | Beta candidate: security fixes may be made, but not approved for production use |
| Earlier pre-release builds | Not supported |

No stable release is available as of 2026-10-24.

## Report a vulnerability privately

**Do not open a public GitHub issue containing an exploit, secrets or personal data.** Once this repository has been published and its owner has enabled GitHub Private Vulnerability Reporting, use **Security → Advisories → Report a vulnerability**. The maintainer must enable this setting before inviting public reporting. If it is not enabled, use a non-public contact method supplied by the repository owner; otherwise ask for a private channel without disclosing vulnerability details.

Please include affected version, impact, reproducible steps and sanitized evidence. Do not probe government websites or other third-party systems beyond authorized ordinary use. Maintainers will acknowledge reports when feasible, coordinate fixes and credit researchers by agreement. No fixed response-time SLA is promised for this volunteer-run project.

## Security boundaries

- The integration fetches a public feed over HTTPS; it does not need a consumer account or send household keyword preferences to the source.
- RSS/Atom XML is treated as untrusted data and parsed with `defusedxml` and size/length limits.
- Headline matching and product extraction are heuristic and never a guarantee of a product's safety.
- The project does not request Home Assistant administrator tokens, passwords or remote shell access.

See [Security and privacy](docs/SECURITY_AND_PRIVACY.md) for the project's threat model and operational assumptions.
