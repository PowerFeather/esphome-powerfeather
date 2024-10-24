import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import(
    sensor,
    binary_sensor,
    switch,
    number,
    button
)
from esphome.const import (
    CONF_ID,
    ICON_EMPTY,
    UNIT_VOLT,
    UNIT_AMPERE,
    UNIT_PERCENT,
    UNIT_EMPTY,
    UNIT_HOUR,
    UNIT_CELSIUS
)

AUTO_LOAD = [
    "sensor",
    "binary_sensor",
    "switch",
    "number",
    "button"
]

powerfeather_ns = cg.esphome_ns.namespace("powerfeather_mainboard")
PowerFeatherMainboard = powerfeather_ns.class_(
    "PowerFeatherMainboard", cg.PollingComponent,
)

PowerFeatherSwitch = powerfeather_ns.class_("PowerFeatherSwitch", switch.Switch, cg.Component)
PowerFeatherValue = powerfeather_ns.class_("PowerFeatherValue", switch.Switch, cg.Component)
PowerFeatherButton = powerfeather_ns.class_("PowerFeatherButton", button.Button, cg.Component)

BatteryType = powerfeather_ns.enum("BatteryType")
BATTERY_TYPES = {
    "Generic_3V7" : BatteryType.Generic_3V7
}

TaskUpdateType = powerfeather_ns.enum("TaskUpdateType")
TASK_UPDATE_TYPES = {
    "ENABLE_EN" : TaskUpdateType.ENABLE_EN,
    "ENABLE_3V3" : TaskUpdateType.ENABLE_3V3,
    "ENABLE_VSQT" : TaskUpdateType.ENABLE_VSQT,
    "ENABLE_BATTERY_TEMP_SENSE" : TaskUpdateType.ENABLE_BATTERY_TEMP_SENSE,
    "ENABLE_BATTERY_FUEL_GAUGE" : TaskUpdateType.ENABLE_BATTERY_FUEL_GAUGE,
    "ENABLE_BATTERY_CHARGING" : TaskUpdateType.ENABLE_BATTERY_CHARGING,
    "SHIP_MODE" : TaskUpdateType.SHIP_MODE,
    "SHUTDOWN" : TaskUpdateType.SHUTDOWN,
    "POWERCYCLE" : TaskUpdateType.POWERCYCLE,
    "SUPPLY_MAINTAIN_VOLTAGE" : TaskUpdateType.SUPPLY_MAINTAIN_VOLTAGE,
    "BATTERY_CHARGING_MAX_CURRENT" : TaskUpdateType.BATTERY_CHARGING_MAX_CURRENT,
}

# Top-level configuration
CONF_BATTERY_CAPACITY = "battery_capacity"
CONF_BATTERY_TYPE = "battery_type"
# Sensors
CONF_SUPPLY_VOLTAGE_SENSOR = "supply_voltage"
CONF_SUPPLY_CURRENT_SENSOR = "supply_current"
CONF_SUPPLY_GOOD_SENSOR = "supply_good"
CONF_BATTERY_VOLTAGE_SENSOR = "battery_voltage"
CONF_BATTERY_CURRENT_SENSOR = "battery_current"
CONF_BATTERY_CHARGE_SENSOR = "battery_charge"
CONF_BATTERY_HEALTH_SENSOR = "battery_health"
CONF_BATTERY_CYCLES_SENSOR = "battery_cycles"
CONF_BATTERY_TIME_LEFT_SENSOR = "battery_time_left"
CONF_BATTERY_TEMPERATURE_SENSOR = "battery_temperature"
# Switches
CONF_ENABLE_EN_SWITCH = "enable_EN"
CONF_ENABLE_3V3_SWITCH = "enable_3V3"
CONF_ENABLE_VSQT_SWITCH = "enable_VSQT"
CONF_ENABLE_BATTERY_TEMP_SENSE_SWITCH = "enable_battery_temp_sense"
CONF_ENABLE_BATTERY_CHARGING_SWITCH = "enable_battery_charging"
CONF_ENABLE_BATTERY_FUEL_GAUGE_SWITCH = "enable_battery_fuel_gauge"
# Button
CONF_SHIP_MODE_BUTTON = "ship_mode"
CONF_SHUTDOWN_BUTTON = "shutdown"
CONF_POWER_CYCLE_BUTTON = "powercycle"
# Values
CONF_SUPPLY_MAINTAIN_VOLTAGE_VALUE = "supply_maintain_voltage"
CONF_BATTERY_CHARGING_MAX_CURRENT_VALUE = "battery_charging_max_current"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(PowerFeatherMainboard),
        cv.Optional(CONF_BATTERY_CAPACITY): cv.positive_int,
        cv.Optional(CONF_BATTERY_TYPE): cv.enum(BATTERY_TYPES),
    }
).extend(
   {
        cv.Optional(CONF_SUPPLY_VOLTAGE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT, icon=ICON_EMPTY, accuracy_decimals=2
        ),
        cv.Optional(CONF_SUPPLY_CURRENT_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE, icon=ICON_EMPTY, accuracy_decimals=2
        ),
        cv.Optional(CONF_SUPPLY_GOOD_SENSOR): binary_sensor.binary_sensor_schema(),
        cv.Optional(CONF_BATTERY_VOLTAGE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT, icon=ICON_EMPTY, accuracy_decimals=3
        ),
        cv.Optional(CONF_BATTERY_CURRENT_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT, icon=ICON_EMPTY, accuracy_decimals=3
        ),
        cv.Optional(CONF_BATTERY_CHARGE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT, icon=ICON_EMPTY
        ),
        cv.Optional(CONF_BATTERY_HEALTH_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT, icon=ICON_EMPTY
        ),
        cv.Optional(CONF_BATTERY_CYCLES_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY, icon=ICON_EMPTY
        ),
        cv.Optional(CONF_BATTERY_TIME_LEFT_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOUR, icon=ICON_EMPTY
        ),
        cv.Optional(CONF_BATTERY_TEMPERATURE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS, icon=ICON_EMPTY
        ),
        cv.Optional(CONF_ENABLE_EN_SWITCH): switch.switch_schema(PowerFeatherSwitch),
        cv.Optional(CONF_ENABLE_3V3_SWITCH): switch.switch_schema(PowerFeatherSwitch),
        cv.Optional(CONF_ENABLE_VSQT_SWITCH): switch.switch_schema(PowerFeatherSwitch),
        cv.Optional(CONF_ENABLE_BATTERY_TEMP_SENSE_SWITCH): switch.switch_schema(PowerFeatherSwitch),
        cv.Optional(CONF_ENABLE_BATTERY_CHARGING_SWITCH): switch.switch_schema(PowerFeatherSwitch),
        cv.Optional(CONF_ENABLE_BATTERY_FUEL_GAUGE_SWITCH): switch.switch_schema(PowerFeatherSwitch),
        cv.Optional(CONF_SHIP_MODE_BUTTON): button.button_schema(PowerFeatherButton),
        cv.Optional(CONF_SHUTDOWN_BUTTON): button.button_schema(PowerFeatherButton),
        cv.Optional(CONF_POWER_CYCLE_BUTTON): button.button_schema(PowerFeatherButton),
        cv.Optional(CONF_SUPPLY_MAINTAIN_VOLTAGE_VALUE): number.number_schema(PowerFeatherValue),
        cv.Optional(CONF_BATTERY_CHARGING_MAX_CURRENT_VALUE): number.number_schema(PowerFeatherValue),
    }
).extend(cv.polling_component_schema("60s"))

async def to_code(config):
    mainboard = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(mainboard, config)

    cg.add_library("powerfeather/PowerFeather-SDK", "1.0.7")

    # Main
    if battery_capacity_config := config.get(CONF_BATTERY_CAPACITY):
        cg.add(mainboard.set_battery_capacity(battery_capacity_config))
    if battery_type_config := config.get(CONF_BATTERY_TYPE):
        cg.add(mainboard.set_battery_type(battery_type_config))

    # Sensors
    if supply_voltage_sensor_config := config.get(CONF_SUPPLY_VOLTAGE_SENSOR):
        sens = await sensor.new_sensor(supply_voltage_sensor_config)
        cg.add(mainboard.set_supply_voltage_sensor(sens))
    if supply_current_sensor_config := config.get(CONF_SUPPLY_CURRENT_SENSOR):
        sens = await sensor.new_sensor(supply_current_sensor_config)
        cg.add(mainboard.set_supply_current_sensor(sens))
    if supply_good_sensor_config := config.get(CONF_SUPPLY_GOOD_SENSOR):
        sens = await binary_sensor.new_binary_sensor(supply_good_sensor_config)
        cg.add(mainboard.set_supply_good_sensor(sens))
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

    # Switches
    if CONF_ENABLE_EN_SWITCH in config:
        sw = await switch.new_switch(config[CONF_ENABLE_EN_SWITCH])
        await cg.register_parented(sw, mainboard)
        cg.add(sw.set_update_type(TASK_UPDATE_TYPES["ENABLE_EN"]))
        cg.add(mainboard.set_enable_EN_switch(sw))

    if CONF_ENABLE_3V3_SWITCH in config:
        sw = await switch.new_switch(config[CONF_ENABLE_3V3_SWITCH])
        await cg.register_parented(sw, mainboard)
        cg.add(sw.set_update_type(TASK_UPDATE_TYPES["ENABLE_3V3"]))
        cg.add(mainboard.set_enable_3V3_switch(sw))

    if CONF_ENABLE_VSQT_SWITCH in config:
        sw = await switch.new_switch(config[CONF_ENABLE_VSQT_SWITCH])
        await cg.register_parented(sw, mainboard)
        cg.add(sw.set_update_type(TASK_UPDATE_TYPES["ENABLE_VSQT"]))
        cg.add(mainboard.set_enable_VSQT_switch(sw))

    if CONF_ENABLE_BATTERY_TEMP_SENSE_SWITCH in config:
        sw = await switch.new_switch(config[CONF_ENABLE_BATTERY_TEMP_SENSE_SWITCH])
        await cg.register_parented(sw, mainboard)
        cg.add(sw.set_update_type(TASK_UPDATE_TYPES["ENABLE_BATTERY_TEMP_SENSE"]))
        cg.add(mainboard.set_enable_battery_temp_sense_switch(sw))

    if CONF_ENABLE_BATTERY_CHARGING_SWITCH in config:
        sw = await switch.new_switch(config[CONF_ENABLE_BATTERY_CHARGING_SWITCH])
        await cg.register_parented(sw, mainboard)
        cg.add(sw.set_update_type(TASK_UPDATE_TYPES["ENABLE_BATTERY_CHARGING"]))
        cg.add(mainboard.set_enable_battery_charging_switch(sw))

    if CONF_ENABLE_BATTERY_FUEL_GAUGE_SWITCH in config:
        sw = await switch.new_switch(config[CONF_ENABLE_BATTERY_FUEL_GAUGE_SWITCH])
        await cg.register_parented(sw, mainboard)
        cg.add(sw.set_update_type(TASK_UPDATE_TYPES["ENABLE_BATTERY_FUEL_GAUGE"]))
        cg.add(mainboard.set_enable_battery_fuel_gauge_switch(sw))


    # Button
    if CONF_SHIP_MODE_BUTTON in config:
        btn = await button.new_button(config[CONF_SHIP_MODE_BUTTON])
        await cg.register_parented(btn, mainboard)
        cg.add(btn.set_update_type(TASK_UPDATE_TYPES["SHIP_MODE"]))
        cg.add(mainboard.set_ship_mode_button(btn))

    if CONF_SHUTDOWN_BUTTON in config:
        btn = await button.new_button(config[CONF_SHUTDOWN_BUTTON])
        await cg.register_parented(btn, mainboard)
        cg.add(btn.set_update_type(TASK_UPDATE_TYPES["SHUTDOWN"]))
        cg.add(mainboard.set_shutdown_button(btn))

    if CONF_POWER_CYCLE_BUTTON in config:
        btn = await button.new_button(config[CONF_POWER_CYCLE_BUTTON])
        await cg.register_parented(btn, mainboard)
        cg.add(btn.set_update_type(TASK_UPDATE_TYPES["POWERCYCLE"]))
        cg.add(mainboard.set_powercycle_button(btn))

    # Values
    if CONF_SUPPLY_MAINTAIN_VOLTAGE_VALUE in config:
        val = await number.new_number(config[CONF_SUPPLY_MAINTAIN_VOLTAGE_VALUE], min_value = 4.6, max_value = 16.8, step = 0.1)
        await cg.register_parented(sw, mainboard)
        cg.add(val.set_update_type(TASK_UPDATE_TYPES["SUPPLY_MAINTAIN_VOLTAGE"]))
        cg.add(mainboard.set_supply_maintain_voltage_value(val))

    # battery charging max current
    if CONF_BATTERY_CHARGING_MAX_CURRENT_VALUE in config:
        val = await number.new_number(config[CONF_BATTERY_CHARGING_MAX_CURRENT_VALUE], min_value = 0.05, max_value = 2000, step = 0.01)
        await cg.register_parented(sw, mainboard)
        cg.add(val.set_update_type(TASK_UPDATE_TYPES["BATTERY_CHARGING_MAX_CURRENT"]))
        cg.add(mainboard.set_battery_charging_max_current_value(val))
        
    # TODO
    #   - low voltage alarm
    #   - high voltage alarm
    #   - low charge alarm


