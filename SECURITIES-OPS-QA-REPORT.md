# Securities Ops Control Tower — QA Test Report

**Scope (validated):** Functional + data-integrity + parity for *built* features.
Unbuilt legacy reports (BTST, ROS/Register, Transaction Statement, CUSPA ageing,
Repledge/API-EPI MIS) **excluded** by decision. Quantity-only (no ₹ value views)
**accepted as design** per spec.

**Method:** Automated headless Chromium drive of `securities-ops-control-tower.html`,
asserting row counts, filter logic, drilldown context, and data math.
**Result: 110 / 110 PASS · 0 JS errors** (cumulative, through the Collateral Management pass).

**Note on this pass:** the persistent test script (`qa.cjs`) lives outside the repo as a
scratch file and was lost to an environment/container reset between sessions — it was never
committed. This pass re-verified the screens actually touched — Scrip Details, Client Details
(including the follow-up TPIN column), and Settlement Explorer (Settlement Summary/"none" mode
removed entirely, and the Process Type report's Level 2/3 rebuilt as the new SHARE ACCOUNTING
net format) — with a focused **54 / 54 PASS** run (see updated sections below). The other areas
in this report (Settlement Dashboard, Security Lookup, Client-Wise Report, Shortage-Wise Report,
Process Lookup, Securities Lookup, Transaction Reports, Collateral Management, Corporate
Actions/Downloads) were not touched by today's changes and were not re-run this pass.

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

### B. Settlement Explorer — filters
| TC | Case | Result |
|----|------|--------|
| SE-P1 | Party Code input field removed from Settlement Explorer's filter bar | PASS |
| SE-P2 | Settlement Number label carries a required-field star | PASS |
| SE-P3 | Process Type label carries a required-field star | PASS |
| SE-P4 | Process Type dropdown no longer has a blank "none/settlement totals" option — only Shares Payout / Shares Payin, defaulting to Shares Payout | PASS |

**Behaviour change (by request):** The **Party Code filter has been removed** (it scoped both the old Settlement Summary and the Process Type report). **Settlement Number and Process Type are now both required** (starred) — Process Type no longer has a blank "none" option, so there is no longer a "settlement totals" mode: **the old Settlement Summary screen (its own L1 scrip-wise list, L2 clients, L3 party-securities drill) has been deleted entirely**, since it was only reachable via that now-removed option. Selecting Process Type is now mandatory, defaulting to Shares Payout.

### B2. Settlement Explorer · Process Type — Level 1 (scrip list, unchanged)
| TC | Case | Result |
|----|------|--------|
| SE1 | Payout L1 columns: Scrip, ISIN, Series, Payout Obligation, Payout Received, Payout Shortage, Excess Payin Reversal Payout | PASS |
| SE2 | Payin L1 columns: Scrip, ISIN, Series, Payin Obligation, Earmarked Quantity, Payin Shortage | PASS |
| SE9 | ISIN text filter, no match → empty state | PASS |
| SE10 | ISIN text filter narrows L1 to one matching scrip | PASS |
| SE11 | No settlement number → guidance prompt | PASS |
| SE12 | Out-of-window settlement → guard message | PASS |
| SE13 | Settlement has no chosen Settlement Type leg → guard message | PASS |

### B3. Settlement Explorer · SHARE ACCOUNTING (Process Type Levels 2/3 — new format, by request)
| TC | Case | Result |
|----|------|--------|
| SA1 | Click a scrip (L1) → L2 "SHARE ACCOUNTING (Scripwise report of all Clients)" | PASS |
| SA2 | L2 columns: Code, Client Name, Net Payout, Net Payin, Payout Received, Payin Done, Shortage | PASS |
| SA3 | L2 has client rows | PASS |
| SA4 | **True net settlement**: exactly one of Net Payout/Net Payin is nonzero per client (never both) | PASS |
| SA5 | Shortage = obligation − completed for whichever side applies | PASS |
| SA6 | Zero-valued (inapplicable-side) cells are plain "0", not clickable | PASS |
| SA7 | Clicking a nonzero metric cell opens the quantity-detail modal *without* also drilling into that client (defect found & fixed — see below) | PASS |
| SA8 | L2 "Total" footer reconciles exactly to the sum of the client rows | PASS |
| SA9 | Click a client (L2) → L3 "SHARE ACCOUNTING" with a "Code: … · Client Name: …" subtitle | PASS |
| SA10 | L3 subtitle correctly shows the clicked client's Code and Client Name | PASS |
| SA11 | L3 columns: Scrip, Series, Net Payout, Net Payin, Payout Received, Payin Done, Shortage | PASS |
| SA12 | L3 lists **every** scrip that client traded this settlement, not just the one drilled from | PASS |
| SA13 | L3's first row is the originally-selected scrip, tagged "selected" | PASS |
| SA14 | L2 and L3 agree exactly on the same client+scrip figures (both derive from the same `seNetRow` function) | PASS |
| SA15 | L3 breadcrumb has two links back up (scrip list, scrip's clients) | PASS |
| SA16 | Breadcrumb click returns all the way to L1 | PASS |
| SA17 | L2's SHARE ACCOUNTING format is identical whether entered via Shares Payout or Shares Payin | PASS |
| SA18 | Changing any filter resets the drill state back to L1 | PASS |

**Defect found & fixed during this pass:** the new L2 client rows are both row-clickable (drill to L3) and have inline clickable quantity cells (open the narration modal) — clicking a quantity cell's link bubbled the click event up to the row, triggering *both* the modal *and* the L3 drill simultaneously. Fixed by adding `event.stopPropagation()` to the cell links, matching the pattern already used for Settlement Summary's old shortage-cell links.

**Behaviour change (by request):** Clicking a scrip (L1) no longer shows the old single-metric client breakdown (Party Code / Obligation Quantity / Completed / Shortage / extra column) — it now shows the **SHARE ACCOUNTING** format matching the attached legacy report exactly: **Net Payout, Net Payin, Payout Received, Payin Done, Shortage**, with each client netted to **exactly one side** (a true net-settlement model, not today's independent Payin+Payout obligations). Clicking a client name drills to the mirror view — every scrip that client traded this settlement, same 5-metric format, titled "Code: … · Client Name: …" per the attached format. Both levels are unaffected by which Process Type (Payout/Payin) was selected to get there, since a client's net position on a scrip+settlement is a single objective fact, not view-dependent.

**Design calls made without an explicit spec — flagged for review:**
- **Net Payout/Net Payin/Payout Received/Payin Done/Shortage are five separate columns**, per your written spec — even though the attached screenshot shows a single signed "Net Qty" column instead of two separate Net Payout/Net Payin columns. I followed the written column list over the screenshot's exact visual, since the two conflict slightly; flag if the single signed-column layout was actually intended.
- **L1 (the scrip-list aggregate) was left untouched** and still uses the old independent-obligation model (`seRow`), while L2/L3 now use the new true-net model (`seNetRow`) for the *same* clients. **This means L1's totals and L2's SHARE ACCOUNTING totals no longer reconcile to each other** — they're now two different models answering two different questions (L1: "what's each side's total obligation, computed independently" vs. L2/L3: "what does each client actually net to"). This breaks the reconciliation-by-construction principle followed everywhere else in this app. If you'd like L1 recomputed as the sum of the same net rows so the two levels agree again, let me know and I'll wire it up.
- Client names in this report (`seClientName`) reuse the existing `PW_NAMES` list via a hash of the party code — the same mechanism already used for the party-wise bifurcation modal elsewhere, so names are stable and consistent, but are cosmetic and not tied to any real identity.
- Kept the metric-cell click behavior consistent with this report's own existing precedent (all of Obligation/Completed/Shortage were already clickable in the old L2/L3): all five SHARE ACCOUNTING columns are clickable when nonzero, even though the attached screenshot's static styling suggests only Delivered/Received (not Net Qty or Shortage) were links.
- Omitted the legacy screenshot's decorative "Bill" and "Net" icon columns — they correspond to print/netting actions with no equivalent feature in this app.

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
| SD1 | Empty by default on fresh load — no eager full list until a filter is entered | PASS |
| SD2 | **Clicking Apply with both fields blank now lists every scrip** (17 scrips) | PASS |
| SD3 | Scrip master search columns: Scrip Code, Series, ISIN, Status, Company Name (**Last Price column removed**) | PASS |
| SD4 | Status values restricted to **Active / Inactive only** (Suspended and Pledged dropped) | PASS |
| SD5 | Scrip Code filter narrows to one match | PASS |
| SD6 | ISIN prefix filter narrows the list | PASS |
| SD7 | No `undefined` values from the hash-shift bug (scrip master) | PASS |
| SD8 | Row click links directly to Security Lookup | PASS |
| SD9 | Deep-link `ctx.isin` prefills Scrip Code and shows the result immediately (bypasses the empty state) | PASS |
| SD10 | Reset clears fields and the Apply-shows-all state, back to the empty prompt | PASS |
| CD1 | Party Code label carries a required-field star | PASS |
| CD2 | **DP ID and Status inputs removed** — only Party Code + Beneficiary Owner ID filters remain | PASS |
| CD3 | Empty by default — **Party Code is now required** to search at all (type `*`/`%` for all clients) | PASS |
| CD4 | Result columns: Party Code, Name of the Holder, **Beneficiary Owner ID** (renamed from Client ID; **DP ID column removed**), Default DP ID, DP Type, POA Status, **TPIN** (new), **Process Applicable** (renamed from DDPI Status) | PASS |
| CD5 | Wildcard `*` on Party Code lists accounts for every client | PASS |
| CD6 | POA Status values restricted to **POA / NON POA / DDPI Active** | PASS |
| CD7 | **Default DP ID → Process Applicable = "Payout and Payin"; non-default → "Payin" only** | PASS |
| CD8 | A client with POA registered always shows "POA" (never DDPI Active/NON POA), and vice versa | PASS |
| CD9 | Beneficiary Owner ID shows the client's real **full** 16-digit BOID for CDSL default accounts (not a truncated half, unlike the old DP ID + Client ID split) | PASS |
| CD14 | **TPIN shows "Received"/"Not Received" only on NON POA rows; POA and DDPI Active rows show "—"** | PASS |
| CD15 | TPIN's Received/Not Received split is verified directly against a wider hash sample (both values occur) | PASS |
| CD10 | Party Code substring filter narrows to one client's accounts | PASS |
| CD11 | Row click links to Client-Wise Report | PASS |
| CD12 | Deep-link `ctx.party` prefills Party Code and shows the result immediately | PASS |
| CD13 | Reset clears fields back to the empty state | PASS |

**Behaviour change (by request):** **Scrip Details** — clicking Apply with both Scrip Code and ISIN blank now lists every scrip (previously blank stayed blank until the Reset button); Last Price column removed; Status is now binary (Active/Inactive), Suspended and Pledged dropped.

**Behaviour change (by request):** **Client Details** — Party Code is now a required field (starred) and is the sole gate on the empty state; the DP ID and Status filters were removed entirely (Status doesn't exist as a concept in the new model). In the results: the DP ID column is gone, "Client ID" is renamed **Beneficiary Owner ID** and now shows the account's full identifier (previously it showed only the second half of a DP ID + Client ID split — since the column is now explicitly a BOID, showing half of it would have been wrong, so for CDSL default accounts it now reconstructs to the client's real, existing 16-digit BOID in full). "POA Status" is now a three-way value — **POA / NON POA / DDPI Active** — reflecting SEBI's shift from POA to DDPI (Demat Debit and Pledge Instruction) as the account-debit authorisation mechanism; a client already on POA always shows "POA", and a client with no POA is deterministically split between "DDPI Active" and "NON POA". "DDPI Status" is renamed **Process Applicable**, driven purely by the existing Default/non-default flag: a Default DP ID always shows "Payout and Payin", a non-default one always shows "Payin" only, per spec.

**Behaviour change (by request):** Added a **TPIN** column (CDSL's Transaction Password/PIN, used to authorise a debit when there's no standing POA/DDPI authorisation on file) between POA Status and Process Applicable. It's only meaningful when POA Status is "NON POA" — those rows show "Received" or "Not Received" (deterministic per account); POA and DDPI Active rows show "—", following the same "not applicable stays blank" convention used for Payout figures elsewhere in the app.

**Design calls made without an explicit spec — flagged for review:**
- With only 4 demo clients in `CLIENTS`, the "NON POA" value never actually appears in a quick spot-check (both no-POA clients happened to hash into "DDPI Active"); the ~40/60 split logic is verified directly against the data (CD8), but visually you may need to try a few more hash seeds to see "NON POA" — and consequently a live TPIN value — render. Not a bug — just a small-sample coincidence (CD15 verifies the TPIN split directly against a wider sample instead).
- The Party Code filter's compulsory star does **not** block a literal `*`/`%` wildcard from being "the required value" — typing a wildcard still counts as satisfying the requirement (consistent with how `*`/`%` is treated as a valid, deliberate "all" input everywhere else in the app). Flag if Party Code should instead require a **specific** client, not a wildcard.
- Renamed the input field label too (previously "Client DP No", now "Beneficiary Owner ID") to stay consistent with the renamed result column — the request only mentioned the result column by name, so this is my own consistency call.
- Placed TPIN right after POA Status (rather than at the end of the table) since the two are the same underlying concept (debit authorisation) — flag if a different position was intended.

**Defect found & fixed during the original pass:** `hsh()` returns unsigned 32-bit hashes that can exceed 2^31; using the *signed* right-shift operator (`>>`) on such values could flip them negative, making `% arrayLength` return a negative index — silently producing `undefined` (e.g. a DDPI badge rendered "undefined") or corrupted holdings figures app-wide. Fixed by switching every `hash >> n` pattern to the unsigned `>>> n`, including in pre-existing code not touched by this feature.

**Update — Security/Client Summary + Holdings widgets removed** from both screens per follow-up feedback; each screen is now search-table only, with each row linking straight to the deeper operational screen (Security Lookup / Client-Wise Report). "Introducer" renamed to "Name of the Holder" (shows the client's real name); added a "Default DP ID" column — clients now have a 50% chance of a second, non-default DP account for realism, and the default account is always the one derived from the existing BOID.

**Update — Client Details now also starts empty by default** (no Party Code / DP ID / Client DP No / Status filter → guidance prompt, no eager 4-client list), matching Scrip Details' behavior for consistency. Selecting a non-"All" Status alone, or any text filter (including `*`/`%`), triggers the search. *(Superseded by the CD1-13 pass above: DP ID and Status filters no longer exist — Party Code alone now gates the empty state.)*

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
