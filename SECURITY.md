# Security & Regulatory-Accuracy Policy

## Scope clarification

The repositories in this account are **open reference implementations and decision-support tools**. They are **not medical devices**, **not certified regulatory submissions**, and **not clinical advice**. Security here means: (a) the integrity of the code/tools, and (b) the accuracy of regulatory references.

## Reporting a vulnerability

If you find a security vulnerability in the code (e.g. unsafe eval, path traversal, supply-chain issue):

1. **Do not open a public Issue.**
2. Email the maintainer via the contact shown in the repository README, or use GitHub's private security advisory for the repo.
3. Include: affected repo/version, reproduction steps, impact, suggested fix.

We aim to acknowledge within **7 days** and provide a remediation plan within **30 days** for confirmed issues.

## Reporting regulatory-accuracy concerns

If a regulatory constant, citation, or date appears wrong or outdated:

1. Open an Issue with label `regulatory-accuracy`.
2. Provide: the exact claim, the official source + version + URL, and the date you verified it.
3. We will correct the value and stamp a new "verified on" date. Until then the field is marked `⚠️ 待核实`.

## What we will NOT do

- We will not silently change medical-risk calculations or regulatory judgments for layout/cosmetic reasons. Such changes require an Issue, impact analysis, and maintainer approval.
- We will not present static analysis as a runtime test, nor present unaudited code as expert-reviewed.

## Supported versions

Only the latest `main` of each actively maintained module is supported for security fixes.
