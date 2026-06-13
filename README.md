# PowerFeather ESPHome

ESPHome external component for PowerFeather boards.

This integration exposes PowerFeather mainboard power monitoring and management
features to Home Assistant. The current component surface is
`powerfeather.mainboard`, which represents the single physical mainboard in one
ESPHome node.

For the full setup guide, see the PowerFeather documentation:
https://docs.powerfeather.dev/guides/create_esphome_device/

## Compatibility

This component uses PowerFeather-SDK V2 and supports both PowerFeather board
revisions.

| Board revision | ESPHome framework | Battery types |
| --- | --- | --- |
| `v1` | `esp-idf`, `arduino` | `Generic_3V7`, `ICR18650_26H`, `UR18650ZY` |
| `v2` | `esp-idf`, `arduino` | `Generic_3V7`, `ICR18650_26H`, `UR18650ZY`, `Generic_LFP` |

Each ESPHome YAML builds firmware for one physical PowerFeather board, so
`powerfeather.mainboard` is a single object. To use multiple PowerFeather boards
in one Home Assistant installation, create one ESPHome node/config per board.

## Examples

Start from the example that matches your board and framework:

| Example | Purpose |
| --- | --- |
| [examples/powerfeather-v1.yaml](examples/powerfeather-v1.yaml) | PowerFeather V1, ESP-IDF, 3.7 V lithium battery. |
| [examples/powerfeather-v2.yaml](examples/powerfeather-v2.yaml) | PowerFeather V2, ESP-IDF, 3.7 V lithium battery. |
| [examples/powerfeather-v2-lfp.yaml](examples/powerfeather-v2-lfp.yaml) | PowerFeather V2, ESP-IDF, LiFePO4 battery. |
| [examples/powerfeather-v2-arduino.yaml](examples/powerfeather-v2-arduino.yaml) | PowerFeather V2, Arduino framework, 3.7 V lithium battery. |

The examples use ESPHome secrets:

```yaml
api_encryption_key: "..."
fallback_ap_password: "..."
ota_password: "..."
wifi_ssid: "..."
wifi_password: "..."
```

## Installation

Install the component from GitHub:

```yaml
external_components:
  - source: github://powerfeatherdev/esphome-powerfeather@main
    components: [powerfeather]
```

For a formal release, prefer a tagged source instead of `@main`, for example:

```yaml
external_components:
  - source: github://powerfeatherdev/esphome-powerfeather@v0.1.0
    components: [powerfeather]
```

For local development from this repository:

```yaml
external_components:
  - source:
      type: local
      path: ../components
    components: [powerfeather]
    refresh: 0s
```

## Minimal Config

```yaml
powerfeather:
  mainboard:
    id: powerfeather_mainboard
    board_revision: v2
    battery:
      capacity: 1000
      type: Generic_3V7
```

`battery.capacity` is in mAh. Set it to `0` to initialize the SDK without a
configured battery.

See [config/powerfeather.yaml](config/powerfeather.yaml) for a full local
development config that exposes every supported entity.

## Entities

The component groups ESPHome entities under `powerfeather.mainboard`.

| Group | Purpose |
| --- | --- |
| `sensors` | Supply and battery measurements. |
| `binary_sensors` | Boolean board state. |
| `switches` | Persistent board controls. |
| `buttons` | One-shot board actions. |
| `numbers` | Runtime charger and battery alarm settings. |

### Sensors

| Key | Unit | Notes |
| --- | --- | --- |
| `supply_voltage` | V | Input supply voltage. |
| `supply_current` | mA | Input supply current. |
| `battery_voltage` | V | Battery voltage. |
| `battery_current` | mA | Battery current. |
| `battery_charge` | % | Fuel gauge state of charge. |
| `battery_health` | % | Fuel gauge state of health. |
| `battery_cycles` | count | Fuel gauge cycle count. |
| `battery_time_left` | min | Fuel gauge estimate; can be unknown until the gauge has valid data. |
| `battery_temperature` | C | Returns unknown when battery temperature sense is disabled. |

### Binary Sensors

| Key | Notes |
| --- | --- |
| `supply_good` | Whether the board reports supply-good. |

### Switches

| Key | Notes |
| --- | --- |
| `enable_EN` | Controls the EN pin. |
| `enable_3V3` | Controls the 3V3 output. |
| `enable_VSQT` | Controls the VSQT output. |
| `enable_battery_temp_sense` | Enables battery temperature sensing. |
| `enable_battery_charging` | Enables battery charging. |
| `enable_battery_fuel_gauge` | Enables the battery fuel gauge. |
| `enable_stat` | Enables the charger STAT LED. |

### Buttons

| Key | Notes |
| --- | --- |
| `update_battery_fuel_gauge_temp` | Sends the current battery temperature to the fuel gauge. |
| `ship_mode` | Enters ship mode. |
| `shutdown` | Enters shutdown mode. |
| `powercycle` | Requests a board power cycle. |

The example configs include only `update_battery_fuel_gauge_temp` by default.
Add `ship_mode`, `shutdown`, or `powercycle` only when you want those actions
available from Home Assistant.

### Numbers

| Key | Unit | Notes |
| --- | --- | --- |
| `supply_maintain_voltage` | V | Charger input voltage regulation target. |
| `battery_charging_max_current` | mA | Charger current limit. |
| `battery_low_voltage_alarm` | V | Battery low-voltage alarm threshold. |
| `battery_high_voltage_alarm` | V | Battery high-voltage alarm threshold. |
| `battery_low_charge_alarm` | % | Battery low-charge alarm threshold. |

Battery alarm thresholds are write-only in the SDK. ESPHome will show them as
unknown at boot until you set them from Home Assistant or YAML automation.

## Local Checks

The CI checks can also be run locally with Docker:

```bash
bash scripts/esphome-ci.sh validate
bash scripts/esphome-ci.sh compile esp-idf v2
bash scripts/esphome-ci.sh compile arduino v2
```

Run the full validation and compile matrix:

```bash
bash scripts/esphome-ci.sh all
```

The script uses the official ESPHome Docker image by default:

```bash
ESPHOME_DOCKER_IMAGE=ghcr.io/esphome/esphome:stable bash scripts/esphome-ci.sh all
```
