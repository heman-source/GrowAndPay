# Securities Ops Control Tower — QA Test Report

**Scope (validated):** Functional + data-integrity + parity for *built* features.
Unbuilt legacy reports (BTST, ROS/Register, Transaction Statement, CUSPA ageing,
Repledge/API-EPI MIS) **excluded** by decision. Quantity-only (no ₹ value views)
**accepted as design** per spec.

**Method:** Automated headless Chromium drive of `securities-ops-control-tower.html`,
asserting row counts, filter logic, drilldown context, and data math.
**Result: 42 / 42 PASS · 0 JS errors.**

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
| G3 | All 6 screens reachable (Operations Overview removed) | PASS | — |
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

### E. Client-Wise Report
| TC | Case | Result |
|----|------|--------|
| CL1 | POA badge + BOID copy on client card | PASS |
| CL2 | Party-only → all tenure scrips with pagination (>10) | PASS |
| CL3 | Click scrip → its settlements with the full 9-column data | PASS |
| CL4 | Party + Settlement Number → scrips traded that settlement (data inline) | PASS |

*Params: Settlement Type, Settlement Number, Party Code. No cross-settlement aggregation; blank processes shown as "—".*

### F. Shortage-Wise Report
| TC | Case | Result |
|----|------|--------|
| SH1 | Single settlement → scrips in shortage (invocation excluded) | PASS |
| SH2 | Click scrip → parties in shortage (→ Client-Wise Report) | PASS |
| SH3 | Scrip → shortage across settlements (paginated) | PASS |
| SH4 | Party → shortage across settlements | PASS |
| SH5 | From–To range without Order By → prompt (compulsory) | PASS |
| SH6 | Range + Order By = Party-code-wise | PASS |
| SH7 | Range + Order By = Scrip-wise | PASS |
| SH8 | Settlement Explorer shortage deep-link → prefiltered | PASS |

### H. Process Lookup
| TC | Case | Result |
|----|------|--------|
| PL1 | Payin/Payout + Shortage → Party, Scrip, ISIN, Obligation Qty, Shortage Qty, Type of Shortage | PASS |
| PL2 | Invocation + Shortage → Party, Scrip, ISIN, Pledge Type, Invoke Qty, Failed Qty | PASS |
| PL3 | Payin/Payout + Processed → Party, Scrip, ISIN, Obligation Qty, Holding Type, Processed Qty | PASS |
| PL4 | Invocation + Processed → Party, Scrip, ISIN, Pledge Type, Invoke Qty, Processed Qty | PASS |
| PL5 | Security Lookup removed from sidebar (still reachable via ISIN drilldowns) | PASS |

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
| R-B | Security Lookup summary card (Total Settlements / Shortages / Invocation Count) is static, not derived | Low | Cosmetic for user testing; wire to real aggregates before pilot |
| R-C | Lifecycle Grid stage statuses are heuristic from settlement health, not per-ISIN real status | Low | — |
| R-D | Release KPI is synthetic (≈ invocation done × 1.02), no real release dataset | Info | BOD Release dataset not modelled |
| R-E | Client-Wise / Shortage-Wise data (tenure scrips, per-settlement shortages, party books) is deterministic dummy, not real allocations | Info | For demo realism only |
| R-F | CDSL remark is mapped per exception *type*, not a unique per-record remark | Info | Legacy Invocation Dashboard has per-record CDSL text |
