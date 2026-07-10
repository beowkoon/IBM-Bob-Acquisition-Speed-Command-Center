---
name: acquisition-risk-review
description: Use when the user wants to review, identify, escalate, or assess acquisition integration risks — walks through risk severity classification, ownership assignment, escalation paths, and mitigation actions.
---

# Acquisition Risk Review

Follow these steps to conduct a structured acquisition integration risk review.

## Step 1 — Load Risk Data

Read the risk register:
- Use `read_file` to check `sample_data/risks.csv` (or the uploaded file if available).
- Identify all risks and their key fields: area, severity, owner, status, mitigation.

## Step 2 — Classify and Prioritize Risks

Group risks by severity:

| Severity | Action Required |
|---|---|
| **Critical** | Immediate executive escalation. Block Day 1 if unresolved. |
| **High** | Assign owner and mitigation plan within 48 hours. |
| **Medium** | Monitor weekly. Assign owner and track to resolution. |
| **Low** | Log and review at next integration checkpoint. |

Flag any risks that are:
- Unowned (no assigned owner)
- Unmitigated (no mitigation plan in place)
- Linked to Day 1 readiness (payroll, systems access, legal entity, finance)

## Step 3 — Identify Cross-Workstream Dependencies

Look for risks that could cascade across multiple workstreams:
- Finance mapping delays blocking system cutover
- Legal entity issues blocking payroll or benefits
- Workforce alignment gaps blocking HR and compliance readiness
- Budget overruns blocking vendor or system commitments

## Step 4 — Assign Escalation Paths

For each Critical or High risk:
- Confirm the owner (functional lead responsible)
- Confirm the escalation path (Integration Lead, then Executive Sponsor)
- Confirm the target resolution date relative to Day 1

## Step 5 — Structure the Executive Output

Respond in this format:

**Executive Summary** — Total risks, count by severity (Critical / High / Medium / Low), number unowned or unmitigated.

**Agent Capabilities Used** — Risk & Controls, Integration Navigator.

**Risk Register Summary** — Table of risks with severity, owner, status, and mitigation.

**Critical and High Priority Risks** — Focused list requiring immediate action.

**Unowned / Unmitigated Risks** — Flag any risks with no owner or no plan.

**Recommended Actions** — Numbered steps: assign owners, confirm mitigations, escalate Critical items, schedule weekly risk review.

**Owners** — Integration Lead, functional owners per risk area.

**Timeline** — Critical risks to be resolved before Day 1; High risks within first 2 weeks.

**Budget / Savings / Cash Impact** — Any cost exposure from unresolved risks (e.g. delayed cutover, compliance penalties).

**Readiness Impact** — How unresolved risks affect Day 1 and Day 100 readiness scores.

**Next Steps** — Escalate Critical risks to executive sponsor today and confirm all High risks have owners assigned.
