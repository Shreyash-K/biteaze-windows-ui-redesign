#!/usr/bin/env python3
"""Build the public, source-backed Phase 2 coverage indexes."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "phase-2-remaining-screens"
WORKSPACE = ROOT.parents[1]
PINNED_REVISION = "7932bbbedabdd0cef4295919a91674f35fa815cf"
APPLICATION_REPOSITORY = "https://github.com/Shreyash-K/android-billing-desktop"
SOURCE_RE = re.compile(r"src/[A-Za-z0-9_./-]+\.(?:ts|tsx|js|json)")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def source_paths(value):
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
    return sorted(set(SOURCE_RE.findall(str(value or ""))))


def normalize(area, data):
    if data.get("area") == area and isinstance(data.get("entries"), list):
        return data
    rows = data.get("coverage") if area == "operations" else data.get("entries")
    result = []
    for index, row in enumerate(rows or [], 1):
        rendered = row.get("rendered_ids", row.get("screens", []))
        details = row.get("fields_and_actions", row.get("fields_actions"))
        if details is None:
            details = {"fields": row.get("fields", []), "actions": row.get("actions", [])}
        result.append({
            "number": row.get("number", index),
            "inventory_id": row["inventory_id"],
            "rendered_ids": rendered,
            "source_paths": source_paths(row.get("source")),
            "functionality": details,
            "missing": row.get("missing"),
            "implementation_status": "NOT_STARTED",
            "native_validation": "NOT_MEASURED",
        })
    return {"area": area, "source_revision": data.get("source_revision", PINNED_REVISION), "entries": result}


def load_inputs():
    inventory_dir = PHASE / "inventory"
    work = WORKSPACE / "work"
    specs = {
        "commerce": work / "phase2-commerce-coverage.json",
        "operations": work / "phase2-operations-coverage.json",
        "service": work / "phase2-service-coverage.json",
        "readiness": inventory_dir / "readiness.json",
    }
    normalized = {}
    for area, source in specs.items():
        public_copy = inventory_dir / f"{area}.json"
        chosen = source if source.exists() else public_copy
        if not chosen.exists():
            raise FileNotFoundError(f"Missing coverage input for {area}: {chosen}")
        normalized[area] = normalize(area, read_json(chosen))
        write_json(public_copy, normalized[area])
    return normalized


def build_source_map(paths, source_root):
    target = PHASE / "source-map.json"
    if source_root is None:
        if not target.exists():
            raise SystemExit("--source-root is required for the first source-map build")
        existing = read_json(target)
        recorded = {entry["path"] for entry in existing.get("files", [])}
        if recorded != set(paths):
            raise SystemExit("Recorded source-map paths differ; rerun with --source-root")
        return existing
    source_root = source_root.resolve()
    files = []
    for relative in sorted(paths):
        path = source_root / relative
        if not path.is_file():
            raise FileNotFoundError(f"Missing inspected application source: {relative}")
        payload = path.read_bytes()
        files.append({"path": relative, "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload)})
    result = {
        "schema_version": 1,
        "repository": APPLICATION_REPOSITORY,
        "revision": PINNED_REVISION,
        "local_changes_included": False,
        "content_included": False,
        "files": files,
    }
    write_json(target, result)
    return result


def page_numbers():
    path = PHASE / "pdf-page-map.json"
    if not path.exists():
        return {}
    rows = read_json(path)
    return {row["key"]: row["page"] for row in rows if row.get("key")}


def run(source_root):
    inputs = load_inputs()
    manifest = read_json(PHASE / "screen-manifest.json")
    manifest_ids = {screen["id"] for screen in manifest}
    requirements = []
    all_sources = set(source_paths(" ".join(str(screen.get("source", "")) for screen in manifest)))
    for area in ("commerce", "operations", "service", "readiness"):
        for row in inputs[area]["entries"]:
            unknown = sorted(set(row["rendered_ids"]) - manifest_ids)
            if unknown:
                raise ValueError(f"Unknown rendered IDs for {area}:{row['inventory_id']}: {unknown}")
            all_sources.update(row["source_paths"])
            requirements.append({
                "requirement_id": f"{area}:{row['inventory_id']}",
                "area": area,
                "inventory_number": row["number"],
                "inventory_id": row["inventory_id"],
                "rendered_ids": row["rendered_ids"],
                "source_paths": row["source_paths"],
                "functionality": row["functionality"],
                "missing": row["missing"],
                "implementation_status": "NOT_STARTED",
                "native_validation": "NOT_MEASURED",
            })
    coverage = {
        "schema_version": 1,
        "application": {"repository": APPLICATION_REPOSITORY, "revision": PINNED_REVISION},
        "scope": "Phase 2 visual reference coverage; not native application qualification",
        "inventory_requirement_count": len(requirements),
        "rendered_screen_count": len(manifest),
        "requirements": requirements,
    }
    write_json(PHASE / "requirements-coverage.json", coverage)
    build_source_map(sorted(all_sources), source_root)

    pages = page_numbers()
    csv_path = PHASE / "screen-coverage.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        fields = [
            "id", "title", "group", "kind", "number", "source", "png", "prototype_url", "pdf_page",
            "owner", "implemented_status", "implementation_evidence", "visual_status", "visual_evidence",
            "behavior_status", "behavior_evidence", "windows_device_status", "windows_device_evidence",
            "status", "native_validation",
        ]
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for screen in manifest:
            writer.writerow({
                "id": screen["id"], "title": screen["title"], "group": screen["group"],
                "kind": screen["kind"], "number": screen["number"], "source": screen["source"],
                "png": f"phase-2-remaining-screens/screens/{screen['number']:03d}-{screen['id']}.png",
                "prototype_url": f"phase-2-remaining-screens/index.html?screen={screen['id']}",
                "pdf_page": pages.get(screen["id"], ""),
                "owner": "UNASSIGNED",
                "implemented_status": "NOT_STARTED", "implementation_evidence": "",
                "visual_status": "NOT_MEASURED", "visual_evidence": "",
                "behavior_status": "NOT_MEASURED", "behavior_evidence": "",
                "windows_device_status": "NOT_MEASURED", "windows_device_evidence": "",
                "status": "NOT_STARTED", "native_validation": "NOT_MEASURED",
            })
    print(json.dumps({"requirements": len(requirements), "screens": len(manifest), "sources": len(all_sources), "pdf_pages_mapped": len(pages)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, help="Optional clean checkout of the pinned application revision")
    args = parser.parse_args()
    run(args.source_root)
