import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_UPDATE_INTERVAL
from esphome.core import CORE

try:
    from esphome.components.esp32 import add_idf_sdkconfig_option
except ImportError:
    add_idf_sdkconfig_option = None

ICON_CURRENT_DC = "mdi:current-dc"
ICON_VOLTAGE = "mdi:sine-wave"
ICON_ENERGY = "mdi:lightning-bolt"
ICON_LED_ON = "mdi:led-on"
UNIT_MILLIAMPERE = "mA"
UNIT_MINUTES = "min"
UNIT_VOLT = "V"

CODEOWNERS = ["powerfeatherdev (dev@powerfeather.dev)"]
AUTO_LOAD = ["sensor", "binary_sensor", "switch", "button", "number"]

CONF_POWERFEATHER_MAINBOARD_ID = "mainboard_id"

powerfeather_ns = cg.esphome_ns.namespace("powerfeather_mainboard")
PowerFeatherMainboard = powerfeather_ns.class_(
    "PowerFeatherMainboard", cg.PollingComponent,
)

UPDATE_INTERVAL_MINIMUM = "500ms"

# Definitions from SDK, needs to be duplicated here
BATTERY_CAPACITY_MINIMUM_V1 = 50
BATTERY_CAPACITY_MAXIMUM_V1 = 6000
BATTERY_CAPACITY_MINIMUM_V2 = 1
BATTERY_CAPACITY_MAXIMUM_V2 = 16383
BatteryType = powerfeather_ns.enum("BatteryType")
BATTERY_TYPES = {
    "Generic_3V7" : BatteryType.Generic_3V7,
    "ICR18650_26H" : BatteryType.ICR18650_26H,
    "UR18650ZY" : BatteryType.UR18650ZY,
    "Generic_LFP" : BatteryType.Generic_LFP,
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
CONF_BOARD_REVISION = "board_revision"

BOARD_REVISION_V1 = "v1"
BOARD_REVISION_V2 = "v2"
BOARD_REVISIONS = {
    BOARD_REVISION_V1: BOARD_REVISION_V1,
    BOARD_REVISION_V2: BOARD_REVISION_V2,
}

POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_POWERFEATHER_MAINBOARD_ID): cv.use_id(PowerFeatherMainboard),
    }
)

def validate_update_interval(value):
    value = cv.positive_time_period_milliseconds(value)
    if value < cv.time_period(UPDATE_INTERVAL_MINIMUM):
        raise cv.Invalid(
            "Update interval must be at least {}".format(UPDATE_INTERVAL_MINIMUM)
        )
    return value

def validate_battery_capacity_for_board_revision(config):
    capacity = config[CONF_BATTERY_CAPACITY]
    if (
        config[CONF_BOARD_REVISION] == BOARD_REVISION_V1
        and config[CONF_BATTERY_TYPE] == BatteryType.Generic_LFP
    ):
        raise cv.Invalid("Generic_LFP battery_type requires board_revision v2")

    if capacity == 0:
        return config

    if config[CONF_BOARD_REVISION] == BOARD_REVISION_V1:
        if not BATTERY_CAPACITY_MINIMUM_V1 <= capacity <= BATTERY_CAPACITY_MAXIMUM_V1:
            raise cv.Invalid(
                "battery_capacity for board_revision v1 must be 0 or between "
                f"{BATTERY_CAPACITY_MINIMUM_V1} and {BATTERY_CAPACITY_MAXIMUM_V1} mAh"
            )
    elif not BATTERY_CAPACITY_MINIMUM_V2 <= capacity <= BATTERY_CAPACITY_MAXIMUM_V2:
        raise cv.Invalid(
            "battery_capacity for board_revision v2 must be 0 or between "
            f"{BATTERY_CAPACITY_MINIMUM_V2} and {BATTERY_CAPACITY_MAXIMUM_V2} mAh"
        )

    return config

CONFIG_SCHEMA = cv.All(cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(PowerFeatherMainboard),
        cv.Optional(CONF_BATTERY_CAPACITY, default = 0): cv.int_range(
            min=0,
            max=BATTERY_CAPACITY_MAXIMUM_V2,
        ),
        cv.Optional(CONF_BATTERY_TYPE, "Generic_3V7"): cv.enum(BATTERY_TYPES),
        cv.Optional(CONF_BOARD_REVISION, default=BOARD_REVISION_V1): cv.enum(BOARD_REVISIONS),
        cv.Optional(CONF_UPDATE_INTERVAL, "10s") : validate_update_interval
    }
), validate_battery_capacity_for_board_revision)

async def to_code(config):
    mainboard = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(mainboard, config)

    cg.add_library(name="PowerFeather-SDK", version="^2.0.0")

    if config[CONF_BOARD_REVISION] == BOARD_REVISION_V2:
        cg.add_build_flag("-DPOWERFEATHER_BOARD_V2")
        if not CORE.using_arduino and add_idf_sdkconfig_option is not None:
            add_idf_sdkconfig_option("CONFIG_ESP32S3_POWERFEATHER_V2", True)

    cg.add(mainboard.set_battery_capacity(config[CONF_BATTERY_CAPACITY]))
    cg.add(mainboard.set_battery_type(config[CONF_BATTERY_TYPE]))
