# Securities Ops Control Tower — QA Test Report

**Scope (validated):** Functional + data-integrity + parity for *built* features.
Unbuilt legacy reports (BTST, ROS/Register, Transaction Statement, CUSPA ageing,
Repledge/API-EPI MIS) **excluded** by decision. Quantity-only (no ₹ value views)
**accepted as design** per spec.

**Method:** Automated headless Chromium drive of `securities-ops-control-tower.html`,
asserting row counts, filter logic, drilldown context, and data math.
**Result: 35 / 35 PASS · 0 JS errors.**

## Defects found & fixed during the pass
| # | Defect | Severity | Fix |
|---|--------|----------|-----|
| 1 | Settlement Dashboard payout net-diff never balanced (components summed ~97.5%) | High | POT made the balancing residual → nets to 0 ✓ |
| 2 | Exception Snapshot counts were hardcoded by health, contradicting Exception Center | Medium | Derived from the live EXC list for that exact (no, type) leg |
| 3 | CDSL/system failure remark (key Invocation Dashboard column) not surfaced | Medium | Added per-type System/CDSL remark block to Root Cause drawer |
| 4 | Corporate Action Monitor table had no Download (violates global rule 1) | Low | Added CSV download |

## Test results

### A. Global / consolidation
| TC | Case | Result | Excel ref |
|----|------|--------|-----------|
| G1 | Search 2025006 deduped, shows all legs | PASS | ISIN/Client Search |
| G2 | Search by ISIN / Symbol / UCC / BOID / Party → right entity | PASS | ISIN/Client Search |
| G3 | All 8 screens reachable | PASS | — |
| G4 | Every report table has a Download | PASS | Global rule 1 |

### B. Settlement Overview (Settlement Explorer)
| TC | Case | Result | Excel ref |
|----|------|--------|-----------|
| S1 | Type M/Z/A/X → 10/5/4/4 rows | PASS | Settlement types |
| S2 | No 2025006 → 4 legs | PASS | — |
| S3 | Type M + 2025006 → single M leg | PASS | — |
| S5 | ISIN scope recomputes settlement totals | PASS | Scripwise reports |
| S6 | Out-of-window no. → download notice | PASS | Global rule 2 |
| S7 | Shortage = Obligation − Done across all 23 rows | PASS | Payin MIS / Invocation |

### C. Settlement Dashboard
| TC | Case | Result | Excel ref |
|----|------|--------|-----------|
| D1 | Type-specific; links to other legs | PASS | — |
| D2 | Payin KPI % = 46380/50000 = 92.8% | PASS | Payin MIS |
| D3 | Exception snapshot derived from EXC (2025006-M → 2 clients / 2 ISINs / ₹5.58 Cr) | PASS | PIPO / Payin Shortage |
| D5 | Payout net-diff balances to 0 across sample legs | PASS | PIPO Payout Dashboard |

### D. Scrip Overview (Security Lookup)
| TC | Case | Result | Excel ref |
|----|------|--------|-----------|
| SC2 | Holdings widget — 5 buckets | PASS | As-on Holding |
| SC3 | Script-level tables list settlements | PASS | Scripwise Payout / Invocation |
| SC4 | Script + Settlement No filter (2025009 → 2 legs) | PASS | — |
| SC5 | Settlement row → party-wise bifurcation in scrollable modal overlay (large book) with search | PASS | Scripwise Payout (party rows) |

### E. Client Overview (Client Explorer)
| TC | Case | Result | Excel ref |
|----|------|--------|-----------|
| CL1 | POA badge on client card; BOID copy icon | PASS | Clientwise / Client Search |
| CL3 | Settlement Number lists ISINs traded in that settlement (no aggregation, single-settlement rows) | PASS | Clientwise All Settlement |
| CL4 | Adding ISIN narrows to that one script | PASS | — |

*Note: UCC filter/display, From–To range and the summary stats (Total Settlements/Shortages/Invocation) were removed per request. Activity is now driven by a single Settlement Number + optional ISIN.*

### F. Exception Center
| TC | Case | Result | Excel ref |
|----|------|--------|-----------|
| EX1 | 14 exceptions load | PASS | PIPO / shortage reports |
| EX2 | Settlement Type filter (Z → 3) | PASS | New requirement |
| EX3 | 2025006 + Type A → single A-leg exception | PASS | — |
| EX4 | Party Code text filter (substring match) | PASS | — |
| EX5 | Investigation tree: Obligation→Free→MTF→CUSPA→Margin Pledge→Shortage (6 nodes) | PASS | PIPO Purchase Shortage |
| EX6 | Drawer Settlement link → correct leg dashboard | PASS | — |
| EX7 | CDSL/system remark surfaced in drawer | PASS | Invocation Dashboard |

### G. Corporate Actions / Downloads
| TC | Case | Result | Excel ref |
|----|------|--------|-----------|
| CA1 | Timeline 5 stages | PASS | Corporate Action MIS |
| CA2 | Types incl Bonus/Split/Merger/Demerger | PASS | Corporate Action MIS |
| DL1 | 5 reconciliation reports listed | PASS | Holding Reco / ROS |

## Residual risks (PASS-with-caveat — for prototype awareness, not blockers)
| ID | Risk | Severity | Note |
|----|------|----------|------|
| R-A | Sub-level splits (ISIN scope, party-wise bifurcation, investigation-tree quantities) use fixed proportional weights, not real allocation logic | Medium | Testers should not read exact sub-numbers as production values |
| R-B | Security/Client summary cards (Total Settlements / Shortages / Invocation Count) are static, not derived — won't change with the selected entity | Low | Cosmetic for user testing; wire to real aggregates before pilot |
| R-C | Lifecycle Grid stage statuses are heuristic from settlement health, not per-ISIN real status | Low | — |
| R-D | Release KPI is synthetic (≈ invocation done × 1.02), no real release dataset | Info | BOD Release dataset not modelled |
| R-E | Date filters (Settlement Explorer, Exception Center) are decorative | Info | Add date filtering before pilot |
| R-F | CDSL remark is mapped per exception *type*, not a unique per-record remark | Info | Legacy Invocation Dashboard has per-record CDSL text |
