import adafruit_bme680
import time
import board
import busio
import csv
import sys
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



start= time.time()
run_time = 300
run_time = int(sys.argv[1])

t = 0

meta_data = ['Time','PM1','PM2.5','PM10','Temperature','Humidity','Pressure','Altitude']

name_of_file = "aq_and_w_data.csv"
name_of_file = (sys.argv[2])
file = open(name_of_file,"w",newline="")
data_writer = csv.writer(file)
data_writer.writerow(meta_data)


print("Found PM2.5 sensor, reading data...")

while t<run_time:
    try:
        aqdata = pm25.read()
        
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue
    
    data_entry = [(time.time() - start), aqdata["pm10 standard"], 
                    aqdata["pm25 standard"], aqdata["pm100 standard"], 
                    bme680.temperature, bme680.relative_humidity,
                    bme680.pressure, bme680.altitude]
    data_writer.writerow(data_entry)
    
    print("="*39)
    print("Seconds from start: %0.3f" % (time.time() - start))
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")
    print("Temperature: %0.1f C" % bme680.temperature)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude: %0.2f meters" % bme680.altitude)
    print("="*39)
    
    time.sleep(1)
    t +=1
