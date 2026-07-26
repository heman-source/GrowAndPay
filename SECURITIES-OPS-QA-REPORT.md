# Securities Ops Control Tower — QA Test Report

**Scope (validated):** Functional + data-integrity + parity for *built* features.
Unbuilt legacy reports (BTST, ROS/Register, Transaction Statement, CUSPA ageing,
Repledge/API-EPI MIS) **excluded** by decision. Quantity-only (no ₹ value views)
**accepted as design** per spec.

**Method:** Automated headless Chromium drive of `securities-ops-control-tower.html`,
asserting row counts, filter logic, drilldown context, and data math.
**Result: 110 / 110 PASS · 0 JS errors.**

## Defects found & fixed during the pass
| # | Defect | Severity | Fix |
|---|--------|----------|-----|
| 1 | Settlement Dashboard payout net-diff never balanced (components summed ~97.5%) | High | POT made the balancing residual → nets to 0 ✓ |
| 2 | Exception Snapshot counts were hardcoded by health, contradicting Exception Center | Medium | Derived from the live EXC list for that exact (no, type) leg |
| 3 | CDSL/system failure remark (key Invocation Dashboard column) not surfaced | Medium | Added per-type System/CDSL remark block to Root Cause drawer |
| 4 | Corporate Action Monitor table had no Download (violates global rule 1) | Low | Added CSV download |
| 5 | Client-Wise Report deep-link (`{party}`) only reset the drill-down state if the target party differed from whatever party was already loaded — clicking a "party X" link elsewhere while Client-Wise Report was already mid-drill into party X's scrip left the user stuck in that scrip's settlement view instead of the fresh tenure list | Low | Deep-link with `{party}` now always resets to Mode C, regardless of prior state |

## Test results

### A. Global / consolidation
| TC | Case | Result | Excel ref |
|----|------|--------|-----------|
| G1 | Search 2025006 deduped, shows all legs | PASS | ISIN/Client Search |
| G2 | Search by ISIN / Symbol / UCC / BOID / Party → right entity | PASS | ISIN/Client Search |
| G3 | All 6 screens reachable (Operations Overview removed) | PASS | — |
| G4 | Every report table has a Download | PASS | Global rule 1 |

### B. Settlement Overview (Settlement Explorer) — Settlement Summary, now scrip-wise
| TC | Case | Result | Excel ref |
|----|------|--------|-----------|
| S1 | Settlement Number only → scrip-wise columns: Scrip Code, ISIN, Payin Obligation, Total Payin Delivered, Payin Shortage, Payout Obligation, Payout Received, Payout Shortage | PASS | Scripwise reports |
| S2 | Settlement Number only → one row per scrip traded (not per M/Z/A/X leg) | PASS | — |
| S3 | Settlement Type=M scopes the scrip list/values to that leg only | PASS | — |
| S5 | ISIN filter narrows the scrip-wise list to one scrip | PASS | Scripwise reports |
| S6 | Out-of-window settlement number → download notice banner (with CTA) | PASS | Global rule 2 |
| S7 | Shortage = Obligation − Delivered/Received across every scrip row | PASS | Payin MIS |
| S8 | Broad partial settlement number (e.g. "2025") → guidance to enter one exact number | PASS | — |
| S9 | L1 row click drills to L2 (scrip's clients), not Security Lookup | PASS | — |
| S10 | Click a scrip (L1) → L2 client list: Party Code + same 6-metric columns | PASS | — |
| S11 | L2 client rows sum back exactly to the L1 scrip row (reconciliation) | PASS | — |
| S12 | L2 shows a breadcrumb back to Settlement Summary | PASS | — |
| S13 | Click a client (L2) → L3 "Party X — securities traded" (stays in Settlement Explorer) | PASS | — |
| S14 | L3 columns: Scrip Name/ISIN/Series + same 6 metrics, Payin+Payout combined for that client | PASS | — |
| S15 | L3 quantity cells (Obligation/Delivered-Received/Shortage) open the narration modal | PASS | — |
| S16 | Changing any filter resets the drill state back to L1 | PASS | — |

**Behaviour change (by request):** Settlement Summary used to show settlement-level cumulative totals (one row per M/Z/A/X leg, combined across every scrip). It's now a **scrip-wise bifurcated list** — one row per Scrip Code + ISIN — matching the exact format requested, and it now requires an **exact** single settlement number (no more browsing multiple settlements via a partial digit match), consistent with every other investigation screen in the app. Numbers reconcile with the Process Type report's Payin/Payout Level 1 for the same settlement (verified live).

**Follow-up behaviour change (by request):** Settlement Summary's scrip list no longer links straight out to Security Lookup — clicking a scrip now drills to **L2: the clients who traded it this settlement** (Party Code + the same 6 Payin/Payout metrics, with a Total footer), and clicking a client drills to **L3: that client's own securities this settlement** (Payin + Payout combined, selected scrip highlighted/listed first, every metric cell clickable for its quantity-detail narration). This mirrors the Process Type report's existing scrip→client→securities drill exactly, entirely inside Settlement Explorer — no cross-screen jump to Client-Wise Report — so both reports under Settlement Explorer now share the same drill-down intent. Breadcrumbs (Settlement Summary › Scrip clients › Party) let you step back up a level; changing any filter (Settlement Type/Number, ISIN, Party Code) resets to L1. L2 client sums are verified live to reconcile exactly to the L1 scrip row they drilled from.

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
| CL1 | Client Details: party input + Holdings widget removed | PASS |
| CL2 | No Party Code → prompt "Enter a Party Code to view this client's activity." | PASS |
| CL3 | Unknown Party Code → "No client found for party code…" | PASS |
| CL4 | Party Code filter is a free-text input (not a dropdown) | PASS |
| CL5 | Party-only → all tenure scrips with pagination (>10) | PASS |
| CL6 | Drill into scrip (Mode A) → 8-col canonical format: Settlement No, Settlement Type, Payin Obligation, Total Payin Delivered, Payin Shortage, Payout Obligation, Payout Received, Payout Shortage | PASS |
| CL7 | Obligation cells (Payin/Payout) are plain text, not clickable | PASS |
| CL8 | Party + Settlement Number (Mode B) → 9-col format: Script, ISIN, Settlement Type + same 6 metrics | PASS |
| CL9 | Payin Shortage quantity-detail modal splits "Invoked from MTF/CUSPA/MP" vs "Internal/ Market Shortage" when both apply to the same scrip+ISIN | PASS |
| CL10 | Payout Received quantity-detail modal splits "Excess Payin reversed via Payout" vs "Received from MTF/CUSPA/FREE/MP" | PASS |
| CL11 | Payout Shortage quantity-detail modal is a single "Internal/ Market Shortage" row (no invocation/excess decomposition) | PASS |
| CL12 | Quantity-detail modal rows always sum back to the clicked parent value (sampled across 5 clients × 4 scrips × 2 settlements × 4 clickable metrics) | PASS |
| CL13 | Deep-link with `{party}` always lands on Mode C (tenure list), even if that same party was already mid-drill from a prior visit | PASS |

*Params: Settlement Type, Settlement Number, Party Code (free text). Mode C (party only) lists every scrip traded in the client's tenure; Mode B (party + settlement) lists scrips traded that settlement; Mode A (scrip selected) lists that scrip's settlements. Blank/N-A processes shown as "—" and are not clickable. Total Payin/Payout Delivered and Payin/Payout Shortage cells open a quantity-detail modal that decomposes the figure by source (invocation, excess-payin reversal, base receipt/shortage).*

**Behaviour change (by request):** Party Code is now a free-text field (was a dropdown of demo clients) and the screen shows nothing until a Party Code is entered — no more defaulting to the first client. Mode A/B's data columns were replaced with the canonical 8/9-column format (Settlement No/Script+ISIN, Settlement Type, Payin Obligation, Total Payin Delivered, Payin Shortage, Payout Obligation, Payout Received, Payout Shortage), dropping the old Invocation columns from this screen's inline table. Clicking Total Payin/Payout Delivered or Payin/Payout Shortage now opens a quantity-detail modal: if Invocation applies to that client+scrip+settlement, it appears as a separate "Invoked from MTF/CUSPA/MP" row alongside the base row for the same clicked quantity; if Excess Payin Reversal applies (Payout Received only), it appears as a separate "Excess Payin reversed via Payout" row. All decomposition rows are constructed to sum exactly to the clicked total (verified live across a sample, see CL12). **Design calls made without an explicit spec — flagged for review:**
- Obligation cells (Payin/Payout) are not clickable here, unlike Settlement Explorer's Process Type report where Obligation *is* clickable. Confirm this asymmetry is intended for this screen.
- Invocation-narration is only checked against Payin-side clicks (Delivered/Shortage); Payout-side clicks never show an "Invoked…" row. Flag if Payout should also be checked for invocation.
- Excess Payin Reversal is only checked against Payout Received; Payout Shortage always shows a plain "Internal/ Market Shortage" row with no decomposition. Flag if Excess Reversal should also apply there.
- The exact wording **"Excess Payin reversed via Payout"** is my own phrasing (not specified) — happy to change it to match house terminology.
- Mode A and Mode B show **one row per settlement number** (using the Settlement Type filter's leg if set, else the settlement's first leg) rather than one row per (settlement, leg) pair. A settlement number with M+Z legs on the same scrip today collapses to a single row using the first leg's figures. Flag if you want every leg enumerated as its own row.
- Party Code here is a single exact-match lookup (no `*`/`%` wildcard support), unlike Client Details' search table which supports substring/wildcard matching many clients at once. Kept intentionally asymmetric since this screen is a single-client report, not a multi-result search — flag if wildcard support is wanted here too.

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
| CD9 | Empty by default (no eager full list) — matches Scrip Details | PASS |

**Defect found & fixed during the original pass:** `hsh()` returns unsigned 32-bit hashes that can exceed 2^31; using the *signed* right-shift operator (`>>`) on such values could flip them negative, making `% arrayLength` return a negative index — silently producing `undefined` (e.g. a DDPI badge rendered "undefined") or corrupted holdings figures app-wide. Fixed by switching every `hash >> n` pattern to the unsigned `>>> n`, including in pre-existing code not touched by this feature.

**Update — Security/Client Summary + Holdings widgets removed** from both screens per follow-up feedback; each screen is now search-table only, with each row linking straight to the deeper operational screen (Security Lookup / Client-Wise Report). "Introducer" renamed to "Name of the Holder" (shows the client's real name); added a "Default DP ID" column — clients now have a 50% chance of a second, non-default DP account for realism, and the default account is always the one derived from the existing BOID.

**Update — Client Details now also starts empty by default** (no Party Code / DP ID / Client DP No / Status filter → guidance prompt, no eager 4-client list), matching Scrip Details' behavior for consistency. Selecting a non-"All" Status alone, or any text filter (including `*`/`%`), triggers the search.

### L. Collateral Management · As on Holding Report
| TC | Case | Result |
|----|------|--------|
| CM1 | Empty state when Date / Client ID / Type of Pledge are all blank | PASS |
| CM2 | Still empty with only Holding as on Date filled | PASS |
| CM3 | Still empty with Date + Client ID but no Type of Pledge selected | PASS |
| CM4 | Results render once all three (Date, Client ID, Type of Pledge) are set | PASS |
| CM5 | Summary shows the 6 requested fields, in order: Date of Report, Holding Report As on, Client ID, Client Name, Sub Broker ID, Holding Type | PASS |
| CM6 | Summary's Client ID / Holding Type echo the entered filters | PASS |
| CM7 | Line item columns: Transaction Date, Scrip Name, Scrip Code, ISIN, Pledge Type, PSN, Quantity | PASS |
| CM8 | Has line items for a valid client | PASS |
| CM9 | Type of Pledge = MTF narrows every row to MTF only | PASS |
| CM10 | ISIN / Scrip Name wildcard `*` behaves the same as blank (all scrips) | PASS |
| CM11 | Unknown Client ID → "No client found" message | PASS |
| CM12 | Reset clears all fields back to the empty state | PASS |
| CM13 | Deep-link `{party}` pre-fills Client ID but still requires Date + Type of Pledge before showing data | PASS |

**New feature — Collateral Management is a new top-level nav section** (below Downloads & Reco), with one report so far: **As on Holding Report**. Inputs: Holding as on Date, Client ID (free text, single exact match — same convention as Client-Wise Report's Party Code), ISIN/Scrip Name (`*`/`%` = all), Type of Pledge (a placeholder-first dropdown — "— select —", All, MTF, CUSPA, MP — so the screen stays empty until the user actively picks one, even "All", not just because a dropdown always has *some* value selected). Summary uses the same `.kv-grid` tile style as the Exception drill drawer, for visual consistency with an existing pattern rather than a plain table. Sub Broker ID reuses each client's existing `broker` field; "Client ID" in the summary simply echoes the Client ID entered in the filter (this app has no separate DP-linked numeric Client ID concept for this report — that distinct concept already exists under Client Details' DP Mapping search and was deliberately not reused here, to avoid conflating two different "Client ID" meanings in one screen).

**Design calls made without an explicit spec — flagged for review:**
- "Client ID" here is treated as identical to the "Party Code" (`CLI-…`) used everywhere else in the app (single exact-match lookup) — the request's own empty-state text said "party code," so this seemed like the intended reading rather than a distinct new identifier scheme. Flag if a different Client ID format was actually meant.
- A client's pledge positions (which scrips are pledged, under which type, at what quantity) are generated independently of the Holding as on Date — changing the date only reshuffles each line's **Transaction Date** and **PSN**, it never adds or removes a pledge. This prototype doesn't model pledge/unpledge events over time, so an "as on" date from a year ago shows the exact same holding set as today. Flag if the report should instead reflect a point-in-time snapshot where older dates show fewer/different positions.
- Scrip Name is mapped to the security's full company name (e.g. "Reliance Industries Ltd") and Scrip Code to its trading symbol (e.g. "RELIANCE") — since the request lists them as two distinct columns. Note this differs from most other reports in the app, where a single "Scrip Name" column already means the trading symbol (there's no separate "Scrip Code" column elsewhere) — flag if this new report's naming should instead match that existing convention.
- "PSN" is rendered as a generated pledge-sequence-style identifier (`PSN` + digits); the exact real-world PSN format wasn't specified.

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
