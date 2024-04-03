import RPi.GPIO as GPIO
import datetime
import time
import csv
import sys
import adafruit_bme680
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C

reset_pin = None

import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_pressure = 1013.25

# Global variable to store count
interval=0
intervals = 1
count = 0
totalcounts = 0
timestamps = []
outfile = (sys.argv[1])
meta_data = ['Time','Counts','Total Counts','PM1','PM2.5',
             'PM10','Temperature','Humidity','Pressure','Altitude']
file = open(outfile,"w")
data_writer = csv.writer(file)
data_writer.writerow(meta_data)


def my_callback(channel):
    global count
    global totalcounts
    count += 1
    totalcounts += 1
    timestamp = datetime.datetime.now()
    timestamps.append(timestamp)
    # print('Count detected at ' + str(timestamp))


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set up falling-edge event detection

    # Add falling edge detection with callback
    GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback)

    # Infinite loop with sleep for 10 seconds
    while interval<intervals:
        # Sleep for 10 seconds
        try:
            aqdata = pm25.read()
        
        except RuntimeError:
            print("Unable to read from sensor, retrying...")
            continue
        
        row = [time.time(),count,totalcounts, aqdata["pm10 standard"], 
                    aqdata["pm25 standard"], aqdata["pm100 standard"], 
                    bme680.temperature, bme680.relative_humidity,
                    bme680.pressure, bme680.altitude]
        data_writer.writerow(row)
        print(row)
        
        time.sleep(5)
        # print(f"Counts collected in the last 10 seconds: {count}")
        count = 0
        interval +=1
    file.close()

except KeyboardInterrupt:
    print("\nKeyboard interrupt detected, exiting...")

finally:
    # Clean up GPIO
    GPIO.cleanup()
    
