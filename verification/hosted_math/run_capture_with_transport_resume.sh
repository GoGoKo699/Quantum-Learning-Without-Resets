#!/usr/bin/env bash
set -euo pipefail

collector="$GITHUB_WORKSPACE/verification/hosted_math/capture_hosted_math.cjs"
previous=""
max_attempts=8
for ((attempt=1; attempt<=max_attempts; attempt++)); do
  output="$RUNNER_TEMP/hosted-math-attempt-$attempt"
  resume=()
  if [[ -n "$previous" ]]; then
    resume=(--resume-from "$previous")
  fi
  if node "$collector" --root "$GITHUB_WORKSPACE/checked-source" --repository "$GITHUB_REPOSITORY" --revision "$CAPTURE_REVISION" --output "$output" "${resume[@]}"; then
    mv -- "$output" "$RUNNER_TEMP/hosted-math"
    exit 0
  else
    status=$?
  fi
  if [[ "$attempt" == "$max_attempts" ]]; then
    exit "$status"
  fi
  if ! python3 - "$output" "$GITHUB_REPOSITORY" "$CAPTURE_REVISION" <<'PY'
import json
from pathlib import Path
import re
import sys

output, repository, revision = sys.argv[1:]
try:
    folder = Path(output)
    state = json.loads((folder / 'capture-state.json').read_bytes())
    inventory = json.loads((folder / 'math-source.json').read_bytes())
    report = json.loads((folder / 'hosted-report.json').read_bytes())
    failures = state['failures']
    pages = {p['path']: p['url'] for p in inventory['pages']}
    binding = state['binding']
    allowed = (report['status'] == 'fail' and binding['tree'] == report['tree'] and
               binding['repository'] == report['repository'] == repository and
               binding['revision'] == report['revision'] == revision and
               bool(failures))
    for failure in failures:
        match = re.fullmatch(r'Error: HTTP (502|503|504)', failure['reason'])
        allowed = (allowed and failure['category'] == 'transport_failure' and bool(match) and
                   any(retry['path'] == failure['path'] and retry['url'] == pages[failure['path']] and
                       retry['viewport'] == failure['viewport'] and retry['http_status'] in (502, 503, 504)
                       for retry in state['navigation_retries']))
except (OSError, KeyError, TypeError, ValueError):
    allowed = False
raise SystemExit(0 if allowed else 1)
PY
  then
    exit "$status"
  fi
  previous="$output"
  sleep 5
done
