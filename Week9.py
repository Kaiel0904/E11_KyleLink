import RPi.GPIO as GPIO
import datetime
import time
import csv
import sys

# Global variable to store count
interval=0
intervals = 30
count = 0
totalcounts = 0
timestamps = []
outfile = (sys.argv[1])
meta_data = ['Time','Counts','Total Counts']
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
    print('Count detected at ' + str(timestamp))


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set up falling-edge event detection

    # Add falling edge detection with callback
    GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback)

    # Infinite loop with sleep for 1 minute
    while interval<intervals:
        # Sleep for 1 minute
        time.sleep(10)
        # Print the count and reset it
        print(f"Counts collected in the last 10 seconds: {count}")
        data_writer.writerow([time.time(),count,totalcounts])
        count = 0
        interval +=1
    file.close()

except KeyboardInterrupt:
    print("\nKeyboard interrupt detected, exiting...")

finally:
    # Clean up GPIO
    GPIO.cleanup()
    
