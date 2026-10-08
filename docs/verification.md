# Verification: what a pass means

## Checks without the game

`python eu4.py test` exercises the parser, full mission-series range conflicts, branch exclusivity, native arrow geometry, missing/cyclic prerequisites, loading-selector failure, invalid launcher enum, and copy-only installation into a temporary user directory. It also checks the example's authoring data for duplicate IDs, lost gates and inconsistent placement.

The installer test compares the launcher database and enabled-mod configuration byte for byte, and confirms an unrelated mod survives both first and repeated installation. It uses a tiny synthetic database, never the user's live launcher.

## Checks using your installed game

`python eu4.py build <country>` compiles into staging, checks the package, generates the HTML, then replaces the previous successful build. A failed check prevents publication of that build. `check` rechecks an already built package.

| Failure | Check |
|---|---|
| Tree cut off despite unique cells | Compare entire row spans for all active series in configured assignment fixtures |
| Disconnected arrows | Cross-column next-row rule; no occupied cells inside vertical skips |
| Layout repair drops a gate | Explicit arrow/checklist partition, compiled trigger equality, missing-parent truth cases |
| Hidden circular dependencies | Traverse mission references inside conditional and counted requirements |
| Vanilla behavior changed accidentally | Baseline coordinates, prerequisites, icons, rewards and allowed trigger differences |
| Wrong branch visible/completable | Tag/DLC/random-map/flag fixtures and retained path gate |
| Broken identifiers | Parse scripts; resolve referenced custom events, modifiers, buildings and map areas/regions |
| Impossible area count | Compare configured ownership thresholds with actual local map data |
| Claims arrive too late | Configured provider must be a logical ancestor; provider must contain claim metadata |
| Unaffordable event options | Explicit treasury trigger for direct treasury costs and an unconditional fallback |
| Stale event planner | Compare each option's condition/effect AST with its authored preview snapshot |
| Localization corruption | UTF-8 BOM, tested cp1252 character range, required mission localization keys |
| One-image loading crash | More than one effective DDS entry and no loading-directory replace_path |
| Launcher crash or other mods disabled | No writes to launcher state; copy and hash-verify only this mod; preserve configuration bytes |

Claims metadata and historical prose still require review against the actual reward script. Modifier stacking, diplomacy, religious policies, AI behavior, all conditional costs and all native trigger types are not exhaustively simulated. The assignment evaluator covers a deliberately limited vocabulary; unsupported conditions fail rather than guess. The configured primary mission file and any explicit `assignment_mission_files` are checked together; this does not reconstruct every other DLC/generic tree or third-party mod's assignment precedence.

## Browser checks

`npm run test:preview` loads the actual generated standalone file, visits every mission's requirements/rewards, tries missing remote gates and pure mission-count alternatives, inspects event labels, and checks images and JavaScript errors. A counted province condition is a world condition, not a counted mission condition. Inspect the screenshot as well: automated DOM checks cannot establish visual quality.

The planner reads compiled triggers/effects but only evaluates selected flags and mission state. It assumes unchecked world conditions; it does not spend ducats, simulate time, read saves or calculate wars. Conditional requirements remain visible. Unknown world conditions are marked for checking in-game.

## Runtime handoff

Do not start EU4 or its launcher without explicit user authorization. When authorized, test a new campaign with the relevant DLC and a controlled playset, inspect opening and committed branches, inspect bottom-of-tree arrows and tooltips, and compare fresh game logs with the exact built package. Record the version and what was actually observed. Do not present an older campaign test as verification of a newer build.
