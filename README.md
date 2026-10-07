# EU4 Mod Workbench

A small workspace for extending country mission trees, inspecting them in an EU4-style HTML preview, and producing an installable mod. The first example is **The Order Without End**, a continuation of the Teutonic Crusader path: 32 original mission entries and 56 additions.

## Build and preview

Requires Python 3.9+ and your own EU4 installation. The included example was checked against **EU4 1.37.2** and requires **Lions of the North** for its mission route.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python eu4.py build teutonic
```

Open **`dist/teutonic/preview.html`** in a browser. On macOS:

```sh
open dist/teutonic/preview.html
```

Click any mission to see conditions, rewards, choices and historical context. The same viewer includes decisions and a campaign walkthrough. It uses the local game's frames, icons and grid. Marks in the planner are assumptions, not checks against your save.

The game path is detected in common Steam locations. Otherwise:

```sh
python eu4.py build teutonic --game "/path/to/Europa Universalis IV"
```

You can instead set `EU4_GAME_PATH` or create gitignored `local.json` containing `{"game":"/path/to/Europa Universalis IV"}`. A base-file fingerprint mismatch stops the build for a compatibility review.

## Install

Close EU4 and its launcher, then:

```sh
python eu4.py install teutonic
```

This rebuilds and checks the package, backs up an existing copy, and copies only `order_without_end` and its descriptor into the default EU4 Documents mod directory. Use `--user-dir "/path/to/EU4/user/directory"` if yours differs. It never launches the game, edits launcher databases, switches playsets, or disables other mods. Enable a new mod yourself in your chosen launcher playset.

For manual installation, copy these two items from `dist/teutonic/` into your EU4 user directory's `mod/` folder:

```text
order_without_end/
order_without_end.mod
```

The source folder `mods/teutonic/` is the editable project; `dist/teutonic/` is the generated, drop-in package. Keep native game files and generated previews local.

## Add another country

```sh
python eu4.py new france --tag FRA
python eu4.py build france
```

This creates two illustrative missions and a working preview. It is deliberately a **draft**, not a researched or safely integrated France extension. Review that country's native series, DLC/branch assignment and occupied rows, then configure the project before setting `draft` to false. The installer rejects drafts. Follow the generated country README and the Teutonic example's format, without copying its campaign design.

```text
AGENTS.md                  country-neutral guidance for a fresh AI session
CLAUDE.md -> AGENTS.md      the same instructions for Claude Code
workbench/                 shared build, checks, installer and existing HTML viewer
tests/                     structural regressions and optional browser checks
mods/teutonic/
  project.json             native integration, version pins and assignment fixtures
  missions.json            the 56 added missions, triggers, rewards and sources
  patch.py                 narrow country-specific native visibility change
  preview-content.json     authored baseline, event and decision explanations
  content/                 custom EU4 scripts, portraits and credited music
  assets/                  custom loading art and generation prompts
  docs/                    native-route research and extension reference
dist/<country>/             generated mod, HTML, data and verification report
.local/                    ignored local backups and migration archive
```

## Verification

```sh
python eu4.py test
python eu4.py build teutonic
python eu4.py check teutonic
```

The validator rejects conflicting series spans, undrawable native arrows, missing prerequisites, cycles, changed original missions, bad references and unguarded paid choices. It checks configured claim routes and branch assignments. See [verification coverage](docs/verification.md) for limits.

Optional browser regression test ([Playwright](https://playwright.dev/docs/library)):

```sh
npm ci
npx playwright install chromium
npm run test:preview
```

Or use installed Chrome with `PLAYWRIGHT_CHANNEL=chrome npm run test:preview`. Pass another HTML path with `npm run test:preview -- dist/france/preview.html`. The test inspects every mission reward panel, checklist gates, events and images; its screenshot stays alongside the generated HTML.

GitHub Actions runs game-independent checks only. Full local builds use your installed game; no game files, saves, databases or generated previews are shipped in this public repository. The migration retained older tools and high-resolution masters in a local ignored archive, while this repository contains the current source needed to reproduce the mod.

This tooling is not a campaign simulator. Successful offline checks do not prove engine rendering, balance, mod compatibility or old-save behavior. EU4 is never launched by these commands. Read [AGENTS.md](AGENTS.md) before asking an AI to extend the project, and [asset credits](THIRD_PARTY.md) before redistributing assets.
