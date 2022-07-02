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
    def __init__(self, output_pin, num_of_leds, state_machine_id=0):
        self.NUM_OF_LEDS = num_of_leds
        self.SM_FREQUENCY = 8_000_000
        self.pixel_state = ((0, 0, 0) for _ in range(self.NUM_OF_LEDS))
        self.sm = rp2.StateMachine(
            state_machine_id,
            signal_generator,
            self.SM_FREQUENCY,
            sideset_base=Pin(output_pin))

