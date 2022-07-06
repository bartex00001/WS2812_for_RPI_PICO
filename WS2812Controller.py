import time
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

    @staticmethod
    # Linear interpolation between two colors
    def lerp_color(color1, color2, alpha):
        if alpha < 0 or alpha > 1:
            raise ValueError("alpha must be between 0 and 1")

        r = int(color1[0] + (color2[0] - color1[0]) * alpha)
        g = int(color1[1] + (color2[1] - color1[1]) * alpha)
        b = int(color1[2] + (color2[2] - color1[2]) * alpha)

        return (r, g, b)

    # TODO: add support for non-linear interpolation
    # TODO: empty pixel_list should count as including all pixels
    # TODO: make the function 'look better'
    def fade_pixels_to_color(self, color, pixel_list, fade_time, refresh_frequency_hz=100):
        WS2812Controller.check_values_for_fade_pixels(pixel_list, fade_time, refresh_frequency_hz)
        start_pixel_states = [self.get_pixel_color(i) for i in range(self.NUM_OF_LEDS)]

        steps = fade_time * refresh_frequency_hz
        sleep_time_ms = int(1000 / refresh_frequency_hz)
        for i in range(1, steps+1):
            time.sleep_ms(sleep_time_ms)
            for pixel in pixel_list:
                self.pixel_set(
                    pixel,
                    WS2812Controller.lerp_color(start_pixel_states[pixel], color, i / steps),
                    refresh=False)

            self.WS2812.refresh()

    @staticmethod
    def check_values_for_fade_pixels(pixel_list, fade_time, refresh_frequency_hz):
        if len(pixel_list) == 0:
            raise ValueError("pixel_list must not be empty")
        if fade_time < 0:
            raise ValueError("fade_time must be greater than 0")
        if refresh_frequency_hz <= 0:
            raise ValueError("refresh_frequency_hz must be greater than 0")
