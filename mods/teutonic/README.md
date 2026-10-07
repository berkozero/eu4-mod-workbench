# The Order Without End — Crusader Continuation

The first example in EU4 Mod Workbench extends the existing Teutonic Crusader campaign. It preserves 32 original mission entries and adds 56: eight optional support tasks and 48 continuation missions. Historical foundations, source links and clearly labeled fictional developments accompany the additions.

The extension covers northern chapters, Persia and India, Mongolia and China, the Mediterranean and Red Sea, Jerusalem and later institutions. Rewards mix sequential permanent claims, modest modifiers and 18 choice events. Four decisions include the restored useful recruitment/support options. This migration preserves the existing gameplay scripts; it is not another redesign.

## Use

Run these commands from the repository root:

```sh
python eu4.py build teutonic
python eu4.py install teutonic
```

Build first to inspect `dist/teutonic/preview.html`. Installation requires the game and launcher to be closed. It replaces only this mod's folder and descriptor, backs up the prior copy, and does not change playsets. Alternatively copy `dist/teutonic/order_without_end/` and `dist/teutonic/order_without_end.mod` together into your EU4 user directory's `mod/` folder.

The source folder is portable with the repository's shared tools. A generated package is directly usable by EU4 without Python. The package includes custom portraits, loading artwork, music, decisions and events; native mission files are merged from your local game at build time.

## Compatibility and branch behavior

- Reviewed against **EU4 1.37.2**; the manifest pins three native mission files. A changed base file stops compilation.
- Requires **Lions of the North** for the Crusader route. Other mods replacing the same native mission files can conflict; the workbench does not resolve arbitrary mod load orders.
- The Crusader tree is visible from the opening, but its missions still require choosing the Crusader path and satisfying the actual conditions. Visibility does not award claims or complete missions.
- The opening inspection contains 88 entries. After Crusader commitment, the optional Seek Imperial Protection entry disappears, leaving 87. The configured alternate Prussian assignment is preserved.
- Original mission positions, icons, prerequisites, rewards and world conditions remain intact, apart from the explicit branch completion gate for early visibility.
- The current layout uses 79 native arrows plus 21 earlier-milestone checklist requirements, preserving 100 logical parent relationships. Disconnected long arrows are not hidden behind browser-only routing.
- Custom loading art is expanded into the native rotation's filenames during build, avoiding the single-entry loading-selector crash. The opening music overrides `maintheme.ogg`; credited tracks join the music pool. Exact order still depends on the game and other active mods.

## Edit and research

[Native Crusader reference](docs/vanilla-crusader-path.md) documents all 32 original entries and their design. [Extension reference](docs/extension.md) lists all 56 additions, conditions, rewards and historical rationale. `missions.json` is the editable authority for additions; update the reference after design changes.

`content/` contains the current EU4 scripts and custom assets. `patch.py` is the narrowly scoped opening-visibility patch. `preview-content.json` contains human-written baseline/event/decision explanations. `assets/` contains the custom loading painting and generation prompts. Legacy `owe_` modifiers, localization and sprite assets remain for compatibility; the retired large mission tree is not active.

The local migration archive `.local/legacy-project/` preserves the old tools, source masters, prior reference pages and evidence. It is ignored and not available in a fresh public clone. Large redundant historical backups remain at the original project location. The public repository contains the current reproducible build inputs, shared tools and useful guidance.

## Verification record

During migration, all three compiled native mission ASTs matched the existing working mod. Event, decision, modifier, music and interface files were byte-identical. The new builder checked all 88 missions, 32 original entries, 17 configured claim routes and six assignment scenarios. Browser checks visited all mission reward panels and 18 events. Temporary installation tests preserved launcher and unrelated-mod state.

These are offline checks. EU4 was not opened for this migration; no new engine-runtime or campaign-balance claim is made. See the shared [verification coverage](../../docs/verification.md) and [AI instructions](../../AGENTS.md).
