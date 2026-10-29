#!/usr/bin/env python3
"""Bind a completed Phase 2 capture and rebuilt PDF to their editable inputs."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "phase-2-remaining-screens"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def identities(paths):
    return [{"path": str(path.relative_to(ROOT)),
             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in sorted(paths)]


report = read(ROOT / "artifacts/phase2-validation.json")
manifest = read(PHASE / "screen-manifest.json")
continuations = read(PHASE / "continuations.json")
responsive = read(PHASE / "responsive.json")
assert report["state"] == "PASS"
assert report["screens"] == len(manifest)
assert report["observations"] == len(manifest) * 3
assert all(check["state"] == "PASS" for check in report["interactions"])
assert report["action_outcomes"] and all(check["state"] == "PASS" for check in report["action_outcomes"])
inputs = list(PHASE.glob("*.js")) + list(PHASE.glob("*.css")) + list(PHASE.glob("*.html"))
inputs += [ROOT / "reference/design" / path for path in (
    "core.js", "design.css", "assets/brand-tokens.css", "assets/Inter.ttf", "assets/PlusJakartaSans.ttf")]
outputs = list((PHASE / "screens").glob("*.png")) + list((PHASE / "responsive").glob("*.png"))
outputs += [PHASE / "Biteaze-Windows-Phase-2-Reference.pdf", PHASE / "pdf-page-map.json"]
evidence = {
    "schema_version": 1,
    "scope": "Phase 2 design reference only; not application or Windows qualification",
    "capture_date": "2026-10-29",
    "state": "PASS",
    "screens": len(manifest),
    "layout_observations": report["observations"],
    "sizes": [[1920, 1080], [1366, 768], [1280, 720]],
    "seconds": report["seconds"],
    "mechanism": "Three concurrent viewport pages in one Chromium process, all states at all sizes; then all declared dialog/navigation/identity checks and every enabled workspace/dialog action",
    "interactions": report["interactions"],
    "action_outcomes": report["action_outcomes"],
    "full_hd_pngs": len(manifest) + len(continuations),
    "compact_pngs": len(responsive),
    "pdf_pages": len(read(PHASE / "pdf-page-map.json")),
    "inputs": identities(inputs),
    "outputs": identities(outputs),
    "native_validation": "NOT_MEASURED",
    "application_implementation": "NOT_STARTED",
}
(PHASE / "capture-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: evidence[key] for key in ("state", "screens", "layout_observations", "seconds", "full_hd_pngs", "compact_pngs", "pdf_pages")}))
