
#include "esphome/core/log.h"
#include "powerfeather.h"

#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_timer.h"

namespace esphome
{
  namespace powerfeather
  {
    static const char *TAG = "powerfeather.mainboard";
    // Mirrored from SDK-managed Mainboard::Pin values. The SDK exposes setters,
    // but not getters, so setup reads the retained RTC output levels directly.
    static constexpr gpio_num_t PIN_EN_3V3 = GPIO_NUM_4;
    static constexpr gpio_num_t PIN_EN_VSQT = GPIO_NUM_14;
    static constexpr gpio_num_t PIN_EN0 = GPIO_NUM_13;

    static uint32_t millis()
    {
      return esp_timer_get_time() / 1000;
    }

    static bool check_result(const char *operation, PowerFeather::Result result)
    {
      if (result == PowerFeather::Result::Ok)
      {
        return true;
      }
      ESP_LOGW(TAG, "%s failed with SDK result %u", operation, static_cast<uint32_t>(result));
      return false;
    }

    static bool check_bool_result(const char *operation, bool result)
    {
      if (result)
      {
        return true;
      }
      ESP_LOGW(TAG, "%s failed", operation);
      return false;
    }

    template<typename T, typename ReadFn> void read_mainboard_value(const char *operation, T &target, ReadFn read)
    {
      T value{};
      if (check_result(operation, read(value)))
      {
        target = value;
      }
    }

    void PowerFeatherMainboard::update_sensors_()
    {
      if (supply_voltage_sensor_ != nullptr)
      {
        read_mainboard_value("Read supply voltage", supply_voltage_, [](float &value) {
          return PowerFeather::Board.getSupplyVoltage(value);
        });
      }

      if (supply_current_sensor_ != nullptr)
      {
        read_mainboard_value("Read supply current", supply_current_, [](float &value) {
          return PowerFeather::Board.getSupplyCurrent(value);
        });
      }

      if (supply_good_sensor_ != nullptr)
      {
        read_mainboard_value("Read supply good state", supply_good_, [](bool &value) {
          return PowerFeather::Board.checkSupplyGood(value);
        });
      }

      if (battery_voltage_sensor_ != nullptr)
      {
        read_mainboard_value("Read battery voltage", battery_voltage_, [](float &value) {
          return PowerFeather::Board.getBatteryVoltage(value);
        });
      }

      if (battery_current_sensor_ != nullptr)
      {
        read_mainboard_value("Read battery current", battery_current_, [](float &value) {
          return PowerFeather::Board.getBatteryCurrent(value);
        });
      }

      if (battery_charge_sensor_ != nullptr)
      {
        uint8_t battery_charge = 0;
        if (check_result("Read battery charge", PowerFeather::Board.getBatteryCharge(battery_charge)))
        {
          battery_charge_ = battery_charge;
        }
      }

      if (battery_health_sensor_ != nullptr)
      {
        uint8_t battery_health = 0;
        if (check_result("Read battery health", PowerFeather::Board.getBatteryHealth(battery_health)))
        {
          battery_health_ = battery_health;
        }
      }

      if (battery_cycles_sensor_ != nullptr)
      {
        uint16_t battery_cycles = 0;
        if (check_result("Read battery cycles", PowerFeather::Board.getBatteryCycles(battery_cycles)))
        {
          battery_cycles_ = battery_cycles;
        }
      }

      if (battery_time_left_sensor_ != nullptr)
      {
        read_mainboard_value("Read battery time left", battery_time_left_, [](float &value) {
          int battery_time_left = 0;
          auto result = PowerFeather::Board.getBatteryTimeLeft(battery_time_left);
          value = battery_time_left;
          return result;
        });
      }

      if (battery_temperature_sensor_ != nullptr)
      {
        read_mainboard_value("Read battery temperature", battery_temperature_, [](float &value) {
          return PowerFeather::Board.getBatteryTemperature(value);
        });
      }
    }

    void PowerFeatherMainboard::update_task_(void *param)
    {
      powerfeather::PowerFeatherMainboard *mainboard =
        reinterpret_cast<powerfeather::PowerFeatherMainboard *>(param);

      auto publish_bool = [mainboard](TaskUpdateType type, bool state) {
        TaskUpdate control_state;
        control_state.type = type;
        control_state.data.b = state;
        mainboard->send_control_state_(control_state);
      };

      auto publish_float = [mainboard](TaskUpdateType type, float state) {
        TaskUpdate control_state;
        control_state.type = type;
        control_state.data.f = state;
        mainboard->send_control_state_(control_state);
      };

      while (true)
      {
        TaskUpdate update;
        update.type = TaskUpdateType::SENSORS;
        xQueueReceive(mainboard->update_task_queue_, &update, portMAX_DELAY);
        switch (update.type)
        {
        case TaskUpdateType::ENABLE_EN:
          ESP_LOGD(TAG, "Received EN enable state: %d", update.data.b);
          if (check_result("Set EN enable state", PowerFeather::Board.setEN(update.data.b)))
          {
            mainboard->enable_EN_ = update.data.b;
          }
          publish_bool(TaskUpdateType::ENABLE_EN, mainboard->enable_EN_);
          break;

        case TaskUpdateType::ENABLE_3V3:
          ESP_LOGD(TAG, "Received 3V3 enable state: %d", update.data.b);
          if (check_result("Set 3V3 enable state", PowerFeather::Board.enable3V3(update.data.b)))
          {
            mainboard->enable_3V3_ = update.data.b;
          }
          publish_bool(TaskUpdateType::ENABLE_3V3, mainboard->enable_3V3_);
          break;

        case TaskUpdateType::ENABLE_VSQT:
          ESP_LOGD(TAG, "Received VSQT enable state: %d", update.data.b);
          if (check_result("Set VSQT enable state", PowerFeather::Board.enableVSQT(update.data.b)))
          {
            mainboard->enable_VSQT_ = update.data.b;
          }
          publish_bool(TaskUpdateType::ENABLE_VSQT, mainboard->enable_VSQT_);
          break;

        case TaskUpdateType::ENABLE_BATTERY_TEMP_SENSE:
          ESP_LOGD(TAG, "Received enable battery temp sense: %d", update.data.b);
          if (check_result("Set battery temp sense enable state", PowerFeather::Board.enableBatteryTempSense(update.data.b)))
          {
            mainboard->enable_battery_temp_sense_ = update.data.b;
          }
          publish_bool(TaskUpdateType::ENABLE_BATTERY_TEMP_SENSE, mainboard->enable_battery_temp_sense_);
          break;

        case TaskUpdateType::ENABLE_BATTERY_FUEL_GAUGE:
          ESP_LOGD(TAG, "Received enable battery fuel gauge: %d", update.data.b);
          if (check_result("Set battery fuel gauge enable state", PowerFeather::Board.enableBatteryFuelGauge(update.data.b)))
          {
            mainboard->enable_battery_fuel_gauge_ = update.data.b;
          }
          publish_bool(TaskUpdateType::ENABLE_BATTERY_FUEL_GAUGE, mainboard->enable_battery_fuel_gauge_);
          break;

        case TaskUpdateType::ENABLE_BATTERY_CHARGING:
          ESP_LOGD(TAG, "Received enable battery charging: %d", update.data.b);
          if (check_result("Set battery charging enable state", PowerFeather::Board.enableBatteryCharging(update.data.b)))
          {
            mainboard->enable_battery_charging_ = update.data.b;
          }
          publish_bool(TaskUpdateType::ENABLE_BATTERY_CHARGING, mainboard->enable_battery_charging_);
          break;

        case TaskUpdateType::ENABLE_STAT:
          ESP_LOGD(TAG, "Received enable STAT LED: %d", update.data.b);
          if (check_result("Set STAT LED enable state", PowerFeather::Board.enableSTAT(update.data.b)))
          {
            mainboard->enable_stat_ = update.data.b;
          }
          publish_bool(TaskUpdateType::ENABLE_STAT, mainboard->enable_stat_);
          break;

        case TaskUpdateType::POWERCYCLE:
          ESP_LOGD(TAG, "Received powercycle request");
          check_result("Power cycle", PowerFeather::Board.doPowerCycle());
          break;

        case TaskUpdateType::UPDATE_BATTERY_FUEL_GAUGE_TEMP:
          ESP_LOGD(TAG, "Received battery fuel gauge temperature update request");
          check_result("Update battery fuel gauge temperature", PowerFeather::Board.updateBatteryFuelGaugeTemp());
          break;

        case TaskUpdateType::SHIP_MODE:
          ESP_LOGD(TAG, "Received ship mode request");
          check_result("Enter ship mode", PowerFeather::Board.enterShipMode());
          break;

        case TaskUpdateType::SHUTDOWN:
          ESP_LOGD(TAG, "Received shutdown request");
          check_result("Enter shutdown mode", PowerFeather::Board.enterShutdownMode());
          break;

        case TaskUpdateType::SUPPLY_MAINTAIN_VOLTAGE:
          ESP_LOGD(TAG, "Received supply maintain voltage value update: %f", update.data.f);
          if (check_result("Set supply maintain voltage", PowerFeather::Board.setSupplyMaintainVoltage(update.data.f)))
          {
            mainboard->supply_maintain_voltage_ = update.data.f;
          }
          publish_float(TaskUpdateType::SUPPLY_MAINTAIN_VOLTAGE, mainboard->supply_maintain_voltage_);
          break;

        case TaskUpdateType::BATTERY_CHARGING_MAX_CURRENT:
          ESP_LOGD(TAG, "Received battery charging max current update: %f", update.data.f);
          if (check_result("Set battery charging max current", PowerFeather::Board.setBatteryChargingMaxCurrent(update.data.f)))
          {
            mainboard->battery_charging_max_current_ = update.data.f;
          }
          publish_float(TaskUpdateType::BATTERY_CHARGING_MAX_CURRENT, mainboard->battery_charging_max_current_);
          break;

        case TaskUpdateType::BATTERY_LOW_VOLTAGE_ALARM:
          ESP_LOGD(TAG, "Received battery low voltage alarm update: %f", update.data.f);
          if (check_result("Set battery low voltage alarm", PowerFeather::Board.setBatteryLowVoltageAlarm(update.data.f)))
          {
            mainboard->battery_low_voltage_alarm_ = update.data.f;
          }
          publish_float(TaskUpdateType::BATTERY_LOW_VOLTAGE_ALARM, mainboard->battery_low_voltage_alarm_);
          break;

        case TaskUpdateType::BATTERY_HIGH_VOLTAGE_ALARM:
          ESP_LOGD(TAG, "Received battery high voltage alarm update: %f", update.data.f);
          if (check_result("Set battery high voltage alarm", PowerFeather::Board.setBatteryHighVoltageAlarm(update.data.f)))
          {
            mainboard->battery_high_voltage_alarm_ = update.data.f;
          }
          publish_float(TaskUpdateType::BATTERY_HIGH_VOLTAGE_ALARM, mainboard->battery_high_voltage_alarm_);
          break;

        case TaskUpdateType::BATTERY_LOW_CHARGE_ALARM:
          ESP_LOGD(TAG, "Received battery low charge alarm update: %f", update.data.f);
          if (check_result("Set battery low charge alarm", PowerFeather::Board.setBatteryLowChargeAlarm(static_cast<uint8_t>(update.data.f))))
          {
            mainboard->battery_low_charge_alarm_ = update.data.f;
          }
          publish_float(TaskUpdateType::BATTERY_LOW_CHARGE_ALARM, mainboard->battery_low_charge_alarm_);
          break;

        case TaskUpdateType::SENSORS:
        default:
        {
          ESP_LOGD(TAG, "Received sensors update request");
          mainboard->update_sensors_();
        }
        break;
        }
      }
    }

    void PowerFeatherMainboard::setup()
    {
      #define EXIT_SETUP()        { mark_failed(); ESP_LOGE(TAG, "Failed setup at line %d", __LINE__); return; }
      #define CHECK_RES(operation, res)      if (!check_result((operation), (res))) EXIT_SETUP();
      #define CHECK_BOOL(operation, res)     if (!check_bool_result((operation), (res))) EXIT_SETUP();

      ESP_LOGD(TAG, "Initializing board, capacity: %d mAh and type: %u", this->battery_capacity_, static_cast<uint32_t>(this->battery_type_));
      if (this->battery_capacity_)
      {
        CHECK_RES("Initialize PowerFeather board with battery", PowerFeather::Board.init(this->battery_capacity_, this->battery_type_));
      }
      else
      {
        CHECK_RES("Initialize PowerFeather board without battery", PowerFeather::Board.init());
      }

      update_sensors_();

      if (enable_3V3_switch_)
      {
        enable_3V3_ = rtc_gpio_get_level(PIN_EN_3V3);
        enable_3V3_switch_->publish_state(enable_3V3_);
      }

      if (enable_VSQT_switch_)
      {
        enable_VSQT_ = rtc_gpio_get_level(PIN_EN_VSQT);
        enable_VSQT_switch_->publish_state(enable_VSQT_);
      }

      if (enable_EN_switch_)
      {
        enable_EN_ = rtc_gpio_get_level(PIN_EN0);
        enable_EN_switch_->publish_state(enable_EN_);
      }

      if (enable_stat_switch_)
      {
        CHECK_BOOL("Read STAT LED enable state", PowerFeather::Board.getCharger().getSTATEnabled(enable_stat_));
        enable_stat_switch_->publish_state(enable_stat_);
      }

      if (supply_maintain_voltage_value_)
      {
        float value = 0.0f;
        CHECK_BOOL("Read supply maintain voltage", PowerFeather::Board.getCharger().getVINDPM(value));
        supply_maintain_voltage_ = value;
        supply_maintain_voltage_value_->publish_state(supply_maintain_voltage_);
      }

      if (battery_charging_max_current_value_)
      {
        float value = 0.0f;
        CHECK_BOOL("Read battery charging max current", PowerFeather::Board.getCharger().getChargeCurrentLimit(value));
        battery_charging_max_current_ = value;
        battery_charging_max_current_value_->publish_state(battery_charging_max_current_);
      }

      if (enable_battery_charging_switch_ && battery_capacity_)
      {
        CHECK_BOOL("Read battery charging enable state", PowerFeather::Board.getCharger().getChargingEnabled(enable_battery_charging_));
        enable_battery_charging_switch_->publish_state(enable_battery_charging_);
      }

      if (enable_battery_temp_sense_switch_)
      {
        CHECK_BOOL("Read battery temp sense enable state", PowerFeather::Board.getCharger().getTSEnabled(enable_battery_temp_sense_));
        enable_battery_temp_sense_switch_->publish_state(enable_battery_temp_sense_);
      }

      if (enable_battery_fuel_gauge_switch_ && battery_capacity_)
      {
        // Can fail here when no battery is actually connected, so do not check the result.
        // In that case, consider as not enabled. Initialize value before attempting to read.
        enable_battery_fuel_gauge_ = false;
        PowerFeather::Board.getFuelGauge().getEnabled(enable_battery_fuel_gauge_);
        enable_battery_fuel_gauge_switch_->publish_state(enable_battery_fuel_gauge_);
      }

      #undef CHECK_RES
      #undef CHECK_BOOL

      update_task_queue_ = xQueueCreate(UPDATE_TASK_QUEUE_SIZE_, sizeof(TaskUpdate));
      if (update_task_queue_ == NULL)
      {
        ESP_LOGE(TAG, "Failed to create PowerFeather task queue");
        mark_failed();
        return;
      }

      control_state_queue_ = xQueueCreate(UPDATE_TASK_QUEUE_SIZE_, sizeof(TaskUpdate));
      if (control_state_queue_ == NULL)
      {
        ESP_LOGE(TAG, "Failed to create PowerFeather control state queue");
        mark_failed();
        return;
      }

      if (xTaskCreate(update_task_, "powerfeather", UPDATE_TASK_STACK_SIZE_, this, uxTaskPriorityGet(NULL), NULL) != pdTRUE)
      {
        ESP_LOGE(TAG, "Failed to create PowerFeather update task");
        mark_failed();
        return;
      }

    }

    void PowerFeatherMainboard::loop()
    {
      publish_control_states_();

      uint32_t now = millis();
      // Do sensors update before an anticipated read
      if (!sensors_updated_ && now >= ((sensors_publish_time_ + update_interval_) - UPDATE_TASK_SENSOR_UPDATE_MS_))
      {
        ESP_LOGD(TAG, "Updating sensor values t=%u ms", now);
        TaskUpdate update;
        update.type = TaskUpdateType::SENSORS;
        send_task_update(update);
        sensors_updated_ = true;
      }
    }

    void PowerFeatherMainboard::update()
    {
      uint32_t now = millis();
      ESP_LOGD(TAG, "Publishing sensor values t=%u ms", now);
      if (this->supply_voltage_sensor_ != nullptr)
      {
        this->supply_voltage_sensor_->publish_state(this->supply_voltage_);
      }
      if (this->supply_current_sensor_ != nullptr)
      {
        this->supply_current_sensor_->publish_state(this->supply_current_);
      }
      if (this->supply_good_sensor_ != nullptr)
      {
        this->supply_good_sensor_->publish_state(this->supply_good_);
      }
      if (this->battery_voltage_sensor_ != nullptr)
      {
        this->battery_voltage_sensor_->publish_state(this->battery_voltage_);
      }
      if (this->battery_current_sensor_ != nullptr)
      {
        this->battery_current_sensor_->publish_state(this->battery_current_);
      }
      if (this->battery_charge_sensor_ != nullptr)
      {
        this->battery_charge_sensor_->publish_state(this->battery_charge_);
      }
      if (this->battery_health_sensor_ != nullptr)
      {
        this->battery_health_sensor_->publish_state(this->battery_health_);
      }
      if (this->battery_cycles_sensor_ != nullptr)
      {
        this->battery_cycles_sensor_->publish_state(this->battery_cycles_);
      }
      if (this->battery_time_left_sensor_ != nullptr)
      {
        this->battery_time_left_sensor_->publish_state(this->battery_time_left_);
      }
      if (this->battery_temperature_sensor_ != nullptr)
      {
        this->battery_temperature_sensor_->publish_state(this->battery_temperature_);
      }
      sensors_publish_time_ = now;
      sensors_updated_ = false;
    }

    void PowerFeatherMainboard::dump_config()
    {
      ESP_LOGCONFIG(TAG, "Battery Capacity: %u", battery_capacity_);
      const char* battery_type_str;
      switch (battery_type_)
      {
      case PowerFeather::Mainboard::BatteryType::Generic_3V7:
        battery_type_str = "Generic_3V7";
        break;

      case PowerFeather::Mainboard::BatteryType::ICR18650_26H:
        battery_type_str = "ICR18650_26H";
        break;

      case PowerFeather::Mainboard::BatteryType::UR18650ZY:
        battery_type_str = "UR18650ZY";
        break;

      case PowerFeather::Mainboard::BatteryType::Generic_LFP:
        battery_type_str = "Generic_LFP";
        break;
      
      default:
        battery_type_str = "Invalid";
        break;
      }
      ESP_LOGCONFIG(TAG, "Battery Type: %s", battery_type_str);
    }

    void PowerFeatherMainboard::publish_control_states_()
    {
      if (control_state_queue_ == NULL)
      {
        return;
      }

      TaskUpdate control_state;
      while (xQueueReceive(control_state_queue_, &control_state, 0) == pdTRUE)
      {
        switch (control_state.type)
        {
        case TaskUpdateType::ENABLE_EN:
          if (enable_EN_switch_ != nullptr)
          {
            enable_EN_switch_->publish_state(control_state.data.b);
          }
          break;

        case TaskUpdateType::ENABLE_3V3:
          if (enable_3V3_switch_ != nullptr)
          {
            enable_3V3_switch_->publish_state(control_state.data.b);
          }
          break;

        case TaskUpdateType::ENABLE_VSQT:
          if (enable_VSQT_switch_ != nullptr)
          {
            enable_VSQT_switch_->publish_state(control_state.data.b);
          }
          break;

        case TaskUpdateType::ENABLE_BATTERY_TEMP_SENSE:
          if (enable_battery_temp_sense_switch_ != nullptr)
          {
            enable_battery_temp_sense_switch_->publish_state(control_state.data.b);
          }
          break;

        case TaskUpdateType::ENABLE_BATTERY_FUEL_GAUGE:
          if (enable_battery_fuel_gauge_switch_ != nullptr)
          {
            enable_battery_fuel_gauge_switch_->publish_state(control_state.data.b);
          }
          break;

        case TaskUpdateType::ENABLE_BATTERY_CHARGING:
          if (enable_battery_charging_switch_ != nullptr)
          {
            enable_battery_charging_switch_->publish_state(control_state.data.b);
          }
          break;

        case TaskUpdateType::ENABLE_STAT:
          if (enable_stat_switch_ != nullptr)
          {
            enable_stat_switch_->publish_state(control_state.data.b);
          }
          break;

        case TaskUpdateType::SUPPLY_MAINTAIN_VOLTAGE:
          if (supply_maintain_voltage_value_ != nullptr)
          {
            supply_maintain_voltage_value_->publish_state(control_state.data.f);
          }
          break;

        case TaskUpdateType::BATTERY_CHARGING_MAX_CURRENT:
          if (battery_charging_max_current_value_ != nullptr)
          {
            battery_charging_max_current_value_->publish_state(control_state.data.f);
          }
          break;

        case TaskUpdateType::BATTERY_LOW_VOLTAGE_ALARM:
          if (battery_low_voltage_alarm_value_ != nullptr)
          {
            battery_low_voltage_alarm_value_->publish_state(control_state.data.f);
          }
          break;

        case TaskUpdateType::BATTERY_HIGH_VOLTAGE_ALARM:
          if (battery_high_voltage_alarm_value_ != nullptr)
          {
            battery_high_voltage_alarm_value_->publish_state(control_state.data.f);
          }
          break;

        case TaskUpdateType::BATTERY_LOW_CHARGE_ALARM:
          if (battery_low_charge_alarm_value_ != nullptr)
          {
            battery_low_charge_alarm_value_->publish_state(control_state.data.f);
          }
          break;

        default:
          break;
        }
      }
    }

    void PowerFeatherMainboard::send_task_update(TaskUpdate update)
    {
      if (update_task_queue_ == NULL)
      {
        ESP_LOGW(TAG, "PowerFeather update queue is not available");
        return;
      }

      if (xQueueSend(update_task_queue_, &update, portMAX_DELAY) != pdTRUE)
      {
        ESP_LOGW(TAG, "Failed to queue PowerFeather update");
      }
    }

    void PowerFeatherMainboard::send_control_state_(TaskUpdate update)
    {
      if (control_state_queue_ == NULL)
      {
        ESP_LOGW(TAG, "PowerFeather control state queue is not available");
        return;
      }

      if (xQueueSend(control_state_queue_, &update, 0) != pdTRUE)
      {
        ESP_LOGW(TAG, "Failed to queue PowerFeather control state");
      }
    }

  } // namespace powerfeather
} // namespace esphome
