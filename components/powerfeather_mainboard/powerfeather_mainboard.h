#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/number/number.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/button/button.h"

#include <PowerFeather.h>

namespace esphome
{
  namespace powerfeather_mainboard
  {
    enum BatteryType
    {
      Generic_3V7
    };

   enum TaskUpdateType
    {
      SENSORS = 0,
      ENABLE_EN,
      ENABLE_3V3,
      ENABLE_VSQT,
      ENABLE_BATTERY_TEMP_SENSE,
      ENABLE_BATTERY_FUEL_GAUGE,
      ENABLE_BATTERY_CHARGING,
      ENABLE_STAT,
      POWERCYCLE,
      SHIP_MODE,
      SHUTDOWN,
      SUPPLY_MAINTAIN_VOLTAGE,
      BATTERY_CHARGING_MAX_CURRENT,
    };

    typedef struct
    {
      TaskUpdateType type;
      union
      {
        bool b;
        int32_t i;
        float f;
        uint32_t u;
      } data;
    } TaskUpdate;

    class PowerFeatherUpdateable
    {
    public:
      PowerFeatherUpdateable() = default;
      void set_update_type(TaskUpdateType type) { type_ = type; }
    protected:
      TaskUpdateType type_;
    };

    class PowerFeatherMainboard : public PollingComponent
    {
    public:
      void setup() override;
      void update() override;
      void dump_config() override;

      void set_battery_capacity(int32_t battery_capacity) { battery_capacity_ = battery_capacity; }
      void set_battery_type(BatteryType battery_type)
      {
        switch (battery_type)
        {
        case Generic_3V7:
        default:
          battery_type_ = PowerFeather::Mainboard::BatteryType::Generic_3V7;
          break;
        }
      }
      void set_supply_voltage_sensor(sensor::Sensor *sensor) { supply_voltage_sensor_ = sensor; }
      void set_supply_current_sensor(sensor::Sensor *sensor) { supply_current_sensor_ = sensor; }
      void set_supply_good_sensor(binary_sensor::BinarySensor *sensor) { supply_good_sensor_ = sensor; }
      void set_battery_voltage_sensor(sensor::Sensor *sensor) { battery_voltage_sensor_ = sensor; }
      void set_battery_current_sensor(sensor::Sensor *sensor) { battery_current_sensor_ = sensor; }
      void set_battery_charge_sensor(sensor::Sensor *sensor) { battery_charge_sensor_ = sensor; }
      void set_battery_health_sensor(sensor::Sensor *sensor) { battery_health_sensor_ = sensor; }
      void set_battery_cycles_sensor(sensor::Sensor *sensor) { battery_cycles_sensor_ = sensor; }
      void set_battery_time_left_sensor(sensor::Sensor *sensor) { battery_time_left_sensor_ = sensor; }
      void set_battery_temperature_sensor(sensor::Sensor *sensor) { battery_temperature_sensor_ = sensor; }

      void set_enable_3V3_switch(switch_::Switch *sw) { enable_3V3_switch_ = sw; }
      void set_enable_VSQT_switch(switch_::Switch *sw) { enable_VSQT_switch_ = sw; }
      void set_enable_EN_switch(switch_::Switch *sw) { enable_EN_switch_ = sw; }
      void set_enable_battery_charging_switch(switch_::Switch *sw) { enable_battery_charging_switch_ = sw; }
      void set_enable_battery_temp_sense_switch(switch_::Switch *sw) { enable_battery_temp_sense_switch_ = sw; }
      void set_enable_battery_fuel_gauge_switch(switch_::Switch *sw) { enable_battery_fuel_gauge_switch_ = sw; }
      void set_enable_stat_switch(switch_::Switch *sw) { enable_stat_switch_ = sw; }

      void set_ship_mode_button(button::Button *button) { ship_mode_button_ = button; }
      void set_shutdown_button(button::Button *button) { shutdown_button_ = button; }
      void set_powercycle_button(button::Button *button) { powercycle_button_ = button; }

      void set_supply_maintain_voltage_value(number::Number *value) { supply_maintain_voltage_value_ = value; }
      void set_battery_charging_max_current_value(number::Number *value) { battery_charging_max_current_value_ = value; }

      void send_task_update(TaskUpdate update);

    private:
      static const size_t UPDATE_TASK_STACK_SIZE_ = 3192;
      static const size_t UPDATE_TASK_QUEUE_SIZE_ = 10;
      static const uint32_t UPDATE_TASK_QUEUE_WAIT_MS_ = 250;

      int32_t battery_capacity_;
      PowerFeather::Mainboard::BatteryType battery_type_;

      bool supply_good_;
      bool enable_EN_;
      bool enable_3V3_;
      bool enable_VSQT_;
      bool enable_battery_charging_;
      bool enable_battery_temp_sense_;
      bool enable_battery_fuel_gauge_;
      bool enable_stat_;
      float supply_voltage_;
      float supply_current_;
      float battery_voltage_;
      float battery_current_;
      float battery_charge_;
      float battery_health_;
      float battery_cycles_;
      float battery_time_left_;
      float battery_temperature_;
      float battery_charging_max_current_;
      float supply_maintain_voltage_;

      QueueHandle_t update_task_queue_ = NULL;

      switch_::Switch *enable_EN_switch_;
      switch_::Switch *enable_3V3_switch_;
      switch_::Switch *enable_VSQT_switch_;
      switch_::Switch *enable_battery_temp_sense_switch_;
      switch_::Switch *enable_battery_charging_switch_;
      switch_::Switch *enable_battery_fuel_gauge_switch_;
      switch_::Switch *enable_stat_switch_;
      binary_sensor::BinarySensor *supply_good_sensor_;
      sensor::Sensor *supply_voltage_sensor_;
      sensor::Sensor *supply_current_sensor_;
      sensor::Sensor *battery_voltage_sensor_;
      sensor::Sensor *battery_current_sensor_;
      sensor::Sensor *battery_charge_sensor_;
      sensor::Sensor *battery_health_sensor_;
      sensor::Sensor *battery_cycles_sensor_;
      sensor::Sensor *battery_time_left_sensor_;
      sensor::Sensor *battery_temperature_sensor_;
      button::Button *ship_mode_button_;
      button::Button *shutdown_button_;
      button::Button *powercycle_button_;
      number::Number *supply_maintain_voltage_value_;
      number::Number *battery_charging_max_current_value_;

      static void update_task_(void *param);
    };
  } // namespace empty_compound_sensor
} // namespace esphome