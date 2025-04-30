import time
from grove.adc import ADC
import io
import time
from picamera import PiCamera
from grove.grove_relay import GroveRelay
import json
from grove.gpio import GPIO
import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from keys import *

connection_string = connection_string
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)


print('Connecting')
device_client.connect()
print('Connected')


def handle_method_request(request):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off() 
    
    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)

device_client.on_method_request_received = handle_method_request
#tells iot hub client to call handle method request function when direct method is called




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

 

    relay = GPIO(12,GPIO.OUT)
    relay = GroveRelay(5)

    print(f"Testing Grove Light Sensor on pin A{pin}...")
    while True:
        light_value = sensor.read_light()
        print(f"Light Sensor Value: {light_value}")
        telemetry = json.dumps({'light_value' : light_value})
        print("Sending telemetry ", telemetry)
        message = Message(json.dumps({ 'light_value': light_value }))
        device_client.send_message(message)
        time.sleep(5) 
        time.sleep(1)
        if light_value > 100:
            relay.on()
            image = io.BytesIO()
            camera.capture(image, 'jpeg')
            image.seek(0)
            with open('image.jpg', 'wb') as image_file:
                print('Taking Photo')
                image_file.write(image.read())
        elif light_value <= 100:
            relay.off()
 

  

if __name__ == "__main__":
    main()
 


