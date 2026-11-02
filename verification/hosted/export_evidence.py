#!/usr/bin/env python3
"""Export small exact JSON evidence and separately bounded visual review crops."""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import io
import json
import re
import tarfile
from pathlib import Path


def pack(label: str, files: dict[str, bytes], note: dict) -> bytes:
    manifest = {"schema_version": 1, "label": label,
                "transport": "base64-tar-gzip-public-evidence", **note,
                "files": [{"path": name, "size_bytes": len(data),
                           "sha256": hashlib.sha256(data).hexdigest()}
                          for name, data in sorted(files.items())]}
    entries = {**files, "transport-manifest.json": (json.dumps(manifest, indent=2) + "\n").encode()}
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for name, data in sorted(entries.items()):
            info = tarfile.TarInfo(name)
            info.size, info.mode, info.mtime = len(data), 0o644, 0
            archive.addfile(info, io.BytesIO(data))
    return gzip.compress(raw.getvalue(), compresslevel=9, mtime=0)


def emit(label: str, packed: bytes, files: int) -> None:
    encoded = base64.b64encode(packed).decode("ascii")
    chunks = [encoded[i:i + 48000] for i in range(0, len(encoded), 48000)]
    meta = {"label": label, "parts": len(chunks), "bytes": len(packed),
            "sha256": hashlib.sha256(packed).hexdigest(), "files": files}
    print("HOSTED_BUNDLE_META " + json.dumps(meta, separators=(",", ":")), flush=True)
    for i, chunk in enumerate(chunks, 1):
        print(f"HOSTED_BUNDLE_PART {label} {i:05d}/{len(chunks):05d} {chunk}", flush=True)
    print("HOSTED_BUNDLE_END " + label + " " + meta["sha256"], flush=True)


def json_evidence(root: Path) -> dict[str, bytes]:
    allowed = [p for p in root.iterdir() if p.is_file() and (
        p.name in {"hosted-report.json", "math-source.json", "math-contract.json"} or
        p.name.startswith("math-capture-") or p.name.startswith("math-result-"))]
    if any(p.is_symlink() for p in allowed):
        raise ValueError("Evidence files must not be symbolic links")
    return {p.name: p.read_bytes() for p in allowed}


def review_evidence(root: Path, quality: int, positions: tuple[str, ...]) -> dict[str, bytes]:
    from PIL import Image
    captures = {}
    for path in root.glob("math-capture-*.json"):
        capture = json.loads(path.read_text())
        for page in capture["pages"]:
            name = page.get("artifacts", {}).get("screenshot")
            if name:
                captures[name] = page
    records, files = [], {}
    for name, page in sorted(captures.items()):
        original = root / name
        if original.is_symlink() or Path(name).name != name:
            raise ValueError("Unsafe screenshot path")
        data = original.read_bytes()
        image = Image.open(io.BytesIO(data)).convert("RGB")
        width, height = image.size
        available = [m.get("geometry", {}).get("available_width") for m in page["math"]]
        available = [v for v in available if isinstance(v, (int, float)) and v > 0]
        left = max(0, int(width - max(available) - 96)) if available else 0
        tile_height = min(1000, height)
        offsets = {"first": min(260, height - tile_height),
                   "middle": max(0, (height - tile_height) // 2),
                   "last": max(0, height - tile_height)}
        used = set()
        for position in positions:
            top = offsets[position]
            if top in used:
                continue
            used.add(top)
            box = [left, top, width, top + tile_height]
            crop = image.crop(tuple(box))
            stream = io.BytesIO()
            crop.save(stream, format="JPEG", quality=quality, optimize=True, subsampling=0)
            output = "review-" + Path(name).stem + "-" + position + ".jpg"
            files[output] = stream.getvalue()
            records.append({"path": output, "source_page": page["path"],
                            "url": page["url"], "original_screenshot": name,
                            "original_sha256": hashlib.sha256(data).hexdigest(),
                            "original_size": [width, height], "crop_box_xyxy": box,
                            "region": position, "jpeg_quality": quality,
                            "sha256": hashlib.sha256(files[output]).hexdigest()})
    manifest = {"schema_version": 1, "kind": "derived_visual_review_crops",
                "source": "Actual collector PNG screenshots; full originals remain in the complete Actions artifact.",
                "coverage": "Selected first-body, middle and last regions, not every pixel of every source page.",
                "collector_report_altered": False, "records": records}
    files["review-manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--mode", choices=("json", "review"), default="json")
    parser.add_argument("--max-mib", type=int, default=4)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9_-]{1,32}", args.label) or not 1 <= args.max_mib <= 32:
        parser.error("Use a short lowercase label and a size cap between 1 and 32 MiB")
    root = Path(args.root)
    if not (root / "hosted-report.json").is_file():
        print("HOSTED_BUNDLE_ABSENT " + args.label)
        return 0
    limit = args.max_mib * 1024 * 1024
    if args.mode == "json":
        files = json_evidence(root)
        packed = pack(args.label, files, {"mode": "json", "excluded_reproducible_files": ["*.html", "expected-mathml.json", "*.png"]})
        if len(packed) > limit:
            raise ValueError(f"Exact JSON evidence is {len(packed)} bytes, above {limit}; do not truncate")
        emit(args.label, packed, len(files))
        return 0
    for positions in (("first", "middle", "last"), ("first", "last")):
        for quality in (55, 45, 35, 25):
            files = review_evidence(root, quality, positions)
            packed = pack(args.label, files, {"mode": "review", "collector_report_altered": False})
            if len(packed) <= limit:
                saved = root / "review"
                saved.mkdir(exist_ok=True)
                for name, data in files.items():
                    (saved / name).write_bytes(data)
                emit(args.label, packed, len(files))
                return 0
    print("HOSTED_REVIEW_OVERSIZE " + json.dumps({"label": args.label, "limit_bytes": limit,
          "next_action": "Inspect the complete original screenshots in the uploaded Actions artifact; JSON evidence has already been exported separately."}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
