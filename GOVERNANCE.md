# Governance

Recall Watch is a volunteer-maintained, unofficial project. The repository owner is the release manager and has final authority over technical direction, merging pull requests and issuing releases. This is not an official Home Assistant governance document.

## Maintainer responsibilities

- Keep the repository's public description, contact channels and documentation current.
- Review changes for security, licensing, data provenance and product-safety wording.
- Require passing automated checks and recorded manual validation before releases.
- Maintain English as the documentation source language and support Swedish translations.
- Never claim a successful Home Assistant Core review, HACS catalog listing, regulatory endorsement or safety guarantee without evidence.

## Decision making

Material changes should begin with a GitHub issue, link to supporting data, and be resolved through a reviewed pull request. Compatibility breaks should be announced in a changelog and release notes. Repository ownership cannot be assigned to a fictitious contributor; the real GitHub owner must be configured before release.

## Maintainer handover

Any change to ownership or release access should be documented in a reviewable GitHub issue or PR, with a transition of CODEOWNERS, `manifest.json` URLs, GitHub settings, release credentials and private vulnerability-reporting access. Do not publish passwords or tokens while performing a handover.
