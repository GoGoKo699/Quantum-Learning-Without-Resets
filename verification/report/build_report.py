#!/usr/bin/env python3
"""Build the self-contained report with pdfLaTeX (TeX Live 2025).

Requires Python 3, the selected TeX installation, and Poppler's pdfinfo and
pdftotext. The stored PDF is retained as the accepted reader copy. A fresh
build is checked by page count and extracted text, not by outer PDF bytes,
which may differ because of PDF metadata or delivery processing.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def run(command, **kwargs):
    return subprocess.run(command, check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, **kwargs).stdout


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def page_count(path):
    information = run(["pdfinfo", str(path)]).decode("utf-8", errors="replace")
    match = re.search(r"^Pages:\s+(\d+)\s*$", information, re.MULTILINE)
    if not match:
        raise RuntimeError("pdfinfo did not return a page count")
    return int(match.group(1))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", default="pdflatex",
                        help="pdfLaTeX executable from TeX Live 2025")
    parser.add_argument("--output-dir", type=Path,
                        help="build directory; defaults to a new temporary directory")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    sources = sorted((root / "learning/source").glob("*_Report.tex"))
    if len(sources) != 1:
        raise RuntimeError("Expected exactly one learning/source/*_Report.tex")
    source = sources[0]
    stored_pdf = root / "learning/report" / (source.stem + ".pdf")
    if not stored_pdf.is_file():
        raise RuntimeError("The accepted report PDF is missing")
    engine = shutil.which(args.engine)
    if engine is None:
        raise RuntimeError("pdfLaTeX executable not found: " + args.engine)
    banner = run([engine, "--version"]).decode("utf-8", errors="replace").splitlines()[0]
    if not banner.startswith("pdfTeX ") or "TeX Live 2025" not in banner:
        raise RuntimeError("TeX Live 2025 is required; observed: " + banner)
    for executable in ("pdfinfo", "pdftotext"):
        if shutil.which(executable) is None:
            raise RuntimeError("Required Poppler tool not found: " + executable)
    output = (args.output_dir or Path(tempfile.mkdtemp(prefix=source.stem + "-"))).resolve()
    protected_directories = (source.parent, stored_pdf.parent)
    if any(output == directory or directory in output.parents
           for directory in protected_directories):
        raise RuntimeError("The build directory must be outside learning/source and learning/report")
    output.mkdir(parents=True, exist_ok=True)
    command = [engine, "-shell-restricted", "-interaction=nonstopmode",
               "-halt-on-error", "-file-line-error", "-output-directory=" + str(output),
               source.name]
    for number in range(1, 4):
        try:
            transcript = run(command, cwd=source.parent)
        except subprocess.CalledProcessError as error:
            (output / ("pass-" + str(number) + ".txt")).write_bytes(error.stdout)
            raise
        (output / ("pass-" + str(number) + ".txt")).write_bytes(transcript)
    fresh_pdf = output / (source.stem + ".pdf")
    final_log = output / (source.stem + ".log")
    log_text = final_log.read_text(encoding="utf-8", errors="replace")
    warnings = re.findall(r"^.*(?:LaTeX Warning:|Package \S+ Warning:|"
                          r"Overfull \\[hv]box|Underfull \\[hv]box).*$",
                          log_text, re.MULTILINE)
    if warnings:
        raise RuntimeError("Final build has warnings:\n" + "\n".join(warnings))
    fresh_text = run(["pdftotext", "-enc", "UTF-8", str(fresh_pdf), "-"])
    stored_text = run(["pdftotext", "-enc", "UTF-8", str(stored_pdf), "-"])
    fresh_pages, stored_pages = page_count(fresh_pdf), page_count(stored_pdf)
    if fresh_text != stored_text or fresh_pages != stored_pages:
        raise RuntimeError("Fresh and accepted reports differ in extracted text or page count")
    summary = {
        "source": str(source.relative_to(root)),
        "source_sha256": digest(source),
        "stored_pdf": str(stored_pdf.relative_to(root)),
        "stored_pdf_sha256": digest(stored_pdf),
        "fresh_pdf": str(fresh_pdf),
        "fresh_pdf_sha256": digest(fresh_pdf),
        "final_log": str(final_log),
        "final_log_sha256": digest(final_log),
        "engine": banner,
        "passes": 3,
        "pages": fresh_pages,
        "final_log_warnings": warnings,
        "stored_and_fresh_text_equal": True,
        "extracted_text_sha256": hashlib.sha256(fresh_text).hexdigest(),
        "comparison_scope": "Page count and Poppler extracted text; no byte-identity claim.",
    }
    encoded = json.dumps(summary, indent=2) + "\n"
    (output / "build_summary.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
