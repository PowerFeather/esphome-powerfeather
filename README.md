## PowerFeather ESPHome External Components

ESPHome external components for integrating PowerFeather functionality in HomeAssistant.

Currently only the `powerfeather.mainboard` component is available, which gives
easy access to a PowerFeather mainboard's power monitoring and management functions.
It exposes measured values as sensors, power-management state as switches,
one-shot power actions as buttons, and configurable charger or battery alarm
thresholds as numbers.

See documentation at https://docs.powerfeather.dev/guides/create_esphome_device/
for the full guide.

## Compatibility

This component uses PowerFeather-SDK V2 and supports both PowerFeather board
revisions:

| Board revision | ESPHome framework | Notes |
| --- | --- | --- |
| `v1` | `esp-idf`, `arduino` | `Generic_LFP` batteries are not supported. |
| `v2` | `esp-idf`, `arduino` | Supports `Generic_3V7`, `ICR18650_26H`, `UR18650ZY`, and `Generic_LFP`. |

## Usage

Install the component from GitHub:

```yaml
external_components:
  - source: github://powerfeatherdev/esphome-powerfeather@main
    components: [powerfeather]
```

For local development from this repository:

```yaml
external_components:
  - source:
      type: local
      path: ../components
    refresh: 0s
```

Minimal configuration:

```yaml
powerfeather:
  mainboard:
    id: my_powerfeather
    board_revision: v2
    battery:
      capacity: 1000
      type: Generic_3V7
```

See [config/powerfeather.yaml](config/powerfeather.yaml) for a full example.

## Entities

The component groups ESPHome entities under `powerfeather.mainboard`:

| Group | Purpose |
| --- | --- |
| `sensors` | Supply and battery measurements such as voltage, current, charge, health, cycles, time left, and temperature. |
| `binary_sensors` | Boolean board state such as `supply_good`. |
| `switches` | Persistent board controls such as `enable_3V3`, `enable_VSQT`, `enable_EN`, battery charging, fuel gauge, temperature sense, and STAT LED. |
| `buttons` | One-shot actions such as ship mode, shutdown, power cycle, and fuel-gauge temperature update. |
| `numbers` | Runtime thresholds and limits such as supply maintain voltage, charge current, and battery alarms. |

Battery alarm thresholds are write-only in the SDK. ESPHome will show them as
unknown at boot until you set them from Home Assistant or YAML automation.

## Local checks

The CI checks can also be run locally with Docker:

```bash
bash scripts/esphome-ci.sh validate
bash scripts/esphome-ci.sh compile esp-idf v2
bash scripts/esphome-ci.sh compile arduino v2
```

Run `bash scripts/esphome-ci.sh all` to execute the schema checks and full
ESP-IDF/Arduino, V1/V2 compile matrix.

The script uses the official ESPHome Docker image by default:

```bash
ESPHOME_DOCKER_IMAGE=ghcr.io/esphome/esphome:stable bash scripts/esphome-ci.sh all
```
