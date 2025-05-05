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
from datetime import datetime
from keys import *
import requests
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient


connection_string = connection_string
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
id = "a5046072-6943-4d0c-a294-1aa93032e545"
server_command_topic = id + '/commands'

client_name = id + 'soilmoisturesensor_client'
client_telemetry_topic = id + '/telemetry'

print('Connecting')
device_client.connect()
print('Connected')

relay = GPIO(12,GPIO.OUT)
relay = GroveRelay(5)

prediction_url = prediction_url
prediction_key = prediction_key
parts = prediction_url.split('/')
endpoint = 'https://' + parts[2]
project_id = parts[6]
iteration_name = parts[9]
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)

def handle_method_request(request):
    try:
        print("Direct method received - ", request.name)

        if request.name == "relay_on":
            relay.on()
        elif request.name == "relay_off":
            relay.off() 
        
        method_response = MethodResponse.create_from_method_request(request, 200)
        device_client.send_method_response(method_response)
    except Exception:
            print("Error Receiving relay response: %s",Exception)


#tells iot hub client to call handle method request function when direct method is called
device_client.on_method_request_received = handle_method_request




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
 
    print(f"Testing Grove Light Sensor on pin A{pin}...")
    

    while True:
        light_value = sensor.read_light()
        timestamp = datetime.utcnow().isoformat()
        print(f"Light Sensor Value: {light_value}")
        telemetry = json.dumps({'light_value': light_value, 'timestamp': timestamp})
        print("Sending telemetry ", telemetry)
        try:
            message = Message(json.dumps( telemetry ))
            device_client.send_message(message)
        except Exception: 
            print("Error Sending Light Values: %s",Exception)


        image = io.BytesIO()
        camera.capture(image, 'jpeg')
        image.seek(0)
        results = predictor.classify_image(project_id, iteration_name, image)
        for prediction in results.predictions:
            print(f'{prediction.tag_name}:\t{prediction.probability * 100:.2f}%')
        with open('image.jpg', 'wb') as image_file:
            print('Taking Photo')
            image_file.write(image.read())
        image.close()
        time.sleep(5) 

 

  

if __name__ == "__main__":
    main()
 


