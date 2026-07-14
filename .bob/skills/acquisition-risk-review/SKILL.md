---
name: acquisition-risk-review
description: Use when the user wants to review, identify, escalate, or assess acquisition integration risks — walks through risk severity classification, ownership assignment, escalation paths, mitigation actions, and separation of duties (SoD) assessment by process and task.
---

# Acquisition Risk Review

Follow these steps to conduct a structured acquisition integration risk review, including Separation of Duties (SoD) assessment.

## Step 1 — Load Risk Data

Read the risk register:
- Use `read_file` to check `sample_data/risks.csv` (or the uploaded file if available).
- Identify all risks and their key fields: risk_id, risk, severity, owner, status, mitigation.

Also load the SoD matrix if available:
- Use `read_file` to check `sample_data/sod_matrix.csv`.
- Key fields: process, task, sod_role, assigned_to, conflicts_with, sod_risk, severity, mitigation.

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

## Step 3 — Separation of Duties (SoD) Assessment

**Definition:** No single individual should be able to perform more than one of the following roles for the same process or transaction:

| SoD Role | Description |
|---|---|
| **Authorize** | Approve or sanction a transaction, action, or access |
| **Record** | Enter, post, or maintain data in systems or ledgers |
| **Verify** | Reconcile, review, or validate transactions or balances |
| **Custody** | Hold, safeguard, or control assets or privileged system access |

**Why SoD matters:** If one person can Authorize AND Record AND Verify AND hold Custody — they can create, approve, process, hide, and protect a fraudulent transaction with no deterrence or timely detection.

### Step 3a — Assess SoD by Process

For each process area in the SoD matrix, check:
1. Are the four roles (Authorize / Record / Verify / Custody) assigned to **different people**?
2. Does any single person hold **two or more conflicting roles** in the same process?
3. Are **Critical SoD conflicts** identified — especially in Bank/Treasury, Payroll, and Vendor Master?

### Step 3b — Assess SoD by Task

For each task within a process:
1. Identify the `sod_role` the task belongs to
2. Check `conflicts_with` — what other roles does this task conflict with?
3. Check `assigned_to` — does this person also perform any of the conflicting roles?
4. Flag as **SoD Conflict** if one person holds conflicting roles for the same task/process

### Step 3c — Priority SoD Risk Areas

Always flag these processes as highest priority for SoD review during acquisition integration:

| Process | Critical SoD Risk |
|---|---|
| **Bank & Treasury** | Payment authorization + custody of bank credentials + recording — must be separated with dual authorization |
| **Payroll** | Payroll approval + processing + custody of bank details — must be separated |
| **Accounts Payable** | Invoice approval + vendor master custody + payment processing — must be separated |
| **Vendor Master** | Ability to add/change vendor data + process payments — Critical fraud risk |
| **General Ledger** | Manual journal posting + approval — must require secondary approval |
| **Procurement** | PO approval + vendor management + goods receipt — must be separated |

## Step 4 — Identify Cross-Workstream Risk Dependencies

Look for risks that could cascade across multiple workstreams:
- Finance mapping delays blocking system cutover
- Legal entity issues blocking payroll or benefits
- Workforce alignment gaps blocking HR and compliance readiness
- Budget overruns blocking vendor or system commitments
- SoD conflicts in acquired entity carried forward into IBM controls environment

## Step 5 — Assign Escalation Paths

For each Critical or High risk (including SoD conflicts):
- Confirm the owner (functional lead responsible)
- Confirm the escalation path (Integration Lead → CFO / Chief Compliance Officer → Executive Sponsor)
- Confirm the target resolution date relative to Day 1

## Step 6 — Structure the Executive Output

Respond in this format:

**Executive Summary** — Total risks by severity, number of SoD conflicts identified, overall control risk rating.

**Agent Capabilities Used** — Risk & Controls Agent, Finance & Account Mapping Agent, Integration Navigator.

**Risk Register Summary** — Table of risks with severity, owner, status, and mitigation.

**Critical and High Priority Risks** — Focused list requiring immediate action.

**Separation of Duties Assessment** — Summary table by process showing:
- Process name
- SoD conflict identified (Yes/No)
- Conflicting roles
- Person holding conflicting roles
- Severity
- Recommended mitigation

**SoD Conflicts by Process** — Grouped list: Bank & Treasury → Payroll → Accounts Payable → General Ledger → Procurement → Fixed Assets.

**SoD Conflicts by Task** — Detailed task-level view of where the four roles overlap.

**Unowned / Unmitigated Risks** — Flag any risks with no owner or no plan.

**Recommended Actions** — Numbered steps:
1. Resolve all Critical SoD conflicts before Day 1 (Bank, Payroll, Vendor Master)
2. Implement dual authorization for all bank payments
3. Separate payroll processing from payroll approval and bank detail custody
4. Restrict vendor master access to controls team only
5. Require secondary approval for all manual journal entries
6. Assign owners to all unmitigated risks
7. Schedule weekly risk and controls review

**Owners** — Integration Lead, CFO, Chief Compliance Officer, Internal Audit, functional owners per risk area.

**Timeline** — Critical SoD conflicts: resolve before Day 1. High SoD conflicts: resolve within first 2 weeks.

**Budget / Savings / Cash Impact** — SoD failures can result in financial loss, fraud, audit findings, and regulatory penalties — quantify exposure where possible.

**Readiness Impact** — Unresolved SoD conflicts are a Day 1 controls readiness blocker and an audit risk for the first post-acquisition financial close.

**Next Steps** — Escalate Critical SoD conflicts to CFO and Chief Compliance Officer today. Confirm dual authorization controls for Bank and Payroll before Day 1.
