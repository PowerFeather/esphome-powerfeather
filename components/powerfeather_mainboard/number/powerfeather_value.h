#pragma once

#include "esphome/core/component.h"
#include "esphome/components/number/number.h"

#include "../powerfeather_mainboard.h"

namespace esphome
{
  namespace powerfeather_mainboard
  {
    class PowerFeatherValue : public number::Number, public Parented<PowerFeatherMainboard>, public Updateable
    {
    public:
      PowerFeatherValue() = default;

    protected:
      void control(float value) override
      {
        TaskUpdate update;
        update.type = type_;
        update.data.u = value * 1000;
        this->parent_->send_task_update(update);
        this->publish_state(value);
      }
    };
  }
}