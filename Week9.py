import RPi.GPIO as GPIO
import datetime
import time

# Global variable to store count
count = 0

def my_callback(channel):
    global count
    count += 1
    if GPIO.input(channel) == GPIO.HIGH:
        print('\n▼  at ' + str(datetime.datetime.now()))
    else:
        print('\n ▲ at ' + str(datetime.datetime.now()))

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set up falling-edge event detection

    # Add falling edge detection with callback
    GPIO.add_event_detect(6, GPIO.FALLING, callback=my_callback)

    # Infinite loop with sleep for 1 minute
    while True:
        # Sleep for 1 minute
        time.sleep(60)
        # Print the count and reset it
        print(f"Counts collected in the last minute: {count}")
        count = 0

except KeyboardInterrupt:
    print("\nKeyboard interrupt detected, exiting...")

finally:
    # Clean up GPIO
    GPIO.cleanup()
    