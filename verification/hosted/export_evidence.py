#!/usr/bin/env python3
"""Export public hosted-math evidence in a bounded, hash-checked log transport."""
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--max-mib", type=int, default=30)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9_-]{1,32}", args.label):
        parser.error("Use a short lowercase evidence label")
    if not 1 <= args.max_mib <= 32:
        parser.error("Maximum bundle size must be between 1 and 32 MiB")
    root = Path(args.root)
    if not root.is_dir():
        print("HOSTED_BUNDLE_ABSENT " + args.label)
        return 0
    files = sorted(p for p in root.iterdir() if p.is_file() and (
        p.name == "hosted-report.json" or p.name == "math-source.json" or
        p.name == "math-contract.json" or p.name.startswith("math-capture-") or
        p.name.startswith("math-result-") or p.suffix == ".png"))
    if not any(p.name == "hosted-report.json" for p in files):
        raise ValueError("Collector did not produce a hosted report")
    manifest = {"schema_version": 1, "label": args.label,
                "transport": "base64-tar-gzip-public-evidence",
                "excluded_reproducible_files": ["*.html", "expected-mathml.json"],
                "files": []}
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for item in files:
            if item.is_symlink():
                raise ValueError("Evidence files must not be symbolic links")
            data = item.read_bytes()
            info = tarfile.TarInfo(item.name)
            info.size = len(data)
            info.mode = 0o644
            info.mtime = 0
            archive.addfile(info, io.BytesIO(data))
            manifest["files"].append({"path": item.name, "size_bytes": len(data),
                                      "sha256": hashlib.sha256(data).hexdigest()})
        data = (json.dumps(manifest, indent=2) + "\n").encode()
        info = tarfile.TarInfo("transport-manifest.json")
        info.size = len(data)
        info.mode = 0o644
        info.mtime = 0
        archive.addfile(info, io.BytesIO(data))
    packed = gzip.compress(raw.getvalue(), compresslevel=9, mtime=0)
    limit = args.max_mib * 1024 * 1024
    if len(packed) > limit:
        raise ValueError(f"Evidence transport is {len(packed)} bytes, above {limit}; "
                         "use the complete uploaded Actions artifact, not a truncated log bundle")
    encoded = base64.b64encode(packed).decode("ascii")
    chunks = [encoded[i:i + 48000] for i in range(0, len(encoded), 48000)]
    meta = {"label": args.label, "parts": len(chunks), "bytes": len(packed),
            "sha256": hashlib.sha256(packed).hexdigest(), "files": len(files)}
    print("HOSTED_BUNDLE_META " + json.dumps(meta, separators=(",", ":")), flush=True)
    for i, chunk in enumerate(chunks, 1):
        print(f"HOSTED_BUNDLE_PART {args.label} {i:05d}/{len(chunks):05d} {chunk}", flush=True)
    print("HOSTED_BUNDLE_END " + args.label + " " + meta["sha256"], flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
