## Documentation


[1] ABOUT THE PROJECT

xmetrics is a weekly analytical AI framework that simulates the decision-making process of a top hedge fund. Every Friday after the US market closes, a snapshot of **100 metrics** on the US market, macroeconomics, credit, sentiment, and options is captured. This dataset is processed by **five virtual analytical agents**, whose reasoning is calibrated to the methodologies of Howard Marks, Stanley Druckenmiller, Aswath Damodaran, Nassim Taleb, and a professional technical analyst. All five reports are then delivered to the **CIO director**, who reviews the agents' outputs, conducts a debate among the agents, and synthesizes the final investment stance.

The engine powering the system is **Anthropic Claude Opus**. The key thing — the system **remembers**. A three-tier memory (short-term, medium-term, long-term) allows the CIO to track predictions, penalize agents whose calls failed, reward those who got it right, dynamically adjust weights, and progressively refine the decision matrix.

The goal of the project is a deeper understanding of the SPX market — what is happening beneath the surface of its price action. Every conclusion is **falsifiable** (each report contains specific hypotheses with a verification date), every weight change is **auditable**, and the entire chain of reasoning is always on display.

```
SCORE SCALE:               1.0 (extreme bear) → 10.0 (extreme bull)
AGENTS:                    5 independent agents + 1 agent (CIO)
METRICS PER ANALYSIS:      ~100
FREQUENCY:                 Weekly (Fridays, post-close)
LEARNING LOOP:             3-tier (weekly / quarterly / cumulative)
FALSIFIABILITY:            Each report contains testable hypotheses
ENGINE:                    Claude Opus (Anthropic)
```

---

[2] WHY THE SYSTEM EXISTS

The ordinary investor is, in their decision-making, dependent on standard information sources. And those have three problems: **methodological one-sidedness** (every analytical framework has blind spots), **narrative inertia** (analysts cling to their earlier views even when the data say something else), and **a lack of accountability** (predictions are not tracked systematically).

xmetrics addresses:

- **Diversification of perspectives.** Five agents reason independently across incompatible frameworks. Value and cycle (Marks), liquidity and money flows (Druckenmiller), intrinsic value (Damodaran), tail risk (Taleb), and price structure (TA) rarely agree by chance. When they converge, the signal is stronger than any single methodology.

- **Contrarian test.** When all five agents point in the same direction, the super-agent must actively formulate a counter-argument. This is not a polite concession — it is a formal step in the pipeline. Consensus is often a warning, not a confirmation.

- **Measured accuracy.** Every prediction comes with triggers and a verification date. Every subsequent report starts with feedback on the previous one. Agents who are repeatedly wrong have their weight reduced. Agents who hit the mark have their weight strengthened. The system is able to learn.

---

[3] SYSTEM ARCHITECTURE

-  D - Weekly Dataset --> 

-  R1: H. Marks - Value & Cycle
-  R2: Druckenmiller - Macro & Liquidity 
-  R3: Damodaran - Valuation DCF
-  R4: Taleb - Tail Risk
-  R5: TA Analyst - Price & GEX 

-  R6: CIO Synthesis (Price & GEX) -->  M (Memory)

---

[4] DATA LAYER — 100 METRICS, ONE SOURCE OF TRUTH

Every Friday the system generates a single canonical dataset — `D_YYYY-MM-DD.csv` — used by all agents. This is intentional: agents must reason from a strictly fixed set of metrics. Any disagreement between them is therefore purely methodological, never informational.

The dataset covers eight functional domains:

```
| Domain                | Representative metrics                                                   |
|-----------------------|--------------------------------------------------------------------------|
| Price and technicals  | SPX_CLOSE, SMA_50, SMA_200, VWAP_ANCHORED, Fib retracement, RSI, MACD, ADX |
| Volume and flow       | VOL_RATIO, OBV_TREND, MFI_14, CMF_20, UP_VOL_PCT_5D                      |
| Breadth and rotation  | SPXA50R, SPXA200R, MAG7_REL, RUT_IWM_REL, XLF/XLE/XLK relative strength  |
| Volatility            | VIX, SKEW, SKEW/VIX ratio, VIX term structure, realized vs. implied      |
| GEX / options         | GEX_FLIP, CALL_WALL, PUT_WALL, GEX_NET_VALUE, GEX_REGIME                 |
| Macro and rates       | FFR, 10Y / 2Y / 3M, M2, RRP, real rates, DXY, gold, oil                  |
| Valuation             | ERP, CAPE, P/E TTM, Forward P/E, Buffett Indicator, HY/IG credit spreads |
| Sentiment and economy | AAII, Margin Debt, CNN F&G, ISM, Consumer Sentiment, NFP, PCE, SLOOS     |
```

Each metric carries three time dimensions: `D-0` (analysis day), `D-1` (previous session), `D-5` (one trading week back). For slower-evolving macro series (monthly PCE, weekly jobless claims), the `D-1` and `D-5` columns are intentionally marked `—`.

**Data completeness is tracked explicitly.** If a critical metric is missing, the super-agent lowers its confidence band and reduces the weight of the affected agent for that session. The system never pretends to have information it does not.

---

[5] AGENT LAYER — FIVE METHODOLOGIES, ONE DATASET

Each agent is a reasoning module, calibrated to reproduce the methodology of a reference analyst. The calibration covers four dimensions:

- **Pillar structure.** The thematic lenses through which the agent slices the data (Marks uses six pillars including Monetary Environment and Cyclical Position; Taleb uses five including Convexity and Systemic Fragility).
- **Pillar weights.** The relative importance of each lens (Damodaran assigns Implied ERP 40% of his total weight; Druckenmiller gives Liquidity and Fed 30%).
- **Trigger language.** The characteristic phrasing, thresholds, and rhetoric of the reference thinker (e.g., Marks's "pendulum" frame for sentiment; Taleb's "fragility" rating of positions).
- **Confidence calibration.** How the agent expresses conviction — Damodaran anchors explicit mathematical sensitivity tables; Marks speaks in ranges and probabilities; Taleb avoids point forecasts.

5A — Agent lineup

```
R1 — HOWARD MARKS              Value, position in the cycle, sentiment pendulum
    Pillars:       Monetary | Valuation | Sentiment | Economy | Credit | Cross-Asset
    Main weight:   Valuation + Credit
    Signature:     "Where are we in the cycle?" — mapping asymmetry

R2 — STANLEY DRUCKENMILLER     Macro liquidity and flows
    Pillars:       Liquidity & Fed | Yield Curve / Credit | Valuation | Sentiment | Cycle | Cross-Asset
    Main weight:   Liquidity 30%
    Signature:     Anticipatory positioning by central-bank liquidity regime

R3 — ASWATH DAMODARAN          Intrinsic value (DCF / ERP)
    Pillars:       Market Valuation | Implied ERP | Macro Environment | Risk Premium
    Main weight:   ERP 40%
    Signature:     Explicit fair-value sensitivity tables; no point forecasts

R4 — NASSIM TALEB              Tail risk, convexity, systemic fragility
    Pillars:       Tail Risk | Convexity & Payoff | Systemic Fragility | Black Swan proximity | Cross-Asset
    Main weight:   Tail structures
    Signature:     Fragility score; barbell positioning; Dual Complacency detection

R5 — TECHNICAL ANALYSIS        Price, momentum, options microstructure
    Pillars:       Trend & Structure | Momentum | Volume & Flow | GEX / Options | Breadth | Macro TA context
    Main weight:   GEX + Breadth
    Signature:     Fibonacci / VWAP confluence; Elliott Wave count; GEX regime

R6 — CIO SUPER-AGENT           Inter-agent synthesis and arbiter
    Pillars:       (Not applicable — works on agent outputs, not raw metrics)
    Main weight:   Dynamic — re-balances agents every session
    Signature:     Confrontational debate; contrarian testing; application of disqualifiers
```

5B — Anatomy of an agent report

Each R1–R5 report has a fixed structure:

```
[1] EXECUTIVE SUMMARY        — Score, cycle phase, asymmetry, stance, primary trigger
[2] DATASET — VALUES READ    — Explicit restatement of the input data used
[3] PILLAR ANALYSIS          — In-depth breakdown of each thematic pillar (score 1–10)
[4] SYNTHETIC DECISION MATRIX — Weighted score, signal consistency, R/R
[5] AGENT CONCLUSION         — Position, change triggers, allocation breakdown
[6] AI LEARNING METADATA     — Falsifiable hypotheses, trigger events, feedback loop
```

Section `[6]` is not cosmetic. It is a **machine-readable contract** between this report and the next. Every hypothesis stated here will be evaluated in the feedback section of the following session.

5C — Continuity with previous reports

Each agent receives not only the current dataset, but also **its own previous report** (plus the super-agent's previous verdict). Before producing this analysis, the agent must:

1. Read its earlier call.
2. Assess how the market evolved relative to its triggers.
3. Identify what it got right and what it missed.
4. Explicitly state which stances are now upgraded, downgraded, or unchanged.

This produces **continuity of thinking without dependence on the previous direction**. The agent can reverse its position — but only if it admits the mistake and explains what new information changed the view.

---

[6] CIO LAYER — ARBITER, DEBATE, AND VERDICT

The super-agent processes the five reports + the raw dataset and produces `R6_YYYY-MM-DD.md`. This is where the system gains its value. A naive average of the five scores would be worthless. The CIO does four things no single agent can:

6A — Detection of shared data vs. independent signal

R1 (Marks) and R2 (Druckenmiller) share approximately 85% of their data base (both are macro-oriented). If they agree, that agreement weighs roughly **1.2×** one agent — not 2× independent confirmation. The CIO applies an overlap correction (typically −0.07 to the final score) whenever these two point in the same direction. This prevents the system from double-counting what is essentially one methodology read in two ways.

The truly independent methodologies in the lineup: R3 (pure valuation math), R4 (fragility / payoff geometry), R5 (price and options structure). When any of these independently confirms R1+R2, the signal earns real cross-methodological weight.

6B — Confrontational debate

When the agents disagree — or when they all agree and a contrarian test is required — the CIO simulates an explicit debate:

```
CONFRONTATION 1 — Valuation (R3) vs. Technical structure (R5)
  R3 POSITION:      CAPE fair value = 3,012–3,897 → SPX overvalued by 45–58%
  DIRECT CHALLENGE: R5 — GEX +2.00G, Market Makers sell rallies / buy dips → mechanical floor
  R6 VERDICT:       Both are right on different horizons. R3 = magnitude and direction.
                    R5 = the timing mechanism delaying the turn. Synthesis: a break
                    of GEX Flip 7,000 releases the accumulated compression non-linearly.
```

Each confrontation is resolved by an explicit **dominant framework assignment** — which methodology governs timing, which magnitude, and under what conditions that assignment would flip.

6C — Application of disqualifiers

Some conditions are strong enough to **override agent-level scores regardless of consensus**. These are the system's hard safety rails:


```
| Disqualifier                 | Trigger                                    | Impact                                          |
|------------------------------|--------------------------------------------|-------------------------------------------------|
| BREADTH_COLLAPSE             | SPXA200R < 30% AND falling                 | R6 score −1.5 (after haircut from R5 floor: −0.75) |
| BREADTH_ALERT                | SPXA200R < 20%                             | R5 score −1.0 additionally                      |
| ETF_DISQ_R6                  | 3-of-3 mega-cap rally concentration        | R6 score −1.0 (after haircut: −0.5)             |
| VIX_BACKWARDATION            | VIX term structure < 0                     | Absolute disqualification of long positions     |
| SKEW_VIX_>7                  | SKEW/VIX ratio > 7.0                       | Modifier −0.30                                  |
| DUAL_COMPLACENCY-ERP         | ERP < 0% AND VIX < 15 (simultaneously)     | R6 score −1.0; R4 weight +20%                   |
| TOPPING_ALERT                | EW Wave 5 + RSI_DIV + DELTA_MACD falling   | Score −0.5                                      |

```

Disqualifiers are listed explicitly in every R6 report — you always see which rails were active.

6D — Re-balancing of agent weights

The base weights are not fixed. **They are modified every session** based on two factors:

1. **Market regime.** If ERP is negative (Dual Complacency), Taleb's tail-risk weight is boosted. If the volatility structure signals a GEX-dominated regime, TA is boosted. If credit is under stress, Druckenmiller is boosted.
2. **Historical accuracy.** Agents whose previous predictions verified have their weight in that session multiplied by **1.05×**; agents whose predictions failed two times in a row have their weight multiplied by **0.90×**. This is the long-memory learning loop in practice.

Every weight adjustment is logged in section `[8B] — Weights Used in This Report` and is therefore fully auditable.

---

[7] MEMORY ARCHITECTURE

Most AI analytical systems are stateless. xmetrics intentionally is not. It operates on three timescales:

```
┌─────────────────────────────────────────────────────────────────┐
│  SHORT-TERM MEMORY        (1 week)                              │
│  ─────────────────────────────────────                          │
│  Each agent reads its own previous report. Each CIO             │
│  verdict references the previous R6 report. Continuity is       │
│  mandatory — an agent reversing its view must explicitly        │
│  acknowledge and justify that reversal.                         │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  MEDIUM-TERM MEMORY       (quarterly, 12–13 reports)            │
│  ─────────────────────────────────────                          │
│  The CIO tracks the hit rate on every falsifiable hypothesis.   │
│  Quarterly weight recalibration. Identification of regime       │
│  shifts that render past weights obsolete. Detection of agents  │
│  who are systematically early or late.                          │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  LONG-TERM MEMORY         (cumulative, all sessions)            │
│  ─────────────────────────────────────                          │
│  Full history of every prediction, outcome, and weight change.  │
│  Drives structural revisions: new metrics (e.g., SPXA50R was    │
│  promoted to mandatory after the April 2026 session),           │
│  refinement of disqualifier thresholds, expansion of            │
│  confrontation templates, potentially new agents.               │
└─────────────────────────────────────────────────────────────────┘
```

---

[8] OUTPUT QUALITY — WHAT YOU CONCRETELY GET

A complete weekly session produces seven artifacts:

```
reports/YYYY-MM-DD/
├── D_YYYY-MM-DD.csv       ~100 metrics, three time dimensions, explicit units
├── R1_YYYY-MM-DD.md       Howard Marks report (~14–18 KB)
├── R2_YYYY-MM-DD.md       Druckenmiller report (~11–15 KB)
├── R3_YYYY-MM-DD.md       Damodaran report (~12–14 KB)
├── R4_YYYY-MM-DD.md       Taleb report (~15–17 KB)
├── R5_YYYY-MM-DD.md       Technical analyst report (~26–30 KB)
└── R6_YYYY-MM-DD.md       CIO synthesis (~30–35 KB)
```

Total output per session: **approximately 120–140 KB of structured analysis**, broken down by domain, cross-checked against five incompatible frameworks, and synthesized into a single actionable verdict with explicit triggers.

For comparison: a typical weekly market wrap from a major bank has 8–15 KB of text with no falsifiable claims, no scoring, and no methodology transparency. Institutional buy-side research is longer but rarely reveals its own weighting logic. xmetrics does both, every week, for every session — and it is publicly accessible.

> **Note for retail investors:** Reports R1–R6 are in English. This is intentional — we use precise terminology from the investment world that many translations would dilute. This documentation and the metrics reference are provided for context. 

---

[9] LEARNING SYSTEM

Each report ends with section `[6]` or `[8]` containing a block of falsifiable hypotheses:

```
H1 (Breadth + Cycle):
  SPX does not hold an ATH for more than 3 weeks with SPXA50R <15%
  → by 2026-05-10 SPX below 7,000
  Verification: SPX close + SPXA50R on 2026-05-10

H2 (Liquidity + TA):
  Bear steepener + GEX Flip proximity
  → 10Y reaches 4.6% by 2026-05-15 and SPX corrects by −5 to −10%
  Verification: 10Y yield + SPX on 2026-05-15
```

On 2026-05-15 the next weekly report opens with:

```
H1: VERIFIED / FAILED / PARTIALLY VERIFIED
H2: VERIFIED / FAILED / PARTIALLY VERIFIED
```

And the weights adjust accordingly. Over time this produces a **public per-agent accuracy record** — Marks's hit rate, Druckenmiller's hit rate, the system's aggregate hit rate. Institutional research does not publish this. xmetrics does, because transparency is the only way the system can justify the weights it assigns to itself.

---

[10] WHO IT IS BUILT FOR

xmetrics is built for three types of users:

- **Investors** who hold an ETF core in their portfolio and actively think about risk. Who want to understand what is going on, not just buy ETFs on someone's recommendation. Who have years or decades of investing ahead of them and know that 50 viral moments are worth less than 52 weeks of consistent thinking.

- **Students** who want to see how incompatible methodologies actually reason about the same data, how disagreements are resolved, and what a disciplined scoring framework looks like in practice. This is an educational tool — explicitly.

- **People who lack a second opinion.** Single-analyst research carries structural weaknesses (one-sidedness, narrative inertia). Having five independent methodologies available at once, plus a historical audit trail, is something an ordinary investor will not get from the media.

xmetrics is **not** built for day traders, options scalpers, or anyone looking for intraday signals. The cadence is weekly by design. Market structure shifts on this timescale; on shorter ones, noise dominates.

---

[11] HOW TO READ A REPORT

Recommended reading order of a weekly session:

1. **Open `R6_YYYY-MM-DD.md`.** Read section `[1]` (CIO verdict) and `[2]` (feedback on the previous prediction).
2. **Check the list of disqualifiers** in the Executive Summary. Any active disqualifier overrides agent-level scores — you need to know which rails are active before reading on.
3. **Read section `[3A]` — Agent Dashboard.** A one-line summary per agent. This tells you where the consensus is and where the dissent.
4. **If the consensus is 5/5, jump to the Contrarian Test.** This is the CIO's active attempt to falsify the consensus. If the test produces strong evidence, the verdict is upgraded to higher confidence.
5. **Read section `[4] — Confrontational Debate`**. Each confrontation produces a dominant framework assignment (timing vs. magnitude).
6. **Jump to section `[8] — AI Learning Metadata`.** The hypotheses tell you exactly what the system is predicting and how it will score itself next week.
7. **Only then**, if you want deeper detail, open the individual R1–R5 agent reports.

Reading in this order takes ~15 minutes and captures 90% of the actionable content.


---

[12] METHODOLOGY — SCORING AND WEIGHTS

12A — Pillar scoring (scale 1–10)

Each pillar in each agent's report is scored on a uniform 1–10 scale with the following semantics:

```
1.0 – 2.5    Extremely bearish / serious dysfunction / major structural warning
2.6 – 4.0    Bearish / unfavorable / elevated risk
4.1 – 6.0    Neutral / mixed signals / no clear edge
6.1 – 7.5    Bullish / favorable / supportive conditions
7.6 – 10.0   Extremely bullish / strong structural tailwind / low risk
```

The agent's overall score is the weighted sum of pillar scores using that agent's weights.

12B — CIO weighted aggregation

```
SYSTEM_SCORE = Σ ( agent_score_i × agent_weight_i ) + modifiers
where:
  agent_weight_i  = base_weight_i × regime_modifier_i × accuracy_modifier_i
  Σ agent_weight_i  = 100% (normalized after modifiers)
  modifiers       = SKEW_VIX_mod + sentiment_mod + overlap_correction
```

Base weights (before modifiers):
```
  R1 Marks          20%
  R2 Druckenmiller  25%
  R3 Damodaran      20%
  R4 Taleb          20%
  R5 TA             15%
```

12C — Probabilistic distribution

Each R6 report provides three probability-weighted scenarios:

```
P_BULL   — probability weight of the bullish case, with a 4-week target range
P_BASE   — probability weight of the base case, with a 4-week range
P_BEAR   — probability weight of the bearish case, with a 4-week range

Σ P = 100%
```

These are calibrated, not marketing. A report with P_BEAR = 40% does not mean "I am 40% convinced of the bear scenario" — it means "in 40 comparable historical setups, this outcome occurred roughly eighteen times."

---

[13] GLOSSARY

Key terminology across the xmetrics reports. The scope expands as new concepts enter.

| **ERP**                      | Equity Risk Premium — the premium investors demand over the risk-free rate for holding equities    |
| **Naive ERP**                | Proxy calculation: earnings yield (1 / P/E) minus the 10-year Treasury yield                       |
| **CAPE**                     | Cyclically-Adjusted P/E (Shiller P/E) — price ÷ 10-year average of inflation-adjusted earnings     |
| **GEX**                      | Gamma Exposure — a metric of options market structure capturing Market Maker hedging               |
| **GEX Flip**                 | The price level where net GEX flips negative; below this point MM hedging amplifies moves          |
| **GEX Regime POSITIVE**      | MMs are long gamma → sell rallies, buy dips → dampen volatility                                    |
| **GEX Regime NEGATIVE**      | MMs are short gamma → sell dips, buy rallies → amplify volatility                                  |
| **Call Wall / Put Wall**     | Strikes with the highest concentration of gamma exposure — act as support/resistance               |
| **VIX**                      | CBOE 30-day implied volatility from SPX options                                                    |
| **VIX term structure**       | Spread between longer (VIX3M) and spot VIX. Positive = contango (normal), negative = backwardation (stress) |
| **SKEW**                     | CBOE SKEW Index measuring the cost of insurance against tail risk in SPX options                  |
| **SKEW/VIX Ratio**           | Ratio of SKEW to VIX. > 7.0 indicates calm on the surface with institutional tail hedging beneath  |
| **RRP**                      | Reverse Repo Program — Fed facility that drains systemic liquidity as the balance falls            |
| **M2**                       | Broad measure of US money supply                                                                   |
| **FFR / Real FFR**           | Federal Funds Rate / FFR adjusted for inflation expectations                                       |
| **Bear Steepener**           | Steepening of the yield curve driven by rising long-dated yields (unfavorable for equities)        |
| **Bull Steepener**           | Steepening of the yield curve driven by falling short-dated yields (typically Fed easing)          |
| **PCR**                      | Put/Call Ratio                                                                                     |
| **HY / IG**                  | High-Yield / Investment-Grade credit spreads over Treasuries                                       |
| **SLOOS**                    | Senior Loan Officer Opinion Survey — quarterly Fed survey on lending standards                     |
| **CC Delinquency**           | Credit card delinquency rate — an indicator of consumer credit stress                              |
| **Buffett Indicator**        | Total US market capitalization ÷ GDP. Historically a preferred valuation metric                    |
| **SPXA50R / SPXA200R**       | % of SPX constituents above their 50-day / 200-day moving average                                  |
| **Breadth Collapse**         | Formal disqualifier — SPXA200R below 30% AND falling                                               |
| **Breadth Critical Divergence** | SPXA50R below 15% while SPX is at or near ATH — early warning signal                            |
| **Dual Complacency**         | Simultaneous occurrence of negative ERP + elevated SKEW/VIX — triggers a boost to R4's weight      |
| **VPVR / POC**               | Volume Profile Visible Range / Point of Control — the price level with the most traded volume     |
| **VWAP (Anchored)**          | Volume-Weighted Average Price anchored to a specific reference event                               |
| **Fibonacci Retracement**    | Classic TA levels at 38.2% / 50.0% / 61.8% of the previous swing                                   |
| **RSI-14**                   | Relative Strength Index over 14 periods — a momentum oscillator (0–100)                            |
| **ADX-14**                   | Average Directional Index — a measure of trend strength (directionally neutral)                    |
| **Stoch RSI**                | Stochastic RSI — RSI normalized to its own recent range                                            |
| **MACD Histogram**           | Moving Average Convergence Divergence difference — a momentum indicator                            |
| **OBV**                      | On-Balance Volume — cumulative volume flow                                                         |
| **MFI-14 / CMF-20**          | Money Flow Index / Chaikin Money Flow — volume-weighted momentum                                   |
| **Elliott Wave**             | A wave-count framework identifying impulse (IMP) and corrective (COR) structures                   |
| **Fragility Score**          | Taleb's 1–10 scale where 1 = maximally fragile, 10 = robust/antifragile                            |
| **Barbell Positioning**      | Taleb's strategy — concentrate exposure at the extremes, avoid the middle                          |
| **Disqualifier**             | A hard rule overriding the aggregated score when triggered                                         |
| **Nonlinearity Multiplier**  | CIO estimate of how much a typical signal would be amplified by current market structure           |
| **Falsifiable hypothesis**   | An explicit prediction with a verification date and a binary outcome — "H1: X by Y"                |
| **Contrarian Test**          | A mandatory CIO step in case of 5/5 consensus — actively attempts to falsify the consensus          |
| **Overlap Correction**       | A CIO adjustment applied when two agents share >80% of their data base                             |
| **Regime Modifier**          | A dynamic weight adjustment based on the current market regime (e.g., ERP negative → R4 boost)     |
| **Accuracy Modifier**        | A dynamic weight adjustment based on the recent hypothesis track record of the given agent         |
| **Disqualifier Haircut**     | R6 system rule — disqualifiers applied in the R5 score floor are applied at R6 with a 0.5× haircut |
| **RRP Data Discontinuity**   | If the RRP w/w change > 200%, the signal is PAUSED and substituted by M2_YOY decel + 2Y w/w move   |
| **Gamma-regime Suspension**  | R5 does not report a 1W directional prediction under GEX_REGIME POSITIVE with NET > +1.0G; structural reading continues |

---

[14] SYSTEM INTEGRITY — WHAT THE SYSTEM DOES NOT DO

In the interest of intellectual honesty, it is just as important to document the boundaries as it is to document the capabilities:

- **It does not provide intraday signals.** The cadence is weekly. Anything faster is noise relative to the macro framework.
- **It does not execute trades.** It produces analysis, not orders. Position sizing is guidance — execution is the reader's responsibility.
- **It does not predict individual stock prices.** The scope is the index (SPX) and major sector rotation. Single-name analysis is out of scope.
- **It does not guarantee a hit rate.** Falsifiable hypotheses will fail. The learning loop exists precisely because prediction is difficult — the system gains its edge by correcting itself faster than the alternatives, not by hitting more often in absolute numbers.
- **It does not replace a portfolio manager.** Human judgment on position sizing, portfolio context, and risk tolerance remains essential. xmetrics is a decision-support tool of unusual depth — not a decision-making tool.
- **It is not investment advice.** xmetrics is not a broker and not a regulated financial institution. All content is for education, not as a recommendation to buy/sell. For investment decisions, consult a licensed advisor.

---

[15] FRAMEWORK CHANGES

Structural changes to the framework — new metrics, modified disqualifier thresholds, new agents, adjusted base weights — are documented. Changes propagate into subsequent reports automatically and their rationale is traceable in section `[10B] Patterns` of the R6 report, where every pattern has its own `STATUS` (ACTIVE / MONITORING / PAUSED / RETIRED).

---

*End of xmetrics documentation. For methodological questions beyond this document, refer to the individual agent reports, which contain detailed examples of each framework in action. The glossary in [13] explains the English terminology used in reports R1–R6.*
