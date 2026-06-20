# Grow & Pay v2 — incorporation plan (P0 + P1)

Locked decisions: **Hybrid model (seed + sweep rule)** · **light KYC confirm
(reuse AngelOne KYC)** · differentiation **deferred** · discoverability
**deferred**. Build target: `grow-and-pay-flow.html` (extend in place, `pw-*` /
`v2-` namespaced, design system unchanged).

## Rebuilt onboarding chain
```
Holdings widget → CONSENT → (analysis) → DECK → SUMMARY → SWEEP RULE
   → KYC CONFIRM → ADD MONEY (seed, pre-filled) → CONFIRM(+tax/load)
   → Processing → Order Placed → DASHBOARD (Spendable/Growing + sweep status)
```

---

## P0 — build first

### P0-A · Consent & privacy  *(new screen, before analysis)*
- Entry: Holdings "Review" → Consent (instead of straight to deck).
- Copy: "Analyse your spends? We read transaction SMS **on your device** — raw
  messages never leave your phone. You're in control."
- Actions: **Allow & analyse** (→ deck) · **Not now** (→ manual idle-amount input,
  then deck).
- Persisting cue: provenance strip "Analysed on your device · you control it" on
  deck + analysis.
- States: allow · manual fallback.

### P0-B · Sweep rule  *(new screen, after Summary)*
- Summary CTA changes to "Set it up →" (no longer straight to Add-Money).
- Controls:
  - **Invest now (seed):** editable, pre-filled with deck total.
  - **Auto-sweep toggle:** "Sweep idle cash above ₹__ every [month ▾ / on each
    payout]." Buffer slider (₹0–₹50k), default ₹20k.
  - Reassurance: "Pause or change anytime."
  - **Mandate consent** line + checkbox.
- Output: seed → Add-Money; rule object stored for dashboard.
- States: sweep on / off; buffer value.

### P0-C · KYC confirm  *(new light step / sheet)*
- "Confirm your details" — PAN (masked, prefilled), FATCA declaration checkbox,
  **nominee** (pick existing / add), risk-consent checkbox.
- CTA "Confirm & continue" → Add-Money. Only shown once.

### P0-D · Tax & exit-load honesty  *(modify Add-Money + Confirm sheet)*
- Projection: **"Show after-tax" toggle** (default shows "before tax"); explainer
  sheet: "Debt-fund gains are taxed at your slab rate. Each spend is a redemption."
- Confirm sheet: add exit-load note "Spending/withdrawing within 7 days incurs a
  small exit load."

### P0-E · Spendable now vs Growing split  *(component, threaded everywhere)*
- Pattern: **Spendable now ₹X** (instant-redeemable, capped) · **Growing ₹Y**
  (settles T+1). Applied to Dashboard header, Scanner, Withdraw.
- Constants: instant cap = min(₹50,000, 90% of balance).

### P0-F · Scan & Pay real payment  *(rebuild scanner sheet flow)*
- scan (viewfinder) → **enter amount** → **confirmation** ("Paid from: Spendable
  ₹X" + "Bank fallback ₹Z" when over cap) → **UPI PIN** → **result**.
- States: within-cap success · above-cap bank fallback · insufficient → top-up ·
  failure/retry.

---

## P1 — build second

### P1-G · Withdraw to bank  *(new flow from Dashboard)*
- Amount (Spendable cap shown) → **Instant** (≤ cap) vs **Standard T+1** → exit-
  load/tax warning if within 7 days → bank select → timeline confirmation.
- Mirrors Add-Money calculator pattern.

### P1-H · Dashboard steady-state loop  *(enrich S5)*
- Header: Spendable/Growing split.
- **Sweep status row:** "Auto-sweep on · last swept ₹12k on 18 Jun · next 1 Jul."
- **Idle-detected nudge card:** "₹14,200 sat idle this week → Sweep it" (mini-
  sweep, reuses value prop without full deck).
- **Pre-bill cover note:** "Rent ₹48k due in 3 days — you're covered."

---

## Parked (explicit, not now)
- Discoverability surfaces (cash-moment interception, pinned card, notifications,
  header chip).
- Differentiation hook (pledge-as-margin / brokerage offset).

## Build sequence
1. Slice 1 (onboarding): Consent → Sweep Rule → KYC confirm + Summary handoff.
2. Slice 2: tax/load honesty + Spendable/Growing split + Scan & Pay flow.
3. Slice 3 (P1): Withdraw + Dashboard loop.
Each slice: validate JS, commit, push, deliver file.
