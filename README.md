## PowerFeather ESPHome External Components

ESPHome external components for integrating PowerFeather functionality in HomeAssistant.

Currently only the `powerfeather.mainboard` component is available, which gives
easy access to a PowerFeather mainboard's power monitoring and management functions.
It exposes measured values as sensors, power-management state as switches,
one-shot power actions as buttons, and configurable charger or battery alarm
thresholds as numbers.

See documentation at https://docs.powerfeather.dev/guides/create_esphome_device/
for instructions on how to use this component.

## Local checks

The CI checks can also be run locally with Docker:

```bash
bash scripts/esphome-ci.sh validate
bash scripts/esphome-ci.sh compile esp-idf v2
bash scripts/esphome-ci.sh compile arduino v2
```

Run `bash scripts/esphome-ci.sh all` to execute the schema checks and full
ESP-IDF/Arduino, V1/V2 compile matrix.
