---
name: finance-accounting-sme-routing
description: Use when the user wants to find, identify, or route to a Finance or Accounting SME — matches SMEs based on function, geography, job profile, or specific skills such as chart of accounts, SAP, IFRS, consolidation, or cost centre mapping.
---

# Finance & Accounting SME Routing

Follow these steps to identify and route to the right Finance or Accounting SME based on function, geography, job profile, or required skills.

## Step 1 — Understand the Request

Clarify what the user needs:
- **Function** — e.g. Accounting & Process Mapping, Accounting, Tax, Treasury
- **Geography** — e.g. Singapore, Malaysia, APAC, US
- **Skill required** — e.g. chart of accounts, SAP S/4HANA, IFRS, consolidation, intercompany, cost centre mapping
- **Job profile** — e.g. Controller, Finance Integration Lead, Senior Accountant

If the user has not specified, ask: "Which function, geography, or skill are you looking for?"

## Step 2 — Load SME Directory Data

Use `read_file` to read `sample_data/sme_directory.csv` (or uploaded file if available).

Key columns to use for matching:
| Column | Used for |
|---|---|
| `function` | Match by workstream (Accounting & Process Mapping, Accounting, Tax, Treasury) |
| `geography` | Match by country or region |
| `primary_sme` | First point of contact |
| `backup_sme` | Use if primary is unavailable |
| `escalation_path` | Use if both SMEs are unavailable |
| `job_profile` | Match by role type (Controller, Finance Lead, Analyst) |
| `skills` | Match by specific skill keywords |

## Step 3 — Match SME by Skill or Job Profile

Apply this matching priority order:

1. **Exact function + geography match** — best match, use primary SME directly
2. **Function match, any geography** — use if geography is not critical
3. **Skill keyword match** — search the `skills` column for relevant keywords (e.g. "SAP", "IFRS", "chart of accounts", "consolidation")
4. **Job profile match** — search the `job_profile` column for role type (e.g. "Controller", "Finance Lead")
5. **Escalation** — if no match found, route to the escalation path of the closest function

## Step 4 — Finance & Accounting Skill Reference

Use this guide to match common Finance/Accounting integration tasks to the right skill profile:

| Task | Required Skill | Typical Job Profile |
|---|---|---|
| Chart of accounts mapping | COA mapping, ERP migration, SAP/Oracle | Finance Integration Lead |
| Financial close and consolidation | Consolidation, intercompany accounting, IFRS/GAAP | Controller, Senior Accountant |
| Cost centre and profit centre mapping | Cost centre mapping, ERP setup | Finance Systems Analyst |
| Intercompany reconciliation | Intercompany transactions, transfer pricing | Controller, Tax Manager |
| ERP migration (SAP/Oracle) | SAP S/4HANA, Oracle ERP, data migration | Finance Integration Lead, IT Integration Architect |
| Tax registration and compliance | Tax registration, corporate tax, VAT | Tax Manager, Tax Director |
| Treasury and cash management | Cash management, bank rationalisation, FX | Treasury Manager |
| Audit and financial reporting | IFRS, US GAAP, financial reporting | Controller, Senior Accountant |

## Step 5 — Structure the Output

Respond in this format:

**Executive Summary** — Who the best-matched SME is and why they were selected.

**Agent Capabilities Used** — Finance & Account Mapping Agent, SME Discovery Agent.

**Matched SME(s)** — Table showing: Function, Geography, Primary SME, Backup SME, Job Profile, Matched Skills, Escalation Path.

**Why This Match** — Explain which column matched (function, geography, skill, or job profile).

**Recommended Actions** — How to engage the SME (contact primary, confirm availability, escalate if needed).

**Owners** — Integration Lead, Finance Lead, functional SME.

**Timeline** — When the SME needs to be engaged relative to Day 1 or Day 100.

**Risks** — What happens if this SME is not engaged in time.

**Next Steps** — The single most important action: contact the primary SME today.
