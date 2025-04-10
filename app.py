import time
from grove.adc import ADC
import io
import time
from picamera import PiCamera
from grove.grove_relay import GroveRelay
import json
from grove.gpio import GPIO



class GroveLightSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC(0x08)

    def read_light(self):
        return self.adc.read(self.channel)

def main():
    pin = 2  
    sensor = GroveLightSensor(pin)


    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.rotation = 180

    time.sleep(2)

    image = io.BytesIO()
    camera.capture(image, 'jpeg')
    image.seek(0)
    with open('image.jpg', 'wb') as image_file:
        print('Taking Photo')
        image_file.write(image.read())

    relay = GPIO(12,GPIO.OUT)
    relay = GroveRelay(5)

    print(f"Testing Grove Light Sensor on pin A{pin}...")
    while True:
        light_value = sensor.read_light()
        print(f"Light Sensor Value: {light_value}")
        time.sleep(1)
        if light_value > 100:
            relay.on()
        elif light_value <= 100:
            relay.off()

if __name__ == "__main__":
    main()



