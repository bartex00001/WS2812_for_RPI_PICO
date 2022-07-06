from WS2812 import WS2812


class WS2812Controller:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, output_pin, num_of_leds, state_machine_id, active_on_init=True):
        self.NUM_OF_LEDS = num_of_leds

        WS2812Controller.check_sm_id(state_machine_id)
        self.WS2812 = WS2812(output_pin, self.NUM_OF_LEDS, state_machine_id=state_machine_id)
        self.WS2812.active(active_on_init)

    @staticmethod
    def check_sm_id(sm_id):
        if sm_id < 0 or sm_id > 7:
            raise ValueError("State machine ID must be between 0 and 7")

    def fill_pixels(self, color, refresh=True):
        for i in range(self.NUM_OF_LEDS):
            self.WS2812.change_pixel(i, color)

        if refresh:
            self.WS2812.refresh()

    def pixel_set(self, index, color, refresh=True):
        self.WS2812.change_pixel(index, color)

        if refresh:
            self.WS2812.refresh()

    def get_pixel_color(self, index):
        if index < 0 or index >= self.NUM_OF_LEDS:
            raise IndexError("Index must be between 0 and {}".format(self.NUM_OF_LEDS - 1))

        return self.WS2812.pixel_states[index]
