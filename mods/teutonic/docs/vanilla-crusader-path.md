---
title: "Vanilla Teutonic Order — Crusader Path reference"
created: 2026-10-06
status: research-baseline
scope: "Vanilla Lions of the North missions; no mod changes"
game_version: "EU4 v1.37.2.0 Inca (7a4b)"
---

# Vanilla Teutonic Order: Crusader Path

This is the baseline for **extending the existing vanilla tree**, rather than replacing it with an unrelated campaign. It records the installed game’s prerequisites, completion conditions, rewards, branching events and progression logic. Proposed design interpretations are explicitly separated from script facts.

**Coverage: 32 distinct missions relevant to this route — 6 opening/shared missions and 26 Crusader-specific missions.** Seek Imperial Protection disappears upon committing to the Crusader path, leaving 31 of these mission entries on that committed tree. Preview placeholders, Prussian branches, generic missions and the separate Livonian Crusader tree are excluded.

Checked on **6 October 2026** against the installed **1.37.2.0 Inca (7a4b)** files. This is the installed-version baseline, not a claim that it is the newest available EU4 patch. EU4 and its launcher were not opened. No existing mod files were changed.

## Sources and how to read this reference

- [Paradox’s original Teutonic developer diary, 3 May 2022](https://forum.paradoxplaza.com/forum/developer-diary/europa-universalis-iv-development-diary-3rd-of-may-2022.1523186/). The forum returned a browser challenge; its content was read through the [official Steam republication — scroll to 3 May 2022](https://store.steampowered.com/news/posts/?appids=236850%2C231740%2C210908%2C202270%2C225420%2C210904%2C210905%2C226660%2C203770%2C204080%2C218130%2C227760%2C202130%2C48700%2C25800%2C42990%2C22130%2C230940%2C73170%2C42910%2C48720%2C200370%2C22100%2C25890%252&enddate=1655825040). This is **prerelease design commentary**, not final numeric authority.
- [Teutonic missions wiki](https://eu4.paradoxwikis.com/Teutonic_missions): useful cross-reference link, but the page could not be retrieved during this check; it was not treated as verified evidence.
- `missions/SCA_Teutonic_Missions.txt`: primary authority for the 32 entries and dependency graph below. Each mission links to its own source location.
- `events/flavorTEU.txt` and `localisation/scandinavia_l_english.yml`: actual event effects and displayed names. The events file credits **Ogulcan Yildirim** in its header.
- `common/event_modifiers/01_mission_modifiers.txt`, `common/government_reforms/03_government_reforms_theocracies.txt`, and the supporting sources listed at the end resolve the effects hidden behind identifiers.

**Conventions.** Numeric thresholds mean “at least” unless explicitly stated otherwise. “You/subjects” below means the native non-sovereign-subject ownership check where specified, not arbitrary allies or tributaries. Allied and Catholic-owner exceptions are stated separately. Permanent claims exclude provinces already cored or permanently claimed by you; they do not transfer land or grant cores. A modifier’s “permanent” duration is distinct from 25- or 100-year durations. Percentages and percentage points are distinguished.

All 26 Crusader entries require **Lions of the North**, **TEU**, a non-random map, the committed `teu_crusader_path` flag, and not being in mission-preview mode. All explicitly require Catholic religion except Fall of the Third Rome, whose trigger omission is noted below. Completing a mission requires all its listed parents, even when its numeric conditions have already been met. Slot/row describe the native five-column layout, not a forced order of play.

## Original design and the campaign’s direction

The developer diary describes a deliberately counterfactual Catholic route: expand and convert through Russia and the steppe, while the army adapts through successive cavalry reforms. It distinguishes this from the Prussian path and explicitly describes stronger military modifiers replacing earlier ones. Its endpoint is the Holy Horde, with religious expansion continuing eastward. These are the designer’s stated themes; the mission-by-mission “Design reading” comments below are our interpretation of the installed implementation.

A concrete version difference matters: the prerelease diary described **Defeat Poland** as four provinces **or three victories against Polish armies**. The installed 1.37.2 mission only checks four provinces in Kuyavia/Wielkopolska. We should extend the installed rules rather than copying old preview requirements.

## Branch commitment and initial claims

**Expand our Army → Defeat Poland → select Crusader path.** Livonian Alliance is also a required parent of Defeat Poland. Handle the Confederation and Seek Imperial Protection are useful opening tasks but are not parents of that unlock.

Defeat Poland opens the modern branching-mission review; `flavor_teu.10` is the alternate/AI selection event. Confirming the Crusader choice sets its branch flag, clears conflicting Prussian/HRE-path flags, sets `formed_prussia_flag`, enables the battle counter when applicable, and leaves the HRE if you are a member. It gives permanent claims in **Samogitia, Lithuania, Mazovia, Malopolska and Central Poland**. This is a separate reward stage from the mission’s 25 power projection.

The player-preview completion effect and the event contain corresponding commitment logic. This baseline preserves both when planning a future extension. It should not give these claims merely for hovering over the branch preview.

## Complete inventory

Numbers identify entries in this document, not a required sequence. “None” means an independent entry within the relevant unlocked tree.

| # | Mission | Slot / row | Required missions |
|---|---|---|---|
| 01 | [Seek Imperial Protection](#teu_seek_imperial_protection) | 1 / 1 | None |
| 02 | [Livonian Alliance](#teu_livonian_alliance) | 2 / 1 | None |
| 03 | [Bound of the Orders](#teu_strengthen_livonia) | 2 / 2 | 2 Livonian Alliance |
| 04 | [Handle the Confederation](#teu_handle_the_prussian_confederation) | 3 / 1 | None |
| 05 | [Defeat Poland](#teu_defeat_the_poles) | 3 / 2 | 2 Livonian Alliance, 6 Expand our Army |
| 06 | [Expand our Army](#teu_build_to_force_limit) | 4 / 1 | None |
| 07 | [Grant Clergy Privileges](#teu_crusader_clergy_influence) | 1 / 2 | 2 Livonian Alliance |
| 08 | [Conquest of Novgorod](#teu_crusader_conquer_novgorod) | 1 / 3 | 7 Grant Clergy Privileges, 3 Bound of the Orders |
| 09 | [Fall of the Third Rome](#teu_crusader_third_rome) | 1 / 4 | 8 Conquest of Novgorod |
| 10 | [End the Schism](#teu_crusader_end_the_schism) | 1 / 5 | 9 Fall of the Third Rome |
| 11 | [Found Churches](#teu_crusader_land_of_churches) | 1 / 6 | None |
| 12 | [Construct Cathedrals](#teu_crusader_build_cathedrals) | 1 / 7 | 11 Found Churches |
| 13 | [Annex Lithuania](#teu_crusader_lithuanian_crusade) | 2 / 3 | 5 Defeat Poland |
| 14 | [Christianize the Steppes](#teu_crusader_conquer_crimea) | 2 / 4 | 13 Annex Lithuania |
| 15 | [Fortify the Caucasus](#teu_crusader_fortify_the_caucasus) | 2 / 5 | 14 Christianize the Steppes |
| 16 | [Defeat the Ottomans](#teu_crusader_bulwark_against_the_turks) | 2 / 6 | 15 Fortify the Caucasus |
| 17 | [Conquer Poland](#teu_crusader_conquer_poland) | 3 / 3 | 5 Defeat Poland |
| 18 | [The Ruthenian Plains](#teu_crusader_push_into_ruthenia) | 3 / 4 | 17 Conquer Poland, 13 Annex Lithuania |
| 19 | [Eliminate the Hordes](#teu_crusader_eliminate_the_great_horde) | 3 / 5 | 14 Christianize the Steppes, 18 The Ruthenian Plains |
| 20 | [Push into the Steppes](#teu_crusader_steppes_crusade) | 3 / 6 | 19 Eliminate the Hordes |
| 21 | [Crusaders of the Steppes](#teu_crusader_a_holy_horde) | 3 / 7 | 20 Push into the Steppes, 25 Establish a Great Cavalry |
| 22 | [Gain Combat Experience](#teu_crusader_mil_reform_1) | 4 / 3 | 6 Expand our Army |
| 23 | [Reform the Army](#teu_crusader_mil_reform_2) | 4 / 4 | 17 Conquer Poland, 22 Gain Combat Experience |
| 24 | [Adapt to the Plains](#teu_crusader_mil_reform_3) | 4 / 5 | 18 The Ruthenian Plains, 23 Reform the Army |
| 25 | [Establish a Great Cavalry](#teu_crusader_mil_reform_4) | 4 / 6 | 19 Eliminate the Hordes, 24 Adapt to the Plains |
| 26 | [Secure Papal Alliance](#teu_crusader_secure_papal_alliance) | 5 / 1 | None |
| 27 | [Embrace Religious Ideas](#teu_crusader_embrace_religious_ideas) | 5 / 2 | 26 Secure Papal Alliance |
| 28 | [Convert the Land](#teu_crusader_convert_provinces) | 5 / 3 | 27 Embrace Religious Ideas |
| 29 | [Increase our Income](#teu_crusader_gain_income) | 5 / 4 | None |
| 30 | [Castle Expertise](#teu_crusader_castle_expertise) | 5 / 5 | 29 Increase our Income |
| 31 | [Resist the Reformation](#teu_crusader_survive_the_reformation) | 5 / 6 | None |
| 32 | [Crush the Heresy](#teu_crusader_destroy_the_heresies) | 5 / 7 | 31 Resist the Reformation |

## Every mission: conditions, rewards and purpose

<a id="teu_seek_imperial_protection"></a>

### 01. Seek Imperial Protection

**ID:** `teu_seek_imperial_protection` · **Position:** column 1, row 1 · `missions/SCA_Teutonic_Missions.txt:22`

**Required missions:** None.

**Conditions:** If the HRE exists: the Emperor’s opinion of you must be at least +100; with Emperor DLC, no imperial incident may be active. If the HRE no longer exists: stability at least +1. Cannot complete in mission-preview mode.

**Rewards:** If TEU is outside an existing HRE, fires **The Empire and the Teutonic Order** (`flavor_teu.17`): request entry, or refuse protection for **100 MIL** and **25 years of +1 yearly prestige and +5% army morale**, with −75 Emperor opinion decaying by 3/year. Requesting entry can lead to admission, conditional admission, or rejection; see the event appendix. Otherwise receive **100 DIP**. This mission disappears when the Crusader branch is selected.

**Design reading:** An optional survival instrument before choosing an identity. It is not a mandatory ancestor of Defeat Poland or the Holy Horde.

<a id="teu_livonian_alliance"></a>

### 02. Livonian Alliance

**ID:** `teu_livonian_alliance` · **Position:** column 2, row 1 · `missions/SCA_Teutonic_Missions.txt:85`

**Required missions:** None.

**Conditions:** If LIV exists, satisfy any one: rival and embargo LIV; ally LIV with their opinion of you at least +150; or make LIV your subject. If LIV does not exist, have at least +1 stability.

**Rewards:** Allied/opinion route: **Unification of the Orders?** (`flavor_teu.13`). Propose vassalization: acceptance makes LIV your vassal, refusal gives a **30-year Subjugation CB**. Alternatively preserve the alliance for **+10 mutual trust** and a **level-1 Statesman at 25% normal cost**. Rival/embargo route: the same 30-year CB. Already-subject route: no new material reward. If LIV is gone: **100 MIL**. The script tests the allied route before the rival route.

**Design reading:** Allow diplomacy or coercion to solve the same strategic need without requiring the player to restart if Livonia disappears.

<a id="teu_strengthen_livonia"></a>

### 03. Bound of the Orders

**ID:** `teu_strengthen_livonia` · **Position:** column 2, row 2 · `missions/SCA_Teutonic_Missions.txt:154`

**Required missions:** [Livonian Alliance](#teu_livonian_alliance).

**Conditions:** Any one: (a) allied LIV has +190 opinion and, with Leviathan, 80 trust toward you; without Leviathan it instead needs the received-gift opinion modifier from you; (b) subject LIV has +190 opinion and liberty desire **below 10%**; (c) you/non-sovereign subjects hold at least **8 provinces** across Livonia, Curonia and Estonia/Ingria. If LIV is gone, only (c) applies.

**Rewards:** First matching reward, **25 years**: subject LIV → **+10% manpower recovery and +0.5 yearly army tradition**; allied LIV → **+1 diplomatic relation and +20% monthly favor growth**; territorial route → **−1 national unrest and +10% national manpower**. Modifier IDs: `teu_unified_orders`, `teu_livonian_teutonic_alliance`, `teu_ruler_over_livonia`.

**Design reading:** The reward reflects how the relationship was resolved. A diplomatic ally is a valid foundation for the Russian branch; annexation is not compulsory.

<a id="teu_handle_the_prussian_confederation"></a>

### 04. Handle the Confederation

**ID:** `teu_handle_the_prussian_confederation` · **Position:** column 3, row 1 · `missions/SCA_Teutonic_Missions.txt:286`

**Required missions:** None.

**Conditions:** Always: no Prussian Confederation Burgher privilege. In addition, any one: (a) +1 stability, no rebel-controlled provinces, no spawned particularist rebels, and either no Burghers estate or at least 40% crownland; (b) past the Age of Discovery and no active Prussian Confederation disaster; (c) the `pru_confederation_happened` flag is already set.

**Rewards:** End the Prussian Confederation disaster, set its curtailed flag, gain **10 prestige** and **−1 national unrest for 20 years** (`pru_confederation_curtailed_modifier`).

**Design reading:** Resolve the historical domestic threat. It stands independently in the layout; it is not a scripted prerequisite for defeating Poland.

<a id="teu_defeat_the_poles"></a>

### 05. Defeat Poland

**ID:** `teu_defeat_the_poles` · **Position:** column 3, row 2 · `missions/SCA_Teutonic_Missions.txt:328`

**Required missions:** [Livonian Alliance](#teu_livonian_alliance); [Expand our Army](#teu_build_to_force_limit).

**Conditions:** You/non-sovereign subjects hold **4 provinces total** across Kuyavia and Wielkopolska. There is no requirement to eliminate Poland or to own all of either area. The installed version has **no alternative three-battle completion route**.

**Rewards:** **25 mission power projection**, then unlock the branching mission review. Confirming the Crusader path supplies the initial Lithuania/Poland claims, leaves the HRE if necessary, and blocks ordinary Prussia formation; see branch selection below.

**Design reading:** A limited first victory earns a choice of national direction. The threshold is deliberately much smaller than full Polish conquest.

<a id="teu_build_to_force_limit"></a>

### 06. Expand our Army

**ID:** `teu_build_to_force_limit` · **Position:** column 4, row 1 · `missions/SCA_Teutonic_Missions.txt:386`

**Required missions:** None.

**Conditions:** Field an army at **100% of force limit or more** and employ a military advisor.

**Rewards:** **+20% fort defensiveness and −10% shock damage received for 25 years** (`teu_teutonic_persistance`), plus **permanent claims on Kuyavia and Wielkopolska**.

**Design reading:** Preparation pays forward: an attainable opening task gives the claims and resilience needed for the first Polish war.

<a id="teu_crusader_clergy_influence"></a>

### 07. Grant Clergy Privileges

**ID:** `teu_crusader_clergy_influence` · **Position:** column 1, row 2 · `missions/SCA_Teutonic_Missions.txt:4609`

**Required missions:** [Livonian Alliance](#teu_livonian_alliance).

**Conditions:** Catholic. If the Clergy estate exists: at least **50 influence, 60 loyalty and 3 privileges**. The estate requirements are waived if that estate does not exist.

**Rewards:** Unlock **Issue the Anti-Heresy Act** (`estate_church_anti_heresy_act`) and gain **permanent claims on Karelia, Novgorod and Pskov**. Unlocking does not automatically enact the privilege. Its benefits and political costs are detailed below.

**Design reading:** Build an ecclesiastical coalition before claiming a mandate to expand into Orthodox lands.

<a id="teu_crusader_conquer_novgorod"></a>

### 08. Conquest of Novgorod

**ID:** `teu_crusader_conquer_novgorod` · **Position:** column 1, row 3 · `missions/SCA_Teutonic_Missions.txt:4664`

**Required missions:** [Grant Clergy Privileges](#teu_crusader_clergy_influence); [Bound of the Orders](#teu_strengthen_livonia).

**Conditions:** Catholic. Neva (33) and Novgorod (310) must each have a Catholic owner. At least **8 provinces** across Karelia, Pskov and Novgorod must be owned by a Catholic **you, ally or subject**. Those two named provinces do not individually require an allied owner. Provincial Catholic conversion is **not** required here.

**Rewards:** **100 government reform progress** and **permanent claims on Moscow, Tver and Vladimir**.

**Design reading:** A Catholic sphere can substitute for annexation. This is a political foothold before later missions demand actual religious conversion.

<a id="teu_crusader_third_rome"></a>

### 09. Fall of the Third Rome

**ID:** `teu_crusader_third_rome` · **Position:** column 1, row 4 · `missions/SCA_Teutonic_Missions.txt:4738`

**Required missions:** [Conquest of Novgorod](#teu_crusader_conquer_novgorod).

**Conditions:** Moscow (295) is either **directly owned and cored by you**, or owned by a **Catholic ally**. Unlike the other Crusader-specific missions, this trigger has no explicit `religion = catholic` check; its ordinary route still comes through Catholic predecessors.

**Rewards:** Direct ownership/core fires **The Fate of Moscow** (`flavor_teu.37`): integration, church repurposing or sack, with distinct costs and benefits. Allied ownership instead gives **100 DIP**. In either case gain **permanent claims on the entire Russia region**. Full choices appear below.

**Design reading:** A major city creates a political and moral fork. Integration trades easier local stability and development against harder future conversion.

<a id="teu_crusader_end_the_schism"></a>

### 10. End the Schism

**ID:** `teu_crusader_end_the_schism` · **Position:** column 1, row 5 · `missions/SCA_Teutonic_Missions.txt:4797`

**Required missions:** [Fall of the Third Rome](#teu_crusader_third_rome).

**Conditions:** Catholic, and either: (a) Moscow, Neva and Novgorod are Catholic provinces with Catholic owners, plus at least **40 Catholic provinces in the Russia region** owned by Catholic you/allies/subjects; or (b) global flag `catholics_healed_schism` is already set.

**Rewards:** If this is the first declaration, set that global flag and fire `flavor_teu.38` for **every Orthodox country that knows you**. Recipients choose whether to convert; the mission does not forcibly convert everyone. If the flag was already set, gain **100 papal influence** instead. Always gain **permanent +1 tolerance of the true faith and +1 percentage point missionary strength against heretics** (`teu_crusade_end_of_the_schism`).

**Design reading:** Territorial and religious achievement culminates in a world-facing event, with a fallback if another country already resolved the objective.

<a id="teu_crusader_land_of_churches"></a>

### 11. Found Churches

**ID:** `teu_crusader_land_of_churches` · **Position:** column 1, row 6 · `missions/SCA_Teutonic_Missions.txt:4872`

**Required missions:** None.

**Conditions:** Catholic. Own at least **15 provinces of your religion** containing a church or cathedral. Direct ownership is required.

**Rewards:** **25 papal influence**, **+10 Clergy loyalty**, and, if the Papal State exists, **+50 Papal State opinion of you**, decaying by 2/year.

**Design reading:** An independent internal-development entry point; it can progress alongside wars rather than waiting behind conquest.

<a id="teu_crusader_build_cathedrals"></a>

### 12. Construct Cathedrals

**ID:** `teu_crusader_build_cathedrals` · **Position:** column 1, row 7 · `missions/SCA_Teutonic_Missions.txt:4908`

**Required missions:** [Found Churches](#teu_crusader_land_of_churches).

**Conditions:** Catholic. At least **10 cathedrals** and an employed **level-3-or-higher Theologian**.

**Rewards:** Each currently owned cathedral province gains **+200% local tax and −3 local unrest for 25 years** (`teu_crusade_teutonic_cathedral`). Gain **5 papal influence per such province**. Ten cathedrals means 50 influence, but the payout scales if you have more. This does not automatically cover future cathedrals.

**Design reading:** A sizable but local and temporary return on expensive infrastructure, rather than another permanent army bonus.

<a id="teu_crusader_lithuanian_crusade"></a>

### 13. Annex Lithuania

**ID:** `teu_crusader_lithuanian_crusade` · **Position:** column 2, row 3 · `missions/SCA_Teutonic_Missions.txt:4953`

**Required missions:** [Defeat Poland](#teu_defeat_the_poles).

**Conditions:** Catholic. You/non-sovereign subjects hold at least **5 Catholic provinces** across Samogitia and Lithuania.

**Rewards:** **20 army tradition, 25 devotion**, and **permanent claims on the Crimea region**. If Conquer Poland is incomplete, also receive **permanent Ruthenia claims**; otherwise **150 ADM**. If the Zeal modifier is absent, gain **+2 percentage points missionary strength and +10% manpower in true-faith provinces for 25 years** (`teu_crusade_zeal_of_the_crusader`); if it is already active, receive **0.25 years of manpower** instead.

**Design reading:** Conversion is part of victory, and either Lithuania or Poland can open Ruthenia. Duplicate support is compensated rather than blindly stacked.

<a id="teu_crusader_conquer_crimea"></a>

### 14. Christianize the Steppes

**ID:** `teu_crusader_conquer_crimea` · **Position:** column 2, row 4 · `missions/SCA_Teutonic_Missions.txt:5017`

**Required missions:** [Annex Lithuania](#teu_crusader_lithuanian_crusade).

**Conditions:** Catholic. You/non-sovereign subjects hold at least **15 Catholic provinces in the Crimea region**.

**Rewards:** **−20% cavalry cost and +5% movement speed for 25 years** (`teu_crusade_horses_of_the_steppes`); **permanent claims on Circassia and Dagestan areas**. If The Ruthenian Plains is completed, also gain **permanent claims on the Ural region**; otherwise gain **100 ADM**.

**Design reading:** Steppe conquest starts changing the army’s economics. The Ural claim gate waits until both southern and central corridors have been established.

<a id="teu_crusader_fortify_the_caucasus"></a>

### 15. Fortify the Caucasus

**ID:** `teu_crusader_fortify_the_caucasus` · **Position:** column 2, row 5 · `missions/SCA_Teutonic_Missions.txt:5074`

**Required missions:** [Christianize the Steppes](#teu_crusader_conquer_crimea).

**Conditions:** Catholic. Circassia (463) and Lakia (4306) must be held by you/non-sovereign subjects, be Catholic, and each contain a **current-technology fort**. The relevant technology is the province owner’s.

**Rewards:** A **level-3 Fortification Expert of your religion at 10% normal cost**. Both named provinces permanently gain **+50% local defensiveness, +25% garrison size and −90% local fort maintenance** (`teu_pru_fortified_border`).

**Design reading:** Anchor a specific frontier. Very large percentages are restricted to two forts; copying them into a national modifier would distort the balance.

<a id="teu_crusader_bulwark_against_the_turks"></a>

### 16. Defeat the Ottomans

**ID:** `teu_crusader_bulwark_against_the_turks` · **Position:** column 2, row 6 · `missions/SCA_Teutonic_Missions.txt:5125`

**Required missions:** [Fortify the Caucasus](#teu_crusader_fortify_the_caucasus).

**Conditions:** Catholic and Defender of the Faith. The Ottomans either do not exist, or you have won a war against them **within the last 100 years**.

**Rewards:** If TUR exists, fire **Humiliation of the Ottoman Empire** (`flavor_teu.40`): **100 mission power projection**, permanent **+1 tolerance of the true faith and −1 percentage point yearly prestige decay**, and conversion/unrest effects on Ottoman Christian provinces. If TUR is gone, receive only that permanent modifier (`teu_crusade_ottomans_vanquished`).

**Design reading:** A celebrated victory destabilizes the adversary rather than handing you territory. Ottoman disappearance has a sensible, smaller fallback.

<a id="teu_crusader_conquer_poland"></a>

### 17. Conquer Poland

**ID:** `teu_crusader_conquer_poland` · **Position:** column 3, row 3 · `missions/SCA_Teutonic_Missions.txt:5176`

**Required missions:** [Defeat Poland](#teu_defeat_the_poles).

**Conditions:** Catholic. You/non-sovereign subjects hold at least **20 Catholic provinces in the Poland region**.

**Rewards:** **2 years of manpower and 10 army tradition**. If Annex Lithuania is incomplete, receive **permanent claims on Ruthenia**; otherwise **150 ADM**. If Zeal of the Crusader is absent, receive its **25-year +2 percentage points missionary strength and +10% true-faith manpower**; if active, receive **50 MIL** instead.

**Design reading:** The full Polish campaign replenishes the army and supports the next wave of conversion. Its compensation differs intentionally from Lithuania’s.

<a id="teu_crusader_push_into_ruthenia"></a>

### 18. The Ruthenian Plains

**ID:** `teu_crusader_push_into_ruthenia` · **Position:** column 3, row 4 · `missions/SCA_Teutonic_Missions.txt:5227`

**Required missions:** [Conquer Poland](#teu_crusader_conquer_poland); [Annex Lithuania](#teu_crusader_lithuanian_crusade).

**Conditions:** Catholic. You/non-sovereign subjects hold at least **25 Catholic provinces in the Ruthenia region**.

**Rewards:** Fire **Formation of a Crusader Order** (`flavor_teu.39`): adopt the Crusader Order reform, or unlock it for later and receive **50 reform progress**. If Christianize the Steppes is already complete, also gain **permanent Ural claims**; otherwise **100 ADM**.

**Design reading:** The size and religious character of the realm justify a constitutional change. Both Polish and Lithuanian predecessors are required.

<a id="teu_crusader_eliminate_the_great_horde"></a>

### 19. Eliminate the Hordes

**ID:** `teu_crusader_eliminate_the_great_horde` · **Position:** column 3, row 5 · `missions/SCA_Teutonic_Missions.txt:5272`

**Required missions:** [Christianize the Steppes](#teu_crusader_conquer_crimea); [The Ruthenian Plains](#teu_crusader_push_into_ruthenia).

**Conditions:** Catholic. You/non-sovereign subjects hold at least **20 Catholic provinces in the Ural region**. Despite its title, this does not directly test whether any particular Horde tag still exists.

**Rewards:** **+5 percentage points army professionalism**, **50 papal influence**, and **permanent claims on the Central Asia region**.

**Design reading:** Geographic and religious success matters more than tag cleanup. The next frontier opens only after both Crimea and Ruthenia are complete.

<a id="teu_crusader_steppes_crusade"></a>

### 20. Push into the Steppes

**ID:** `teu_crusader_steppes_crusade` · **Position:** column 3, row 6 · `missions/SCA_Teutonic_Missions.txt:5308`

**Required missions:** [Eliminate the Hordes](#teu_crusader_eliminate_the_great_horde).

**Conditions:** Catholic. You/non-sovereign subjects hold at least **20 Catholic provinces in Central Asia**.

**Rewards:** **1,000 ducats and 10,000 manpower**, plus a lump sum of **4 years of production income and 4 years of manpower** from directly owned, state-religion provinces in the **Ural, Crimea and Central Asia regions**. The extra payout scales with converted territory; subject provinces satisfy the mission but are not included in these direct-owned payouts.

**Design reading:** A campaign dividend based on what has been integrated religiously, helping the player assemble the final large cavalry army.

<a id="teu_crusader_a_holy_horde"></a>

### 21. Crusaders of the Steppes

**ID:** `teu_crusader_a_holy_horde` · **Position:** column 3, row 7 · `missions/SCA_Teutonic_Missions.txt:5358`

**Required missions:** [Push into the Steppes](#teu_crusader_steppes_crusade); [Establish a Great Cavalry](#teu_crusader_mil_reform_4).

**Conditions:** Catholic; **80% religious unity**, **100 cities**, an army of **100 regiments**, and **at least 50% cavalry**. Both the steppe-conquest and final military-reform branches must be completed.

**Rewards:** Fire **Crusaders of the Steppes** (`flavor_teu.41`), adopting the **Holy Horde** theocratic reform and empire rank. The event also installs a conditional capital modifier and, without The Cossacks, a permanent **−10% core-creation cost** substitute. Full reform effects and DLC differences are below.

**Design reading:** A new mode of play is the main reward. The vanilla eastern campaign ends here; Jerusalem is not this tree’s endpoint or a prerequisite.

<a id="teu_crusader_mil_reform_1"></a>

### 22. Gain Combat Experience

**ID:** `teu_crusader_mil_reform_1` · **Position:** column 4, row 3 · `missions/SCA_Teutonic_Missions.txt:5397`

**Required missions:** [Expand our Army](#teu_build_to_force_limit).

**Conditions:** Catholic. The `num_won_battles` counter is at least **20**. The Crusader battle-counting flag is enabled when the branch is committed; this is not simply a claim that every earlier 1444 battle counted.

**Rewards:** **10 army tradition** and permanent stage I: **+10 percentage points cavalry-to-infantry ratio and +0.25 yearly army tradition**. Separately, reaching the counter threshold fires **Teutonic Victories** (`flavor_teu.12`) for **50 MIL** and **+3 percentage points professionalism** with Cradle of Civilization, or **15 army tradition** without it.

**Design reading:** The first improvement is earned through field experience. The threshold event is separate from clicking the mission reward.

<a id="teu_crusader_mil_reform_2"></a>

### 23. Reform the Army

**ID:** `teu_crusader_mil_reform_2` · **Position:** column 4, row 4 · `missions/SCA_Teutonic_Missions.txt:5422`

**Required missions:** [Conquer Poland](#teu_crusader_conquer_poland); [Gain Combat Experience](#teu_crusader_mil_reform_1).

**Conditions:** Catholic; an employed military advisor of at least **level 2**; with Cradle of Civilization, **30% professionalism**; without it, **40 army tradition**.

**Rewards:** **100 MIL**. Replace stage I with permanent stage II: **+10 percentage points cavalry ratio and +0.75 yearly army tradition**.

**Design reading:** Institutional reform follows battlefield experience and Polish conquest. The older permanent modifier is removed, so these stages do not stack.

<a id="teu_crusader_mil_reform_3"></a>

### 24. Adapt to the Plains

**ID:** `teu_crusader_mil_reform_3` · **Position:** column 4, row 5 · `missions/SCA_Teutonic_Missions.txt:5462`

**Required missions:** [The Ruthenian Plains](#teu_crusader_push_into_ruthenia); [Reform the Army](#teu_crusader_mil_reform_2).

**Conditions:** Catholic; **2 generals**, **one fully completed military-category idea group**, and **25 cavalry regiments**.

**Rewards:** A **level-3 Commandant at 25% normal cost**. Replace stage II with permanent stage III: **+25 percentage points cavalry ratio, +10% cavalry combat ability, +5% movement speed and +0.75 yearly army tradition**.

**Design reading:** Entering Ruthenia links doctrinal investment and actual cavalry recruitment to a more mobile army.

<a id="teu_crusader_mil_reform_4"></a>

### 25. Establish a Great Cavalry

**ID:** `teu_crusader_mil_reform_4` · **Position:** column 4, row 6 · `missions/SCA_Teutonic_Missions.txt:5501`

**Required missions:** [Eliminate the Hordes](#teu_crusader_eliminate_the_great_horde); [Adapt to the Plains](#teu_crusader_mil_reform_3).

**Conditions:** Catholic; **8 barracks OR 8 training fields**; **20 owned grain-producing provinces** (`grain = 20`); **10 monthly MIL generation**; and **50 cavalry regiments**. The building script is two separate thresholds, not an explicit combined total of eight mixed buildings.

**Rewards:** **+10 percentage points professionalism and 20 army tradition**. Replace stage III with permanent stage IV: **+50 percentage points cavalry ratio, +15% cavalry combat ability, +10% movement speed, +50% cavalry flanking ability and +1 yearly army tradition**.

**Design reading:** The large army must have recruitment infrastructure, a supply base and military leadership. This is the completed specialization, not permission to keep stacking identical upgrades indefinitely.

<a id="teu_crusader_secure_papal_alliance"></a>

### 26. Secure Papal Alliance

**ID:** `teu_crusader_secure_papal_alliance` · **Position:** column 5, row 1 · `missions/SCA_Teutonic_Missions.txt:5561`

**Required missions:** None.

**Conditions:** Catholic. If PAP exists, ally it and either (a) have **1 cardinal and 30 invested papal influence**, or (b) have at least **2** of these active modifiers: Papal Sanction for Church Taxes, Papal Blessing, Papal Indulgence, Usury Forgiven, Papal Sanction for Holy War. If PAP does not exist, only the two-modifier condition is used.

**Rewards:** **75 papal influence** and a **discounted level-1 Inquisitor of your religion** (`discount = yes`, the standard half-cost advisor setting).

**Design reading:** Participation in Catholic institutions supplies the resources to continue that participation. Invested influence is distinct from unspent influence.

<a id="teu_crusader_embrace_religious_ideas"></a>

### 27. Embrace Religious Ideas

**ID:** `teu_crusader_embrace_religious_ideas` · **Position:** column 5, row 2 · `missions/SCA_Teutonic_Missions.txt:5615`

**Required missions:** [Secure Papal Alliance](#teu_crusader_secure_papal_alliance).

**Conditions:** Catholic; complete **Religious OR Divine ideas**; employ a **level-3-or-higher Inquisitor or Theologian**. With Common Sense, reach **100 legitimacy-equivalent** (Devotion for the usual Teutonic theocracy); without it, have **+2 stability**.

**Rewards:** If Religious ideas are completed, the **current ruler gains +2 ADM skill**. If Divine ideas are completed, the **current ruler gains +2 MIL skill**. Both checks are independent, so both rewards can apply. These are ruler stats, subject to the normal cap, not permanent monthly monarch-point modifiers.

**Design reading:** Religious learning and military devotion offer two compatible approaches. Reward timing matters because it improves the current ruler.

<a id="teu_crusader_convert_provinces"></a>

### 28. Convert the Land

**ID:** `teu_crusader_convert_provinces` · **Position:** column 5, row 3 · `missions/SCA_Teutonic_Missions.txt:5665`

**Required missions:** [Embrace Religious Ideas](#teu_crusader_embrace_religious_ideas).

**Conditions:** Catholic; the game’s `num_converted_religion` counter is at least **75**. This is a conversion-count check, not a test that 75 currently owned provinces are Catholic, and not a requirement to own 75 newly conquered provinces.

**Rewards:** **+2 tolerance of the true faith and +1 yearly papal influence for 100 years** (`teu_crusader_the_great_missionaries`).

**Design reading:** A sustained conversion campaign earns long-lived religious stability. The effect is long, but the script does not mark it permanent.

<a id="teu_crusader_gain_income"></a>

### 29. Increase our Income

**ID:** `teu_crusader_gain_income` · **Position:** column 5, row 4 · `missions/SCA_Teutonic_Missions.txt:5689`

**Required missions:** None.

**Conditions:** Catholic; **monthly income at least twice the starting-income baseline**, no deficit, **no loans**, **corruption below 1**, and **+2 stability**.

**Rewards:** Capital gains **+1 tax, +1 production and +1 manpower development**. Currently owned provinces in the capital’s area gain **−10% local development cost and −10% local building cost for 25 years** (`growth_of_capital`). Country gains **−10% building cost and −25% building time for 25 years** (`growing_economy`).

**Design reading:** An independent economic recovery gate finances the next infrastructure task. It checks fiscal health as well as income growth.

<a id="teu_crusader_castle_expertise"></a>

### 30. Castle Expertise

**ID:** `teu_crusader_castle_expertise` · **Position:** column 5, row 5 · `missions/SCA_Teutonic_Missions.txt:5723`

**Required missions:** [Increase our Income](#teu_crusader_gain_income).

**Conditions:** Catholic; **25 directly owned provinces with current-technology forts** and an employed **level-3-or-higher Fortification Expert**.

**Rewards:** **+25% fort defensiveness, −25% fort maintenance and +1 attrition for enemies for 100 years** (`teu_crusader_a_fortified_order`).

**Design reading:** A very expensive defensive network unlocks a long-term operating-cost reduction. It is separate from the two targeted Caucasus forts.

<a id="teu_crusader_survive_the_reformation"></a>

### 31. Resist the Reformation

**ID:** `teu_crusader_survive_the_reformation` · **Position:** column 5, row 6 · `missions/SCA_Teutonic_Missions.txt:5748`

**Required missions:** None.

**Conditions:** Catholic; **90% religious unity**; after the Age of Discovery; own **no Hussite, Protestant, Reformed or Anglican provinces**. During the Age of Reformation also have the Counter-Reformation modifier; in later ages that extra condition is waived.

**Rewards:** Set the permanent flag **`can_always_embrace_the_counter_reformation`**, allowing the Counter-Reformation decision beyond its normal historical availability window. This does not automatically enact its modifier or remove the decision’s other eligibility requirements.

**Design reading:** An age-sensitive independent branch rewards religious persistence with continued access to an institution, not just points.

<a id="teu_crusader_destroy_the_heresies"></a>

### 32. Crush the Heresy

**ID:** `teu_crusader_destroy_the_heresies` · **Position:** column 5, row 7 · `missions/SCA_Teutonic_Missions.txt:5787`

**Required missions:** [Resist the Reformation](#teu_crusader_survive_the_reformation).

**Conditions:** Catholic and after the Age of Discovery. During the Age of Reformation, **no European province may contain a Center of Reformation**; this center check is waived in later ages. In all eligible ages, **no European province may be owned by a Protestant or Reformed country**. This tests province location plus owner religion; it neither demands every European province be Catholic nor explicitly targets Anglican/Hussite owners.

**Rewards:** Permanent **+0.25 yearly papal influence, +1 papal influence per cardinal and +0.25 prestige per development from conversion** (`teu_crusader_crushed_the_reformation`).

**Design reading:** A continent-scale denominational objective is the religious branch’s endgame. It rewards continued conversions and Catholic institutions without requiring direct annexation of all Europe.

## Event choices and institutional rewards

These effects are part of the progression even when the mission tooltip only announces an event. Events 37–41 are defined in `events/flavorTEU.txt`; modifiers below were resolved against their definitions rather than guessed from their names.

### Moscow: three genuinely different outcomes (`flavor_teu.37`)

| Choice | Immediate benefit | Cost or consequence |
|---|---|---|
| Integrate the Muscovites | Accept Muscovite culture, or its updated culture equivalent through the native accepted-culture/DIP fallback effect; **+100 DIP** separately. Moscow gains **+3 tax, +3 production, +2 manpower** and loses **100 devastation**. | Held, non-state-religion provinces in **Moscow, Tver and Vladimir** receive **−5 percentage points local missionary strength, +100% local culture-conversion cost and −1 unrest for 25 years**. It is materially harder to meet the next conversion mission quickly. |
| Repurpose the churches | **50 papal influence**, **+3 tax development** in Moscow, convert Moscow to your religion, and add a church if the script finds none. | Spawn **Orthodox zealots, scripted size 1**, in Moscow. Size is a rebel-spawn factor, not one regiment. |
| Allow the sack | **100 papal influence**, development-scaled ducats/MIL and the province’s available loot. | **+80 devastation**, **−2 tax, −2 production, −1 manpower**, each development component floored at 1; **size-3 separatist rebels** supporting Russia if it exists, otherwise Muscovy. The script does not convert Moscow in this option. |

The sack uses Moscow’s development before its reduction:

| Development | Ducats, excluding available province loot | MIL |
|---|---:|---:|
| Below 18 | 400 | 15 |
| 18–20 | 435 | 15 |
| 21–23 | 455 | 25 |
| 24–26 | 480 | 30 |
| 27–29 | 510 | 40 |
| 30–32 | 530 | 50 |
| 33+ | 550 | 55 |

The culture helper can supply DIP instead of accepting culture; that native helper outcome is separate from the explicit 100 DIP. No specific additional fallback amount is assumed here. The source localization invokes the Fourth Crusade as the knights’ analogy; that is the game’s narrative framing, not evidence that a historical Teutonic plan to sack Moscow existed.

### The Schism: recipient countries decide (`flavor_teu.38`)

Every eligible Orthodox recipient gets a choice:

- **Accept:** become Catholic; convert its capital if necessary; lose **1 stability and 30 prestige**.
- **Reject:** remain Orthodox and lose **2 stability**.

These costs affect the recipient, not the Teutonic player. Thus End the Schism is neither free conversion of every Orthodox province nor guaranteed conversion of every Orthodox state.

### Crusader Order constitution (`flavor_teu.39`)

- **Adopt now:** switch to a theocracy if necessary, unlock and enact `crusading_kingdom_reform`.
- **Keep current rules:** unlock the reform for later, gain **50 government reform progress**, and do not immediately enact it.

The reform fixes **kingdom rank** and grants **+1 percentage point missionary strength, +25% army tradition from battles and +2.5% discipline**. Rulers and heirs can be generals. It remains a monastic order and disallows ordinary religious conversion through the standard government setting. The normal eligibility is Catholic. These reform effects are conditional on keeping that reform, not extra independent permanent mission modifiers.

### Ottoman humiliation (`flavor_teu.40`)

This event has **one option**, not a menu of reward choices. Alongside 100 mission power projection and the permanent country modifier, it converts **all directly Ottoman-owned Christian, non-Catholic provinces to Catholic**, then gives **all directly Ottoman-owned Christian provinces +20 unrest for 10 years**. It does not convert Ottoman Muslim provinces, transfer land to you, or apply to every Ottoman subject’s province.

### Holy Horde (`flavor_teu.41`)

This event likewise has **one option**. It switches you to a theocracy if necessary and installs `holy_horde_reform`, whose benefits are:

- Fixed **empire rank**.
- A religious-enemy CB mechanic, **−10% cavalry cost**, **+10% movement speed**, **+1 missionary**, and **+2 percentage points missionary strength**.
- Rulers and heirs can be generals; continued monastic-order status; access to the **Horde idea group**.
- **With The Cossacks:** razing enabled. The installed defines use **0.33 Devotion per development razed** and a Devotion-razing power-reduction base at military technology **12**. The developer diary specifies that this theocratic form razes heathen/heretic land; the general engine’s province-eligibility checks are not reproduced by this research.
- **Without The Cossacks:** the event grants **permanent −10% core-creation cost** (`teu_holy_horde_modifier`) instead of relying on razing access.

The event also adds `holy_horde_capital` to the capital. Its **+25% manpower in true-faith provinces** is active when the owner has the Holy Horde reform **and has completed Religious ideas**. It is not an unconditional extra 25% on adopting the reform. The earlier cavalry mission’s stage-IV modifier remains separately active; the prior Crusader Order reform’s discipline bonus should not be counted as stacking with the replacement first-tier reform.

The event’s own narrative explicitly distinguishes this eastern route from other orders pursuing the Holy Land. A future Jerusalem branch can be added, but it would be **our new extension**, not restoration of a missing vanilla endpoint.

### Anti-Heresy Act: unlock versus enactment

The unlocked Clergy privilege gives **+2 percentage points missionary strength against heretics**, **+5 percentage points Clergy loyalty equilibrium**, and **+5 percentage points Clergy influence**. Costs: **−10 percentage points Burgher loyalty equilibrium** and normally **−5 maximum absolutism**; the script’s privilege-absolutism-reduction condition offsets 1 of that penalty where applicable.

It can be selected by eligible non-Orthodox/non-Coptic Christian states that own a same-religion-group heretic province. If Burgher Orthodox Tolerance is already enacted, granting this privilege removes it and immediately costs **20 Burgher loyalty**. The mission unlock itself neither pays nor imposes these enactment effects.

### Imperial protection: the opening diplomatic fork

Requesting protection starts an imperial incident with Emperor DLC; without it, the Emperor receives `flavor_teu.28`. The reply chain can:

1. **Admit without conditions** (`.29`): enter the HRE and set the permission-to-stay flag. In the direct `.28` branch, your opinion of the Emperor gains +100, decaying by 2/year; neighboring HRE members resent the Emperor by −150, decaying by 5/year.
2. **Offer conditional admission** (`.30`): accepting sets HRE membership and the probation flag unless the Crusader path has already been selected; a committed Crusader instead remains/ends outside. Rejecting exits the HRE if necessary and applies **−100 mutual opinions**, each decaying by 2/year.
3. **Reject admission** (`.31`): remain/leave outside; the direct reply chain applies **−100 opinions in both directions**, decaying by 2/year.

The opening mission’s independent refusal option was listed in its reward entry. The HRE probation/enforcement machinery is not an additional Crusader mission branch: committing to Crusader removes membership anyway. These options should be retained if the extension preserves the vanilla opening.

### Counter-Reformation access is a meaningful decision reward

The permanent unlock from Resist the Reformation bypasses the decision’s normal global-start and religion-age availability gates. It does **not** bypass Catholic religion, excluded ideas, absence of the Edict of Nantes modifier, or the Pope/Emperor/opinion eligibility checks. The decision still checks that the Counter-Reformation modifier is not already active.

Enacting the decision gives **+2 missionaries, +3 percentage points heretic missionary strength and +0.5 yearly papal influence**, balanced by **−2 heretic tolerance, +5% technology cost and +5% idea cost**. Its native modifier duration is permanent but is marked religion-dependent. This explains why “unlock a decision” is not equivalent to awarding unconditional missionary bonuses.

## The permanent-claim sequence

These are actual vanilla claim rewards, not proposed additions. Regions and areas use EU4’s map definitions.

| When completed | Permanent claims supplied for the next campaign |
|---|---|
| Expand our Army | Kuyavia + Wielkopolska areas |
| Confirm Crusader branch after Defeat Poland | Samogitia + Lithuania + Mazovia + Malopolska + Central Poland areas |
| Grant Clergy Privileges | Karelia + Novgorod + Pskov areas |
| Conquest of Novgorod | Moscow + Tver + Vladimir areas |
| Fall of the Third Rome | Russia region |
| First of Annex Lithuania / Conquer Poland | Ruthenia region; the second gives ADM compensation |
| Annex Lithuania | Crimea region |
| Christianize the Steppes | Circassia + Dagestan areas |
| Second of Christianize the Steppes / The Ruthenian Plains | Ural region; the first gives ADM compensation |
| Eliminate the Hordes | Central Asia region |

There is **no next-region permanent-claim grant at the Holy Horde endpoint**. That is a clean place for a future continuation to provide an opening objective and then claims toward its next theatre, while respecting existing ownership and religion checks.

## Military modifier ladder: replace, do not add together

| Stage | Cavalry ratio | Cavalry combat ability | Movement speed | Cavalry flanking | Yearly army tradition |
|---|---:|---:|---:|---:|---:|
| I: combat experience | +10 percentage points | — | — | — | +0.25 |
| II: reform | +10 percentage points | — | — | — | +0.75 |
| III: plains adaptation | +25 percentage points | +10% | +5% | — | +0.75 |
| IV: great cavalry | +50 percentage points | +15% | +10% | +50% | +1 |

The effective mission reward at stage IV is the **last row**, not the sum of all rows. Large cavalry-ratio or local-fort numbers are different mechanics from large national discipline/morale bonuses. An extension should budget the full existing package, including Holy Horde and temporary modifiers, before adding more combat power.

## How to extend this in the same design language

These are **our design conclusions from the source**, not claims about the author’s private intentions or implemented new missions.

1. **Preserve the existing opening and identity choice.** Do not replace survival against Poland with arbitrary early world-conquest goals. The existing commitment already grants claims, starts counters and makes government decisions consequential.
2. **Continue several branches at different speeds.** The Holy Horde, End the Schism, Defeat the Ottomans and Crush the Heresy are different end states. A continuation need not demand every vanilla mission first. Making all four mandatory would force an eastern campaign to wait for an independent European religious cleanup.
3. **Use conquest → conversion → consolidation → new frontier.** The installed tree often asks for some converted provinces in a region, not ownership of every province. Claims arrive before the next targeted conquest; cheaper fort operations follow completed fort construction.
4. **Retain independent internal tasks and branch joins.** Churches, income and Reformation resistance start independently, while military reform rejoins territorial progress. That creates parallel activity and occasional convergence without a solid wall of identical vertical chains.
5. **Use different kinds of payoff.** Advisors, temporary modifiers, province development, permanent local fort effects, decision/privilege access, ruler skills, scaled income, world events and reforms already coexist. Extra missions should extend this vocabulary rather than repeat small ADM payments.
6. **Make choice costs affect future objectives.** Moscow’s integration option makes conversion harder. That is a stronger event design than three interchangeable positive bonuses. Do not add a choice merely because a mission is difficult: the existing Ottoman and Holy Horde events intentionally have one outcome.
7. **Handle progress in either order.** The paired Ruthenia/Ural claim gates compensate the first/second branch appropriately. Future intersecting routes should avoid duplicate claims, expired prerequisites or requiring a tag that the player already destroyed.
8. **Earn a broader ambition through the established identity.** Eastward continuation follows directly from the Holy Horde narrative. A Holy Land or Mediterranean branch fits more naturally after the Caucasus/Ottoman line and needs an explicit new narrative bridge. Neither requires pretending that the historical Order had an actual unlimited world-conquest plan.

### Candidate attachment points for the next design pass

| Existing endpoint | Natural continuation theme | What the new first step should acknowledge |
|---|---|---|
| Crusaders of the Steppes | Further eastern campaigns and governing a vast missionary cavalry state | The player already has 100 cities, a large cavalry army and Holy Horde mechanics; another basic recruitment test would add little. |
| End the Schism | Administration and integration of the Russian Catholic sphere | Allies can satisfy the vanilla objective. Do not silently require annexation as the only valid continuation. |
| Defeat the Ottomans | Caucasus security, Anatolia, then a justified Levant/Holy Land route | The Ottomans may already be extinct; winning one war did not necessarily give the player land in Anatolia. |
| Construct Cathedrals / Castle Expertise | Religious institutions, frontier logistics and fiscal consolidation | The existing rewards already subsidize expensive infrastructure; avoid endless permanent cost reductions. |
| Crush the Heresy | A post-Reformation Catholic settlement | The mission concerns Protestant/Reformed ownership in Europe, not universal Catholic conversion. |

**Next step:** design a modest continuation against these exact attachment points, then review its claims, dependencies and cumulative reward budget before changing the playable mod. A count such as 100 or 250 should follow a convincing campaign structure, not determine it.

## Technical notes and verification boundary

- A current-technology fort means: military technology below 14 → castle or better; 14–18 → bastion or better; 19–23 → star fort or better; 24+ → fortress. The helper checks the **owner’s** military technology, including on qualifying subject-owned forts.
- `num_won_battles` is raised through the battle-won on-action helper only while the corresponding counting flag is set. At 20, the helper clears the flag and dispatches `.12`. The mission’s own effects do not issue that event a second time.
- `num_converted_religion` is an engine-maintained conversion statistic used by the mission. The mission does not reset it or maintain an owned-province list. Exact edge cases around engine counting were not tested by launching a campaign.
- Display highlights and completion triggers can differ. Crush the Heresy’s map highlighting includes owner-capital geography, but its actual trigger scans **European provinces and their owners’ religions**. The trigger is the authority in this reference.
- The document is a **source-verified research baseline**, not a new mod build or an in-game test. No game, save or launcher was opened.

### Supporting-source manifest

These SHA-256 fingerprints pin this research to the files actually inspected. Paths below link to this machine’s vanilla installation.

| Source | SHA-256 |
|---|---|
| `launcher-settings.json` | `333127cb22b594d54c5ddf3e0f3948f618660c6c78245aa24bd66738da55e5de` |
| `missions/SCA_Teutonic_Missions.txt` | `e1ca246cb218674d611c0879369a8736bf27ce105b16ed89bacd3cb80297ae9d` |
| `events/flavorTEU.txt` | `deecf55a854c60c7fe48f9d5feb41d3fd17e48393a71d715ae8a8821fc899a56` |
| `localisation/scandinavia_l_english.yml` | `097d769a41e548ecf1d6dfb36165f1d62ac6322b845e7098cb468acfecccc362` |
| `common/event_modifiers/01_mission_modifiers.txt` | `b4433805ef2b27ae25a5b059c4511812b47d99e1d00cb23f03044ef644137a3d` |
| `common/event_modifiers/00_event_modifiers.txt` | `7a4311ed75c953c21c9b4830094ff9d72dc02b250f21208b84ee77344aecffc5` |
| `common/opinion_modifiers/00_opinion_modifiers.txt` | `ecce70e5099dc2e6bd0f2acc17e702ee883d304e48860d2c207a84aa9e19802c` |
| `common/estate_privileges/01_church_privileges.txt` | `21138312dbfe887e690c58993d42679079d867daa129168353b95b008555ea3c` |
| `common/government_reforms/03_government_reforms_theocracies.txt` | `f71f736de04b23c98fa6c1db8299968bc7cc6030439f70e9f0542cbe4959714b` |
| `common/province_triggered_modifiers/00_modifiers.txt` | `c9769f31020ada79f8e5fbabcaf475da5b6e3279643ffbe4a9b35c826b69bb6f` |
| `common/scripted_triggers/00_scripted_triggers.txt` | `4dedcc7b7b091c2f51cf333f86ebb4044894018dc53a31c05eb8c2da05eaaf36` |
| `common/scripted_effects/00_scripted_effects.txt` | `a572f46852c539885bc59f3e0ba4dda2bc1110a54d04edc3daa2229a6e8577f3` |
| `common/scripted_effects/01_scripted_effects_for_on_actions.txt` | `1387882cc0864e98f33fd3461f15a53b52d23f89aa7b7c48ba217f28d84005dd` |
| `common/scripted_effects/02_scripted_effects_preview_missions.txt` | `74d070aebd4ff72a96c6b9e90ebc3a691eb626455c038781593553aa5ecd65f9` |
| `decisions/ReligiousConversion.txt` | `2c5c9c11a09f4566c5a3e667c96980e248d21401215d6ae368ec1e4215c5f0db` |
| `common/defines.lua` | `e3cf26836c70f8825a2ffd93160b2a09cdad29f78355787d07803138eb156f18` |

**Structural verification passed:** 32 unique source mission IDs; 32 condition/reward/design entries; all 32 prerequisite links resolve; dependency graph is acyclic; all 20 directly awarded mission modifier IDs resolve in the vanilla definitions; local source links exist. Event outcomes and numeric prose were reviewed against the linked scripts. These checks do not emulate the EU4 engine.
