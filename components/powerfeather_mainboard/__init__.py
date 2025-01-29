import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

ICON_CURRENT_DC = "mdi:current-dc"
ICON_VOLTAGE = "mdi:sine-wave"
ICON_ENERGY = "mdi:lightning-bolt"

CODEOWNERS = ["powerfeatherdev (dev@powerfeather.dev)"]
AUTO_LOAD = ["sensor", "binary_sensor", "switch", "button", "number"]

CONF_POWERFEATHER_MAINBOARD_ID = "powerfeather_mainboard_id"

powerfeather_ns = cg.esphome_ns.namespace("powerfeather_mainboard")
PowerFeatherMainboard = powerfeather_ns.class_(
    "PowerFeatherMainboard", cg.PollingComponent,
)

# Definitions from SDK, needs to be duplicated here
BATTERY_CAPACITY_MINIMUM = 50
BatteryType = powerfeather_ns.enum("BatteryType")
BATTERY_TYPES = {
    "Generic_3V7" : BatteryType.Generic_3V7,
    "ICR18650_26H" : BatteryType.ICR18650_26H,
    "UR18650ZY" : BatteryType.UR18650ZY
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
        cv.Optional(CONF_BATTERY_CAPACITY, default = 0): cv.Any(
            cv.Range(min=BATTERY_CAPACITY_MINIMUM),
            cv.Range(max=0)
        ),
        cv.Optional(CONF_BATTERY_TYPE, "Generic_3V7"): cv.enum(BATTERY_TYPES),
    }
).extend(cv.polling_component_schema("1s"))

async def to_code(config):
    mainboard = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(mainboard, config)

    cg.add_library(name="PowerFeather-SDK", version="^1.1.0")

    if battery_capacity_config := config.get(CONF_BATTERY_CAPACITY):
        cg.add(mainboard.set_battery_capacity(battery_capacity_config))
    if battery_type_config := config.get(CONF_BATTERY_TYPE):
        cg.add(mainboard.set_battery_type(battery_type_config))


