#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CI_SCRIPT="$ROOT_DIR/scripts/esphome-ci.sh"

usage() {
  printf 'Usage: %s [v1|v2]\n' "$0"
  printf '\n'
  printf 'Runs a local smoke test with the official ESPHome Docker image:\n'
  printf '  - shell syntax checks\n'
  printf '  - ESPHome config validation cases\n'
  printf '  - ESP-IDF compile for the selected board revision\n'
  printf '  - Arduino compile for the selected board revision\n'
}

revision="${1:-v2}"
if [[ "$revision" == "-h" || "$revision" == "--help" ]]; then
  usage
  exit 0
fi

if [[ ! "$revision" =~ ^(v1|v2)$ ]]; then
  usage >&2
  exit 2
fi

bash -n "$CI_SCRIPT"
bash -n "$0"

bash "$CI_SCRIPT" validate
bash "$CI_SCRIPT" compile esp-idf "$revision"
bash "$CI_SCRIPT" compile arduino "$revision"
