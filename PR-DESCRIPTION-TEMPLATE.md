# PR Description Template
# Use this on every PR. The more detail you provide, the tighter Winston's review.

## Context
[What this PR is trying to accomplish.]

## Codex claims
- [What Codex says it did -- one bullet per change]
- [Be specific: "Added X to Y", "Moved Z"]
- [Include what was NOT done: "No DB migrations", "No direct client writes"]

## Changed files
- [file 1]
- [file 2]

## Validation
- lint: [passed / failed / not run]
- build: [passed / failed / not run]
- tsc: [passed / failed / not run]
- authenticated manual QA: [what was tested, or "not run"]

## Review focus
- [Specific thing Winston should verify]
- [Auth gate, data exposure, routing regression, mobile breakage, etc.]
