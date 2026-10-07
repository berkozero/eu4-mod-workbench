# Shared agent instruction conventions

Reviewed against official documentation on 7 October 2026. There is no universal “2026 SOTA” certification for an instruction file; the useful standard is whether agents can discover it, act on its concrete rules and verify their work.

- **Single source:** `AGENTS.md` holds the instructions; `CLAUDE.md` is a relative symlink to it. Git records that link, so edits cannot leave the two agents with conflicting copies. This was checked as a filesystem/Git link, not by launching a fresh Claude session.
- **Scope:** root instructions are country-independent. Country research and content live under `mods/<country>/`; a new project extends its own native design.
- **Actionable context:** preserve project-specific pitfalls, exact validation commands, source-of-truth locations and runtime boundaries. Keep detailed design history outside the always-loaded file.
- **Maintenance:** keep the file concise, remove contradictory/stale rules, and verify linked paths. Instructions guide the model; software checks enforce only the specific properties they actually test.

OpenAI documents root-to-working-directory instruction discovery and the default 32 KiB combined limit in [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Anthropic recommends specific, verifiable, organized instructions, generally under 200 lines, in [How Claude remembers your project](https://code.claude.com/docs/en/memory). These informed the layout; they do not establish that this file is optimal for every agent or task.

Check the local setup with `ls -l CLAUDE.md`, `cmp AGENTS.md CLAUDE.md` and `git ls-files -s CLAUDE.md` (expected Git mode `120000`). Start the next agent session in this repository. On a system that checks out symlinks as plain text, restore symlink support before relying on automatic Claude instruction loading.
