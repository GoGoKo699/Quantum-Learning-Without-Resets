# Inspect actual GitHub mathematics

The collector compares every recognized mathematical expression in a pinned source tree with the accessible MathML on its real GitHub page. It inspects anonymous Chromium contexts at widths 1440 and 760, saves the original hosted HTML and full-page screenshots, and checks symbols and structure against local MathJax compilation. Local TeX compilation alone does not establish hosted rendering.

The workflow first inspects the README as an early inline/display/table sample, then scans every tracked Markdown page. It runs on pull requests, pushes to main and manual dispatch, using only read access to repository contents. It has no secret inputs or write token, and it never modifies a repository or its visibility.

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

For tools that retrieve decoded job logs, exact JSON evidence is exported first in small, separately hash-checked sample/full bundles. Each contains the original collector report, source inventory, captures and check results without changing any report bytes. HTML, expected MathML and original PNGs remain in the complete Actions artifact.

A separate review bundle contains selected first-body, middle and last JPEG crops from each available page screenshot at both widths. The derivative manifest records the original PNG SHA256, original dimensions, exact crop coordinates, JPEG quality and resulting file identities. The original PNGs and collector report are unchanged. Review exports target a 4 MiB compressed cap, trying JPEG qualities 55,45,35 and25; if necessary they retain first/last regions, explicitly recording actual coverage. These crops do not represent every pixel. Supplement them with the original screenshot or actual hosted page whenever required to inspect a proof, repaired formula or flagged region. If the cap still cannot be met, a clear oversize record is printed rather than truncating evidence.

Each JSON bundle has a 4 MiB cap, review images have a separate 4 MiB cap, and log lines contain at most 48000 base64 payload characters. Exact size and SHA256 checks bind every bundle and restored file. Restore a selected label from the decoded job log:

```bash
python3 verification/hosted/restore_evidence.py --log job.log --label full-json --output /absolute/new-empty-json-output
python3 verification/hosted/restore_evidence.py --log job.log --label review --output /absolute/new-empty-review-output
```

A successful automated report still requires actual screenshot inspection and comparison with the pinned scientific source. Review main claims, substantial proofs, learning routes, repaired expressions, navigation and non-mathematical layout at both widths. Neither a generated screenshot nor a green workflow alone certifies that visual work, scientific correctness or literature priority.
