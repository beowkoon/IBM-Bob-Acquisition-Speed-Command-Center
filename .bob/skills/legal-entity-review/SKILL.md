---
name: legal-entity-review
description: Use when the user wants to review, assess, or decide on legal entity actions — walks through retain, merge, dissolve, and further assessment decisions with compliance risk, approval requirements, and savings impact.
---

# Legal Entity Review

Follow these steps to conduct a structured legal entity simplification review.

## Step 1 — Load Legal Entity Data

Read the legal entity data:
- Use `read_file` to check `sample_data/legal_entities.csv` (or the uploaded file if available).
- Note all entities and their key fields: employees, annual_revenue, active_contracts, regulatory_required, duplicate_ibm_presence.

## Step 2 — Apply Decision Logic

For each entity, apply this decision framework:

| Condition | Recommended Action |
|---|---|
| regulatory_required = Yes | **Retain** — regulatory requirement exists |
| employees = 0, revenue = 0, active_contracts = No | **Dissolve** — no activity, no obligations |
| duplicate_ibm_presence = Yes, regulatory_required = No | **Merge** — consolidate into IBM entity |
| None of the above | **Further Assessment** — requires deeper review |

## Step 3 — Assess Compliance Risk and Approvals

For each entity, determine:
- **Compliance Risk:** High (regulatory required), Medium (active contracts), Low (otherwise)
- **Required Approval:** Retain = Legal; Dissolve = Legal / Tax; Merge = Legal / Treasury; Further Assessment = Legal / Tax / Treasury
- **Confidence Level:** High (clear rule met), Medium (duplicate present), Low (unclear)

## Step 4 — Calculate Savings Impact

Summarize the financial impact:
- Total annual admin cost for Merge/Dissolve candidates
- Total saving_if_action_is_taken for all candidates
- Annual audit fees that could be eliminated
- Cash release opportunity from simplification

## Step 5 — Structure the Executive Output

Respond in this format:

**Executive Summary** — Number of entities reviewed, how many flagged for action, total savings opportunity.

**Agent Capabilities Used** — Legal Entity Optimization, Budget & Value Tracking.

**Entity Action Table** — Entity name, recommended action, reason, confidence, compliance risk, required approval, savings.

**Merge / Dissolve Candidates** — Focused list with financial detail for entities recommended for action.

**Recommended Actions** — Numbered steps: validate candidates, confirm contracts/tax/regulatory dependencies, get required approvals, execute.

**Owners** — Legal, Tax, Treasury, Integration Lead.

**Timeline** — Assess in current planning cycle; target completion by Day 100.

**Risks** — Active contracts, incomplete regulatory information, or tax dependencies that could block action.

**Budget / Savings / Cash Impact** — Total admin cost reduction, action savings, and cash release opportunity.

**Next Steps** — Confirm the top Merge/Dissolve candidates and initiate approval process.
