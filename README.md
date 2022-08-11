> Work in progress, remaining sections will be filled *'soon'*

# WS2812_for_RPI_PIC

Micropython library for Raspberry Pi Pico providing high level API control over WS2812 RGB LEDs.

## Table of contents

- [**Features**](#features)
- [**WS2812 API**](#ws2812-api)
- [**WS2812 Controller API**](#ws2812-controller-api)
- [**How to flash library**](#how-to-flash-library)
- [**Examples**](#examples)

## Features

- Library provides both high and low level control over WS2812 RGB LEDs.

- Signal is generated via State Machines *(SM)* - processor is used only to write data to SM's registers.

- LED's can be controlled by all GPIO pins.

- Up to 8 different WS2812 LED chains can be controlled.

## WS2812 API

`WS2812` class is designed to be minimal hence it provides only basic control over WS2812 LEDs. If you want higher-level control along with more built-in features the [WS2812 Controller](#ws2812-controller-api) class might be a better choice.

### Creating an instance of WS2812 class

The class Exposes following constructor:

```python
def __init__(self, output_pin: int, num_of_leds: int, state_machine_id: int, auto_reset=True):
```

- `output_pin` is the GPIO pin to which the LED chain is connected.
- `num_of_leds` is the number of WS2812 LEDs in the chain.
- `state_machine_id` is the unique identifier of state machine. Must be in range `0,7` inclusive.
- `auto_reset` is a flag that determines whether `reset_signal_generator()` is automatically called on refresh. It's purpose is described [here](#refresh-the-led-chain).

The constructor will check whether `state_machine_id` is in valid range, but will not check it's uniqueness.  
Created WS2812 class creates SM, which needs to be [activated before use](#activating-state-machine).

### Activating state machine

After initialization state machine is not active. To send data to LED chain it needs to be activated.

```python
def active(self, value):
```

Activation is done by setting `value` to `True` or `False`.  

Note that turning off SM will not affect the LEDs. WS2812 modules keep their color when they do not receive signal.  
For more details see [this](#examples) section.

### Change color of single led

The `change_pixel()` method allows for changing the color of a single LED by specifying its index and desired color.  
Indexing of the LEDs starts at 0.

```python
def change_pixel(self, index: int, color: (int, int, int)):
```

- `index` is the index of the LED in the chain. `IndexError` will be raised if the index is invalid.
- `color` is the desired color of the LED in 8-bit RGB. `ValueError` will be raised if the color is invalid.

### Change color of chosen leds

Method will change the color of all LEDs found in dictionary.

```python
def change_pixels(self, pixel_data: {int: (int, int, int)}):
```

- `pixel_data` is a dictionary where keys are indexes of LEDs and values are colors of LEDs. The `change_pixel()` function is called for all specified LEDs.

### Refresh the LED chain

Pixels on the chain are not automatically updated after `change...()`. Instead, change calls are stored in a buffer and pushed to SM when `refresh()` is called. This allows for multiple LEDs to be changed *instantly*. Refreshing can be handled by default in [WS2812 Controller](#ws2812-controller-api).


```python
def refresh(self):
```

Between refresh calls `T=50us` must pass. The on-by-default `auto_reset` takes care of this by calling `reset_signal_generator()`, which waits for `T` if it's necessary to do so.

### Get current color of an LED

This can be done by accessing the `pixel_states` list.  
The values in this list are guaranteed to be up to date only after `refresh()` is called as this list acts as a buffer for changes.  

The color of the `i-th` LED is stored in `pixel_states[i]` an 8-bit RGB tuple. Indexes are counted from 0.

## WS2812 Controller API

The `WS2812Controller` class is designed to be fully featured and flexible. It provides high level control over WS2812 LEDs but allows you to reach both WS2812 and SM if required. The class contains `WS2812` class as a member and builds it's API around it while also adding additional features.

### Creating an instance of WS2812Controller class

The class Exposes following constructor:

```python
def __init__(self, output_pin: int, num_of_leds: int, state_machine_id: int, active_on_init=True):
```

- `output_pin` is the GPIO pin to which the LED chain is connected.
- `num_of_leds` is the number of WS2812 LEDs in the chain.
- `state_machine_id` is the unique identifier of state machine. Must be in range `0,7` inclusive.
- `active_on_init` is a flag that determines whether state machine is activated on initialization.

The constructor will check whether `state_machine_id` is in valid range but will not check it's uniqueness.  
During this step the `WS2812` class is created as a member of the `WS2812Controller` class. It can be accessed via `self.WS2812`.

### Activate and deactivate state machine

After initialization SM is active by default. To turn it off/on use following method:

```python
def active(self, active: bool):
```

Activation is done by setting `value` to `True` or `False`.  

Note that turning off SM will not affect the LEDs. WS2812 modules keep their color when they do not receive signal.  
For more details see [this](#examples) section.

### Change LEDs color

The `pixel_set()` method allows for changing single LEDs color.

```python
def pixel_set(self, index: int, color: (int, int, int), refresh=True):
```

- `index` is the index of the LED in the chain. `IndexError` will be raised if the index is invalid.
- `color` is the desired color of the LED in 8-bit RGB. `ValueError` will be raised if the color is invalid.
- `refresh` is a flag that determines whether LEDs will be refreshed after the change. For more details see [this](#examples) section.

### Change color of all LEDs

The following method allows for changing color of all LEDs.

```python
def pixels_fill(self, color: (int, int, int), refresh=True):
```

- `color` is the desired for the LEDs in 8-bit RGB. `ValueError` will be raised if the color is invalid.
- `refresh` is a flag that determines whether LEDs will be refreshed after the change. For more details see [this](#examples) section.

### Get pixel color

A method for getting the color of a single LED.

```python
def get_pixel_color(self, index: int):
```

- `index` is the index of the LED in the chain. `IndexError` will be raised if the index is invalid.
- `@returns` the color of the LED in 8-bit RGB.

Note that the color returned is pulled from the buffer - it is not guaranteed to be up to date.

### Get color of all pixels

A method for getting a list of colors of all LEDs.

```python
def get_pixels_color(self):
```

- `@returns` a list of colors of all LEDs in 8-bit RGB.

Note that the color returned is pulled from the buffer - it is not guaranteed to be up to date.

### Fade LEDs to color (effect)

A built-in effect for fading chosen LEDs to selected color.

```python
def pixels_fade_to_color(self, color: (int, int, int), fade_time, pixel_list=[], refresh_frequency_hz=100, exponent=1.0):
```

- `color` is the desired for the LEDs in 8-bit RGB. `ValueError` will be raised if the color is invalid.
- `fade_time` is the time in seconds for the effect to complete.
- `pixel_list` is a list of indexes of LEDs to be affected. If empty, all LEDs will be affected.
- `refresh_frequency_hz` is the frequency at which the effect will be refreshed. Effect might glitch if the value is too high.
- `exponent` is the exponent of the fading curve.

### Perform a pixel chase (effect)

A built-in effect for performing a pixel chase.

```python
def pixel_chase(self, color: (int, int, int), cycle_time, cycles, background_color=BLACK, fade_pixels=0, fade_exponent=1.0, direction=True):
```

- `color` is the desired for the LEDs in 8-bit RGB. `ValueError` will be raised if the color is invalid.
- `cycle_time` time taken for a full cycle.
- `cycles` is the number of cycles to be performed. Non integer values are allowed.
- `background_color` is the color of the background LEDs - not active.
- `fade_pixels` is the number of pixels faded after lead pixel.
- `fade_exponent` is the exponent of the fading curve - how fast faded pixels turn to background color.
- `direction` is a flag that determines whether the effect is performed from index 0 to the last LED or from the last LED to index 0.

### Lerp color (static)

Method allows for lerping between two colors.

```python
@staticmethod
def lerp_color(color1: (int, int, int), color2: (int, int, int), alpha):
```

- `color1` is the first color to be lerped.
- `color2` is the second color to be lerped.
- `alpha` is the lerp alpha value. Must be in range `0,1` inclusive, otherwise ValueError is raised.

### Convert HSL to RGB (static)

Method for converting a color from 8-bit HSL to 8-bit RGB.

```python
@staticmethod
def hsl_to_rgb(hue: int, sat=1.0, lum=0.5):
```

- `hue` is the hue of the color in 8-bit.
- `sat` is the saturation of the color in 8-bit.
- `lum` is the luminance of the color in 8-bit.

The values are not checked for validity.

### Built in colors (static)

The following static, member, color variables are available:

```python
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
```

These are just the basic colors I decided to put here. They can be easily extended.

## How to flash library
(WIP)

## Examples
(WIP)
