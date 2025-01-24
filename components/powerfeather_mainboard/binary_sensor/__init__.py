import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from .. import CONF_POWERFEATHER_MAINBOARD_ID, POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA, TASK_UPDATE_TYPES, powerfeather_ns, PowerFeatherMainboard

CONF_SUPPLY_GOOD_SENSOR = "supply_good"

CONFIG_SCHEMA = POWERFEATHER_MAINBOARD_COMPONENT_SCHEMA.extend(
    {
        cv.Optional(CONF_SUPPLY_GOOD_SENSOR): binary_sensor.binary_sensor_schema()
    }
)

async def to_code(config):
    mainboard = await cg.get_variable(config[CONF_POWERFEATHER_MAINBOARD_ID])
    if supply_good_sensor_config := config.get(CONF_SUPPLY_GOOD_SENSOR):
        sens = await binary_sensor.new_binary_sensor(supply_good_sensor_config)
        cg.add(mainboard.set_supply_good_sensor(sens))