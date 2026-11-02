#!/usr/bin/env python3
"""Restore a public collector bundle from decoded GitHub Actions job logs."""
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
    parser.add_argument("--log", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    log = Path(args.log).read_text()
    meta = [json.loads(m) for m in re.findall(r"HOSTED_BUNDLE_META (\{[^\r\n]+\})", log)]
    candidates = [m for m in meta if m["label"] == args.label]
    if len(candidates) != 1:
        raise ValueError("Require exactly one metadata record for the selected label")
    expected = candidates[0]
    pattern = r"HOSTED_BUNDLE_PART " + re.escape(args.label) + r" (\d+)/(\d+) ([A-Za-z0-9+/=]+)"
    parts = re.findall(pattern, log)
    if len(parts) != expected["parts"]:
        raise ValueError("Missing or duplicate log parts")
    numbers = [int(p[0]) for p in parts]
    if numbers != list(range(1, expected["parts"] + 1)) or any(int(p[1]) != expected["parts"] for p in parts):
        raise ValueError("Log parts are not in complete order")
    packed = base64.b64decode("".join(p[2] for p in parts), validate=True)
    if len(packed) != expected["bytes"] or hashlib.sha256(packed).hexdigest() != expected["sha256"]:
        raise ValueError("Bundle size or SHA256 mismatch")
    if len(packed) > 32 * 1024 * 1024:
        raise ValueError("Bundle is above the documented size cap")
    output = Path(args.output)
    if output.exists() and any(output.iterdir()):
        raise ValueError("Use a new empty output directory")
    output.mkdir(parents=True, exist_ok=True)
    raw = gzip.decompress(packed)
    if len(raw) > 512 * 1024 * 1024:
        raise ValueError("Expanded bundle is above the size cap")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        members = archive.getmembers()
        names = [m.name for m in members]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate archive paths")
        for member in members:
            if not member.isfile() or Path(member.name).name != member.name or member.name in ("", ".", ".."):
                raise ValueError("Unsafe evidence archive path or type")
            data = archive.extractfile(member).read()
            (output / member.name).write_bytes(data)
    manifest = json.loads((output / "transport-manifest.json").read_text())
    for entry in manifest["files"]:
        data = (output / entry["path"]).read_bytes()
        if len(data) != entry["size_bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError("Evidence file identity mismatch")
    print(json.dumps({"status": "restored", "label": args.label, "files": len(manifest["files"]),
                      "bundle_sha256": expected["sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
