import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import (
    UNIT_AMPERE,
    UNIT_VOLT
)
from .. import (
    CONF_POWERFEATHER_MAINBOARD_ID,
    POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA,
    TASK_UPDATE_TYPES,
    powerfeather_ns
)

CONF_SUPPLY_MAINTAIN_VOLTAGE_VALUE = "supply_maintain_voltage"
CONF_BATTERY_CHARGING_MAX_CURRENT_VALUE = "battery_charging_max_current"

PowerFeatherValue = powerfeather_ns.class_("PowerFeatherValue", number.Number, cg.Component)

CONFIG_SCHEMA = POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA.extend(
    {
        cv.Optional(CONF_SUPPLY_MAINTAIN_VOLTAGE_VALUE): number.number_schema(
            PowerFeatherValue,
            unit_of_measurement = UNIT_AMPERE),
        cv.Optional(CONF_BATTERY_CHARGING_MAX_CURRENT_VALUE): number.number_schema(
            PowerFeatherValue,
            unit_of_measurement = UNIT_VOLT),
    })

async def to_code(config):
    mainboard = await cg.get_variable(config[CONF_POWERFEATHER_MAINBOARD_ID])

    if CONF_SUPPLY_MAINTAIN_VOLTAGE_VALUE in config:
        val = await number.new_number(config[CONF_SUPPLY_MAINTAIN_VOLTAGE_VALUE], min_value = 4.6, max_value = 16.8, step = 0.12)
        await cg.register_parented(val, mainboard)
        cg.add(val.set_update_type(TASK_UPDATE_TYPES["SUPPLY_MAINTAIN_VOLTAGE"]))
        cg.add(mainboard.set_supply_maintain_voltage_value(val))

    if CONF_BATTERY_CHARGING_MAX_CURRENT_VALUE in config:
        val = await number.new_number(config[CONF_BATTERY_CHARGING_MAX_CURRENT_VALUE], min_value = 0.05, max_value = 2, step = 0.04)
        await cg.register_parented(val, mainboard)
        cg.add(val.set_update_type(TASK_UPDATE_TYPES["BATTERY_CHARGING_MAX_CURRENT"]))
        cg.add(mainboard.set_battery_charging_max_current_value(val))