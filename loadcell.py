#! /usr/bin/python3
# sampler for a pi hx711/loadcell combination
# ross lazarus me fecit May 2019
# based on the hx711py example.py code.

import time
import sys

EMULATE_HX711=False
logdat = True
logfname = "loadcell.xls"
SAMPINT = 30 # seconds to sleep between samples


if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    # print("Cleaning up")

    if not EMULATE_HX711:
        GPIO.cleanup()
    if logdat:
        lout.close()
    sys.exit()

hx = HX711(5, 6)
#hx.OFFSET = OFFSET

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
#hx.set_reference_unit(-1776.3)
#
# with hx.set_reference_unit(1)
# 4kg gave around -910310.0

scale = -910310/4000 # int(measured_weight)/int(item_weight) for 1/10 g resolution
#scale = 1
print("Scale factor = %d" % scale)
hx.set_reference_unit(scale)

hx.reset()

hx.tare()

print("Tare done! Ready now...")

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()
if logdat:
    lout = open(logfname,'w')
    started = time.time()

while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
        
        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        # val = hx.read_average(times=10) 
        val = hx.get_weight(times=10)
        dur = int(time.time()) # seconds is enough for us
        s = '%d\t%.2f' % (dur,val)
        print(s) 
        if logdat:
                lout.write(s)
                lout.write('\n')
                lout.flush()
        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        time.sleep(SAMPINT)
        hx.power_up()

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
