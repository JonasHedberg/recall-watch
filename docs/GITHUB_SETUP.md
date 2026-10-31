# GitHub repository setup (maintainer runbook)

**This repository must be public to work with HACS and Home Assistant Marketplace.** See [HACS general requirements](https://hacs.dev/docs/publish/start/) and [Marketplace repository structure](https://contributors.home-assistant.io/marketplace/reference/repository-structure/).

The public repository already exists at [JonasHedberg/recall-watch](https://github.com/JonasHedberg/recall-watch). Its initial source tree is a beta candidate, **not a public release**. The instructions below also describe how to set up a fork or other account.

## 1. Create the repository

1. Sign in at GitHub and select **New repository**.
2. Repository name: `recall-watch`. Owner: your personal account or organization.
3. Visibility: **Public**. Set the default branch to `main`.
4. Do **not** initialize with another README, license or `.gitignore`; they are included already.
5. After creation, enable **Issues** and **Actions**. Optionally enable Discussions.
6. Description: `International product recall monitoring for Home Assistant: Sweden, Canada, United Kingdom and United States.`
7. Topics: `home-assistant`, `homeassistant`, `hacs`, `custom-integration`, `food-safety`, `product-recalls`, `sweden`, `canada`, `united-kingdom`, `united-states`, `python`.
8. Under repository **Settings → Security and quality → Advanced Security**, enable **Private vulnerability reporting**. The exact labels can change.

## 2. Apply owner-specific metadata

From the local repository root, replace `YOUR_GITHUB_OWNER` with your **real** GitHub account or organization name:

```sh
python scripts/configure_repository.py --owner YOUR_GITHUB_OWNER
python scripts/validate_repository.py
python scripts/pre_release_check.py
```

This updates `manifest.json`, `.github/CODEOWNERS` and the custom-repository path in `README.md`. It does **not** create a GitHub account, repo or a release. Review changes and check that the owner exists and has publishing rights. Use the repository name `recall-watch`; changing it requires updating links and metadata consistently.

## 3. Publish the files

```sh
git init -b main
git add .
git commit -m "Add international Recall Watch 0.3 beta candidate"
git remote add origin https://github.com/YOUR_GITHUB_OWNER/recall-watch.git
git push -u origin main
```

If the ZIP was extracted inside another Git repository, run these commands in a new clean directory or adapt them to your existing branch. Do not check in secrets, personal data, caches or CI tokens. GitHub may prompt for authentication through its configured credentials/CLI.

## 4. Set repository protections

- Require pull requests, reviews and passing CI checks for protected `main` when available on your plan.
- Give GitHub Actions only **read** permission by default; maintainers handle releases manually.
- Enable Dependabot alerts and update pull requests where available.
- Confirm `README.md`, license, contribution and security policies appear under GitHub's community standards.
- Run and inspect the `Check integration` workflow after the first push. Fix all errors, including Home Assistant brands/manifest warnings.
- Do not claim HACS catalog approval merely because the repository is public.

## 5. Brand assets and catalog

HACS documentation requires an appropriate entry in [home-assistant/brands](https://github.com/home-assistant/brands); files under `custom_components/recall_watch/brand/` alone do **not** satisfy that requirement. Follow current brand instructions and complete review externally before seeking default-catalog inclusion.

See [Release process](RELEASE_PROCESS.md), [HACS / Marketplace](HACS_MARKETPLACE.md) and [Release checklist](RELEASE_CHECKLIST.md). The initial beta is intended for a **custom repository**, not a default-catalog submission while used primarily as a candidate for Home Assistant Core.


## Updating an existing public repository

Since `recall-watch` already exists, **do not** run `git init` or create a second repository. Place the files into a feature branch of the existing repository, review `git diff`, run tests, and open a pull request. See [RELEASE_PROCESS.md](RELEASE_PROCESS.md). Updating ZIP files locally does not push or modify GitHub.
