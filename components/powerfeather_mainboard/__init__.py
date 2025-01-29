import os

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

CODEOWNERS = ["powerfeatherdev (dev@powerfeather.dev)"]
AUTO_LOAD = ["sensor", "binary_sensor", "switch", "button", "number"]

CONF_POWERFEATHER_MAINBOARD_ID = "powerfeather_mainboard_id"

powerfeather_ns = cg.esphome_ns.namespace("powerfeather_mainboard")
PowerFeatherMainboard = powerfeather_ns.class_(
    "PowerFeatherMainboard", cg.PollingComponent,
)

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
    "ENABLE_STAT" : TaskUpdateType.ENABLE_STAT,
    "SHIP_MODE" : TaskUpdateType.SHIP_MODE,
    "SHUTDOWN" : TaskUpdateType.SHUTDOWN,
    "POWERCYCLE" : TaskUpdateType.POWERCYCLE,
    "SUPPLY_MAINTAIN_VOLTAGE" : TaskUpdateType.SUPPLY_MAINTAIN_VOLTAGE,
    "BATTERY_CHARGING_MAX_CURRENT" : TaskUpdateType.BATTERY_CHARGING_MAX_CURRENT,
}

# Top-level configuration
CONF_BATTERY_CAPACITY = "battery_capacity"
CONF_BATTERY_TYPE = "battery_type"

POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_POWERFEATHER_MAINBOARD_ID): cv.use_id(PowerFeatherMainboard),
    }
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(PowerFeatherMainboard),
        cv.Optional(CONF_BATTERY_CAPACITY): cv.positive_int,
        cv.Optional(CONF_BATTERY_TYPE): cv.enum(BATTERY_TYPES),
    }
).extend(cv.polling_component_schema("1s"))

async def to_code(config):
    mainboard = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(mainboard, config)

    cg.add_library(name="PowerFeather-SDK", version="1.1.0")

    if battery_capacity_config := config.get(CONF_BATTERY_CAPACITY):
        cg.add(mainboard.set_battery_capacity(battery_capacity_config))
    if battery_type_config := config.get(CONF_BATTERY_TYPE):
        cg.add(mainboard.set_battery_type(battery_type_config))



