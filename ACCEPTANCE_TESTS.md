# Acceptance tests — itr3-workpaper v0.1.0

Run date: 2026-07-12

| # | Test | Result |
|---|------|--------|
| 1 | Structure: all section-3 files + valid SKILL.md frontmatter | PASS |
| 2 | Schema ship: real ITD Main V1.1 (`ITR`→`ITR3`, 287 defs) | PASS |
| 3 | Renderer smoke: full canonical workpaper → docx+html+dashboard | PASS |
| 4 | Completeness warning: omit ScheduleFA → warning banner | PASS |
| 5 | E-filing valid skeleton validates and writes upload JSON | PASS |
| 5b | Illegal key `NOT_A_REAL_FIELD` fails; docx/html still written; no efiling file | PASS |
| 6 | extract_text on demo trial_balance.xlsx | PASS |
| 7 | Demo workpaper includes planted recon mismatches | PASS |
| 8 | Zip: `itr3-workpaper/SKILL.md` at top level | PASS |
| 9 | README scope: not portal filing / not tax-audit Form 3CD | PASS |

## Evidence paths

- Full render: `/tmp/itr3-acceptance/full/`
- Bad efiling stderr shows: `Additional properties are not allowed ('NOT_A_REAL_FIELD' was unexpected)`
- Zip: `itr3-workpaper-skill.zip` (~192K without counting large schema compress well)

## Known residual limitations

- Category A CBDT rules not encoded as executable checks
- Demo Form 16 / financial statements are text placeholders, not binary PDFs
- E-filing draft uses structural zeros for many deep required BS/PL/BP nodes — honest incomplete draft for utility completion
- Thresholds file flags some slab amounts as “confirm against Finance Act” rather than hard-coding contested figures
