#!/usr/bin/env python3
"""Validate the complete Phase 2 public reference package."""
import argparse
import csv
import hashlib
import json
import re
import struct
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "phase-2-remaining-screens"
EXPECTED_REVISION = "7932bbbedabdd0cef4295919a91674f35fa815cf"
STARTED = time.perf_counter()
CHECKS, FAILURES = 0, []


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        FAILURES.append(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def png_size(path):
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Invalid PNG: {path}")
    return struct.unpack(">II", data[16:24])


def run(source_root=None, allow_pending_pdf=False):
    excluded_fixture_names = ('Viral Patiyala', 'Browffle', 'Aarav Sharma', 'Alex Kumar', 'Aman Verma', 'Riya Shah', 'Dev Mehta', 'Aarav Shah', 'Raj Malhotra')
    for source in sorted(PHASE.glob('*.js')):
        text = source.read_text(encoding='utf-8')
        check(not any(name.casefold() in text.casefold() for name in excluded_fixture_names), f"Non-synthetic fixture in {source.name}")
    manifest = read_json(PHASE / "screen-manifest.json")
    ids = [row["id"] for row in manifest]
    check(len(manifest) == 214, "Expected 214 rendered screens")
    check(len(set(ids)) == 214, "Rendered screen IDs must be unique")
    check([row["number"] for row in manifest] == list(range(73, 287)), "Screen numbers must be 73–286")
    check([row["phaseNumber"] for row in manifest] == list(range(1, 215)), "Phase numbers must be 1–214")
    id_set = set(ids)

    coverage = read_json(PHASE / "requirements-coverage.json")
    requirements = coverage["requirements"]
    check(len(requirements) == 174, "Expected 174 inventory requirements")
    check(len({row["requirement_id"] for row in requirements}) == 174, "Requirement routes must be unique")
    check(Counter(row["area"] for row in requirements) == {"commerce": 57, "operations": 55, "service": 57, "readiness": 5}, "Area denominators")
    routed_ids = {screen_id for row in requirements for screen_id in row["rendered_ids"]}
    check(routed_ids == id_set - {"phase2-overview"}, "Every non-directory screen must resolve from inventory coverage")
    for row in requirements:
        check(bool(row["rendered_ids"]), f"Requirement has no rendered route: {row['requirement_id']}")
        check(not (set(row["rendered_ids"]) - id_set), f"Unknown rendered route: {row['requirement_id']}")
        check(row["missing"] in (None, [], "none", "None"), f"Unresolved coverage: {row['requirement_id']}")
        check(row["implementation_status"] == "NOT_STARTED", f"Implementation claim: {row['requirement_id']}")
        check(row["native_validation"] == "NOT_MEASURED", f"Native validation claim: {row['requirement_id']}")

    with (PHASE / "screen-coverage.csv").open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        expected_columns = [
            "id", "title", "group", "kind", "number", "source", "png", "prototype_url", "pdf_page",
            "owner", "implemented_status", "implementation_evidence", "visual_status", "visual_evidence",
            "behavior_status", "behavior_evidence", "windows_device_status", "windows_device_evidence",
            "status", "native_validation",
        ]
        check(reader.fieldnames == expected_columns, "Screen coverage ledger columns")
    check(len(rows) == 214, "Expected 214 screen coverage rows")
    check([row["id"] for row in rows] == ids, "Coverage rows must follow manifest order")
    for screen, row in zip(manifest, rows):
        check(int(row["number"]) == screen["number"], f"Coverage number: {screen['id']}")
        check(row["title"] == screen["title"] and row["group"] == screen["group"] and row["kind"] == screen["kind"], f"Coverage identity: {screen['id']}")
        check(row["prototype_url"].endswith("?screen=" + screen["id"]), f"Prototype route: {screen['id']}")
        check(row["status"] == "NOT_STARTED" and row["native_validation"] == "NOT_MEASURED", f"Honest status: {screen['id']}")
        check(row["owner"] == "UNASSIGNED", f"Unclaimed implementation owner: {screen['id']}")
        check(row["implemented_status"] == "NOT_STARTED", f"Implementation status: {screen['id']}")
        check(row["visual_status"] == "NOT_MEASURED", f"Visual status: {screen['id']}")
        check(row["behavior_status"] == "NOT_MEASURED", f"Behavior status: {screen['id']}")
        check(row["windows_device_status"] == "NOT_MEASURED", f"Windows device status: {screen['id']}")
        check(not any(row[name] for name in ("implementation_evidence", "visual_evidence", "behavior_evidence", "windows_device_evidence")), f"Evidence must remain empty before measurement: {screen['id']}")
        png = ROOT / row["png"]
        check(png.is_file(), f"Missing primary PNG: {screen['id']}")
        if png.is_file():
            check(png_size(png) == (1920, 1080), f"Primary PNG dimensions: {screen['id']}")

    primary = list((PHASE / "screens").glob("*.png"))
    primary = [p for p in primary if "-continued-" not in p.stem]
    check(len(primary) == 214, "Expected exactly 214 primary PNGs")

    continuations = read_json(PHASE / "continuations.json")
    continuation_files = {row["file"] for row in continuations}
    actual_continuations = {p.name for p in (PHASE / "screens").glob("*-continued-*.png")}
    check(continuation_files == actual_continuations, "Continuation index must match files")
    continuation_indices = defaultdict(list)
    for row in continuations:
        check(row["screen"] in id_set, f"Unknown continuation screen: {row['screen']}")
        path = PHASE / "screens" / row["file"]
        check(path.is_file() and png_size(path) == (1920, 1080), f"Continuation dimensions: {row['file']}")
        continuation_indices[row["screen"]].append(row["index"])
    for screen, values in continuation_indices.items():
        check(sorted(values) == list(range(1, len(values) + 1)), f"Continuation sequence: {screen}")

    responsive = read_json(PHASE / "responsive.json")
    responsive_files = {row["file"] for row in responsive}
    actual_responsive = {p.name for p in (PHASE / "responsive").glob("*.png")}
    check(responsive_files == actual_responsive, "Responsive index must match files")
    sizes_by_screen = defaultdict(set)
    for row in responsive:
        size = tuple(row["size"])
        path = PHASE / "responsive" / row["file"]
        check(row["screen"] in id_set, f"Unknown responsive screen: {row['screen']}")
        check(size in {(1280, 720), (1366, 768)}, f"Unexpected responsive size: {row['file']}")
        check(path.is_file() and png_size(path) == size, f"Responsive dimensions: {row['file']}")
        sizes_by_screen[row["screen"]].add(size)
    for screen, sizes in sizes_by_screen.items():
        check(sizes == {(1280, 720), (1366, 768)}, f"Responsive pair: {screen}")

    source_map = read_json(PHASE / "source-map.json")
    check(source_map["revision"] == EXPECTED_REVISION, "Pinned source revision")
    check(source_map.get("content_included") is False and source_map.get("local_changes_included") is False, "Source metadata boundaries")
    source_entries = source_map["files"]
    expected_sources = {screen["source"] for screen in manifest}
    expected_sources.update(path for row in requirements for path in row["source_paths"])
    check({row["path"] for row in source_entries} == expected_sources, "Source map must cover every inspected source path")
    check(len({row["path"] for row in source_entries}) == len(source_entries), "Unique source metadata paths")
    for row in source_entries:
        check(bool(re.fullmatch(r"src/[A-Za-z0-9_./-]+\.(?:ts|tsx|js|json)", row["path"])), f"Safe source path: {row['path']}")
        check(bool(re.fullmatch(r"[0-9a-f]{64}", row["sha256"])), f"Source hash format: {row['path']}")
        check(isinstance(row["bytes"], int) and row["bytes"] > 0, f"Source size metadata: {row['path']}")
        if source_root:
            path = source_root / row["path"]
            check(path.is_file(), f"Source exists: {row['path']}")
            if path.is_file():
                check(hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], f"Source hash: {row['path']}")
    all_text = "\n".join((PHASE / name).read_text(encoding="utf-8") for name in ["requirements-coverage.json", "source-map.json", "screen-coverage.csv"])
    check("/Users/" not in all_text and "work/windows-app-remote" not in all_text, "No private local paths")
    copied_product = [p for p in PHASE.rglob("*") if p.is_file() and p.suffix in {".ts", ".tsx"}]
    check(not copied_product, "Application source must not be copied into the reference package")

    evidence = read_json(PHASE / "capture-evidence.json")
    check(evidence["state"] == "PASS" and evidence["screens"] == 214 and evidence["layout_observations"] == 642, "Complete capture denominator")
    check(len(evidence["interactions"]) == 112 and all(row["state"] == "PASS" for row in evidence["interactions"]), "All declared capture interactions passed")
    check(len(evidence.get("action_outcomes", [])) == 462 and all(row["state"] == "PASS" for row in evidence["action_outcomes"]), "All enabled capture actions have an observable outcome")
    check(evidence["native_validation"] == "NOT_MEASURED" and evidence["application_implementation"] == "NOT_STARTED", "Capture scope is reference-only")
    for entry in evidence["inputs"] + evidence["outputs"]:
        path = (ROOT / entry["path"]).resolve()
        check(path.is_relative_to(ROOT) and path.is_file(), f"Capture asset exists: {entry['path']}")
        if path.is_relative_to(ROOT) and path.is_file():
            check(hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"], f"Stale capture evidence: {entry['path']}")

    page_map_path = PHASE / "pdf-page-map.json"
    if page_map_path.exists():
        page_map = read_json(page_map_path)
        keyed = [row for row in page_map if row.get("key") in id_set]
        counts = Counter(row["key"] for row in keyed)
        check(set(counts) == id_set and all(value == 1 for value in counts.values()), "PDF map must contain every screen exactly once")
        page_by_id = {row["key"]: row["page"] for row in keyed}
        for row in rows:
            check(str(page_by_id.get(row["id"], "")) == row["pdf_page"], f"CSV PDF page: {row['id']}")
        pages = [row["page"] for row in page_map]
        check(pages == list(range(1, len(page_map) + 1)), "PDF page map sequence")
        pdfs = list(PHASE.glob("*.pdf"))
        check(len(pdfs) == 1, "Expected one Phase 2 PDF")
        if len(pdfs) == 1:
            try:
                from pypdf import PdfReader
                check(len(PdfReader(pdfs[0]).pages) == len(page_map), "PDF page count must match page map")
            except ImportError:
                check(False, "pypdf is required for final PDF validation")
    else:
        check(allow_pending_pdf, "Missing Phase 2 PDF page map")
        check(all(not row["pdf_page"] for row in rows), "PDF pages must remain blank while page map is pending")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--allow-pending-pdf", action="store_true")
    args = parser.parse_args()
    try:
        run(args.source_root.resolve() if args.source_root else None, args.allow_pending_pdf)
    except Exception as exc:
        FAILURES.append(f"{type(exc).__name__}: {exc}")
    report = {
        "scope": "Phase 2 distributed reference package; not native application qualification",
        "checks": CHECKS, "failures": FAILURES,
        "seconds": round(time.perf_counter() - STARTED, 3),
        "state": "FAIL" if FAILURES else "PASS",
    }
    (ROOT / "artifacts").mkdir(exist_ok=True)
    (ROOT / "artifacts/phase2-package-validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))
    sys.exit(1 if FAILURES else 0)
