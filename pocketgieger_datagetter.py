import RPi.GPIO as GPIO
import datetime

def my_callback(channel):
    if GPIO.input(channel) == GPIO.LOW:
        print('\nCount at ' + str(datetime.datetime.now()))
 
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(6, GPIO.FALLING, callback=my_callback)
    
finally:
    GPIO.cleanup()
