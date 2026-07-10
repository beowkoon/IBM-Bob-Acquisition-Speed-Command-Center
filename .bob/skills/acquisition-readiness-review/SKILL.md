---
name: acquisition-readiness-review
description: Use when the user wants to review, assess, or check Day 1 to Day 100 acquisition integration readiness — walks through readiness scoring, workstream gaps, blockers, and next steps.
---

# Acquisition Readiness Review

Follow these steps to conduct a structured Day 1 to Day 100 readiness review.

## Step 1 — Load Workspace Context

Read the integration status data to understand current readiness:
- Use `read_file` to check `sample_data/integration_status.csv` (or the uploaded file if available).
- Identify how many workstreams are Complete, In Progress, At Risk, or Not Started.
- Calculate the overall readiness score (Complete=100, In Progress=60, At Risk=30, Not Started=0).

## Step 2 — Identify Gaps and Blockers

Review each workstream and flag:
- Any items marked **At Risk** or **Not Started** as priority blockers.
- Any items where an owner has not been assigned.
- Dependencies between workstreams (e.g. finance mapping must precede system cutover).

## Step 3 — Assess Day 1 vs Day 100 Readiness

Split the assessment into two horizons:

**Day 1 Readiness** (minimum requirements):
- Payroll continuity confirmed
- Legal entity structure clear
- Systems access provisioned
- Key SMEs identified and engaged
- Critical risks mitigated or owned

**Day 100 Readiness** (stabilization):
- Finance mapping complete
- Workforce alignment confirmed
- Legal entity simplification in progress
- Budget and savings tracking active
- Knowledge library populated

## Step 4 — Structure the Executive Output

Respond in this format:

**Executive Summary** — Overall readiness percentage and headline status.

**Agent Capabilities Used** — List which agents were applied (Integration Navigator, Risk & Controls, etc.).

**Readiness by Workstream** — Table or list of each area with status and owner.

**Gaps and Blockers** — Prioritized list of incomplete or at-risk items.

**Recommended Actions** — Numbered list of concrete next steps.

**Owners** — Who is responsible for each open action.

**Timeline** — Day 1 date and Day 100 date with key milestones.

**Risks** — Top risks that could delay readiness.

**Budget / Savings / Cash Impact** — Any cost or savings implications from readiness gaps.

**Next Steps** — The single most important action to take today.
