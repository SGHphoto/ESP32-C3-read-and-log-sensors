import time
import board
import busio
import digitalio
import neopixel
import adafruit_sht31d
import adafruit_sdcard
import storage
import adafruit_mqtt
from adafruit_mqtt import MQTTClient
from secrets import secrets

# Set up NeoPixel status LED
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.1

# Set up SHT31D temperature/humidity sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)

# Set up SD card for logging
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D10)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Set up MQTT client
client = MQTTClient("esp32-c3", "192.168.1.10", user=secrets['mqtt_username'], password=secrets['mqtt_password'])

# Connect to WiFi
wifi = None
while not wifi:
    try:
        from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager
        esp32_cs = digitalio.DigitalInOut(board.D13)
        esp32_ready = digitalio.DigitalInOut(board.D11)
        esp32_reset = digitalio.DigitalInOut(board.D12)
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
        wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_pixel=pixel)
    except Exception as e:
        print("Could not connect to WiFi, retrying...", e)
        time.sleep(5)

# Main loop
while True:
    # Read sensor data
    temperature = sensor.temperature
    humidity = sensor.relative_humidity

    # Log sensor data to file
    with open("/sd/data.log", "a") as f:
        f.write("{},{},{}\n".format(time.monotonic(), temperature, humidity))

    # Publish sensor data to MQTT server
    client.connect()
    client.publish("temperature", str(temperature))
    client.publish("humidity", str(humidity))
    client.disconnect()

    # Put ESP32 into deep sleep for 30 seconds
    print("Going to sleep...")
    time.sleep(1)
    client._disconnect()
    esp.deinit()
    time.sleep(30)
    esp.reset()
    print("Woke up!")
