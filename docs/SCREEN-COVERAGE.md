# Screen coverage ledger

[SCREEN-COVERAGE.csv](SCREEN-COVERAGE.csv) contains every one of the72 reference states, its PDF page, interactive link, PNG/continuations, candidate code owner and capability note. Code anchors identify the first place to investigate, not a claim that each proposed screen already exists.

Copy the CSV into the app's task documentation before work. Keep the reference copy immutable. Replace candidates with verified actual files, add implementation commits and screenshot/test paths, and update each row honestly. Proposed states with absent authority remain BLOCKED_CAPABILITY even when their unavailable presentation is designed. Do not delete rows or mark all rows done from a generic route smoke test.

Allowed workflow states: NOT_STARTED, MAPPED, IN_PROGRESS, IMPLEMENTED, VERIFIED, BLOCKED_CAPABILITY, BLOCKED_ENVIRONMENT. VERIFIED requires visual and behavior evidence at declared sizes; Windows device qualification is separate. A blocked row needs a concrete missing contract/environment and a next action. Add additional current app routes to a separate preserved-feature ledger; don't lose them because this design has 72 rows.
