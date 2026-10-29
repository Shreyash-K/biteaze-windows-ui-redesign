# Start here

1. Sign in to GitHub with access to **both** private repositories: this reference repository and `Shreyash-K/android-billing-desktop`.
2. Open the existing app checkout in Antigravity. Clone this reference repository into a sibling directory, or let the starting prompt do that. Keep app source and reference files distinct.
3. Paste `GEMINI-START-PROMPT.md`. The prompt requires Gemini to read this kit, inspect the current application, set ownership for a team of subagents, implement the design in phases, and verify the result.
4. Review the finished app screenshots, coverage ledger and test evidence before release. A local implementation is not evidence that printers, payment providers or real Windows hardware work.

## Clean setup (only when no existing application checkout needs preserving)

```sh
git clone https://github.com/Shreyash-K/android-billing-desktop.git
git clone https://github.com/Shreyash-K/biteaze-windows-ui-redesign.git
```

Open `android-billing-desktop` as the application workspace. Do not clone over an existing directory. With an existing checkout, read status and local coordination files first. If it has active work, use a separate clean clone/worktree and record the excluded changes; do not reset, stash, commit, or push someone else's changes.

## Context that survives a long session

`GEMINI.md` is the short context entry point. The coordinator should read it explicitly and merge its reference pointer into the app's existing agent instructions without replacing them. Copy `templates/IMPLEMENTATION-TRACKER.md` and `docs/SCREEN-COVERAGE.csv` into the app's task documentation and maintain them there. On context compaction or worker restart, read the tracker first, then only the required code map and screen rows. Each worker receives paths and scope explicitly; don't rely on inherited chat memory.

Antigravity surfaces/versions differ. Plain Markdown instructions and the pasted prompt are authoritative for this handoff. This repository also includes `.agents/rules/biteaze-redesign.md` and the legacy `.agent/rules/biteaze-redesign.md` as small pointers. Their placement in the reference repository does not automatically apply them to a separate app workspace. Merge a pointer into the actual app workspace if needed, preserving existing rules. See `docs/ANTIGRAVITY-SETUP.md`.

## What completion means

All 72 rows need an honest disposition and implementation evidence. Reuse every supported production flow and design its normal/error/pending states. Preserve current features outside the screenshot set using the same components. If a proposed screen needs absent backend authority, implement the available UI state, label unavailable behavior truthfully, document the missing contract, and continue independent work. That row stays blocked; do not claim the entire app is complete.

Work through the phases in one continuing session where possible. If credentials, hardware, approval, or runtime limits prevent verification, leave an exact resume point with completed work preserved. Never shorten coverage to claim a single-session finish.
