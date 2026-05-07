## Multiagentní analýza S&P 500

Dokumentace systému xmetrics — jak to funguje, proč to existuje a co z toho má drobný investor.

---

[1] STRUČNĚ O ČEM TO JE

xmetrics je týdenní analytický nástroj, který simuluje rozhodovací proces top hedge fondu. Každý pátek po uzavření amerického trhu je zachycen snímek **100 metrik** o trhu, makroekonomice, kreditu, sentimentu a opcích. Tento dataset projde **pěti virtuálními analytickými agenty**, jejichž uvažování je kalibrováno podle metodologií Howarda Markse, Stanleyho Druckenmillera, Aswatha Damodarana, Nassima Taleba a profesionálního technického analytika. Všech pět reportů pak dostane **CIO ředitel**, který je posuzuje, vede mezi agenty debatu a syntetizuje finální investiční postoj.

Engine pohánějící systém je **Anthropic Claude Opus**. Klíčová věc — systém si **pamatuje**. Tříúrovňová paměť (krátkodobá, střednědobá, dlouhodobá) umožňuje CIO sledovat každou minulou predikci, penalizovat agenty, jejichž volání selhala, posilovat ty, kteří se trefili, dynamicky upravovat váhy a postupně zpřesňovat rozhodovací matici.

Cílem není konkurovat institucím. Cílem je dát drobnému investorovi framework, pro hlubší porozumění, co se děje pod povrchem trhu SPX. Každý závěr je **falsifikovatelný** (každý report obsahuje konkrétní hypotézy s datem ověření), každá změna vah je **auditovatelná** a celý řetězec uvažování je vždy vystaven.


```
ŠKÁLA SKÓRE:               1.0 (extrémní bear) → 10.0 (extrémní bull)
AGENTI:                    5 nezávislých agentů + 1 agent (CIO)
METRIK NA ANALÝZU:         ~100
FREKVENCE:                 Týdně (pátky, po uzávěru)
UČÍCÍ SMYČKA:              3-úrovňová (týdně / kvartálně / kumulativně)
FALSIFIKOVATELNOST:        Každý report obsahuje testovatelné hypotézy
ENGINE:                    Claude Opus (Anthropic)
```

---

[2] PROČ TENHLE SYSTÉM EXISTUJE

Před dvěma lety jsem se ztratil mezi „kup a drž" strategií a aktivním rozhodováním o riziku. Standardní zdroje pro drobné investory mají tři problémy: **metodologickou jednostrannost** (každý analytický framework má slepá místa), **narativní setrvačnost** (analytici drží své dřívější názory i když data říkají něco jiného) a **chybějící zodpovědnost** (predikce se nesledují systematicky).

xmetrics řeší všechny tři:

- **Diverzifikace pohledů.** Pět agentů uvažuje nezávisle přes neslučitelné frameworky. Hodnota a cyklus (Marks), likvidita a peněžní toky (Druckenmiller), vnitřní hodnota (Damodaran), tail risk (Taleb) a cenová struktura (TA) se zřídka shodnou náhodou. Když konvergují, signál je silnější než kterákoliv jednotlivá metodologie.

- **Contrarian test.** Když všech pět agentů ukazuje stejným směrem, super-agent musí aktivně formulovat protiargument. Není to zdvořilý ústupek — je to formální krok v pipeline. Konsenzus je často varování, ne potvrzení.

- **Měřená přesnost.** Každá predikce přichází s triggery a datem ověření. Každý další report začíná zpětnou vazbou na ten předchozí. Agenti, kteří se opakovaně mýlí, mají sníženou váhu. Agenti, kteří se trefují, mají váhu posílenou. Systém se učí — a vidíte to.

---

[3] ARCHITEKTURA SYSTÉMU

Schéma níže ukazuje tok dat od surových metrik k finálnímu CIO verdiktu.

<img src="img/https://xmetrics.dev/img/str-xmetrics.svg" alt="xmetrics architektura" width="600">

---

[4] DATOVÁ VRSTVA — 100 METRIK, JEDEN ZDROJ PRAVDY

Každý pátek systém vygeneruje jediný kanonický dataset — `D_YYYY-MM-DD.csv` — který konzumují všichni agenti. To je záměrně: agenti musí uvažovat na základě striktně daných metrik. Jakákoli neshoda mezi nimi je tedy čistě metodologická, nikdy informační.

Dataset pokrývá osm funkčních domén:

```
| Doména                | Reprezentativní metriky                                                  |
|-----------------------|--------------------------------------------------------------------------|
| Cena a technika       | SPX_CLOSE, SMA_50, SMA_200, VWAP_ANCHORED, Fib retracement, RSI, MACD, ADX |
| Objem a flow          | VOL_RATIO, OBV_TREND, MFI_14, CMF_20, UP_VOL_PCT_5D                      |
| Šíře a rotace         | SPXA50R, SPXA200R, MAG7_REL, RUT_IWM_REL, XLF/XLE/XLK relativní síla     |
| Volatilita            | VIX, SKEW, SKEW/VIX ratio, VIX termová struktura, realizovaná vs. implied |
| GEX / opce            | GEX_FLIP, CALL_WALL, PUT_WALL, GEX_NET_VALUE, GEX_REGIME                 |
| Makro a sazby         | FFR, 10Y / 2Y / 3M, M2, RRP, reálné sazby, DXY, zlato, ropa              |
| Valuace               | ERP, CAPE, P/E TTM, Forward P/E, Buffett Indicator, HY/IG credit spreads |
| Sentiment a ekonomika | AAII, Margin Debt, CNN F&G, ISM, Consumer Sentiment, NFP, PCE, SLOOS     |
```

Každá metrika nese tři časové dimenze: `D-0` (den analýzy), `D-1` (předchozí session), `D-5` (jeden obchodní týden zpět). U pomaleji se vyvíjejících makro řad (měsíční PCE, týdenní jobless claims) jsou sloupce `D-1` a `D-5` záměrně označeny `—`.

**Datová úplnost je sledována explicitně.** Pokud chybí kritická metrika, super-agent sníží svoje confidence pásmo a sníží váhu dotčenému agentovi pro danou session. Systém nikdy nepředstírá, že má informaci, kterou nemá.

---

[5] AGENTNÍ VRSTVA — PĚT METODOLOGIÍ, JEDEN DATASET

Každý agent je modul uvažování, kalibrovaný k reprodukci metodologie referenčního analytika. Kalibrace pokrývá čtyři dimenze:

- **Pilířová struktura.** Tematické čočky, kterými agent krájí data (Marks používá šest pilířů včetně Monetárního prostředí a Cyklické pozice; Taleb používá pět včetně Konvexity a Systémové fragility).
- **Váhy pilířů.** Relativní důležitost každé čočky (Damodaran má Implied ERP 40 % své celkové váhy; Druckenmiller má Likviditu a Fed 30 %).
- **Trigger jazyk.** Charakteristické vyjadřování, prahy a rétorika referenčního myslitele (např. Marksův „kyvadlový" frame sentimentu; Talebovo „fragility" hodnocení pozic).
- **Kalibrace jistoty.** Jak agent vyjadřuje míru přesvědčení — Damodaran kotví explicitní matematické sensitivity tabulky; Marks mluví v rozpětích a pravděpodobnostech; Taleb se vyhýbá bodovým prognózám.

5A — Sestava agentů

```
R1 — HOWARD MARKS              Hodnota, pozice v cyklu, kyvadlo sentimentu
    Pilíře:       Monetární | Valuace | Sentiment | Ekonomika | Kredit | Cross-Asset
    Hlavní váha:  Valuace + Kredit
    Podpis:       „Kde jsme v cyklu?" — mapování asymetrie

R2 — STANLEY DRUCKENMILLER     Makro likvidita a flow
    Pilíře:       Likvidita & Fed | Yield Curve / Kredit | Valuace | Sentiment | Cyklus | Cross-Asset
    Hlavní váha:  Likvidita 30 %
    Podpis:       Anticipativní pozicování podle režimu likvidity centrálních bank

R3 — ASWATH DAMODARAN          Vnitřní hodnota (DCF / ERP)
    Pilíře:       Tržní oceňování | Implied ERP | Makro prostředí | Risk Premium
    Hlavní váha:  ERP 40 %
    Podpis:       Explicitní fair-value sensitivity tabulky; žádné bodové prognózy

R4 — NASSIM TALEB              Tail risk, konvexita, systémová fragilita
    Pilíře:       Tail Risk | Konvexita & Payoff | Systémová fragilita | Black Swan blízkost | Cross-Asset
    Hlavní váha:  Tail struktury
    Podpis:       Fragility skóre; barbell pozicování; detekce Dual Complacency

R5 — TECHNICKÁ ANALÝZA         Cena, momentum, mikrostruktura opcí
    Pilíře:       Trend & Struktura | Momentum | Volume & Flow | GEX / Opce | Šíře | Makro TA kontext
    Hlavní váha:  GEX + Šíře
    Podpis:       Fibonacci / VWAP konfluence; Elliott Wave count; GEX režim

R6 — CIO SUPER-AGENT           Mezi-agentní syntéza a rozhodčí
    Pilíře:       (Neaplikovatelné — pracuje na výstupech agentů, ne na surových metrikách)
    Hlavní váha:  Dynamická — re-balancuje agenty každou session
    Podpis:       Konfrontační debata; contrarian testing; aplikace disqualifierů
```

5B — Anatomie reportu agenta

Každý report R1–R5 má pevnou strukturu:

```
[1] EXECUTIVE SUMMARY        — Skóre, fáze cyklu, asymetrie, postoj, primární trigger
[2] DATASET — VALUES READ    — Explicitní zopakování použitých vstupních dat
[3] PILLAR ANALYSIS          — Hloubkový rozbor každého tematického pilíře (skóre 1–10)
[4] SYNTHETIC DECISION MATRIX — Vážené skóre, konzistence signálů, R/R
[5] AGENT CONCLUSION         — Pozice, triggery změny, allocation breakdown
[6] AI LEARNING METADATA     — Falsifikovatelné hypotézy, trigger události, feedback smyčka
```

Sekce `[6]` není kosmetická. Je to **strojově čitelná smlouva** mezi tímto reportem a tím dalším. Každá hypotéza zde uvedená bude vyhodnocena ve zpětné vazbě další session.

5C — Návaznost na předchozí reporty

Každý agent dostane nejen aktuální dataset, ale také **svůj vlastní předchozí report** (plus předchozí verdikt super-agenta). Před vytvořením této analýzy musí agent:

1. Přečíst své dřívější volání.
2. Posoudit, jak se trh vyvinul vůči jeho triggerům.
3. Identifikovat, co se trefilo a co minul.
4. Explicitně uvést, které postoje jsou nyní upgrade, downgrade nebo beze změny.

Tím vzniká **kontinuita myšlení bez závislosti na minulém směru**. Agent může své stanovisko obrátit — ale jen pokud přizná chybu a vysvětlí, jaká nová informace pohled změnila.

---

[6] CIO VRSTVA — ROZHODČÍ, DEBATA A VERDIKT

Super-agent zpracuje pět reportů + surový dataset a vyprodukuje `R6_YYYY-MM-DD.md`. Tady systém získává svou hodnotu. Naivní průměr pěti skóre by byl bez hodnoty. CIO dělá čtyři věci, které žádný jednotlivý agent dělat nemůže:

6A — Detekce sdílených dat vs. nezávislého signálu

R1 (Marks) a R2 (Druckenmiller) sdílejí přibližně 85 % své datové báze (oba jsou makro-orientovaní). Pokud souhlasí, ta shoda váží zhruba **1,2×** jednoho agenta — ne 2× nezávislé potvrzení. CIO aplikuje korekci překryvu (typicky −0,07 na finální skóre), kdykoli tito dva směřují stejným směrem. To brání systému dvojitě započítat to, co je v podstatě jedna metodologie čtená dvěma způsoby.

Skutečně nezávislé metodologie v sestavě: R3 (čistá valuační matematika), R4 (fragilita / geometrie payoffů), R5 (cena a struktura opcí). Když některá z nich nezávisle potvrdí R1+R2, signál získá skutečnou cross-metodologickou váhu.

6B — Konfrontační debata

Když agenti nesouhlasí — nebo když všichni souhlasí a je vyžadován contrarian test — CIO simuluje explicitní debatu:

```
KONFRONTACE 1 — Valuace (R3) vs. Technická struktura (R5)
  POZICE R3:        CAPE fair value = 3 012–3 897 → SPX nadhodnocen 45–58 %
  PŘÍMÁ VÝZVA:      R5 — GEX +2,00G, Market Makers prodávají rally / kupují poklesy → mechanická podlaha
  R6 VERDIKT:       Oba mají pravdu na různých horizontech. R3 = velikost a směr.
                    R5 = časový mechanismus odkládající obrat. Syntéza: prolomení
                    GEX Flip 7 000 uvolní nahromaděnou kompresi nelineárně.
```

Každá konfrontace je rozřešena explicitním **přiřazením dominantního frameworku** — která metodologie řídí časování, která velikost, a za jakých podmínek by se to přiřazení obrátilo.

6C — Aplikace disqualifierů

Některé podmínky jsou dostatečně silné, aby **přepsaly skóre na úrovni agentů bez ohledu na konsenzus**. To jsou tvrdé bezpečnostní rails systému:


```
| Disqualifier                 | Trigger                                    | Dopad                                          |
|------------------------------|--------------------------------------------|------------------------------------------------|
| BREADTH_COLLAPSE             | SPXA200R < 30 % AND klesá                  | Skóre R6 −1,5 (po haircutu z R5 floor: −0,75)  |
| BREADTH_ALERT                | SPXA200R < 20 %                            | Skóre R5 −1,0 přídavně                         |
| ETF_DISQ_R6                  | 3-of-3 koncentrace mega-cap rally          | Skóre R6 −1,0 (po haircutu: −0,5)              |
| VIX_BACKWARDATION            | VIX termová struktura < 0                  | Absolutní disqualifikace dlouhých pozic        |
| SKEW_VIX_>7                  | SKEW/VIX ratio > 7,0                       | Modifier −0,30                                 |
| DUAL_COMPLACENCY-ERP         | ERP < 0 % AND VIX < 15 (oba současně)      | Skóre R6 −1,0; R4 váha +20 %                   |
| TOPPING_ALERT                | EW Wave 5 + RSI_DIV + DELTA_MACD klesající | Skóre −0,5                                     |

```

Disqualifiers jsou v každém R6 reportu uvedeny explicitně — vždy vidíte, které rails byly aktivní.

6D — Re-balance vah agentů

Základní váhy nejsou pevné. **Modifikují se každou session** podle dvou faktorů:

1. **Tržní režim.** Pokud je ERP záporné (Dual Complacency), tail-risk váha Taleba se posiluje. Pokud volatilní struktura signalizuje GEX-dominovaný režim, posiluje se TA. Pokud je kredit pod stresem, posiluje se Druckenmiller.
2. **Historická přesnost.** Agenti, jejichž předchozí predikce ověřily, mají váhu v té session vynásobenou **1,05×**; agenti, jejichž predikce dvakrát po sobě selhaly, mají váhu vynásobenou **0,90×**. Tady je dlouhopaměťová učící smyčka v praxi.

Každá úprava váhy je zalogována v sekci `[8B] — Weights Used in This Report` a je tedy plně auditovatelná.

---

[7] PAMĚŤOVÁ ARCHITEKTURA

Většina AI analytických systémů je bezstavová. xmetrics záměrně není. Pracuje na třech časových škálách:

```
┌─────────────────────────────────────────────────────────────────┐
│  KRÁTKODOBÁ PAMĚŤ        (1 týden)                              │
│  ─────────────────────────────────────                          │
│  Každý agent čte svůj vlastní předchozí report. Každý CIO       │
│  verdikt odkazuje na předchozí R6 report. Kontinuita je         │
│  povinná — agent, který obrací názor, musí tu reverzaci         │
│  explicitně přiznat a zdůvodnit.                                │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  STŘEDNĚDOBÁ PAMĚŤ       (kvartálně, 12–13 reportů)             │
│  ─────────────────────────────────────                          │
│  CIO sleduje hit rate na každé falsifikovatelné hypotéze.       │
│  Kvartální rekalibrace vah. Identifikace změn režimu, které     │
│  způsobí zastarání minulých vah. Detekce agentů, kteří jsou     │
│  systematicky brzy nebo pozdě.                                  │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  DLOUHODOBÁ PAMĚŤ        (kumulativně, všechny session)         │
│  ─────────────────────────────────────                          │
│  Plná historie každé predikce, výsledku a změny vah.            │
│  Pohání strukturální revize: nové metriky (např. SPXA50R bylo   │
│  povýšeno na povinné po dubnové session 2026), zpřesnění prahů  │
│  disqualifierů, rozšíření šablon konfrontací, potenciálně noví  │
│  agenti.                                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

[8] VÝSTUPNÍ KVALITA — CO KONKRÉTNĚ DOSTANETE

Kompletní týdenní session produkuje sedm artefaktů:

```
reports/YYYY-MM-DD/
├── D_YYYY-MM-DD.csv       ~100 metrik, tři časové dimenze, explicitní jednotky
├── R1_YYYY-MM-DD.md       Howard Marks report (~14–18 KB)
├── R2_YYYY-MM-DD.md       Druckenmiller report (~11–15 KB)
├── R3_YYYY-MM-DD.md       Damodaran report (~12–14 KB)
├── R4_YYYY-MM-DD.md       Taleb report (~15–17 KB)
├── R5_YYYY-MM-DD.md       Technický analytik report (~26–30 KB)
└── R6_YYYY-MM-DD.md       CIO syntéza (~30–35 KB)
```

Celkový výstup na session: **přibližně 120–140 KB strukturované analýzy**, rozčleněné podle domény, prokřížené s pěti neslučitelnými frameworky a syntetizované do jediného akčního verdiktu s explicitními triggery.

Pro srovnání: typický týdenní market wrap od velké banky má 8–15 KB textu bez falsifikovatelných tvrzení, bez skórování a bez transparentnosti metodologie. Institucionální buy-side research je delší, ale málokdy odhaluje vlastní vážicí logiku. xmetrics dělá obojí, každý týden, pro každou session — a je veřejně přístupný.

> **Poznámka pro drobné investory:** Reporty R1–R6 jsou v angličtině. To je záměrně — používáme přesnou terminologii z investičního světa, kterou mnohé české překlady oslabí. Tato dokumentace a metriky jsou v češtině pro pochopení kontextu. Pokud potřebujete terminologii vysvětlit, podívejte se do glossáře v sekci [13].

---

[9] SYSTÉM SE UČÍ VEŘEJNĚ

Každý report končí sekcí `[6]` nebo `[8]` obsahující blok falsifikovatelných hypotéz:

```
H1 (Šíře + Cyklus):
  SPX nedrží ATH déle než 3 týdny při SPXA50R <15 %
  → do 2026-05-10 SPX pod 7 000
  Verifikace: SPX close + SPXA50R na 2026-05-10

H2 (Likvidita + TA):
  Bear steepener + GEX Flip blízkost
  → 10Y dosahuje 4,6 % do 2026-05-15 a SPX koriguje −5 až −10 %
  Verifikace: 10Y yield + SPX na 2026-05-15
```

Na 2026-05-15 další týdenní report otevírá:

```
H1: VERIFIED / FAILED / PARTIALLY VERIFIED
H2: VERIFIED / FAILED / PARTIALLY VERIFIED
```

A váhy se odpovídajícím způsobem upraví. Postupem času toto produkuje **veřejný záznam přesnosti per agent** — Marksův hit rate, Druckenmillerův hit rate, agregátní hit rate systému. Institucionální research toto nepublikuje. xmetrics ano, protože transparentnost je jediný způsob, jak může systém ospravedlnit váhy, které sám sobě přiděluje.

---

[10] PRO KOHO JE TO POSTAVENO

xmetrics je postaven pro tři typy uživatelů:

- **Drobní investoři s portfolii 500 tisíc – 5 milionů Kč**, kteří mají ve svém portfoliu ETF jádro a aktivně přemýšlejí o riziku. Kteří chtějí rozumět tomu, co se děje, ne jen kupovat ETF na základě doporučení. Kteří mají před sebou roky nebo dekády investování a vědí, že 50 viral momentů má menší hodnotu než 52 týdnů konzistentního myšlení.

- **Studenti tržní struktury**, kteří chtějí vidět, jak neslučitelné metodologie skutečně uvažují o stejných datech, jak se neshody řeší a jak vypadá disciplinovaný skórovací framework v praxi. Toto je vzdělávací nástroj — explicitně.

- **Lidé, kterým chybí druhý názor.** Single-analyst research nese strukturální slabosti (jednostrannost, narativní setrvačnost). Mít k dispozici pět nezávislých metodologií současně, navíc s historickou auditní stopou, je něco, co normální drobný investor nezíská odnikud jinud.

xmetrics **není** postaven pro day tradery, options scalpers nebo kohokoli hledajícího intraday signály. Kadence je týdenní záměrně. Tržní struktura se mění na této časové škále; na kratších dominuje šum.

---

[11] JAK ČÍST REPORT

Pro lidi nové k formátu xmetrics — doporučené pořadí čtení týdenní session:

1. **Otevřete `R6_YYYY-MM-DD.md`.** Přečtěte sekci `[1]` (CIO verdikt) a `[2]` (zpětná vazba na předchozí predikci). To je teze v ~500 slovech.
2. **Zkontrolujte seznam disqualifierů** v Executive Summary. Jakýkoli aktivní disqualifier přepisuje skóre na úrovni agentů — musíte vědět, které rails jsou aktivní, než budete číst dál.
3. **Přečtěte sekci `[3A]` — Agent Dashboard.** Jednořádkové shrnutí per agent. Toto vám řekne, kde je konsenzus a kde dissent.
4. **Pokud je konsenzus 5/5, skočte na Contrarian Test.** Toto je aktivní pokus CIO o falsifikaci konsenzu. Pokud test produkuje silné důkazy, verdikt je upgradován na vyšší confidence.
5. **Přečtěte sekci `[4] — Konfrontační debata`** pro dimenzi, která vás zajímá nejvíc. Každá konfrontace produkuje přiřazení dominantního frameworku (časování vs. velikost).
6. **Skočte na sekci `[8] — AI Learning Metadata`.** Hypotézy vám řeknou, co přesně systém predikuje a jak se sám oskóruje příští týden.
7. **Teprve potom**, pokud chcete hlubší detail, otevřete jednotlivé reporty agentů R1–R5.

Čtení v tomto pořadí trvá ~15 minut a zachytí 90 % akčního obsahu.

> **Tip pro drobné investory:** Pokud máte málo času, přečtěte si jen pondělní report na síti X.

---

[12] METODOLOGIE — SKÓROVÁNÍ A VÁHY

12A — Pilířové skórování (škála 1–10)

Každý pilíř v každém reportu agenta je skórován na uniformní škále 1–10 s následující sémantikou:

```
1.0 – 2.5    Extrémně bearish / vážná dysfunkce / hlavní strukturální varování
2.6 – 4.0    Bearish / nepříznivé / zvýšené riziko
4.1 – 6.0    Neutrální / smíšené signály / žádná jasná hrana
6.1 – 7.5    Bullish / příznivé / podpůrné podmínky
7.6 – 10.0   Extrémně bullish / silný strukturální tailwind / nízké riziko
```

Celkové skóre agenta je vážený součet pilířových skóre s použitím vah daného agenta.

12B — CIO vážená agregace

```
SYSTEM_SCORE = Σ ( agent_skóre_i × váha_agenta_i ) + modifikátory
kde:
  váha_agenta_i    = základní_váha_i × regime_modifier_i × accuracy_modifier_i
  Σ váha_agenta_i  = 100 % (normalizováno po modifikátorech)
  modifikátory     = SKEW_VIX_mod + sentiment_mod + overlap_correction

Základní váhy (před modifikátory):
  R1 Marks          20 %
  R2 Druckenmiller  25 %
  R3 Damodaran      20 %
  R4 Taleb          20 %
  R5 TA             15 %
```

12C — Pravděpodobnostní distribuce

Každý R6 report poskytuje tři pravděpodobnostně vážené scénáře:

```
P_BULL   — pravděpodobnostní váha bullish případu, se 4týdenním cílovým pásmem
P_BASE   — pravděpodobnostní váha base case, se 4týdenním pásmem
P_BEAR   — pravděpodobnostní váha bearish případu, se 4týdenním pásmem

Σ P = 100 %
```

Tyto jsou kalibrované, ne marketingové. Report s P_BEAR = 40 % neznamená „jsem 40 % přesvědčený o bear scénáři" — znamená „v 40 srovnatelných historických nastaveních se tento výsledek stal zhruba osmnáctkrát."

---

[13] GLOSÁŘ

Klíčová terminologie napříč xmetrics reporty. Rozsah se rozšiřuje, jak vstupují nové koncepty.

| **ERP**                      | Equity Risk Premium — prémie, kterou investoři požadují nad bezrizikovou sazbou za držení akcií |
| **Naive ERP**                | Proxy výpočet: earnings yield (1 / P/E) minus 10letý Treasury yield                            |
| **CAPE**                     | Cyclically-Adjusted P/E (Shiller P/E) — cena ÷ 10letý průměr inflačně očištěných zisků         |
| **GEX**                      | Gamma Exposure — metrika struktury opčního trhu zachycující hedging Market Makerů              |
| **GEX Flip**                 | Cenová úroveň, kde se net GEX otáčí na záporný; pod tímto bodem hedging MMs amplifikuje pohyby |
| **GEX Regime POSITIVE**      | MMs jsou long gamma → prodávají rally, kupují poklesy → tlumí volatilitu                       |
| **GEX Regime NEGATIVE**      | MMs jsou short gamma → prodávají poklesy, kupují rally → amplifikují volatilitu                |
| **Call Wall / Put Wall**     | Strikes s nejvyšší koncentrací gamma exposure — působí jako support/resistance                 |
| **VIX**                      | CBOE 30denní implied volatility z opcí na SPX                                                  |
| **VIX termová struktura**    | Spread mezi delším (VIX3M) a spotem VIX. Pozitivní = contango (normální), záporný = backwardation (stres) |
| **SKEW**                     | CBOE SKEW Index měřící cenu pojistky proti tail risk v opcích na SPX                          |
| **SKEW/VIX Ratio**           | Poměr SKEW k VIX. > 7,0 indikuje klid na povrchu s institucionálním tail hedgingem pod ním    |
| **RRP**                      | Reverse Repo Program — Fed facility, která drainuje systémovou likviditu, jak balance klesá   |
| **M2**                       | Široké měřítko peněžní zásoby USA                                                              |
| **FFR / Real FFR**           | Federal Funds Rate / FFR upravený o inflační očekávání                                         |
| **Bear Steepener**           | Steepening yield curve poháněné rostoucími dlouhodobými yieldy (nepříznivé pro akcie)         |
| **Bull Steepener**           | Steepening yield curve poháněné klesajícími krátkodobými yieldy (typicky Fed easing)          |
| **PCR**                      | Put/Call Ratio                                                                                 |
| **HY / IG**                  | High-Yield / Investment-Grade credit spreads nad Treasuries                                    |
| **SLOOS**                    | Senior Loan Officer Opinion Survey — kvartální Fed průzkum o lending standardech              |
| **CC Delinquency**           | Credit card delinquency rate — indikátor stresu spotřebitelského kreditu                      |
| **Buffett Indicator**        | Total US tržní kapitalizace ÷ HDP. Historicky preferovaná valuační metrika                    |
| **SPXA50R / SPXA200R**       | % konstituent SPX nad 50denním / 200denním moving average                                     |
| **Breadth Collapse**         | Formální disqualifier — SPXA200R pod 30 % AND klesá                                           |
| **Breadth Critical Divergence** | SPXA50R pod 15 % zatímco SPX je na nebo blízko ATH — early warning signal                  |
| **Dual Complacency**         | Současný výskyt záporného ERP + zvýšený SKEW/VIX — triggeruje boost váhy R4                  |
| **VPVR / POC**               | Volume Profile Visible Range / Point of Control — cenová úroveň s nejvíc obchodovaným objemem |
| **VWAP (Anchored)**          | Volume-Weighted Average Price ukotvený na konkrétní referenční událost                         |
| **Fibonacci Retracement**    | Klasické TA úrovně na 38,2 % / 50,0 % / 61,8 % předchozí swingu                              |
| **RSI-14**                   | Relative Strength Index nad 14 period — momentum oscilátor (0–100)                            |
| **ADX-14**                   | Average Directional Index — měřítko síly trendu (směrově neutrální)                           |
| **Stoch RSI**                | Stochastic RSI — RSI normalizovaný na vlastní nedávný rozsah                                   |
| **MACD Histogram**           | Moving Average Convergence Divergence rozdíl — momentum indikátor                             |
| **OBV**                      | On-Balance Volume — kumulativní volume flow                                                    |
| **MFI-14 / CMF-20**          | Money Flow Index / Chaikin Money Flow — volume-weighted momentum                              |
| **Elliott Wave**             | Wave-count framework identifikující impulse (IMP) a corrective (COR) struktury                |
| **Fragility Score**          | Talebova škála 1–10 kde 1 = maximálně fragilní, 10 = robustní/antifragilní                   |
| **Barbell Positioning**      | Talebova strategie — koncentrace expozice na extrémech, vyhněte se středu                     |
| **Disqualifier**             | Tvrdé pravidlo přepisující agregované skóre při triggeru                                      |
| **Nonlinearity Multiplier**  | CIO odhad, jak moc by typický signál byl amplifikován aktuální tržní strukturou               |
| **Falsifikovatelná hypotéza** | Explicitní predikce s datem ověření a binárním výsledkem — „H1: X do Y"                      |
| **Contrarian Test**          | Povinný CIO krok při konsenzu 5/5 — aktivně se pokouší falsifikovat konsenzus                 |
| **Overlap Correction**       | CIO úprava aplikovaná když dva agenti sdílejí >80 % datové báze                              |
| **Regime Modifier**          | Dynamická úprava váhy podle aktuálního tržního režimu (např. ERP záporné → R4 boost)         |
| **Accuracy Modifier**        | Dynamická úprava váhy podle nedávného track recordu hypotéz daného agenta                    |
| **Disqualifier Haircut**     | R6 systémové pravidlo — disqualifiers aplikované v R5 score floor jsou na úrovni R6 aplikovány s 0,5× haircutem |
| **RRP Data Discontinuity**   | Pokud RRP w/w změna > 200 %, signál je PAUSED a substituován M2_YOY decel + 2Y w/w move        |
| **Gamma-regime Suspension**  | R5 nereportuje 1W směrovou predikci pod GEX_REGIME POSITIVE s NET > +1,0G; strukturální čtení pokračuje |

---

[14] INTEGRITA SYSTÉMU — CO SYSTÉM NEDĚLÁ

V zájmu intelektuální poctivosti je stejně důležité dokumentovat hranice jako schopnosti:

- **Neposkytuje intraday signály.** Kadence je týdenní. Cokoliv rychlejšího je šum vůči makro frameworku.
- **Neexekuuje obchody.** Produkuje analýzu, ne příkazy. Position sizing je vodítko — exekuce je odpovědnost čtenáře.
- **Nepredikuje ceny jednotlivých akcií.** Scope je index (SPX) a hlavní sektorová rotace. Single-name analýza je mimo rámec.
- **Nezaručuje hit rate.** Falsifikovatelné hypotézy budou selhávat. Učící smyčka existuje právě proto, že predikce je obtížná — systém získává svou hranu tím, že se opravuje rychleji než alternativy, ne tím, že se trefuje častěji v absolutních číslech.
- **Nenahrazuje portfolio managera.** Lidský úsudek o position sizing, kontextu portfolia a toleranci rizika zůstává zásadní. xmetrics je decision-support nástroj neobvyklé hloubky — ne decision-making nástroj.
- **Není investiční poradenství.** xmetrics není broker, není regulovaná finanční instituce. Veškerý obsah slouží k edukaci, ne jako doporučení k nákupu/prodeji. Pro investiční rozhodování konzultujte licencovaného poradce.

---

[15] ZMĚNY FRAMEWORKU

Strukturální změny ve frameworku — nové metriky, modifikované prahy disqualifierů, noví agenti, upravené základní váhy — jsou dokumentovány. Změny se promítnou do následujících reportů automaticky a jejich zdůvodnění je dohledatelné v sekci `[10B] Patterns` v R6 reportu, kde každý pattern má svůj `STATUS` (ACTIVE / MONITORING / PAUSED / RETIRED).

---

*Konec dokumentace xmetrics. Pro metodologické otázky nad rámec tohoto dokumentu se podívejte na jednotlivé reporty agentů, které obsahují detailní příklady každého frameworku v akci. Glossář v [13] vysvětluje anglickou terminologii používanou v reportech R1–R6.*
