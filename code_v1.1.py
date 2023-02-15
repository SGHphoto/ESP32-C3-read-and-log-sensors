import time
import board
import busio
import digitalio
import neopixel
import adafruit_ahtx0
import adafruit_bh1750
import adafruit_sdcard
import storage
import adafruit_mqtt
from adafruit_mqtt import MQTTClient
from secrets import secrets

# Set up NeoPixel status LED
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.1

# Set up AHT10 temperature/humidity sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_ahtx0.AHT10(i2c)

# Set up BH1750 light sensor
i2c = busio.I2C(board.SCL, board.SDA)
light_sensor = adafruit_bh1750.BH1750(i2c)

# Set up SD card for logging
sd_cs = digitalio.DigitalInOut(board.D10)
sd_spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
sdcard = adafruit_sdcard.SDCard(sd_spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Set up MQTT client
client = MQTTClient("esp32-c3", "192.168.1.10", user=secrets['mqtt_username'], password=secrets['mqtt_password'])

# Main loop
while True:
    # Read sensor data
    temperature = sensor.temperature
    humidity = sensor.relative_humidity
    light = light_sensor.lux

    # Log sensor data to file
    with open("/sd/data.log", "a") as f:
        f.write("{},{},{},{}\n".format(time.monotonic(), temperature, humidity, light))

    # Publish sensor data to MQTT server
    client.connect()
    client.publish("temperature", str(temperature))
    client.publish("humidity", str(humidity))
    client.publish("light", str(light))
    client.disconnect()

    # Put ESP32 into deep sleep for 30 seconds
    print("Going to sleep...")
    time.sleep(1)
    client._disconnect()
    time.sleep(30)
    pixel.fill((0, 0, 0))
    time.sleep(0.5)
    pixel.fill((255, 0, 0))
    time.sleep(0.5)
    pixel.fill((0, 0, 0))
    time.sleep(0.5)
    pixel.fill((255, 0, 0))
    time.sleep(0.5)
    print("Woke up!")
    time.sleep(1)

    
    
    */
    import time
import board
import busio
import digitalio
import neopixel
import adafruit_ahtx0
import adafruit_bh1750
import adafruit_sdcard
import storage
import adafruit_mqtt
from adafruit_mqtt import MQTTClient
from secrets import secrets

# Set up NeoPixel status LED
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.1

# Set up AHT10 temperature/humidity sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_ahtx0.AHT10(i2c)

# Set up BH1750 light sensor
i2c = busio.I2C(board.SCL, board.SDA)
light_sensor = adafruit_bh1750.BH1750(i2c)

# Set up SD card for logging
sd_cs = digitalio.DigitalInOut(board.D10)
sd_spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
sdcard = adafruit_sdcard.SDCard(sd_spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Set up MQTT client
client = MQTTClient("esp32-c3", "192.168.1.10", user=secrets['mqtt_username'], password=secrets['mqtt_password'])

# Main loop
while True:
    # Read sensor data
    temperature = sensor.temperature
    humidity = sensor.relative_humidity
    light = light_sensor.lux

    # Log sensor data to file
    with open("/sd/data.log", "a") as f:
        f.write("{},{},{},{}\n".format(time.monotonic(), temperature, humidity, light))

    # Publish sensor data to MQTT server
    client.connect()
    client.publish("temperature", str(temperature))
    client.publish("humidity", str(humidity))
    client.publish("light", str(light))
    client.disconnect()

    # Put ESP32 into deep sleep for 30 seconds
    print("Going to sleep...")
    time.sleep(1)
    client._disconnect()
    time.sleep(30)
    pixel.fill((0, 0, 0))
    time.sleep(0.5)
    pixel.fill((255, 0, 0))
    time.sleep(0.5)
    pixel.fill((0, 0, 0))
    time.sleep(0.5)
    pixel.fill((255, 0, 0))
    time.sleep(0.5)
    print("Woke up!")
    time.sleep(1)
/*
