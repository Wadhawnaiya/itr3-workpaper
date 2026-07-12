# AY 2026-27 (FY 2025-26) — Thresholds, rates & due dates

**Authoritative numeric source for this skill.** Where a schedule guide conflicts with this file, **trust this file**. Compiled for Assessment Year 2026-27 / Previous Year 2025-26 (1-Apr-2025 to 31-Mar-2026). Refresh after each Finance Act.

> Figures below reflect commonly published positions for FY 2025-26 / AY 2026-27 as of skill build. Confirm against Finance Act 2025 / CBDT notifications before relying in production.

## 1. Tax regime — new vs old (Sec 115BAC)

| Item | New regime (default for most individuals) | Old regime |
|------|-------------------------------------------|------------|
| Basic exemption (general) | As per new-regime slab table for AY 2026-27 | As per old-regime slab table |
| Standard deduction (salary/pension) | Available (confirm amount for this AY — Budget 2025 enhanced in some years) | Available |
| Common Chapter VI-A (80C/80D etc.) | Largely not available (limited exceptions e.g. employer NPS 80CCD(2) where allowed) | Available within limits |
| Family pension deduction | Per statute under OS | Per statute under OS |

**Workpaper rule:** Regime must be explicit in Cover + Part B notes. If profile says **new regime** but folder contains 80C/80D claims without employer-NPS context → flag **judgment / conflict**, do not silently drop or allow.

## 2. Basic exemption & slabs (use official slab tables)

Do not hard-code slab rupee amounts in e-filing JSON tax computation without computing from official slab tables for the chosen regime. For workpaper:

- Compute tax in notes/table when data allows
- Otherwise mark PartB_TTI tax computation as `judgment` with partial workings

## 3. Common Chapter VI-A limits (old regime / where still available)

| Section | Common limit (illustrative — verify) | Notes |
|---------|--------------------------------------|-------|
| 80C | Rs. 1,50,000 | Combined with 80CCC/80CCD(1) subject to overall limits |
| 80CCD(1B) | Rs. 50,000 | Additional NPS (self) where eligible |
| 80D | Age-based (self/family/parents) | Premium + preventive health check-up caps |
| 80G | 50%/100% with/without qual. limit | Need donation receipt + 80G approval status |
| 80TTA | Rs. 10,000 | Savings interest (non-senior) under OS — regime interaction |
| 80TTB | Rs. 50,000 | Senior citizen interest — regime interaction |

**Only claim with evidence.** Missing proof → `missing` or `judgment`, never invent premium amounts.

## 4. House property

| Item | Rule of thumb |
|------|----------------|
| Self-occupied interest u/s 24(b) | Cap Rs. 2,00,000 (acquisition/construction) subject to conditions |
| Let-out | Interest fully allowable subject to set-off rules; municipal taxes only if paid by owner |
| Co-ownership | Split income/interest by ownership share |
| Vacancy | Let-out property vacant — ALV rules apply; do not treat as self-occupied without facts |

## 5. Presumptive schemes (applicability checks for ITR-3)

| Section | Who | Limit | Rate |
|---------|-----|-------|------|
| 44AD | Resident individual/HUF/firm (not LLP) business | Rs. 2 cr (Rs. 3 cr if ≥95% digital receipts) | 8% / 6% digital |
| 44ADA | Specified professionals | Rs. 50 lakh (Rs. 75 lakh if cash ≤5%) | 50% |
| 44AE | Goods carriage ≤10 vehicles | Per vehicle | Heavy: Rs. 1,000/ton/month; others Rs. 7,500/vehicle/month |

ITR-3 still used in many business situations (including when books maintained or audit applies). **Do not force ITR-4** silently. Document whether books / presumptive / hybrid.

## 6. Tax audit u/s 44AB (PartA_GEN2)

| Category | Standard | Enhanced (cash ≤5% receipts **and** payments) |
|----------|----------|-----------------------------------------------|
| Business turnover | Rs. 1 crore | Rs. 10 crore |
| Profession receipts | Rs. 50 lakh | — |

Also: 44AD(4) lock-in opt-out; 44ADA below 50% with income above basic exemption → audit triggers.

If audit applies: fill PartA_GEN2 audit flags; **never invent UDIN / auditor membership / report date**.

## 7. TDS / TCS — commonly hit in ITR-3 (FY 2025-26)

Budget 2025 rationalisations effective **1-Apr-2025** (verify against latest chart):

| Section | Nature | Threshold (FY 2025-26) | Rate (typical) |
|---------|--------|------------------------|----------------|
| 192 | Salary | Slab / basic exemption | Slab |
| 194A | Interest other than securities | Banks etc. Rs. 50,000 (higher for senior citizens in some cases); others lower | 10% |
| 194C | Contractors | Rs. 30k single / Rs. 1L aggregate | 1%/2% |
| 194H | Commission | Rs. 20,000 | 2% |
| 194I | Rent | Higher thresholds per 194-I / 194-IB | 2%/10% |
| 194J | Professional/technical | Rs. 50,000 | 10%/2% |
| 194Q | Purchase of goods | Rs. 50 lakh aggregate from seller | 0.1% excess |
| **194T** | **Firm/LLP → partners** (salary/remun/interest etc.) | Rs. 20,000 aggregate | 10% |
| 206C(1H) | TCS on sale of goods | **Removed w.e.f. 1-Apr-2025** | Do not apply for FY 2025-26 |

## 8. Capital gains — high-level flags (AY 2026-27)

- Equity STT-paid LTCG (112A): exemption threshold / rate as per current law (historically Rs. 1.25 lakh @ 12.5% post Budget 2024 changes — **confirm current figure** before computing).
- Indexation: limited after recent CG reforms — do not apply old indexation assumptions blindly.
- VDA: special rates/schedule — use Schedule VDA when facts support.
- Missing cost of acquisition → `missing`, never invent cost.

## 9. Advance tax / interest 234A/B/C

- Advance tax if liability ≥ Rs. 10,000 (subject to exceptions for salary-only etc.).
- Compute 234 interest only if instalment data + liability known; else mark judgment.

## 10. Schedule AL (assets & liabilities)

Applicability historically linked to income thresholds (e.g. total income above a floor for individuals). Confirm current threshold before forcing AL. If unclear → `judgment` with notes, not silent invent of asset lists.

## 11. Next-year update checklist

1. Finance Act slab tables + standard deduction
2. VI-A limits and regime interactions
3. TDS/TCS chart (especially partner 194T and any further rationalisation)
4. CG rates / 112A exemption
5. 44AB / presumptive limits
6. Replace ITR-3 schema when ITD publishes new Main version
7. CBDT ITR-3 validation rules PDF version bump
