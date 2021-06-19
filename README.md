# WS2812_for_RPI_PICO
Simple "library" that makes it easy to use LED strings and rings (WS2812 ones) with Raspberry pi PICO

So...
How to use it?

1. Turn off your PICO
2. Connect your leds to PICO and led string (power, ground, data), now it's safe to turn on
3. Download the file and include it in your script
4. You'r ready to go now... if you only knew how to use it :)

To use the library you MUST set up output pin and number of leds on your ring/string:
1. `set_outputPIN(21)`     #sets the pin 21 as the output pin
2. "set_led_count(8)"      #sets the number of led's on a string to 8

Additionaly you can change the brightness of the led's (not mandatory)
1. "set_brightnes(0.5)"    #sets the brightness to half of the max value


To turn of you led's you will need
1. Fill the values in the array
    You can do it one by one:
    "pixels_set(n, color)"   #where n is the number if pixel and color is well... color in rgb (r, g, b) with numbers up to 255
    
    Or you can fill all in one go
    "pixels_fill(color)"    #where color is the color you'll fill the led's with
    
2. Send that data to your led's
    To do this you only need to type one simple line:
    "pixels_show()"
    
3. Clear the pixels at the end:
    "clear_display()"   #just clears the led's, good to use at the end
    

And that's basicly all of basic functionality, hovewer there are some additional "features":
1. color chase effect:
    "color_chase(color, time)"    #where color stands for RGB color, and time stands for transition time in seconds
2. rainbow cycle effect
    "rainbow_cycle(time)"    #where time stands for transition time in seconds
3. some basic colors:
     "BLACK, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE"
     feel free to add your own!
