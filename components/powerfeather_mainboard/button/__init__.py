
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button
from .. import (
    CONF_POWERFEATHER_MAINBOARD_ID,
    POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA,
    TASK_UPDATE_TYPES,
    powerfeather_ns,
)

CONF_SHIP_MODE_BUTTON = "ship_mode"
CONF_SHUTDOWN_BUTTON = "shutdown"
CONF_POWER_CYCLE_BUTTON = "powercycle"

PowerFeatherButton = powerfeather_ns.class_("PowerFeatherButton", button.Button, cg.Component)

CONFIG_SCHEMA = POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA.extend(
    {
        cv.Optional(CONF_SHIP_MODE_BUTTON): button.button_schema(PowerFeatherButton),
        cv.Optional(CONF_SHUTDOWN_BUTTON): button.button_schema(PowerFeatherButton),
        cv.Optional(CONF_POWER_CYCLE_BUTTON): button.button_schema(PowerFeatherButton),
    }
)

async def to_code(config):
    mainboard = await cg.get_variable(config[CONF_POWERFEATHER_MAINBOARD_ID])

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

