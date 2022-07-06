from WS2812 import WS2812


class WS2812Controller:
    def __init__(self, output_pin, num_of_leds, state_machine_id, active_on_init=True):
        self.NUM_OF_LEDS = num_of_leds

        WS2812Controller.check_sm_id(state_machine_id)
        self.WS2812 = WS2812(output_pin, self.NUM_OF_LEDS, state_machine_id=state_machine_id)
        self.WS2812.active(active_on_init)

    @staticmethod
    def check_sm_id(sm_id):
        if sm_id < 0 or sm_id > 7:
            raise ValueError("State machine ID must be between 0 and 7")
