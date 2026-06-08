#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE="${ESPHOME_DOCKER_IMAGE:-ghcr.io/esphome/esphome:stable}"

usage() {
  printf 'Usage:\n'
  printf '  %s validate\n' "$0"
  printf '  %s compile [esp-idf|arduino] [v1|v2]\n' "$0"
  printf '  %s compile-matrix\n' "$0"
  printf '  %s all\n' "$0"
}

make_config() {
  local config_dir="$1"
  local output_name="$2"
  local framework="$3"
  local revision="$4"
  local battery_type="${5:-Generic_3V7}"

  mkdir -p "$config_dir"
  cp "$ROOT_DIR/config/powerfeather.yaml" "$config_dir/$output_name"
  printf 'ssid: "ci-network"\npassword: "ci-password"\n' > "$config_dir/secrets.yaml"

  perl -0pi \
    -e "s/type: esp-idf/type: ${framework}/;" \
    -e "s/board_revision: v2/board_revision: ${revision}/;" \
    -e "s/type: \"Generic_3V7\"/type: \"${battery_type}\"/;" \
    "$config_dir/$output_name"
}

docker_esphome() {
  local config_dir="$1"
  shift

  docker run --rm \
    --user "$(id -u):$(id -g)" \
    -e HOME=/config \
    -e PLATFORMIO_CORE_DIR=/config/.esphome/platformio \
    -e PLATFORMIO_GLOBALLIB_DIR=/config/.esphome/platformio/lib \
    -e PLATFORMIO_SETTING_ENABLE_TELEMETRY=false \
    -v "$config_dir:/config" \
    -v "$ROOT_DIR/components:/components" \
    -w /config \
    "$IMAGE" "$@"
}

run_config_expect_pass() {
  local name="$1"
  local framework="$2"
  local revision="$3"
  local battery_type="$4"
  local tmp_dir
  local log_file
  local status
  tmp_dir="$(mktemp -d)"
  log_file="$tmp_dir/output.log"

  make_config "$tmp_dir" "$name.yaml" "$framework" "$revision" "$battery_type"
  set +e
  docker_esphome "$tmp_dir" config "$name.yaml" >"$log_file" 2>&1
  status=$?
  set -e
  if [ "$status" -ne 0 ]; then
    printf 'Config case %s failed. Output was:\n' "$name" >&2
    cat "$log_file" >&2
  else
    printf 'Config case %s passed.\n' "$name"
  fi
  rm -rf "$tmp_dir"
  return "$status"
}

run_config_expect_fail() {
  local name="$1"
  local framework="$2"
  local revision="$3"
  local battery_type="$4"
  local expected="$5"
  local tmp_dir
  local log_file
  tmp_dir="$(mktemp -d)"
  log_file="$tmp_dir/output.log"

  make_config "$tmp_dir" "$name.yaml" "$framework" "$revision" "$battery_type"
  if docker_esphome "$tmp_dir" config "$name.yaml" >"$log_file" 2>&1; then
    printf 'Expected config case %s to fail, but it passed.\n' "$name" >&2
    cat "$log_file" >&2
    rm -rf "$tmp_dir"
    return 1
  fi

  if ! grep -Fq "$expected" "$log_file"; then
    printf 'Expected config case %s to fail with "%s". Output was:\n' "$name" "$expected" >&2
    cat "$log_file" >&2
    rm -rf "$tmp_dir"
    return 1
  fi

  printf 'Config case %s failed as expected.\n' "$name"
  rm -rf "$tmp_dir"
}

validate() {
  git -C "$ROOT_DIR" diff --check

  run_config_expect_pass "powerfeather-v1-generic" "esp-idf" "v1" "Generic_3V7"
  run_config_expect_pass "powerfeather-v2-generic" "esp-idf" "v2" "Generic_3V7"
  run_config_expect_pass "powerfeather-v2-lfp" "esp-idf" "v2" "Generic_LFP"
  run_config_expect_fail "powerfeather-v1-lfp" "esp-idf" "v1" "Generic_LFP" "Generic_LFP battery type requires board_revision v2"
}

compile_one() {
  local framework="$1"
  local revision="$2"
  local tmp_dir
  local status
  tmp_dir="$(mktemp -d)"

  make_config "$tmp_dir" "powerfeather-compile.yaml" "$framework" "$revision"
  set +e
  docker_esphome "$tmp_dir" compile "powerfeather-compile.yaml"
  status=$?
  set -e
  rm -rf "$tmp_dir"
  return "$status"
}

compile_matrix() {
  compile_one "esp-idf" "v1"
  compile_one "esp-idf" "v2"
  compile_one "arduino" "v1"
  compile_one "arduino" "v2"
}

command="${1:-}"
case "$command" in
  validate)
    validate
    ;;
  compile)
    framework="${2:-}"
    revision="${3:-}"
    if [[ ! "$framework" =~ ^(esp-idf|arduino)$ || ! "$revision" =~ ^(v1|v2)$ ]]; then
      usage >&2
      exit 2
    fi
    compile_one "$framework" "$revision"
    ;;
  compile-matrix)
    compile_matrix
    ;;
  all)
    validate
    compile_matrix
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
