# Security, privacy and threat model

## Data flow

Home Assistant makes outbound HTTPS requests to the selected fixed government endpoints (Sweden, Canada, the UK and the US). Each configured source is polled on a six-hour interval. The client parses a bounded response locally, matches locally configured keywords and publishes Home Assistant sensor state and a response-only action. No Recall Watch cloud backend is used. HTTP access may expose the user's Home Assistant host IP address to the source as in ordinary web traffic; do not imply the fetch is anonymous.

## Assets and risks

| Asset / attack surface | Mitigation or requirement |
| --- | --- |
| Untrusted RSS XML/HTML | Defused parser, bounded payload and field lengths; do not execute embedded content |
| Resource exhaustion | Timeouts, 2 MiB content cap, maximum 250 parsed items, paginated action results |
| Incorrect extraction | Conservative rules, explicit unknown values, source links, manual accuracy review required |
| Home Assistant recorder | Small preview attributes, cached response-only action for larger result sets |
| Personal keyword preferences | Stored by Home Assistant; not added to outbound RSS URLs |
| Dependencies and upstream changes | Pin runtime `defusedxml` version; review Dependabot updates and release test results |
| Malicious issues/logs | Strip credentials and personal paths before posting; use private reporting for vulnerabilities |

## What the integration does not do

No remote commands, device actuation, authentication to third-party accounts, personal shopping inventory, analytics SDK, hidden telemetry or automatic email/SMS notifications. Standard Home Assistant logging, recorder configuration and backups are administered by the user and may persist sensor states locally.

## Governance

Source URLs, file formats, reuse rights and rate limits must be rechecked before public release and periodically afterward. A parsed record is **not** a legal or regulatory certification that a specific product matches a recall. Users must consult the official agency notice.


## International adapter threat model

All supported source URLs are constants in `_client/sources.py`; user input can only select a known source ID, preventing arbitrary-URL configuration. Responses are capped at 2 MiB and parsed with `defusedxml` or the built-in JSON parser. User filters are processed locally and are not sent to government APIs. Upstream servers see the requester IP address and normal HTTPS metadata. The CPSC API receives an automatically generated last-published date parameter, not private product/household data. Each configured source is isolated by source ID; cross-source action data requires explicitly choosing one source.

Remote data is untrusted. Strings and URL fields are bounded; the presence of a hazard phrase does not determine that an individual product is affected. Sources may change content or remove records, and loss of source access must produce a failed update, never a fabricated healthy/safe state. This integration is not authorized to advise on medical decisions.
