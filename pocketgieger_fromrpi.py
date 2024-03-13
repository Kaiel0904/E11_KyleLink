import RPi.GPIO as GPIO
import time
import csv

# Function to initialize GPIO and read data from the radiation sensor
def read_sensor_data():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN)
        
        # Read data from the sensor for 60 seconds to get an average CPM
        count = 0
        start_time = time.time()
        while (time.time() - start_time) < 60:
            if GPIO.input(18):
                count += 1
            time.sleep(1)

        # Calculate CPM (counts per minute)
        cpm = count

        return cpm

    finally:
        GPIO.cleanup()

# Main function to pull data for 30 seconds
def main():
    runtime = 30  # Runtime in seconds
    start_time = time.time()
    data = []

    while (time.time() - start_time) < runtime:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        cpm = read_sensor_data()
        data.append((timestamp, cpm))
        time.sleep(1)  # Adjust the sleep time based on how often you want to read data

    write_to_csv(data)
    print("Data collection complete. CSV file generated.")

if __name__ == "__main__":
    main()
