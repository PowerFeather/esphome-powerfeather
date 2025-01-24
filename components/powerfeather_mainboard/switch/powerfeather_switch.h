#pragma once

#include "esphome/core/component.h"
#include "esphome/components/switch/switch.h"

#include "../powerfeather_mainboard.h"

namespace esphome
{
  namespace powerfeather_mainboard
  {
    class PowerFeatherSwitch : public switch_::Switch, public Parented<PowerFeatherMainboard>, public Updateable
    {
    public:
      PowerFeatherSwitch() = default;

    protected:
      void write_state(bool state) override
      {
        TaskUpdate update;
        update.type = type_;
        update.data.b = state;
        this->parent_->send_task_update(update);
        this->publish_state(state);
      }
    };
  }
}