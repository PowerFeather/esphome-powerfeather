
#include "esphome/core/log.h"
#include "powerfeather_mainboard.h"

#include "freertos/task.h"
#include "freertos/queue.h"

namespace esphome
{
  namespace powerfeather_mainboard
  {
    static const char *TAG = "powerfeather_mainboard";

    void PowerFeatherMainboard::update_task_(void *param)
    {
      powerfeather_mainboard::PowerFeatherMainboard *powerfeather_mainboard =
        reinterpret_cast<powerfeather_mainboard::PowerFeatherMainboard *>(param);

      while (true)
      {
        TaskUpdate update;
        update.type = TaskUpdateType::SENSORS;
        xQueueReceive(powerfeather_mainboard->update_task_queue_, &update, pdMS_TO_TICKS(UPDATE_TASK_QUEUE_WAIT_MS_));
        ESP_LOGD(TAG, "recieved: %d", static_cast<int>(update.type));
        switch (update.type)
        {
        case TaskUpdateType::ENABLE_EN:
          PowerFeather::Board.setEN(powerfeather_mainboard->enable_EN_);
          break;

        case TaskUpdateType::ENABLE_3V3:
          ESP_LOGI(TAG, "Recieved EN enable state: %d", update.data.b);
          powerfeather_mainboard->enable_3V3_ = update.data.b;
          PowerFeather::Board.enable3V3(powerfeather_mainboard->enable_3V3_);
          break;

        case TaskUpdateType::ENABLE_VSQT:
          ESP_LOGI(TAG, "Recieved VSQT enable state: %d", update.data.b);
          powerfeather_mainboard->enable_VSQT_ = update.data.b;
          PowerFeather::Board.enableVSQT(powerfeather_mainboard->enable_VSQT_);
          break;

        case TaskUpdateType::SUPPLY_MAINTAIN_VOLTAGE:
          ESP_LOGI(TAG, "Recieved supply maintain voltage value update: %d", update.data.u);
          powerfeather_mainboard->supply_maintain_voltage_ = static_cast<uint16_t>(update.data.u);
          PowerFeather::Board.setSupplyMaintainVoltage(powerfeather_mainboard->supply_maintain_voltage_);
          break;

        case TaskUpdateType::POWERCYCLE:
          ESP_LOGI(TAG, "Recieved powercycle request");
          PowerFeather::Board.doPowerCycle();
          break;

        case TaskUpdateType::SENSORS:
        default:
        {
          uint16_t supply_voltage = 0;
          PowerFeather::Board.getSupplyVoltage(supply_voltage);
          powerfeather_mainboard->supply_voltage_ = supply_voltage / 1000.0f;

          int16_t supply_current = 0;
          PowerFeather::Board.getSupplyCurrent(supply_current);
          powerfeather_mainboard->supply_current_ = supply_current / 1000.0f;

          bool supply_good = false;
          PowerFeather::Board.checkSupplyGood(supply_good);
          powerfeather_mainboard->supply_good_ = supply_good;

          uint16_t battery_voltage = 0;
          PowerFeather::Board.getBatteryVoltage(battery_voltage);
          powerfeather_mainboard->battery_voltage_ = battery_voltage / 1000.0f;

          int16_t battery_current = 0;
          PowerFeather::Board.getBatteryCurrent(battery_current);
          powerfeather_mainboard->battery_current_ = battery_current / 1000.0f;

          uint8_t battery_charge = 0;
          PowerFeather::Board.getBatteryCharge(battery_charge);
          powerfeather_mainboard->battery_charge_ = battery_charge;

          uint8_t battery_health = 0;
          PowerFeather::Board.getBatteryHealth(battery_health);
          powerfeather_mainboard->battery_health_ = battery_health;

          uint16_t battery_cycles = 0;
          PowerFeather::Board.getBatteryCycles(battery_cycles);
          powerfeather_mainboard->battery_cycles_ = battery_cycles;

          int battery_time_left = 0;
          PowerFeather::Board.getBatteryTimeLeft(battery_time_left);
          powerfeather_mainboard->battery_time_left_ = battery_time_left;

          float battery_temperature = 0;
          PowerFeather::Board.getBatteryTemperature(battery_temperature);
          powerfeather_mainboard->battery_temperature_ = battery_temperature;
        }
        break;
        }
      }
    }

    void PowerFeatherMainboard::setup()
    {
      #define EXIT_SETUP()        { mark_failed(); ESP_LOGE(TAG, "Failed setup at line %d", __LINE__); return; }
      #define CHECK_RES(res)      if ((res) != PowerFeather::Result::Ok) EXIT_SETUP();

      ESP_LOGI(TAG, "Initializing board, capacity: %d mV and type: %u", this->battery_capacity_, static_cast<uint32_t>(this->battery_type_));
      CHECK_RES(PowerFeather::Board.init(this->battery_capacity_, this->battery_type_));

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

      if (battery_charging_max_current_value_)
      {
        CHECK_RES(PowerFeather::Board.getCharger().getVINDPM(supply_maintain_voltage_));
        battery_charging_max_current_value_->publish_state(supply_maintain_voltage_);
      }

      if (battery_charging_max_current_value_)
      {
        CHECK_RES(PowerFeather::Board.getCharger().getChargeCurrentLimit(battery_max_charging_current_));
        battery_charging_max_current_value_->publish_state(battery_max_charging_current_);
      }

      if (enable_battery_charging_switch_ && battery_capacity_)
      {
        CHECK_RES(PowerFeather::Board.getCharger().getChargingEnabled(enable_charging_));
        enable_battery_charging_switch_->publish_state(enable_charging_);
      }

      if (enable_battery_temp_sense_switch_)
      {
        CHECK_RES(PowerFeather::Board.getCharger().getTSEnabled(enable_temp_sense_));
        enable_battery_temp_sense_switch_->publish_state(enable_temp_sense_);
      }

      if (enable_battery_fuel_gauge_switch_ && battery_capacity_)
      {
        // Can fail here when no battery is actually connected, so do not check the result.
        // In that case, consider as not enabled. Initialize value before attempting to read.
        enable_fuel_gauge_ = false;
        PowerFeather::Board.getFuelGauge().getOperationMode(enable_fuel_gauge_);
        enable_battery_fuel_gauge_switch_->publish_state(enable_fuel_gauge_);
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

    void PowerFeatherMainboard::update()
    {
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