# EU4 Mod Workbench: instructions for a fresh AI session

`AGENTS.md` is the canonical instruction file. Keep `CLAUDE.md -> AGENTS.md` as a relative symlink; edit this file, never maintain two copies. These rules apply throughout this repository. Explicit user task instructions take precedence over repository defaults.

## Start here

Read README.md, then the selected `mods/<country>/README.md`, `project.json`, and `missions.json`. Read its country patch and the scripts you will change. Inspect `git status` before editing; preserve unrelated work. General tools live in `workbench/`; country rules belong under `mods/<country>/`.

This repository is a small builder, validator and HTML inspector. Extend it only when an actual country task requires it. Do not introduce a framework, server, database or package manager beyond the existing optional browser test.

## Design principle: understand the original, then extend it

The default task is a continuation of the country's existing mission tree. Preserve its identity and make additions feel authored by the same designer. A new country project is an extension workspace, not permission to invent a replacement campaign. Replace a native tree only when the user explicitly requests that scope.

Before designing additions, read every mission in the relevant native route and its linked events, decisions, modifiers and branch-selection logic. Record the mission IDs, predecessors, exact conditions, rewards/durations, claim regions and source/version in a country-local Markdown reference. Explain the original design's military, religious, diplomatic and institutional themes, its difficulty curve, and how each reward prepares the next objective. Separate observations from interpretation.

For each proposed addition, identify its native predecessor or design analogue and explain **why this condition -> this reward -> this next step** fits that route. Usually continue beyond existing endpoints; add only a few useful optional intermediate tasks. Preserve original objectives, choices and branch variety. Avoid a disconnected new campaign, arbitrary checklist thresholds, symmetric filler columns, repetitive rewards or cosmetic references with unrelated gameplay.

Read the resulting campaign in order as a player: confirm earlier rewards support later requirements, permanent claims precede conquests, subject/religion rules stay coherent, and alternate routes remain possible. Benchmark reward strength and duration against comparable original missions, including the accumulated bonuses already earned. Put this design rationale in the country's reference, not in the shared tooling.

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

## Mission images, startup/loading screen and music

- Every added mission needs a deliberate, relevant image. Inspect original portraits from that route first and match their painterly style, palette, period, composition and native framing. Preserve all original mission images unchanged. Prefer distinct custom illustrations for new missions; placeholders must be labeled as draft work.
- Inspect custom portraits at the actual in-game display size, not just full resolution: clear silhouette, correct heraldry, no lettering, baked-in UI frames or modern/fantasy details. Reuse the repository's art prompts and save new prompts/provenance. Verify each mission icon resolves through its `.gfx` definition to a decodable asset, and inspect it in the generated HTML.
- Carry the project's pre-game presentation through the build: custom startup/loading artwork, its initializer image where used, an opening/main-menu theme, and the registered in-game music. Preserve the existing assets during migration or extension unless replacements are requested. New country presentations must fit that country's original identity; do not copy another country's imagery or music blindly.
- Keep one canonical custom loading painting under the country assets directory, preserve aspect ratio and space for loading text, then let the builder generate the required loading filenames. Never hide the native loading directory with `replace_path`; keep at least two effective DDS entries to avoid the tested selector crash.
- Use only music with documented redistribution rights. Keep composer, track/source, license and modifications in the shipped credits. Verify Ogg files, `.asset` registrations, song names/weights and the `music/maintheme.ogg` opening-theme override. Favor the requested custom opening presentation using the existing mechanisms; do not guarantee first-play order without an authorized runtime check, since other mods and engine behavior can affect it.
- Modern medieval-inspired tracks are atmosphere, not proof of authentic historical music. Verify source and compiled asset presence, image decoding, audio format and opening-theme mapping without launching EU4. Report any runtime uncertainty separately.

## Encoding and installation

- Localization uses UTF-8 with BOM and the tested game's cp1252-compatible characters. Normalize unsupported minus signs. Check identifiers and sprite references, not just encoding.
- Never open EU4 or its launcher without the user's explicit instruction. Offline checks do not authorize a runtime test.
- Use the copy-only installer with both processes closed. Back up only the mod being replaced; preserve every unrelated mod, playset, active selection, `dlc_load.json` and launcher database.
- Do not write launcher SQLite. An earlier installer caused a UI crash by storing `manual` where the launcher expected `custom`; a healthy SQLite integrity check did not detect the invalid application enum. The current installer avoids that integration entirely.
- Do not promise old-save compatibility after changing mission assignment. Offer a new campaign when the user authorizes runtime checking.

## Required verification and handoff

From the repository root, use the configured virtual environment (`source .venv/bin/activate`; setup is in README.md). For code or content changes run `python eu4.py test`, then `python eu4.py build <country>`. For instruction-only changes verify the symlink, referenced paths/commands and public audit; a new game build is unnecessary. For changes to the preview, run the optional Playwright test against the generated HTML and inspect its screenshot. Use a temporary EU4 user directory to exercise installation; do not use the live installation as a test fixture.

The build checks syntax, assignment fixtures, full series spans, dependency cycles, drawable arrows, prerequisite equivalence, native preservation, references, attainable region counts, claim ordering, paid choices and localization. Tests encode the previous structural, loading and launcher failures. CI runs game-independent regressions and source-data checks; native compatibility and browser rendering require a local game installation.

When handing off, give the exact preview/package paths and commands, what passed, and what was not tested. Do not call HTML planning marks, successful parsing, or a previous user's campaign report proof that this exact build ran in the game. Never remove failing checks just to ship a package.

Keep this file concise and project-specific. Put detailed research under the country docs and verification details in [docs/verification.md](docs/verification.md). Remove obsolete or contradictory rules as the workflow changes. See [instruction conventions and sources](docs/agent-instructions.md) for the documentation review.
