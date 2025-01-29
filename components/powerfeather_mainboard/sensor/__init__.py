import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    ICON_EMPTY,
    ICON_BATTERY,
    ICON_THERMOMETER,
    ICON_TIMER,
    ICON_PERCENT,
    UNIT_VOLT,
    UNIT_AMPERE,
    UNIT_PERCENT,
    UNIT_EMPTY,
    UNIT_HOUR,
    UNIT_CELSIUS,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_BATTERY,
    STATE_CLASS_MEASUREMENT
)
from .. import (
    ICON_VOLTAGE,
    ICON_CURRENT_DC,
    CONF_POWERFEATHER_MAINBOARD_ID,
    POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA,
)

CONF_SUPPLY_VOLTAGE_SENSOR = "supply_voltage"
CONF_SUPPLY_CURRENT_SENSOR = "supply_current"
CONF_BATTERY_VOLTAGE_SENSOR = "battery_voltage"
CONF_BATTERY_CURRENT_SENSOR = "battery_current"
CONF_BATTERY_CHARGE_SENSOR = "battery_charge"
CONF_BATTERY_HEALTH_SENSOR = "battery_health"
CONF_BATTERY_CYCLES_SENSOR = "battery_cycles"
CONF_BATTERY_TIME_LEFT_SENSOR = "battery_time_left"
CONF_BATTERY_TEMPERATURE_SENSOR = "battery_temperature"


CONFIG_SCHEMA = POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA.extend(
    {
        cv.Optional(CONF_SUPPLY_VOLTAGE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_VOLTAGE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT
        ),
        cv.Optional(CONF_SUPPLY_CURRENT_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            icon=ICON_CURRENT_DC,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT
        ),
        cv.Optional(CONF_BATTERY_VOLTAGE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_VOLTAGE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT
        ),
        cv.Optional(CONF_BATTERY_CURRENT_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            icon=ICON_CURRENT_DC,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT
        ),
        cv.Optional(CONF_BATTERY_CHARGE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            icon=ICON_BATTERY,
            device_class=DEVICE_CLASS_BATTERY,
            state_class=STATE_CLASS_MEASUREMENT
        ),
        cv.Optional(CONF_BATTERY_HEALTH_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            icon=ICON_PERCENT,
            state_class=STATE_CLASS_MEASUREMENT
        ),
        cv.Optional(CONF_BATTERY_CYCLES_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon=ICON_EMPTY,
            state_class=STATE_CLASS_MEASUREMENT
        ),
        cv.Optional(CONF_BATTERY_TIME_LEFT_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOUR,
            icon=ICON_TIMER,
            device_class=DEVICE_CLASS_DURATION,
            state_class=STATE_CLASS_MEASUREMENT
        ),
        cv.Optional(CONF_BATTERY_TEMPERATURE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            icon=ICON_THERMOMETER,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT
        ),
    }
)

async def to_code(config):
    mainboard = await cg.get_variable(config[CONF_POWERFEATHER_MAINBOARD_ID])

    if supply_voltage_sensor_config := config.get(CONF_SUPPLY_VOLTAGE_SENSOR):
        sens = await sensor.new_sensor(supply_voltage_sensor_config)
        cg.add(mainboard.set_supply_voltage_sensor(sens))
    if supply_current_sensor_config := config.get(CONF_SUPPLY_CURRENT_SENSOR):
        sens = await sensor.new_sensor(supply_current_sensor_config)
        cg.add(mainboard.set_supply_current_sensor(sens))
    if battery_voltage_sensor_config := config.get(CONF_BATTERY_VOLTAGE_SENSOR):
        sens = await sensor.new_sensor(battery_voltage_sensor_config)
        cg.add(mainboard.set_battery_voltage_sensor(sens))
    if battery_current_sensor_config := config.get(CONF_BATTERY_CURRENT_SENSOR):
        sens = await sensor.new_sensor(battery_current_sensor_config)
        cg.add(mainboard.set_battery_current_sensor(sens))
    if battery_charge_sensor_config := config.get(CONF_BATTERY_CHARGE_SENSOR):
        sens = await sensor.new_sensor(battery_charge_sensor_config)
        cg.add(mainboard.set_battery_charge_sensor(sens))
    if battery_health_sensor_config := config.get(CONF_BATTERY_HEALTH_SENSOR):
        sens = await sensor.new_sensor(battery_health_sensor_config)
        cg.add(mainboard.set_battery_health_sensor(sens))
    if battery_cycles_sensor_config := config.get(CONF_BATTERY_CYCLES_SENSOR):
        sens = await sensor.new_sensor(battery_cycles_sensor_config)
        cg.add(mainboard.set_battery_cycles_sensor(sens))
    if battery_time_left_sensor_config := config.get(CONF_BATTERY_TIME_LEFT_SENSOR):
        sens = await sensor.new_sensor(battery_time_left_sensor_config)
        cg.add(mainboard.set_battery_time_left_sensor(sens))
    if battery_temperature_sensor_config := config.get(CONF_BATTERY_TEMPERATURE_SENSOR):
        sens = await sensor.new_sensor(battery_temperature_sensor_config)
        cg.add(mainboard.set_battery_temperature_sensor(sens))

