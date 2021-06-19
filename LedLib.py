import array, time
from machine import Pin
import rp2

# Configure the number of WS2812 LED's
NUM_LEDS = -1
PIN_NUM = -1
brightness = 0.2

#Some wierd totally not ripped off assembly code
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

##########################################################################
#Made to check if setup is OK
def setup_check():
    if PIN_NUM == -1:
        print("no output pin set")
        return False
    
    if NUM_LEDS == -1:
        print("number of LED's not set")
        return False
    
    return True

#displays the pixels 
def pixels_show():
    if not setup_check():
        return False
    
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(10)
    
    return True

#sets the color of one pixel
def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

#fills all the pixels color = (r, g, b)
def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)

#makes the color chase effect color = (r, g, b), wait = [time in seconds]
def color_chase(color, wait):
    for i in range(NUM_LEDS):
        pixels_set(i, color)
        time.sleep(wait)
        pixels_show()
    time.sleep(0.2)

#returns the color of the given LED
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

#makes a rainbow (wow unexpected)
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            pixels_set(i, wheel(rc_index & 255))
        pixels_show()
        time.sleep(wait)
        
#clears the display but does not shut it down!
def clear_display():
    pixels_fill(BLACK)
    pixels_show()

# sets the output pin (GP_)
def set_outputPIN(number):
    PIN_NUM = number
    
#sets the number of leds
def set_led_count(number):
    NUM_LEDS = number

#sets the brightness of the LED's
def set_brightnes(number):
    if number > 1:
        brightness = 1
    elif number < 0:
        brightness = 0
    else:
        brightness = number

#list of colors, feel free to add your own
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
#list of all colors contains all colors
COLORS = (BLACK, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)


