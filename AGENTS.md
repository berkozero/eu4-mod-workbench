# EU4 Mod Workbench: instructions for a fresh AI session

## Start here

Read README.md, then the selected `mods/<country>/README.md`, `project.json`, and `missions.json`. Read its country patch and the scripts you will change. Inspect `git status` before editing; preserve unrelated work. General tools live in `workbench/`; country rules belong under `mods/<country>/`.

This repository is a small builder, validator and HTML inspector. Extend it only when an actual country task requires it. Do not introduce a framework, server, database or package manager beyond the existing optional browser test.

## Source of truth

- Edit `missions.json` for new mission IDs, prerequisites, placement, conditions, rewards and historical roots. Edit `content/` for events, decisions, modifiers, localization and custom assets. Never edit generated `dist/` as the lasting fix.
- Read the user's installed game files before changing native missions. `base_sha256` pins the reviewed version; a mismatch requires a real compatibility review, not just replacing hashes.
- Preserve original mission icons, coordinates, prerequisites, conditions and rewards unless the user explicitly requests a change. A project's `patch.py` must make exceptions narrow and reviewable.
- Native files and art are loaded locally at build time. Keep full base-game files, screenshots containing native art, generated previews, disassembly, saves, logs, launcher databases and personal paths out of public commits.
- Authored prose in `preview-content.json` is not an engine. Update it with script changes. Event option AST parity fails the build when option conditions/rewards drift; mission and decision ASTs are read from the compiled mod. Human-readable summaries still need editorial review.

## Mission structure: prevent the actual failures

1. Validate the whole active tree, not just each new mission. Two series in one slot conflict across their full minimum-to-maximum row ranges even when their occupied cells differ. Prefer extending the native series. Check opening, branch flags, alternate branches, country tags, DLC and map variants.
2. Separate logical prerequisites (`parents`) from engine arrows (`arrowParents`) and explicit checklist gates (`checklistParents`). The latter two must partition the former exactly. Never drop a condition to fix a picture.
3. For the tested native renderer, cross-column arrows must arrive in the next row. Same-column arrows may skip empty rows but cannot pass through occupied mission cells. Do not invent browser-only bends to hide native defects. Restore the logical layout before polishing a screenshot.
4. A remote prerequisite can be a top-level `mission_completed` trigger, displayed as an earlier milestone. This must be an explicit author decision, not a silent repair. Negative tests must prove the mission cannot complete with that milestone missing.
5. Check cycles including mission references inside OR/count conditions. Never turn “any two branches” into “all four.” Distinguish counted missions from counted provinces.
6. Visibility is not completion. Showing a branch at the start must preserve its path-choice and world-condition requirements. Include assignment fixtures for alternate choices. A draft for another country cannot be installed until native integration has been reviewed.

The shared assignment evaluator intentionally supports a small set of conditions and rejects unknown ones. It does not model the whole engine's selection priorities or all other installed mods. Add targeted fixtures when supporting a new native layout, and document coverage honestly.

## Progression and historical design

- Give claims before the next territorial objective. Check the provider is an ancestor and the areas/regions exist; also review the actual provinces and subject rules manually.
- Alternate conquest, conversion, diplomacy, administration, army reform and institutions. Difficulty should grow with the campaign, with optional branches and meaningful merges.
- Compare bonuses to native missions and consider cumulative stacking. Use modest temporary modifiers, useful claims and occasional permanent institutional rewards. Avoid repetitive mana packets or large percentage boosts without a native benchmark.
- Make hard milestones lead to events with coherent choices. Paid choices need affordability triggers and at least one free fallback. Choice rewards are alternatives, not a combined list of bonuses.
- Decisions must have a visible purpose, correct potential versus allow conditions, costs, cooldowns and a payoff. Avoid farmable one-time rewards, contradictory flags and redundant buttons.
- Each historical claim needs a source link. Label fictional continuation and explain how it develops a historical institution or an existing native campaign theme. Do not present invented imperial plans as historical intentions.

## Assets, encoding and installation

- Preserve native assets by reference. Add custom portraits with a consistent period, palette and readable silhouette; keep prompts and music credits. Do not claim modern atmospheric tracks are authentic historical recordings.
- Localization uses UTF-8 with BOM and the tested game's cp1252-compatible characters. Normalize unsupported minus signs. Check identifiers and sprite references, not just encoding.
- Never hide the native loading directory with `replace_path`. The tested loading selector fails with only one effective DDS entry. Keep at least two effective filenames; use a single custom source image to generate the rotation locally.
- Never open EU4 or its launcher without the user's explicit instruction. Offline checks do not authorize a runtime test.
- Use the copy-only installer with both processes closed. Back up only the mod being replaced; preserve every unrelated mod, playset, active selection, `dlc_load.json` and launcher database.
- Do not write launcher SQLite. An earlier installer caused a UI crash by storing `manual` where the launcher expected `custom`; a healthy SQLite integrity check did not detect the invalid application enum. The current installer avoids that integration entirely.
- Do not promise old-save compatibility after changing mission assignment. Offer a new campaign when the user authorizes runtime checking.

## Required verification and handoff

Run `python eu4.py test`, then `python eu4.py build <country>`. For changes to the preview, run the optional Playwright test against the generated HTML and inspect its screenshot. Use a temporary EU4 user directory to exercise installation; do not use the live installation as a test fixture.

The build checks syntax, assignment fixtures, full series spans, dependency cycles, drawable arrows, prerequisite equivalence, native preservation, references, attainable region counts, claim ordering, paid choices and localization. Tests encode the previous structural, loading and launcher failures. CI runs game-independent regressions and source-data checks; native compatibility and browser rendering require a local game installation.

When handing off, give the exact preview/package paths and commands, what passed, and what was not tested. Do not call HTML planning marks, successful parsing, or a previous user's campaign report proof that this exact build ran in the game. Never remove failing checks just to ship a package.
