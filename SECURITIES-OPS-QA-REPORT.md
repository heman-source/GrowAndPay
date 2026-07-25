# Securities Ops Control Tower — QA Test Report

**Scope (validated):** Functional + data-integrity + parity for *built* features.
Unbuilt legacy reports (BTST, ROS/Register, Transaction Statement, CUSPA ageing,
Repledge/API-EPI MIS) **excluded** by decision. Quantity-only (no ₹ value views)
**accepted as design** per spec.

**Method:** Automated headless Chromium drive of `securities-ops-control-tower.html`,
asserting row counts, filter logic, drilldown context, and data math.
**Result: 78 / 78 PASS · 0 JS errors.**

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

### B2. Settlement Explorer · Process Type (Payin/Payout scrip drill)
| TC | Case | Result |
|----|------|--------|
| SE1 | Payout L1 columns: Scrip, ISIN, Series, Payout Obligation, Payout Received, Payout Shortage, Excess Payin Reversal Payout | PASS |
| SE2 | Payin L1 columns: Scrip, ISIN, Series, Payin Obligation, Earmarked Quantity, Payin Shortage | PASS |
| SE3 | L1 → L2 (click scrip): Party Code, Obligation Quantity, Payout Completed, Payout Shortage, **Excess Payin Reversal Payout** | PASS |
| SE4 | L2 client-row sums (incl. the extra column) reconcile exactly to the L1 scrip-level row | PASS |
| SE5 | L2 → L3 (click party): same column format as L1 | PASS |
| SE6 | L3 Obligation-cell click → modal, narration "To be done from MTF/CUSPA/FREE/MP" | PASS |
| SE7 | Payin L3 has 3 clickable qty cells per row (Obligation / Earmarked / Shortage) — verified across **all** rows, not just one | PASS |
| SE8 | Shortage-cell click → modal, narration "Internal/ Market Shortage" | PASS |
| SE9 | ISIN text filter, no match → empty state | PASS |
| SE10 | ISIN text filter narrows L1 to one matching scrip | PASS |
| SE11 | No settlement number → guidance prompt | PASS |
| SE12 | Out-of-window settlement → guard message | PASS |
| SE13 | Settlement has no chosen Settlement Type leg → guard message | PASS |

*ISIN and Party Code are free-text (with `*`/`%` = all); Party Code additionally scopes the Process Type report to matching clients only, in-page (no navigation away). Settlement Summary (no Process Type) is renamed from "Obligation List," starts as an empty state until a Settlement Number is entered, drops the Summary Report Widgets, and excludes Invocation columns (Payin/Payout only). Level 3 (a party's own securities) lists every scrip that party traded in the settlement — the originally-selected scrip highlighted and listed first, followed by their other traded scrips — with every row's qty cells equally clickable to the narration modal. Client codes are drawn from a shared per-settlement pool with a symmetric trade predicate, so a party's membership under one scrip and its own multi-scrip portfolio are always mutually consistent.*

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

### I. Securities Lookup
| TC | Case | Result |
|----|------|--------|
| SL1 | Settlement → scrip list (Scrip, Series, Total Payin, Total Payout, Total Invocation) | PASS |
| SL2 | Click scrip → client bifurcation (Party Code, Total Payout Received, Total Payin Done, Total Invocation Done) | PASS |
| SL3 | Client-level sums reconcile exactly to the scrip-level totals | PASS |

### J. Transaction Reports (Clientwise Transaction Statement)
| TC | Case | Result |
|----|------|--------|
| TR1 | Party-Wise columns (Trans Date … Credit/Debit/Clt Dp Id/Remarks; no Slip/DpID/Party Name) | PASS |
| TR2 | Party-Wise groups under "Party Code : XXX(Name)" headers | PASS |
| TR3 | Scrip-Wise regroups under "Scrip : …" headers with Party columns | PASS |
| TR4 | Party range filter → single group | PASS |
| TR5 | Credit → Payout; Debit → Payin/Invocation | PASS |

### K. Scrip Details / Client Details (Demat Reports Module)
| TC | Case | Result |
|----|------|--------|
| SD1 | Empty by default — no eager full list until a filter is entered | PASS |
| SD2 | Scrip master search columns: Scrip Code, Series, ISIN, Status, Company Name, Last Price (**Sector removed**) | PASS |
| SD3 | Wildcard `*` shows the full master list (17 scrips) | PASS |
| SD4 | Scrip Code filter narrows to one match | PASS |
| SD5 | Row click links directly to Security Lookup (Holdings widget removed) | PASS |
| SD6 | No `undefined` values from the hash-shift bug (scrip master) | PASS |
| SD7 | Deep-link `ctx.isin` prefills Scrip Code and shows the result | PASS |
| CD1 | Client DP mapping search columns: Party Code, **Name of the Holder**, DP ID, Client ID, **Default DP ID**, DP Type, POA Status, DDPI Status | PASS |
| CD2 | No `undefined` DDPI/status values (hash-shift bug fixed) | PASS |
| CD3 | Status=Active filters correctly (was silently 0 rows before the fix) | PASS |
| CD4 | Exactly one **Default DP ID** row per client (multi-account clients show a second, non-default row) | PASS |
| CD5 | Default CDSL DP ID + Client ID reconciles exactly to the existing BOID | PASS |
| CD6 | Name of the Holder column shows the client's actual name, not a code | PASS |
| CD7 | Party Code is a text filter, not a dropdown | PASS |
| CD8 | Holdings widgets fully removed from Client Details | PASS |

**Defect found & fixed during the original pass:** `hsh()` returns unsigned 32-bit hashes that can exceed 2^31; using the *signed* right-shift operator (`>>`) on such values could flip them negative, making `% arrayLength` return a negative index — silently producing `undefined` (e.g. a DDPI badge rendered "undefined") or corrupted holdings figures app-wide. Fixed by switching every `hash >> n` pattern to the unsigned `>>> n`, including in pre-existing code not touched by this feature.

**Update — Security/Client Summary + Holdings widgets removed** from both screens per follow-up feedback; each screen is now search-table only, with each row linking straight to the deeper operational screen (Security Lookup / Client-Wise Report). "Introducer" renamed to "Name of the Holder" (shows the client's real name); added a "Default DP ID" column — clients now have a 50% chance of a second, non-default DP account for realism, and the default account is always the one derived from the existing BOID.

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
