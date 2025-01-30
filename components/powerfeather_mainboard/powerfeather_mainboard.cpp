
#include "esphome/core/log.h"
#include "powerfeather_mainboard.h"

#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_timer.h"

namespace esphome
{
  namespace powerfeather_mainboard
  {
    static const char *TAG = "powerfeather_mainboard";

    static uint32_t millis()
    {
      return esp_timer_get_time() / 1000;
    }

    void PowerFeatherMainboard::update_sensors_()
    {
      if (supply_voltage_sensor_ != nullptr)
      {
        uint16_t supply_voltage = 0;
        PowerFeather::Board.getSupplyVoltage(supply_voltage);
        supply_voltage_ = supply_voltage / 1000.0f;
      }

      if (supply_current_sensor_ != nullptr)
      {
        int16_t supply_current = 0;
        PowerFeather::Board.getSupplyCurrent(supply_current);
        supply_current_ = supply_current / 1000.0f;
      }

      if (supply_good_sensor_ != nullptr)
      {
        bool supply_good = false;
        PowerFeather::Board.checkSupplyGood(supply_good);
        supply_good_ = supply_good;
      }

      if (battery_voltage_sensor_ != nullptr)
      {
        uint16_t battery_voltage = 0;
        PowerFeather::Board.getBatteryVoltage(battery_voltage);
        battery_voltage_ = battery_voltage / 1000.0f;
      }

      if (battery_current_sensor_ != nullptr)
      {
        int16_t battery_current = 0;
        PowerFeather::Board.getBatteryCurrent(battery_current);
        battery_current_ = battery_current / 1000.0f;
      }

      if (battery_charge_sensor_ != nullptr)
      {
        uint8_t battery_charge = 0;
        PowerFeather::Board.getBatteryCharge(battery_charge);
        battery_charge_ = battery_charge;
      }

      if (battery_health_sensor_ != nullptr)
      {
        uint8_t battery_health = 0;
        PowerFeather::Board.getBatteryHealth(battery_health);
        battery_health_ = battery_health;
      }

      if (battery_cycles_sensor_ != nullptr)
      {
        uint16_t battery_cycles = 0;
        PowerFeather::Board.getBatteryCycles(battery_cycles);
        battery_cycles_ = battery_cycles;
      }

      if (battery_time_left_sensor_ != nullptr)
      {
        int battery_time_left = 0;
        PowerFeather::Board.getBatteryTimeLeft(battery_time_left);
        battery_time_left_ = battery_time_left / 60.0f;
      }

      if (battery_temperature_sensor_ != nullptr)
      {
        float battery_temperature = 0;
        PowerFeather::Board.getBatteryTemperature(battery_temperature);
        battery_temperature_ = battery_temperature;
      }
    }

    void PowerFeatherMainboard::update_task_(void *param)
    {
      powerfeather_mainboard::PowerFeatherMainboard *powerfeather_mainboard =
        reinterpret_cast<powerfeather_mainboard::PowerFeatherMainboard *>(param);

      while (true)
      {
        TaskUpdate update;
        update.type = TaskUpdateType::SENSORS;
        xQueueReceive(powerfeather_mainboard->update_task_queue_, &update, portMAX_DELAY);
        switch (update.type)
        {
        case TaskUpdateType::ENABLE_EN:
          PowerFeather::Board.setEN(powerfeather_mainboard->enable_EN_);
          break;

        case TaskUpdateType::ENABLE_3V3:
          ESP_LOGD(TAG, "Recieved EN enable state: %d", update.data.b);
          powerfeather_mainboard->enable_3V3_ = update.data.b;
          PowerFeather::Board.enable3V3(powerfeather_mainboard->enable_3V3_);
          break;

        case TaskUpdateType::ENABLE_VSQT:
          ESP_LOGD(TAG, "Recieved VSQT enable state: %d", update.data.b);
          powerfeather_mainboard->enable_VSQT_ = update.data.b;
          PowerFeather::Board.enableVSQT(powerfeather_mainboard->enable_VSQT_);
          break;

        case TaskUpdateType::ENABLE_BATTERY_TEMP_SENSE:
          ESP_LOGD(TAG, "Recieved enable battery temp sense: %d", update.data.b);
          powerfeather_mainboard->enable_battery_temp_sense_ = update.data.b;
          PowerFeather::Board.enableBatteryTempSense(powerfeather_mainboard->enable_battery_temp_sense_);
          break;

        case TaskUpdateType::ENABLE_BATTERY_FUEL_GAUGE:
          ESP_LOGD(TAG, "Recieved enable battery fuel gauge: %d", update.data.b);
          powerfeather_mainboard->enable_battery_fuel_gauge_ = update.data.b;
          PowerFeather::Board.enableBatteryFuelGauge(powerfeather_mainboard->enable_battery_fuel_gauge_);
          break;

        case TaskUpdateType::ENABLE_BATTERY_CHARGING:
          ESP_LOGD(TAG, "Recieved enable battery charging: %d", update.data.b);
          powerfeather_mainboard->enable_battery_charging_ = update.data.b;
          PowerFeather::Board.enableBatteryCharging(powerfeather_mainboard->enable_battery_charging_);
          break;

        case TaskUpdateType::ENABLE_STAT:
          ESP_LOGD(TAG, "Recieved enable STAT LED: %d", update.data.b);
          powerfeather_mainboard->enable_stat_ = update.data.b;
          PowerFeather::Board.enableSTAT(powerfeather_mainboard->enable_stat_);
          break;

        case TaskUpdateType::POWERCYCLE:
          ESP_LOGD(TAG, "Recieved powercycle request");
          PowerFeather::Board.doPowerCycle();
          break;

        case TaskUpdateType::SHIP_MODE:
          ESP_LOGD(TAG, "Recieved ship mode request");
          PowerFeather::Board.enterShipMode();
          break;

        case TaskUpdateType::SHUTDOWN:
          ESP_LOGD(TAG, "Recieved shutdown request");
          PowerFeather::Board.enterShutdownMode();
          break;

        case TaskUpdateType::SUPPLY_MAINTAIN_VOLTAGE:
          ESP_LOGD(TAG, "Recieved supply maintain voltage value update: %f", update.data.f);
          powerfeather_mainboard->supply_maintain_voltage_ = update.data.f * 1000.f;
          PowerFeather::Board.setSupplyMaintainVoltage(static_cast<uint16_t>(powerfeather_mainboard->supply_maintain_voltage_));
          break;

        case TaskUpdateType::BATTERY_CHARGING_MAX_CURRENT:
          ESP_LOGD(TAG, "Recieved battery charging max current update: %f", update.data.f);
          powerfeather_mainboard->battery_charging_max_current_ = update.data.f * 1000.0f;
          PowerFeather::Board.setBatteryChargingMaxCurrent(static_cast<uint16_t>(powerfeather_mainboard->battery_charging_max_current_));
          break;

        case TaskUpdateType::SENSORS:
        default:
        {
          ESP_LOGD(TAG, "Recieved sensors update request");
          powerfeather_mainboard->update_sensors_();
        }
        break;
        }
      }
    }

    void PowerFeatherMainboard::setup()
    {
      #define EXIT_SETUP()        { mark_failed(); ESP_LOGE(TAG, "Failed setup at line %d", __LINE__); return; }
      #define CHECK_RES(res)      if ((res) != PowerFeather::Result::Ok) EXIT_SETUP();

      ESP_LOGD(TAG, "Initializing board, capacity: %d mV and type: %u", this->battery_capacity_, static_cast<uint32_t>(this->battery_type_));
      CHECK_RES(PowerFeather::Board.init(this->battery_capacity_, this->battery_type_));

      update_sensors_();

      #undef CHECK_RES
      #define CHECK_RES(res)      if (!(res)) EXIT_SETUP();

      if (enable_3V3_switch_)
      {
        static constexpr gpio_num_t EN_3V3 = GPIO_NUM_4;
        enable_3V3_ = rtc_gpio_get_level(EN_3V3);
        enable_3V3_switch_->publish_state(enable_3V3_);
      }

      if (enable_VSQT_switch_)
      {
        static constexpr gpio_num_t EN_VSQT = GPIO_NUM_14;
        enable_VSQT_ = rtc_gpio_get_level(EN_VSQT);
        enable_VSQT_switch_->publish_state(enable_VSQT_);
      }

      if (enable_EN_switch_)
      {
        static constexpr gpio_num_t EN0 = GPIO_NUM_13;
        enable_EN_ = rtc_gpio_get_level(EN0);
        enable_EN_switch_->publish_state(enable_EN_);
      }

      if (enable_stat_switch_)
      {
        CHECK_RES(PowerFeather::Board.getCharger().getSTATEnabled(enable_stat_));
        enable_stat_switch_->publish_state(enable_stat_);
      }

      if (supply_maintain_voltage_value_)
      {
        uint16_t value = 0;
        CHECK_RES(PowerFeather::Board.getCharger().getVINDPM(value));
        supply_maintain_voltage_ = value / 1000.0f;
        supply_maintain_voltage_value_->publish_state(supply_maintain_voltage_);
      }

      if (battery_charging_max_current_value_)
      {
        uint16_t value = 0;
        CHECK_RES(PowerFeather::Board.getCharger().getChargeCurrentLimit(value));
        battery_charging_max_current_ = value / 1000.0f;
        battery_charging_max_current_value_->publish_state(battery_charging_max_current_);
      }

      if (enable_battery_charging_switch_ && battery_capacity_)
      {
        CHECK_RES(PowerFeather::Board.getCharger().getChargingEnabled(enable_battery_charging_));
        enable_battery_charging_switch_->publish_state(enable_battery_charging_);
      }

      if (enable_battery_temp_sense_switch_)
      {
        CHECK_RES(PowerFeather::Board.getCharger().getTSEnabled(enable_battery_temp_sense_));
        enable_battery_temp_sense_switch_->publish_state(enable_battery_temp_sense_);
      }

      if (enable_battery_fuel_gauge_switch_ && battery_capacity_)
      {
        // Can fail here when no battery is actually connected, so do not check the result.
        // In that case, consider as not enabled. Initialize value before attempting to read.
        enable_battery_fuel_gauge_ = false;
        PowerFeather::Board.getFuelGauge().getOperationMode(enable_battery_fuel_gauge_);
        enable_battery_fuel_gauge_switch_->publish_state(enable_battery_fuel_gauge_);
      }

      #undef CHECK_RES

      update_task_queue_ = xQueueCreate(UPDATE_TASK_QUEUE_SIZE_, sizeof(TaskUpdate));
      if (update_task_queue_ == NULL)
      {
        ESP_LOGE(TAG, "Failed to create PowerFeather task queue");
        mark_failed();
        return;
      }

      if (xTaskCreate(update_task_, "powerfeather_mainboard", UPDATE_TASK_STACK_SIZE_, this, uxTaskPriorityGet(NULL), NULL) != pdTRUE)
      {
        ESP_LOGE(TAG, "Failed to create PowerFeather task queue");
        mark_failed();
        return;
      }

    }

    void PowerFeatherMainboard::loop()
    {
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
      // TODO
    }

    void PowerFeatherMainboard::send_task_update(TaskUpdate update)
    {
      xQueueSend(update_task_queue_, &update, portMAX_DELAY);
    }

  } // namespace empty_compound_sensor
} // namespace esphome