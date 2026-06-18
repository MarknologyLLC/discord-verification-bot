# PR Review Process

All changes go through Winston (AI review gate) before Drew merges.

## How it works

1. Paul opens a PR on this repo
2. Winston auto-reviews the diff and posts a structured verdict to `#dev-collab` in Marknology HQ Discord AND on the GitHub PR itself
3. Drew reviews Winston's verdict and squash merges if APPROVED

## Review format

Winston returns 12 sections:
- VERDICT (APPROVED or CHANGES_REQUESTED)
- SUMMARY
- BLOCKERS
- NON-BLOCKING
- RISKIEST FILES
- SCOPE REVIEW
- AUTH / SECURITY REVIEW
- ROUTE / ENDPOINT REVIEW
- COMPONENT / UI REVIEW
- MOBILE / RESPONSIVE REVIEW
- VALIDATION / QA REVIEW
- CODEX FIX PROMPT (copy-paste ready for Codex if changes needed)

## Writing good PR descriptions

Use `PR-DESCRIPTION-TEMPLATE.md`. Include:
- Codex claims (what it changed)
- Validation status (lint/build/tsc passed or not run)
- Manual QA status
- Specific review focus areas

The more structured the PR description, the tighter Winston's review.

## Merge policy

Squash merges only. No direct pushes to main.
