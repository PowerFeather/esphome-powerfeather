import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, button, number, sensor, switch
from esphome.const import (
    CONF_ID,
    CONF_TYPE,
    CONF_UPDATE_INTERVAL,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_RESTART,
    DEVICE_CLASS_SWITCH,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    ICON_BATTERY,
    ICON_EMPTY,
    ICON_GAUGE,
    ICON_PERCENT,
    ICON_RESTART,
    ICON_THERMOMETER,
    ICON_TIMER,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_EMPTY,
    UNIT_PERCENT,
)
from esphome.core import CORE

try:
    from esphome.components.esp32 import add_idf_sdkconfig_option
except ImportError:
    add_idf_sdkconfig_option = None

ICON_CURRENT_DC = "mdi:current-dc"
ICON_ENERGY = "mdi:lightning-bolt"
ICON_LED_ON = "mdi:led-on"
ICON_VOLTAGE = "mdi:sine-wave"
UNIT_MILLIAMPERE = "mA"
UNIT_MINUTES = "min"
UNIT_VOLT = "V"
STATE_CLASS_TOTAL_INCREASING = "total_increasing"

CODEOWNERS = ["powerfeatherdev (dev@powerfeather.dev)"]
AUTO_LOAD = ["sensor", "binary_sensor", "switch", "button", "number"]

CONF_BATTERY = "battery"
CONF_BINARY_SENSORS = "binary_sensors"
CONF_BOARD_REVISION = "board_revision"
CONF_BUTTONS = "buttons"
CONF_CAPACITY = "capacity"
CONF_MAINBOARD = "mainboard"
CONF_NUMBERS = "numbers"
CONF_SENSORS = "sensors"
CONF_SWITCHES = "switches"

CONF_SUPPLY_VOLTAGE = "supply_voltage"
CONF_SUPPLY_CURRENT = "supply_current"
CONF_BATTERY_VOLTAGE = "battery_voltage"
CONF_BATTERY_CURRENT = "battery_current"
CONF_BATTERY_CHARGE = "battery_charge"
CONF_BATTERY_HEALTH = "battery_health"
CONF_BATTERY_CYCLES = "battery_cycles"
CONF_BATTERY_TIME_LEFT = "battery_time_left"
CONF_BATTERY_TEMPERATURE = "battery_temperature"
CONF_SUPPLY_GOOD = "supply_good"
CONF_SHIP_MODE = "ship_mode"
CONF_SHUTDOWN = "shutdown"
CONF_POWER_CYCLE = "powercycle"
CONF_UPDATE_BATTERY_FUEL_GAUGE_TEMP = "update_battery_fuel_gauge_temp"
CONF_SUPPLY_MAINTAIN_VOLTAGE = "supply_maintain_voltage"
CONF_BATTERY_CHARGING_MAX_CURRENT = "battery_charging_max_current"
CONF_BATTERY_LOW_VOLTAGE_ALARM = "battery_low_voltage_alarm"
CONF_BATTERY_HIGH_VOLTAGE_ALARM = "battery_high_voltage_alarm"
CONF_BATTERY_LOW_CHARGE_ALARM = "battery_low_charge_alarm"
CONF_ENABLE_EN = "enable_EN"
CONF_ENABLE_3V3 = "enable_3V3"
CONF_ENABLE_VSQT = "enable_VSQT"
CONF_ENABLE_BATTERY_TEMP_SENSE = "enable_battery_temp_sense"
CONF_ENABLE_BATTERY_CHARGING = "enable_battery_charging"
CONF_ENABLE_BATTERY_FUEL_GAUGE = "enable_battery_fuel_gauge"
CONF_ENABLE_STAT = "enable_stat"

UPDATE_INTERVAL_MINIMUM = "500ms"

BATTERY_CAPACITY_MINIMUM_V1 = 50
BATTERY_CAPACITY_MAXIMUM_V1 = 6000
BATTERY_CAPACITY_MINIMUM_V2 = 1
BATTERY_CAPACITY_MAXIMUM_V2 = 16383
SUPPLY_MAINTAIN_VOLTAGE_MIN = 4.6
SUPPLY_MAINTAIN_VOLTAGE_MAX = 16.8
SUPPLY_MAINTAIN_VOLTAGE_STEP = 0.012
BATTERY_CHARGING_CURRENT_MIN = 40
BATTERY_CHARGING_CURRENT_MAX = 2000
BATTERY_CHARGING_CURRENT_STEP = 4
BATTERY_ALARM_VOLTAGE_MIN = 0
BATTERY_ALARM_VOLTAGE_MAX_V1 = 5.0
BATTERY_ALARM_VOLTAGE_MAX_V2 = 5.1
BATTERY_ALARM_VOLTAGE_STEP = 0.01
BATTERY_ALARM_CHARGE_MIN = 0
BATTERY_ALARM_CHARGE_MAX = 100
BATTERY_ALARM_CHARGE_STEP = 1

BOARD_REVISION_V1 = "v1"
BOARD_REVISION_V2 = "v2"
BOARD_REVISIONS = {
    BOARD_REVISION_V1: BOARD_REVISION_V1,
    BOARD_REVISION_V2: BOARD_REVISION_V2,
}

powerfeather_ns = cg.esphome_ns.namespace("powerfeather")
PowerFeatherMainboard = powerfeather_ns.class_(
    "PowerFeatherMainboard", cg.PollingComponent,
)
PowerFeatherButton = powerfeather_ns.class_("PowerFeatherButton", button.Button, cg.Component)
PowerFeatherSwitch = powerfeather_ns.class_("PowerFeatherSwitch", switch.Switch, cg.Component)
PowerFeatherValue = powerfeather_ns.class_("PowerFeatherValue", number.Number, cg.Component)

BatteryType = powerfeather_ns.enum("BatteryType")
BATTERY_TYPES = {
    "Generic_3V7": BatteryType.Generic_3V7,
    "ICR18650_26H": BatteryType.ICR18650_26H,
    "UR18650ZY": BatteryType.UR18650ZY,
    "Generic_LFP": BatteryType.Generic_LFP,
}
BATTERY_TYPE_OPTIONS = {key: key for key in BATTERY_TYPES}

TaskUpdateType = powerfeather_ns.enum("TaskUpdateType")
TASK_UPDATE_TYPES = {
    "ENABLE_EN": TaskUpdateType.ENABLE_EN,
    "ENABLE_3V3": TaskUpdateType.ENABLE_3V3,
    "ENABLE_VSQT": TaskUpdateType.ENABLE_VSQT,
    "ENABLE_BATTERY_TEMP_SENSE": TaskUpdateType.ENABLE_BATTERY_TEMP_SENSE,
    "ENABLE_BATTERY_FUEL_GAUGE": TaskUpdateType.ENABLE_BATTERY_FUEL_GAUGE,
    "ENABLE_BATTERY_CHARGING": TaskUpdateType.ENABLE_BATTERY_CHARGING,
    "ENABLE_STAT": TaskUpdateType.ENABLE_STAT,
    "SHIP_MODE": TaskUpdateType.SHIP_MODE,
    "SHUTDOWN": TaskUpdateType.SHUTDOWN,
    "POWERCYCLE": TaskUpdateType.POWERCYCLE,
    "UPDATE_BATTERY_FUEL_GAUGE_TEMP": TaskUpdateType.UPDATE_BATTERY_FUEL_GAUGE_TEMP,
    "SUPPLY_MAINTAIN_VOLTAGE": TaskUpdateType.SUPPLY_MAINTAIN_VOLTAGE,
    "BATTERY_CHARGING_MAX_CURRENT": TaskUpdateType.BATTERY_CHARGING_MAX_CURRENT,
    "BATTERY_LOW_VOLTAGE_ALARM": TaskUpdateType.BATTERY_LOW_VOLTAGE_ALARM,
    "BATTERY_HIGH_VOLTAGE_ALARM": TaskUpdateType.BATTERY_HIGH_VOLTAGE_ALARM,
    "BATTERY_LOW_CHARGE_ALARM": TaskUpdateType.BATTERY_LOW_CHARGE_ALARM,
}


def validate_update_interval(value):
    value = cv.positive_time_period_milliseconds(value)
    if value < cv.time_period(UPDATE_INTERVAL_MINIMUM):
        raise cv.Invalid(
            "Update interval must be at least {}".format(UPDATE_INTERVAL_MINIMUM)
        )
    return value


BATTERY_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_CAPACITY, default=0): cv.int_range(
            min=0,
            max=BATTERY_CAPACITY_MAXIMUM_V2,
        ),
        cv.Optional(CONF_TYPE, default="Generic_3V7"): cv.enum(BATTERY_TYPE_OPTIONS),
    }
)

SENSORS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SUPPLY_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_VOLTAGE,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_SUPPLY_CURRENT): sensor.sensor_schema(
            unit_of_measurement=UNIT_MILLIAMPERE,
            icon=ICON_CURRENT_DC,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_VOLTAGE,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_CURRENT): sensor.sensor_schema(
            unit_of_measurement=UNIT_MILLIAMPERE,
            icon=ICON_CURRENT_DC,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_CHARGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            icon=ICON_BATTERY,
            device_class=DEVICE_CLASS_BATTERY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_HEALTH): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            icon=ICON_PERCENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_CYCLES): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon=ICON_EMPTY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_BATTERY_TIME_LEFT): sensor.sensor_schema(
            unit_of_measurement=UNIT_MINUTES,
            icon=ICON_TIMER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_TEMPERATURE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            icon=ICON_THERMOMETER,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

BINARY_SENSORS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SUPPLY_GOOD): binary_sensor.binary_sensor_schema(
            device_class=DEVICE_CLASS_POWER,
        ),
    }
)

BUTTONS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SHIP_MODE): button.button_schema(PowerFeatherButton),
        cv.Optional(CONF_SHUTDOWN): button.button_schema(PowerFeatherButton),
        cv.Optional(CONF_POWER_CYCLE): button.button_schema(
            PowerFeatherButton,
            icon=ICON_RESTART,
            device_class=DEVICE_CLASS_RESTART,
        ),
        cv.Optional(CONF_UPDATE_BATTERY_FUEL_GAUGE_TEMP): button.button_schema(
            PowerFeatherButton,
            icon=ICON_THERMOMETER,
        ),
    }
)

NUMBERS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SUPPLY_MAINTAIN_VOLTAGE): number.number_schema(
            PowerFeatherValue,
            icon=ICON_VOLTAGE,
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_BATTERY_CHARGING_MAX_CURRENT): number.number_schema(
            PowerFeatherValue,
            icon=ICON_CURRENT_DC,
            unit_of_measurement=UNIT_MILLIAMPERE,
            device_class=DEVICE_CLASS_CURRENT,
        ),
        cv.Optional(CONF_BATTERY_LOW_VOLTAGE_ALARM): number.number_schema(
            PowerFeatherValue,
            icon=ICON_VOLTAGE,
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_BATTERY_HIGH_VOLTAGE_ALARM): number.number_schema(
            PowerFeatherValue,
            icon=ICON_VOLTAGE,
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_BATTERY_LOW_CHARGE_ALARM): number.number_schema(
            PowerFeatherValue,
            icon=ICON_BATTERY,
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
    }
)

SWITCHES_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_ENABLE_EN): switch.switch_schema(
            PowerFeatherSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_ENABLE_3V3): switch.switch_schema(
            PowerFeatherSwitch,
            icon=ICON_ENERGY,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_ENABLE_VSQT): switch.switch_schema(
            PowerFeatherSwitch,
            icon=ICON_ENERGY,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_ENABLE_BATTERY_TEMP_SENSE): switch.switch_schema(
            PowerFeatherSwitch,
            icon=ICON_THERMOMETER,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_ENABLE_BATTERY_CHARGING): switch.switch_schema(
            PowerFeatherSwitch,
            icon=ICON_ENERGY,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_ENABLE_BATTERY_FUEL_GAUGE): switch.switch_schema(
            PowerFeatherSwitch,
            icon=ICON_GAUGE,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_ENABLE_STAT): switch.switch_schema(
            PowerFeatherSwitch,
            icon=ICON_LED_ON,
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)


def validate_battery_capacity_for_board_revision(config):
    battery = config[CONF_BATTERY]
    capacity = battery[CONF_CAPACITY]
    battery_type = battery[CONF_TYPE]
    if (
        config[CONF_BOARD_REVISION] == BOARD_REVISION_V1
        and battery_type == "Generic_LFP"
    ):
        raise cv.Invalid("Generic_LFP battery type requires board_revision v2")

    if capacity == 0:
        return config

    if config[CONF_BOARD_REVISION] == BOARD_REVISION_V1:
        if not BATTERY_CAPACITY_MINIMUM_V1 <= capacity <= BATTERY_CAPACITY_MAXIMUM_V1:
            raise cv.Invalid(
                "battery capacity for board_revision v1 must be 0 or between "
                f"{BATTERY_CAPACITY_MINIMUM_V1} and {BATTERY_CAPACITY_MAXIMUM_V1} mAh"
            )
    elif not BATTERY_CAPACITY_MINIMUM_V2 <= capacity <= BATTERY_CAPACITY_MAXIMUM_V2:
        raise cv.Invalid(
            "battery capacity for board_revision v2 must be 0 or between "
            f"{BATTERY_CAPACITY_MINIMUM_V2} and {BATTERY_CAPACITY_MAXIMUM_V2} mAh"
        )

    return config


MAINBOARD_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(PowerFeatherMainboard),
            cv.Optional(CONF_BOARD_REVISION, default=BOARD_REVISION_V1): cv.enum(BOARD_REVISIONS),
            cv.Optional(CONF_BATTERY, default={}): BATTERY_SCHEMA,
            cv.Optional(CONF_UPDATE_INTERVAL, default="10s"): validate_update_interval,
            cv.Optional(CONF_SENSORS, default={}): SENSORS_SCHEMA,
            cv.Optional(CONF_BINARY_SENSORS, default={}): BINARY_SENSORS_SCHEMA,
            cv.Optional(CONF_BUTTONS, default={}): BUTTONS_SCHEMA,
            cv.Optional(CONF_NUMBERS, default={}): NUMBERS_SCHEMA,
            cv.Optional(CONF_SWITCHES, default={}): SWITCHES_SCHEMA,
        }
    ),
    validate_battery_capacity_for_board_revision,
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_MAINBOARD): cv.ensure_list(MAINBOARD_SCHEMA),
    }
)


async def _add_sensor(mainboard, config, key, setter):
    if key not in config:
        return
    sens = await sensor.new_sensor(config[key])
    cg.add(getattr(mainboard, setter)(sens))


async def _add_binary_sensor(mainboard, config, key, setter):
    if key not in config:
        return
    sens = await binary_sensor.new_binary_sensor(config[key])
    cg.add(getattr(mainboard, setter)(sens))


async def _add_button(mainboard, config, key, update_type, setter):
    if key not in config:
        return
    btn = await button.new_button(config[key])
    await cg.register_parented(btn, mainboard)
    cg.add(btn.set_update_type(TASK_UPDATE_TYPES[update_type]))
    cg.add(getattr(mainboard, setter)(btn))


async def _add_number(mainboard, config, key, update_type, setter, min_value, max_value, step):
    if key not in config:
        return
    value = await number.new_number(
        config[key],
        min_value=min_value,
        max_value=max_value,
        step=step,
    )
    await cg.register_parented(value, mainboard)
    cg.add(value.set_update_type(TASK_UPDATE_TYPES[update_type]))
    cg.add(getattr(mainboard, setter)(value))


async def _add_switch(mainboard, config, key, update_type, setter):
    if key not in config:
        return
    sw = await switch.new_switch(config[key])
    await cg.register_parented(sw, mainboard)
    cg.add(sw.set_update_type(TASK_UPDATE_TYPES[update_type]))
    cg.add(getattr(mainboard, setter)(sw))


async def to_code(config):
    cg.add_library(name="PowerFeather-SDK", version="^2.0.0")

    if CORE.using_arduino:
        cg.add_build_flag("-DARDUINO_ESP32S3_POWERFEATHER")

    if any(item[CONF_BOARD_REVISION] == BOARD_REVISION_V2 for item in config[CONF_MAINBOARD]):
        cg.add_build_flag("-DPOWERFEATHER_BOARD_V2")
        if not CORE.using_arduino and add_idf_sdkconfig_option is not None:
            add_idf_sdkconfig_option("CONFIG_ESP32S3_POWERFEATHER_V2", True)

    for mainboard_config in config[CONF_MAINBOARD]:
        mainboard = cg.new_Pvariable(mainboard_config[CONF_ID])
        await cg.register_component(mainboard, mainboard_config)

        battery = mainboard_config[CONF_BATTERY]
        cg.add(mainboard.set_battery_capacity(battery[CONF_CAPACITY]))
        cg.add(mainboard.set_battery_type(BATTERY_TYPES[battery[CONF_TYPE]]))

        sensors = mainboard_config[CONF_SENSORS]
        await _add_sensor(mainboard, sensors, CONF_SUPPLY_VOLTAGE, "set_supply_voltage_sensor")
        await _add_sensor(mainboard, sensors, CONF_SUPPLY_CURRENT, "set_supply_current_sensor")
        await _add_sensor(mainboard, sensors, CONF_BATTERY_VOLTAGE, "set_battery_voltage_sensor")
        await _add_sensor(mainboard, sensors, CONF_BATTERY_CURRENT, "set_battery_current_sensor")
        await _add_sensor(mainboard, sensors, CONF_BATTERY_CHARGE, "set_battery_charge_sensor")
        await _add_sensor(mainboard, sensors, CONF_BATTERY_HEALTH, "set_battery_health_sensor")
        await _add_sensor(mainboard, sensors, CONF_BATTERY_CYCLES, "set_battery_cycles_sensor")
        await _add_sensor(mainboard, sensors, CONF_BATTERY_TIME_LEFT, "set_battery_time_left_sensor")
        await _add_sensor(mainboard, sensors, CONF_BATTERY_TEMPERATURE, "set_battery_temperature_sensor")

        binary_sensors = mainboard_config[CONF_BINARY_SENSORS]
        await _add_binary_sensor(mainboard, binary_sensors, CONF_SUPPLY_GOOD, "set_supply_good_sensor")

        buttons = mainboard_config[CONF_BUTTONS]
        await _add_button(mainboard, buttons, CONF_SHIP_MODE, "SHIP_MODE", "set_ship_mode_button")
        await _add_button(mainboard, buttons, CONF_SHUTDOWN, "SHUTDOWN", "set_shutdown_button")
        await _add_button(mainboard, buttons, CONF_POWER_CYCLE, "POWERCYCLE", "set_powercycle_button")
        await _add_button(
            mainboard,
            buttons,
            CONF_UPDATE_BATTERY_FUEL_GAUGE_TEMP,
            "UPDATE_BATTERY_FUEL_GAUGE_TEMP",
            "set_update_battery_fuel_gauge_temp_button",
        )

        numbers = mainboard_config[CONF_NUMBERS]
        battery_alarm_voltage_max = (
            BATTERY_ALARM_VOLTAGE_MAX_V2
            if mainboard_config[CONF_BOARD_REVISION] == BOARD_REVISION_V2
            else BATTERY_ALARM_VOLTAGE_MAX_V1
        )
        await _add_number(
            mainboard,
            numbers,
            CONF_SUPPLY_MAINTAIN_VOLTAGE,
            "SUPPLY_MAINTAIN_VOLTAGE",
            "set_supply_maintain_voltage_value",
            SUPPLY_MAINTAIN_VOLTAGE_MIN,
            SUPPLY_MAINTAIN_VOLTAGE_MAX,
            SUPPLY_MAINTAIN_VOLTAGE_STEP,
        )
        await _add_number(
            mainboard,
            numbers,
            CONF_BATTERY_CHARGING_MAX_CURRENT,
            "BATTERY_CHARGING_MAX_CURRENT",
            "set_battery_charging_max_current_value",
            BATTERY_CHARGING_CURRENT_MIN,
            BATTERY_CHARGING_CURRENT_MAX,
            BATTERY_CHARGING_CURRENT_STEP,
        )
        await _add_number(
            mainboard,
            numbers,
            CONF_BATTERY_LOW_VOLTAGE_ALARM,
            "BATTERY_LOW_VOLTAGE_ALARM",
            "set_battery_low_voltage_alarm_value",
            BATTERY_ALARM_VOLTAGE_MIN,
            battery_alarm_voltage_max,
            BATTERY_ALARM_VOLTAGE_STEP,
        )
        await _add_number(
            mainboard,
            numbers,
            CONF_BATTERY_HIGH_VOLTAGE_ALARM,
            "BATTERY_HIGH_VOLTAGE_ALARM",
            "set_battery_high_voltage_alarm_value",
            BATTERY_ALARM_VOLTAGE_MIN,
            battery_alarm_voltage_max,
            BATTERY_ALARM_VOLTAGE_STEP,
        )
        await _add_number(
            mainboard,
            numbers,
            CONF_BATTERY_LOW_CHARGE_ALARM,
            "BATTERY_LOW_CHARGE_ALARM",
            "set_battery_low_charge_alarm_value",
            BATTERY_ALARM_CHARGE_MIN,
            BATTERY_ALARM_CHARGE_MAX,
            BATTERY_ALARM_CHARGE_STEP,
        )

        switches = mainboard_config[CONF_SWITCHES]
        await _add_switch(mainboard, switches, CONF_ENABLE_EN, "ENABLE_EN", "set_enable_EN_switch")
        await _add_switch(mainboard, switches, CONF_ENABLE_3V3, "ENABLE_3V3", "set_enable_3V3_switch")
        await _add_switch(mainboard, switches, CONF_ENABLE_VSQT, "ENABLE_VSQT", "set_enable_VSQT_switch")
        await _add_switch(
            mainboard,
            switches,
            CONF_ENABLE_BATTERY_TEMP_SENSE,
            "ENABLE_BATTERY_TEMP_SENSE",
            "set_enable_battery_temp_sense_switch",
        )
        await _add_switch(
            mainboard,
            switches,
            CONF_ENABLE_BATTERY_CHARGING,
            "ENABLE_BATTERY_CHARGING",
            "set_enable_battery_charging_switch",
        )
        await _add_switch(
            mainboard,
            switches,
            CONF_ENABLE_BATTERY_FUEL_GAUGE,
            "ENABLE_BATTERY_FUEL_GAUGE",
            "set_enable_battery_fuel_gauge_switch",
        )
        await _add_switch(mainboard, switches, CONF_ENABLE_STAT, "ENABLE_STAT", "set_enable_stat_switch")
