# Inspect actual GitHub mathematics

The collector compares every recognized mathematical expression in a pinned source tree with the accessible MathML on its real GitHub page. It inspects anonymous Chromium contexts at widths 1440 and 760, saves the original hosted HTML and full-page screenshots, and checks symbols and structure against local MathJax compilation. Local TeX compilation alone does not establish hosted rendering.

The workflow first inspects the README and model at the fixed public baseline `690dbd3f98c466d535fa531785ac64217380603d` as an early inline/display/table sample, then scans every tracked Markdown page at the actual pull-request or main commit. It runs on pull requests and manual dispatch, using only read access to repository contents. It has no secret inputs or write token, and it never modifies a repository or its visibility.

## Run locally

Use Node 18 or newer, Python 3.10 or newer, Git, Playwright and MathJax. Install dependencies in a temporary directory outside the source checkout:

```bash
npm install --prefix /absolute/temporary/dependencies playwright@1.56.1 mathjax-full@3.2.1
/absolute/temporary/dependencies/node_modules/.bin/playwright install chromium
NODE_PATH=/absolute/temporary/dependencies/node_modules node verification/hosted/capture_hosted_math.cjs \
  --root /absolute/source-checkout --repository owner/repository \
  --revision FULL_40_CHARACTER_COMMIT --output /absolute/new-empty-evidence-directory
```

All pages must be public and their URLs must identify that exact commit. A private repository or a browser-policy denial requires a separately permitted compatible inspection route; neither authenticating this collector nor changing visibility is part of it. Keep failed attempts and their failure classifications.

## Read the evidence

`hosted-report.json` records the revision, tree, page/source hashes, both viewport boundaries, structural-comparison results and exact artifact identities. The complete Actions artifact contains the original captures, HTML and screenshots. Its ordinary retention period is 14 days, so it is a reproducible diagnostic cache rather than permanent scientific preservation.

For tools that can retrieve decoded job logs but cannot download a binary Actions artifact, `export_evidence.py` prints a bounded base64 tar/gzip transport. It includes report/source/capture/result JSON and every full-page PNG; it explicitly excludes reproducible HTML and expected-MathML files. Chunk lines contain at most 48000 payload characters, and SHA256 checks bind the compressed bundle and its exact file bytes. Sample and full bundles are capped at 4 MiB and 28 MiB respectively; exceeding a cap fails the export without truncation. The complete original Actions artifact remains separate.

Restore a selected bundle from the decoded job log:

```bash
python3 verification/hosted/restore_evidence.py --log job.log --label full --output /absolute/new-empty-output
```

A successful automated report still requires actual screenshot inspection and comparison with the pinned scientific source. Review main claims, substantial proofs, learning routes, repaired expressions, navigation and non-mathematical layout at both widths. Neither a generated screenshot nor a green workflow alone certifies that visual work, scientific correctness or literature priority.
