import rp2
import time
from machine import Pin


@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_LOW,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=24)
def signal_generator():
    label("bit_loop")
    out(x, 1).side(0)[2]

    jmp(not_x, "zero_bit").side(1)[1]
    jmp("bit_loop")[4]

    label("zero_bit")
    nop().side(0)[4]


class WS2812:
    SM_FREQUENCY = 8_000_000
    BIT_SHIFT = 8
    RESET_TIME_US = 50

    def __init__(self, output_pin: int, num_of_leds: int, state_machine_id=0, auto_reset=True):
        self.NUM_OF_LEDS = num_of_leds
        self.auto_reset = auto_reset
        self.last_reset_time_us = 0
        self.pixel_states = [(0, 0, 0) for _ in range(self.NUM_OF_LEDS)]
        self.sm = rp2.StateMachine(
            state_machine_id,
            signal_generator,
            freq=WS2812.SM_FREQUENCY,
            sideset_base=Pin(output_pin))

    def active(self, value):
        self.sm.active(value)

    def refresh(self):
        # Precompute codes to suffice strict timing demands
        pixel_codes = []
        for pixel_state in self.pixel_states:
            pixel_codes.append(WS2812.pixel_state_to_code(pixel_state))

        if self.auto_reset:
            self.reset_signal_generator()

        for pixel_code in pixel_codes:
            self.sm.put(pixel_code, WS2812.BIT_SHIFT)

    def reset_signal_generator(self):
        # Time passed since last reset -> this one can be shorter
        time_diff_us = int(time.time_ns() / 1000) - self.last_reset_time_us
        if time_diff_us < WS2812.RESET_TIME_US:
            time.sleep_us(time_diff_us)

        self.last_reset_time_us = int(time.time_ns() / 1000)

    @staticmethod
    def pixel_state_to_code(pixel_state: int):
        # WS2812 expects colors in order: G, R, B - each 8-bit long
        return pixel_state[1] << 16 | pixel_state[0] << 8 | pixel_state[2]

    def change_pixel(self, index: int, color: (int, int, int)):
        try:
            WS2812.check_color_data(color)
            self.check_pixel_index(index)
            self.pixel_states[index] = color
        except ValueError:
            print("Invalid data provided for WS2812.change_pixel\nPixel data unchanged")
        except IndexError:
            print("Invalid out of range in WS2812.change_pixel\nPixel data unchanged")

    @staticmethod
    def check_color_data(color: (int, int, int)):
        for val in color:
            if val < 0 or val > 255:
                raise ValueError("Color values must be between 0 and 255")

    def check_pixel_index(self, index: int):
        if index < 0 or index > self.NUM_OF_LEDS:
            raise IndexError("Pixel index must be between 0 and NUM_OF_LEDS")

    def change_pixels(self, pixel_data: {int: (int, int, int)}):
        for pixel_index in pixel_data:
            self.change_pixel(pixel_index, pixel_data[pixel_index])
