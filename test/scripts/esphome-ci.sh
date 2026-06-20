#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
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
  local capacity="${6:-1000}"
  local update_interval="${7:-5s}"

  mkdir -p "$config_dir"
  cp "$ROOT_DIR/test/configs/powerfeather.yaml" "$config_dir/$output_name"
  printf 'wifi_ssid: "ci-network"\nwifi_password: "ci-password"\n' > "$config_dir/secrets.yaml"

  perl -0pi \
    -e "s/type: esp-idf/type: ${framework}/;" \
    -e "s/board_revision: v2/board_revision: ${revision}/;" \
    -e "s/type: \"Generic_3V7\"/type: \"${battery_type}\"/;" \
    -e "s/capacity: 1000/capacity: ${capacity}/;" \
    -e "s/update_interval: 5s/update_interval: ${update_interval}/;" \
    "$config_dir/$output_name"
}

make_example_config() {
  local config_dir="$1"
  local example_name="$2"

  mkdir -p "$config_dir"
  cp "$ROOT_DIR/examples/$example_name" "$config_dir/$example_name"
  cat > "$config_dir/secrets.yaml" <<'EOF'
api_encryption_key: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
fallback_ap_password: "ci-fallback-password"
ota_password: "ci-ota-password"
wifi_ssid: "ci-network"
wifi_password: "ci-password"
EOF

  perl -0pi \
    -e 's#external_components:\n(?:  .+\n)+\npowerfeather:#external_components:\n  - source:\n      type: local\n      path: /components\n    components: [powerfeather]\n    refresh: 0s\n\npowerfeather:#;' \
    "$config_dir/$example_name"
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
  local capacity="${5:-1000}"
  local update_interval="${6:-5s}"
  local tmp_dir
  local log_file
  local status
  tmp_dir="$(mktemp -d)"
  log_file="$tmp_dir/output.log"

  make_config "$tmp_dir" "$name.yaml" "$framework" "$revision" "$battery_type" "$capacity" "$update_interval"
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
  local capacity="${6:-1000}"
  local update_interval="${7:-5s}"
  local tmp_dir
  local log_file
  tmp_dir="$(mktemp -d)"
  log_file="$tmp_dir/output.log"

  make_config "$tmp_dir" "$name.yaml" "$framework" "$revision" "$battery_type" "$capacity" "$update_interval"
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

run_multi_mainboard_expect_fail() {
  local tmp_dir
  local log_file
  tmp_dir="$(mktemp -d)"
  log_file="$tmp_dir/output.log"

  make_config "$tmp_dir" "powerfeather-multi-mainboard.yaml" "esp-idf" "v2"
  perl -0pi \
    -e 's/mainboard:\n    id: "my_powerfeather"/mainboard:\n  - id: "my_powerfeather_a"/;' \
    -e 's/(web_server:\n)/  - id: "my_powerfeather_b"\n    board_revision: v2\n\n\1/;' \
    "$tmp_dir/powerfeather-multi-mainboard.yaml"

  if docker_esphome "$tmp_dir" config "powerfeather-multi-mainboard.yaml" >"$log_file" 2>&1; then
    printf 'Expected config case powerfeather-multi-mainboard to fail, but it passed.\n' >&2
    cat "$log_file" >&2
    rm -rf "$tmp_dir"
    return 1
  fi

  if ! grep -Fq "expected a dictionary" "$log_file"; then
    printf 'Expected config case powerfeather-multi-mainboard to fail with "expected a dictionary". Output was:\n' >&2
    cat "$log_file" >&2
    rm -rf "$tmp_dir"
    return 1
  fi

  printf 'Config case powerfeather-multi-mainboard failed as expected.\n'
  rm -rf "$tmp_dir"
}

run_example_expect_pass() {
  local example_name="$1"
  local tmp_dir
  local log_file
  local status
  tmp_dir="$(mktemp -d)"
  log_file="$tmp_dir/output.log"

  make_example_config "$tmp_dir" "$example_name"
  set +e
  docker_esphome "$tmp_dir" config "$example_name" >"$log_file" 2>&1
  status=$?
  set -e
  if [ "$status" -ne 0 ]; then
    printf 'Example %s failed. Output was:\n' "$example_name" >&2
    cat "$log_file" >&2
  else
    printf 'Example %s passed.\n' "$example_name"
  fi
  rm -rf "$tmp_dir"
  return "$status"
}

validate() {
  git -C "$ROOT_DIR" diff --check

  run_config_expect_pass "powerfeather-v1-generic" "esp-idf" "v1" "Generic_3V7"
  run_config_expect_pass "powerfeather-v2-generic" "esp-idf" "v2" "Generic_3V7"
  run_config_expect_pass "powerfeather-v2-lfp" "esp-idf" "v2" "Generic_LFP"
  run_config_expect_fail "powerfeather-v1-lfp" "esp-idf" "v1" "Generic_LFP" "Generic_LFP battery type requires board_revision v2"
  run_config_expect_fail \
    "powerfeather-v1-small-battery" \
    "esp-idf" \
    "v1" \
    "Generic_3V7" \
    "battery capacity for board_revision v1 must be 0 or between 50 and 6000 mAh" \
    "1"
  run_config_expect_fail \
    "powerfeather-fast-update" \
    "esp-idf" \
    "v2" \
    "Generic_3V7" \
    "Update interval must be at least 500ms" \
    "1000" \
    "100ms"
  run_multi_mainboard_expect_fail
  run_example_expect_pass "powerfeather-v2-idf.yaml"
  run_example_expect_pass "powerfeather-v2-arduino.yaml"
  run_example_expect_pass "powerfeather-v2-idf-lfp.yaml"
  run_example_expect_pass "powerfeather-v2-arduino-lfp.yaml"
  run_example_expect_pass "powerfeather-v1-idf.yaml"
  run_example_expect_pass "powerfeather-v1-arduino.yaml"
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
