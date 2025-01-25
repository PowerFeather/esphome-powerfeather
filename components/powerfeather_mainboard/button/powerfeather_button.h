#pragma once

#include "esphome/core/component.h"
#include "esphome/components/button/button.h"

#include "../powerfeather_mainboard.h"

namespace esphome
{
  namespace powerfeather_mainboard
  {
    class PowerFeatherButton : public button::Button, public Parented<PowerFeatherMainboard>, public PowerFeatherUpdateable
    {
    public:
      PowerFeatherButton() = default;

    protected:
      void press_action() override
      {
        TaskUpdate update;
        update.type = type_;
        this->parent_->send_task_update(update);
      }
    };
  }
}
