
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
      ESP_LOGI(TAG, "Initializing board with capacity %d mV and type %u", this->battery_capacity_, static_cast<uint32_t>(this->battery_type_));
      PowerFeather::Result res = PowerFeather::Board.init(this->battery_capacity_, this->battery_type_);
      ESP_LOGI(TAG, "Initialization result: %d", static_cast<int>(res));

      // Get initial values
      static constexpr gpio_num_t EN_3V3 = GPIO_NUM_4;   // 3V3 enable/disable
      static constexpr gpio_num_t EN_VSQT = GPIO_NUM_14; // VSQT enable/disable
      static constexpr gpio_num_t EN0 = GPIO_NUM_13;     // FeatherWings enable/disable (write)

      enable_3V3_ = rtc_gpio_get_level(EN_3V3);
      enable_VSQT_ = rtc_gpio_get_level(EN_VSQT);
      enable_EN_ = rtc_gpio_get_level(EN0);
      ESP_LOGI(TAG, "EN_3V3: %d,  EN_VSQT: %d,  EN: %d", enable_3V3_, enable_VSQT_, enable_EN_);

      enable_3V3_switch_->publish_state(enable_3V3_);

      update_task_queue_ = xQueueCreate(UPDATE_TASK_QUEUE_SIZE_, sizeof(TaskUpdate));
      xTaskCreate(update_task_, "powerfeather_mainboard", UPDATE_TASK_STACK_SIZE_, this, uxTaskPriorityGet(NULL), NULL);
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

    void PowerFeatherSwitch::write_state(bool state)
    {
      TaskUpdate update;
      update.type = type_;
      update.data.b = state;
      this->parent_->send_task_update(update);
      this->publish_state(state);
    }

    void PowerFeatherValue::control(float value)
    {
      TaskUpdate update;
      update.type = type_;
      update.data.u = value * 1000;
      this->parent_->send_task_update(update);
      this->publish_state(value);
    }

    void PowerFeatherButton::press_action()
    {
      TaskUpdate update;
      update.type = type_;
      this->parent_->send_task_update(update);
    }

  } // namespace empty_compound_sensor
} // namespace esphome