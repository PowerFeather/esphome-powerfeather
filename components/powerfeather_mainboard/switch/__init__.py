import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from .. import CONF_POWERFEATHER_MAINBOARD_ID, POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA, TASK_UPDATE_TYPES, powerfeather_ns


# Switches
CONF_ENABLE_EN_SWITCH = "enable_EN"
CONF_ENABLE_3V3_SWITCH = "enable_3V3"
CONF_ENABLE_VSQT_SWITCH = "enable_VSQT"
CONF_ENABLE_BATTERY_TEMP_SENSE_SWITCH = "enable_battery_temp_sense"
CONF_ENABLE_BATTERY_CHARGING_SWITCH = "enable_battery_charging"
CONF_ENABLE_BATTERY_FUEL_GAUGE_SWITCH = "enable_battery_fuel_gauge"

PowerFeatherSwitch = powerfeather_ns.class_("PowerFeatherSwitch", switch.Switch, cg.Component)

CONFIG_SCHEMA = POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA.extend(
    {
        cv.Optional(CONF_ENABLE_EN_SWITCH): switch.switch_schema(PowerFeatherSwitch),
        cv.Optional(CONF_ENABLE_3V3_SWITCH): switch.switch_schema(PowerFeatherSwitch),
        cv.Optional(CONF_ENABLE_VSQT_SWITCH): switch.switch_schema(PowerFeatherSwitch),
        cv.Optional(CONF_ENABLE_BATTERY_TEMP_SENSE_SWITCH): switch.switch_schema(PowerFeatherSwitch),
        cv.Optional(CONF_ENABLE_BATTERY_CHARGING_SWITCH): switch.switch_schema(PowerFeatherSwitch),
        cv.Optional(CONF_ENABLE_BATTERY_FUEL_GAUGE_SWITCH): switch.switch_schema(PowerFeatherSwitch),
    }
)

async def to_code(config):
    mainboard = await cg.get_variable(config[CONF_POWERFEATHER_MAINBOARD_ID])

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