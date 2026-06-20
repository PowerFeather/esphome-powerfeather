# PowerFeather Test Helper

Internal development/test assets for this repository.

- `configs/powerfeather.yaml` is the full-surface ESPHome fixture used by CI.
- `configs/secrets.yaml` is the env-backed Wi-Fi secrets template.
- `scripts/esphome-ci.sh` runs validation and compile checks with Docker.
- `justfile` contains convenience recipes for local board bring-up with the
  official ESPHome Docker image.

Each target recipe creates a temporary ESPHome config directory, copies one file
from `examples/`, rewrites it to use the local `components/` directory, injects
generated API/OTA/fallback AP credentials, validates the config, then runs
ESPHome to compile, flash, and follow logs.

## Requirements

- Docker
- `just`
- A PowerFeather connected by USB for serial flashing

## Wi-Fi

By default the helper reads Wi-Fi credentials from environment variables:

```bash
export WIFI_SSID="..."
export WIFI_PASSWORD="..."
```

Alternatively, edit `test/configs/secrets.yaml` to use literal Wi-Fi values:

```yaml
wifi_ssid: "..."
wifi_password: "..."
```

Only Wi-Fi belongs in this file. API encryption, OTA, and fallback AP
credentials are generated into the temporary config for each flash run.

## Flash

From this directory:

```bash
just v2-idf /dev/ttyACM0
```

Use `/dev/ttyUSB0` instead if that is how the board appears on your machine.
If you omit the device argument, `/dev/ttyACM0` is used.

## Targets

```bash
just --list
```

Available flash targets:

- `just v2-idf /dev/ttyACM0`
- `just v2-arduino /dev/ttyACM0`
- `just v2-idf-lfp /dev/ttyACM0`
- `just v2-arduino-lfp /dev/ttyACM0`
- `just v1-idf /dev/ttyACM0`
- `just v1-arduino /dev/ttyACM0`

Other recipes:

- `just ports` lists likely USB serial devices.
