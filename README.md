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
(WIP)

## How to flash library
(WIP)

## Examples
(WIP)
