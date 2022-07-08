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

    def get_pixel_colors(self):
        return self.WS2812.pixel_states

    @staticmethod
    # Linear interpolation between two colors
    def lerp_color(color1, color2, alpha):
        if alpha < 0 or alpha > 1:
            raise ValueError("alpha must be between 0 and 1")

        r = int(color1[0] + (color2[0] - color1[0]) * alpha)
        g = int(color1[1] + (color2[1] - color1[1]) * alpha)
        b = int(color1[2] + (color2[2] - color1[2]) * alpha)

        return (r, g, b)

    def fade_pixels_to_color(self, color, fade_time, pixel_list=[], refresh_frequency_hz=100, exponent=1):
        self.check_values_for_fade_pixels(fade_time, refresh_frequency_hz)
        self.fill_pixel_list(pixel_list)
        start_pixel_colors = self.get_pixel_colors()

        steps = fade_time * refresh_frequency_hz
        sleep_time_ms = int(1000 / refresh_frequency_hz)
        for i in range(1, steps+1):
            time.sleep_ms(sleep_time_ms)
            for pixel in pixel_list:
                new_color = self.lerp_color(start_pixel_colors[pixel], color, pow(i/steps, exponent))
                self.pixel_set(pixel, new_color, refresh=False)

            self.WS2812.refresh()

    @staticmethod
    def check_values_for_fade_pixels(fade_time, refresh_frequency_hz):
        if fade_time < 0:
            raise ValueError("fade_time must be greater than 0")
        if refresh_frequency_hz <= 0:
            raise ValueError("refresh_frequency_hz must be greater than 0")

    @staticmethod
    def fill_pixel_list(pixel_list):
        # Empty pixel list is treated a full one
        if len(pixel_list) == 0:
            for i in range(WS2812Controller.NUM_OF_LEDS):
                pixel_list.append(i)
