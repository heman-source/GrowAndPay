# AngelOne · Grow & Pay — Design Specification

A handoff-grade spec for regenerating this prototype in a design tool. Source of
truth: `grow-and-pay-flow.html`. Single mobile artboard (iPhone-class), one app,
multiple screens swapped in place.

- **Product:** "Grow & Pay" inside the AngelOne app. Idle money sits in liquid
  funds earning ~6.7% p.a. and stays spendable until you spend it.
- **Hero mechanic:** a first-run **"Put it to work"** swipe-deck configurator.
- **Platform frame:** 393 × 830 px screen (iPhone 14-class), portrait only.
- **Tone:** confident, honest, growth-green. Loss-aware per card, gain-framed in
  aggregate. SEBI-safe — returns are always "indicative, not guaranteed".

---

## 1. Design tokens

### Color
| Token | Hex | Use |
|---|---|---|
| `--ao-blue` | `#3F5BD9` | primary brand / links / selected |
| `--ao-blue-press` | `#3147B0` | pressed blue |
| `--ao-green` | `#008F75` | growth / earnings / primary CTA |
| `--ao-green-2` | `#41AB98` | secondary green, gains |
| green accent | `#41E0BC` / `#7DF3D6` | bright green on dark (meter, scanner) |
| `--ao-red` / `--ao-red-2` | `#D64D4D` / `#FA6464` | loss |
| `--ao-purple` | `#702BCD` | tertiary (Scan & Pay tile, MTF) |
| `--ao-saffron` | `#FF9933` | SGB / gold accents |
| `--navy-1/2/3` | `#2C355A` / `#222B40` / `#181F29` (deep `#10162A`) | dark headers, meter, scanner |
| `--text-1/2/3` | `#181F29` / `#6B7686` / `#9AA3B2` | text hi/mid/low |
| `--border` | `#E8EBF1` | hairlines |
| `--surface` / `--surface-2` | `#F4F6FB` / `#F4F4F6` | app background |
| `--card` | `#FFFFFF` | cards |
| amber set | `#B57608` text · `#FFF7ED` bg · `#FCE3C2` border | idle / forgone / warnings |

Category accent colors (used on bars, deck cards, L2): Rent `#3F5BD9`, Utilities
`#7C3AED`, Online Shopping `#9333EA`, Swiggy&Zomato `#D97706`, Fuel `#EA580C`,
Groceries `#059669`, House Help `#0EA5A0`, Misc `#0284C7`.

### Type — Inter
| Style | Size / weight |
|---|---|
| Hero number | 40–62 / 800 |
| H1 | 22–25 / 800 |
| Title | 18 / 700 |
| Body | 13–14 / 400–600 |
| Label (caps) | 10–11 / 700–800, letter-spacing .05em, uppercase |
| Micro | 11–12 / 500 |

Numbers use `font-variant-numeric: tabular-nums`. INR formatting is Indian-grouped
(`₹1,15,180`).

### Shape / elevation / motion
- Radii: cards `16px`, pills `8–20px`, sheets `24–26px` top, phone `44px` inner.
- Shadows: card `0 12px 30px -12px rgba(16,24,40,.55)`; CTA glow green
  `0 8px 22px -8px rgba(0,143,117,.5)`; sheet `0 -8px 40px rgba(10,15,25,.22)`.
- Screen transition: slide X, `.34–.42s cubic-bezier(.4,0,.2,1)`; incoming from
  right, outgoing to left.
- Respect `prefers-reduced-motion` (disable all).

---

## 2. Global shell

- **Phone frame:** black bezel, notch, 54px outer radius; screen 393×830.
- **Status bar:** 46px; left time, right signal/wifi/battery. Light variant
  (white) over dark headers.
- **Screen system:** each screen is `position:absolute; inset:0; flex column`.
  Active = `translateX(0)`; others off-canvas.
- **Bottom nav (5 tabs):** Home, Watchlist, Portfolio (active), Orders, Account —
  62px, white, top hairline. Present on Holdings + Dashboard.

---

## 3. Screens

### S1 · Holdings (entry)
Standard AngelOne portfolio screen.
- **App bar:** "Holdings" + "My Wealth", profile / search / overflow icons.
- **Tabs:** Overview (active) · Equity · Mutual Funds · SGB · Tab 1.
- **Portfolio summary card** (navy gradient): total `₹12,91,378`, eye toggle;
  Overall Gain `₹1,23,600.09 (+10.58%)` green; Invested `₹11,67,775`; Today's Gain
  `₹5,385.20 (+0.41%)`; "VERIFIED 🔒" bottom-right.
- **Grow & Pay widget** (green, pulsing dot) — the first-run entry:
  - Title "Idle cash needs attention", sub "₹52,400 idle · could earn **₹7,228/yr**",
    CTA button "Review". → opens the **Put-it-to-work deck**.
- **Assets rows:** Equity `₹3,01,228 / +10.05%`; Mutual Funds `₹8,35,802 / +5.68%`;
  SGB `₹30,745 / +149.03%`. Icons recreated as SVG.
- **Grow & Pay earning row** (hidden until activated): "Grow & Pay · Earning",
  "Liquid Fund · Day 22 · 6.72% p.a.", "+₹214.36 earned", `₹35,214 / +0.61%`. →
  Dashboard.
- **Promos:** MTF Borrowing, Start SIP. **Upcoming Events:** Corporate Action,
  Stock SIP.
- Scan & Pay sleeve docked above nav (see §5).

### S-DECK · "Put your money to work" (first-run configurator) ★
Dark header + light body. This is the signature screen.

**Header (navy gradient):**
- Back (→ Holdings), title "Put your money to work", sub "Swipe each category you
  want earning".
- **Money meter:** eyebrow "MONEY PUT TO WORK"; big `₹` amount (counts up + a
  spring pulse on each add); green pill "● ₹__ /yr earning" (live ticker);
  disclaimer "Indicative at ~6.7% p.a. Liquid-fund returns aren't guaranteed."

**Body (light):**
- **Progress dots** (5): active = elongated green; done = green-2.
- **Auto-protected note** (green tint): 🛡️ "EMIs & SIPs · auto-protected — Never
  touched, they always go out on time."
- **Deck label:** "YOUR SPENDING CATEGORIES" + counter pill "1 / 5".
- **Card stack** (see §4 for the card). Top card draggable; 2 peeking behind
  (scaled/offset).
- **Action buttons:** outlined "← Keep idle" / solid green "Put to work →".
- **Hint:** "Swipe · tap · or ← → keys · *see full breakdown*" (link → Spend
  Analysis).
- **Undo toast** (dark pill, bottom): "**{Category}** put to work / kept idle"
  + "UNDO".

### S-SUMMARY · "Your money, working"
- Back → deck.
- **Hero (green gradient):** eyebrow "✦ YOU JUST MOBILISED"; line "You put **₹X**
  to work across **N categories**"; big total `₹{X + tail + idle}`; sub "now
  earning ~₹Y/yr".
- **Breakdown card** "WHAT'S WORKING NOW": one row per category swiped right
  (icon, name, monthly flow, +₹/yr); then "+ {n} more categories · auto-included";
  then "💸 Idle cash · leftover, now earning full-time". Footer (green): "TOTAL
  EARNING / YEAR" + total, "indicative, not guaranteed".
- **Reconsider card** (amber, only if any skipped): "You left ₹Z/yr on the table",
  "{n} categories are still sitting idle, earning nothing." + button "Reconsider
  those →" (re-runs the deck).
- **Sticky CTA:** green "Activate Grow & Pay · ₹{total} →" + "Amount pre-filled
  from your choices. You can edit it next." → Add Money (pre-filled).

### S-ANALYSIS · Spend Analysis (steady-state)
Reachable from the dashboard tile (and deck "see full breakdown").
- Back → Holdings.
- **Hero card:** dark-green band, eyebrow "● IDLE CASH", sparkline, big `₹49,042`,
  line "Left over after every bill. Not invested, not earning — just sitting." Two
  tiles: idle `₹49,042` / returns `+₹3,335`. Caption "This could be in a liquid
  fund earning **6.7% p.a.** while you decide."
- **Section "Where your money sits idle":** bar list, one tappable **bar-row** per
  category — icon, name, "Idle N days avg", amount, chevron, and a green progress
  bar (width ∝ amount/max). → Category L2.
- Sticky CTA "Activate Grow & Pay" → deck.

### S-CAT · Category L2 detail
- Back → analysis. Title = category name.
- **Insight card:** colored icon, big amount, meta "{type} · idle N days on
  average", green chip "Could earn ₹{amt×6.7%}/yr in a liquid fund", punch line.
- **Section "Recent transactions":** transaction rows (icon, merchant, date,
  amount).
- Sticky CTA "Activate Grow & Pay".

### S2 · Add Money (calculator) — pre-filled by Activate
- Back → Holdings. Title "Adding money to".
- **Balance card:** "Grow & Pay", "▲ Growing at up to **6.7%**", "Powered by
  ICICI & Bajaj".
- **Amount display:** big `₹` number (zero state greyed). Quick chips ₹25,000 /
  ₹50,000 / ₹1,00,000; "★ Recommended".
- **Dark keypad panel:** projection strip "Projected gains (in ₹) in 1 Year" +
  value (= amount × 6.7%); numeric keypad (1–9, ., 0, backspace); green "Confirm
  amount" → Confirm sheet.

### S4 · Order Placed
- Green check orb; "Order placed for" + amount; "Units allocated in 1–2 business
  days". Split card: ICICI / Bajaj halves, Stamp duty ₹1.75, Platform fee ₹0.00
  (green), "Daily earning from tomorrow" (green), Order ID. SEBI disclaimer. CTA
  "See Dashboard →".

### S5 · Earning Dashboard (return / standard state) ★ updated
Dark header "Grow & Pay · Day 22 of earning".
- **Earnings hero (green gradient):** "LIFETIME EARNINGS" `₹214.36`; metrics
  Invested `₹35,000` / Rate `6.72% p.a.` / Return `+0.61%`; note "Yesterday's
  credit ₹6.43 · credited 11 PM · next tonight".
- ~~Brokerage-offset card~~ — **REMOVED. Do not include.**
- **Fund breakdown card:** ICICI Pru Liquid `₹17,608 (+₹108.20, 6.74%)`; Bajaj
  Finserv Liquid `₹17,606 (+₹106.16, 6.71%)`.
- **Tile: Spend Analysis** (green) → S-Analysis. "See where your money sits,
  category by category".
- **Tile: Scan & Pay** (purple) → opens scanner sheet. "Pay any merchant from your
  liquid fund".
- Bottom nav + Scan & Pay sleeve.

### Overlays
- **Confirm sheet** (bottom): split bar, ICICI/Bajaj, total, stamp duty, daily
  earning; SEBI note; green "Confirm & Invest ₹X"; "Cancel". → Processing.
- **Processing cover:** spinning blue orb "Placing your order… / Connecting to BSE
  Star MF"; 3 step rows that tick green sequentially → S4.

---

## 4. Component: the swipe card (deck)

A stacked card, ~ full width of deck area, ~290px tall.
- **Top band** (height ~116px): solid category accent color. Top-right: white
  rounded icon tile with category glyph. Bottom-left: white pill tag (category
  type, uppercase) + white category name (21/800).
- **Body (white):** insight line (one sentence, idle-days framing); divider;
  flow row — left "Monthly flow ₹{amount}", right "+₹{earn} · COULD EARN / YR"
  (green); reassurance chip (grey): "💡 Still spendable anytime — it just **earns
  until you spend it**."
- **Stamps** (appear on drag): right = green "PUT TO WORK" (rot +11°); left = grey
  "KEEP IDLE" (rot −11°), opacity ∝ drag distance.

**Stack layout:** front = full; +1 behind `translateY(10) scale(.96)`; +2
`translateY(19) scale(.92) opacity .7`. On decide, card flies off: right →
`translateX(135%) rotate(12°)`; left → `translateX(-135%) rotate(-12°)` +
`grayscale(1)`; both fade out.

---

## 5. Component: Scan & Pay sleeve + scanner

- **Sleeve (closed):** slim navy pill docked above the bottom nav, centered.
  Single row: small up-chevron · "Scan & Pay" (13/800) · small up-chevron.
  Chevrons gently bob. Present on Holdings + Dashboard only.
- **Interaction:** tap **or swipe up** → scanner sheet. Swipe-down on grip / tap ✕
  / tap backdrop → close.
- **Scanner sheet (open):** dark sheet (~80% height) sliding up over a dimmed
  backdrop. Grip; header "Scan & Pay" + ✕. Viewfinder: 236px rounded square,
  bright-green corner brackets, a sweeping green scan line (glowing). Hint "Point
  at any UPI QR to pay straight from your Grow & Pay balance — it keeps earning
  right up to the moment you pay." Cue "● Balance growing at 6.72% p.a." Footer:
  "Upload QR" (ghost) / "Enter UPI ID" (green).

---

## 6. Flow & navigation

```
S1 Holdings ──[Grow&Pay widget: Review]──▶ S-DECK
S-DECK ──(swipe 5 cards)──▶ S-SUMMARY ──[Activate]──▶ S2 (pre-filled)
S2 ──[Confirm amount]──▶ Confirm sheet ──[Confirm & Invest]──▶ Processing ──▶ S4 ──▶ S5 Dashboard
S5 Dashboard ──[Spend Analysis tile]──▶ S-ANALYSIS ──[bar row]──▶ S-CAT
Scan & Pay sleeve (S1, S5) ──[tap/swipe up]──▶ Scanner sheet
```
- **First run = the deck** (one-time). **Steady state = Dashboard + Spend Analysis
  bars + L2.** After activation the green widget is replaced by the earning row.

---

## 7. Data model & math

**Rate:** 6.7% p.a. (`RATE = 0.067`). Per-category earnings = `amount × RATE`
(matches L2). Meter mobilised = Σ monthly flow of right-swiped cards.

**5 deck cards** (order = build-to-peak, biggest last):
| Order | Category | Monthly flow | Idle days | Accent |
|---|---|---|---|---|
| 1 | Fuel | ₹12,000 | 9 | `#EA580C` |
| 2 | Swiggy & Zomato | ₹12,787 | 11 | `#D97706` |
| 3 | Online Shopping | ₹18,393 | 8 | `#9333EA` |
| 4 | Utilities & Bills | ₹24,000 | 6 | `#7C3AED` |
| 5 | Rent | ₹48,000 | 19 | `#3F5BD9` |

**Auto-included tail** (3 categories, not shown as cards): Groceries ₹9,978 +
House Help ₹7,800 + Miscellaneous ₹6,000 = **₹23,778**.
**Idle cash:** **₹49,042** (earns full-year).
**EMIs & SIPs:** auto-protected, never mobilised.

If all 5 swiped right: mobilised ₹1,15,180 → total with tail + idle ≈ **₹1,88,000**,
earning ≈ **₹12,596/yr**. Activate pre-fills the calculator with the total.

Spend-Analysis bar categories (8): Rent ₹48,000, Utilities & Bills ₹24,000, Online
Shopping ₹18,393, Swiggy & Zomato ₹12,787, Fuel ₹12,000, Groceries ₹9,978, House
Help ₹7,800, Miscellaneous ₹6,000. Each has a punch line + 5 sample transactions.

---

## 8. Interaction & state summary

- **Meter:** count-up tween (~450ms ease-out cubic) + spring pulse on right-swipe.
- **Swipe:** drag threshold ~65px to commit; below = snap back. Stamps fade with
  drag. Keyboard ← / → mirror left/right. Buttons mirror swipe.
- **Undo:** single-level; reverses last decision and rolls the meter/forgone back.
- **Skipped categories:** excluded from mobilised; tallied as "forgone ₹/yr" and
  surfaced in the summary reconsider card.
- **Accessibility:** swipe is never the only path — visible buttons + keys; reduced
  motion supported; focus-visible outline.

---

## 9. Voice & copy principles

- One growing number = the dopamine. Loss framed **per card**, gain framed **in
  aggregate**.
- Defuse the fear: "still spendable anytime — it just earns until you spend it."
- Never imply guaranteed returns; always "indicative / up to ~6.7% p.a."
- Forgone, not "lost": "You left ₹Z/yr on the table — reconsider?"
