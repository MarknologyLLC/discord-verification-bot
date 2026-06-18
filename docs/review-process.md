# PR Review Process

All changes go through Winston (AI review gate) before Drew merges.
Winston acts as a strict reviewer, not a co-author.

## Verdicts

- **APPROVED** -- ready for Drew to merge
- **CHANGES REQUESTED** -- specific blocker must be fixed first
- **NEEDS MANUAL DREW DECISION** -- product/hosting/strategy decision required

Use NEEDS MANUAL DREW DECISION for:
- Hosting preference (Mac Mini vs cloud)
- Server role strategy
- Approval model changes
- Google Sheets / ClickUp integration decisions
- Whether applications should stay local or move to a database

Winston does not merge automatically unless Drew explicitly enables that.

## What Winston checks on every PR

**Security:**
- No secrets committed (.env, tokens, IDs)
- .env.example uses only placeholders
- creators.json and exports are gitignored

**Discord-specific:**
- No bad permission assumptions (bot role above verified role required)
- Role hierarchy problems
- Slash commands properly scoped to staff/admin roles
- Message Content Intent required -- flagged if removed

**Code quality:**
- Broken slash commands
- Missing or inaccurate setup docs
- Poor error handling
- Mismatch between docs and code

**Scope:**
- PR only touches this repo (no drift into other apps)
- No new features during extraction phase (first PR must be boring and clean)

**Data privacy:**
- creators.json not committed
- Applicant data stays private
- Export is ephemeral (ephemeral response, not saved to repo)

**Deployment:**
- Install/run instructions accurate
- No deployment fragility introduced

## Review output format (12 sections)

VERDICT
SUMMARY
BLOCKERS
NON-BLOCKING
RISKIEST FILES
SCOPE REVIEW
AUTH / SECURITY REVIEW
ROUTE / ENDPOINT REVIEW
COMPONENT / UI REVIEW
MOBILE / RESPONSIVE REVIEW
VALIDATION / QA REVIEW
CODEX FIX PROMPT (copy-paste ready for Codex if changes needed)

## First PR scope

The first PR should be boring and clean:
- Extract bot into this repo
- Safe .gitignore
- Correct .env.example
- README
- Deployment notes
- Dependencies confirmed

No new features. No flow changes unless required to make the bot runnable.
Feature changes come after the extraction is clean and approved.

## Merge policy

Squash merges only. No direct pushes to main. Drew merges after APPROVED verdict.
