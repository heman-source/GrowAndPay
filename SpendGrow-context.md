# SpendGrow — "Put it to work" · Development Context & Frozen Spec

> AngelOne Hackathon 2026 · Grow & Pay onboarding
> Status: **Spec frozen — approved decisions captured. No build started yet.**
> Branch: `claude/optimistic-hopper-t503em`

---

## 1. Background

Two reference prototypes informed this:

- **`hi2_1.html` (SpendGrow)** — current build. Its Analysis screen has a Tinder-style
  deck of category cards, but swiping only *advances* cards (a carousel). A static
  "potential earnings" table below un-dims row by row; a counter shows `1/N`.
- **`angeloneholdings.html`** — the AngelOne Holdings + Spend-Analysis reference used
  for the steady-state (return) experience: Holdings screen → green "Grow & Pay"
  widget → Spend Analysis (hero + bars) → category L2 detail.

**The problem with today's deck:** the swipe is decorative. It shows categories but the
user decides nothing — no commitment, no consequence, no accumulation.

---

## 2. The reframed intent

Turn the deck into an **onboarding configurator where the swipe *is* the action**.
Each right-swipe = "put this category's money to work"; the user *feels* it accumulate
("had I done this, I'd have earned ₹___"). The gesture builds understanding **and**
ownership — endowment / IKEA effect: people value what they help build. The aha
compounds card by card.

This is **first-run onboarding** — the moment a customer realises where their money
could have worked.

---

## 3. Frozen decisions

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Configurator vs education | **Configurator** — swipe is consequential |
| 2 | Meter math (what accumulates) | **Full category flow** — the whole monthly spend sits in a liquid fund and earns until spent |
| 3 | Card set | **5 spend cards** + EMIs/SIPs as fixed "auto-protected" note + idle leftover folded into summary |
| 4 | Tail categories (beyond the 5) | **Auto-include** — bundled & put to work, shown in summary as "core 5 + N smaller auto-included" |
| 5 | Left-swipe (keep idle) feel | **Honest & subtle** loss — greyed card, "stays idle · earns ₹0", forgone ₹ tallied for a soft re-offer |
| 6 | Re-entry | **First-run only** — later changes via dashboard, not the deck |
| 7 | Accessibility | **Swipe + visible buttons** (Keep idle / Put to work), keyboard-focusable |
| 8 | Mechanic | **"Put it to work" deck** (swipe cards + buttons + live meter) |

---

## 4. Screen-by-screen spec

### 4.1 Top — the ₹ meter (emotional spine)
- Sticky growing meter. **Big number = ₹ mobilised** (full category flow).
- Sub-ticker = **"earning ~₹__/yr"**, counts up live on each right-swipe with a pulse /
  scale-bounce (haptic-style micro-feedback).
- Persistent micro-disclaimer: *"Indicative at ~6.7% p.a. Liquid-fund returns aren't guaranteed."*
- 5 progress dots.

### 4.2 Middle — the deck (5 cards)
- **Right = Put to work** → card flies up into the meter; principal + yield accumulate.
- **Left = Keep idle** → card greys, "stays idle · earns ₹0" ghosts away, forgone ₹ tallied.
- Each card shows: category, full monthly flow, idle-days insight, "could earn ₹X/yr",
  and the fear-defuser line: *"Still spendable anytime — it just earns until you spend it."*
- **Two real buttons** under the deck (Keep idle / Put to work) — same outcome, focusable.
- **Undo** — toast after each swipe; reverses the last action and rolls the meter back.
- Proposed order (build to peak, largest last):
  Online Shopping → Fuel → Household/House Help → Groceries/Dining → Utilities/Bills.
  *(Confirm exact categories against full data during build.)*
- **EMIs & SIPs** = fixed "🛡 Auto-protected · never touched" note, not swipeable.

### 4.3 End — summary → activate
- *"You mobilised ₹X across N categories → earning ~₹Y/yr."*
- Tail line: *"core 5 + N smaller categories auto-included."*
- Soft re-offer: *"You left ₹Z idle — reconsider?"* (forgone tally; tap to revisit those cards).
- **Activate** → pre-fills the existing S3 Add-Money screen with ₹X; skipped categories zeroed.

### 4.4 Return state (steady state — `angeloneholdings` reference)
- Deck is **first-run only**. Afterwards:
  Holdings → green Grow & Pay widget → **Spend Analysis** with a full **inflow/outflow
  bar graph** (income vs fixed / lifestyle / idle) → each category → **L2 spends** screen.
- Reconfigure via dashboard, **not** the deck.

---

## 5. Design principles
- Growth-green AngelOne tokens.
- **One number that grows** = the dopamine.
- **Loss-framed per card, gain-framed in aggregate.**
- Haptic-style micro-feedback on each add.
- Clear progress sense; always a visible escape / CTA.
- **Regulatory:** SEBI-sensitive. Returns are *indicative, not guaranteed*. The left-swipe
  "loss" is framed as **forgone opportunity**, never "you lost money."

---

## 6. Build approach
- Evolve the existing `hi2` `#s2-deck` **in place** — reuse its tokens, card shell, and
  swipe physics — rather than start fresh. Keeps it consistent with the rest of the prototype.

---

## 7. Open items (before / during build)
- **Green light to build** (pending).
- **Output location:** standalone HTML in this repo on-branch (default) vs. hand-off file.
- Confirm the exact 5 categories + the tail count against the full category data.
