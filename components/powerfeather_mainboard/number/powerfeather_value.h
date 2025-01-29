#pragma once

#include "esphome/core/component.h"
#include "esphome/components/number/number.h"

#include "../powerfeather_mainboard.h"

namespace esphome
{
  namespace powerfeather_mainboard
  {
    class PowerFeatherValue : public number::Number, public Parented<PowerFeatherMainboard>, public PowerFeatherUpdateable
    {
    public:
      PowerFeatherValue() = default;

    protected:
      void control(float value) override
      {
        TaskUpdate update;
        update.type = type_;
        update.data.f = value;
        this->parent_->send_task_update(update);
        this->publish_state(value);
      }
    };
  }
}