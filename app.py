import time
from grove.adc import ADC
import io
import time
from picamera import PiCamera
from grove.grove_relay import GroveRelay
import json
#from grove.gpio import GPIO
from grove.gpio import GPIO as GroveGPIO
import RPi.GPIO as GPIO
import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from datetime import datetime
from keys import *
import requests
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import pandas as pd
import matplotlib.pyplot as plt
from azure.storage.blob import ContainerClient
import base64
import BlynkLib

connection_string = connection_string
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
id = "a5046072-6943-4d0c-a294-1aa93032e545"
server_command_topic = id + '/commands'

client_name = id + 'soilmoisturesensor_client'
client_telemetry_topic = id + '/telemetry'

print('Connecting')
device_client.connect()
print('Connected')

blynk = BlynkLib.Blynk(BLYNK_AUTH)

client = ContainerClient.from_connection_string(connect_str, container_name)
records = []

for blob in client.list_blobs():
    blob_data = client.download_blob(blob).readall()
    lines = blob_data.decode('utf-8').splitlines()
    for line in lines:
        try:
            msg = json.loads(line)
            body = msg.get("Body")
            if body:
                decoded = json.loads(base64.b64decode(body).decode('utf-8'))
                records.append({
                    "timestamp": pd.to_datetime(decoded.get("timestamp", msg.get("EnqueuedTimeUtc"))),
                    "light_value": decoded.get("light_value")
                })
        except Exception as e:
            print(f"Skipped line: {e}")

df = pd.DataFrame(records)

if not df.empty:
    df.sort_values("timestamp", inplace=True)
    plt.plot(df["timestamp"], df["light_value"], marker='o')
    plt.title("Light Values Over Time")
    plt.xlabel("Time")
    plt.ylabel("Light(lux) ")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig("light_plot.png")
else:
    print("No data to plot.")


#relay = GPIO(12,GPIO.OUT)
relay_pin = GroveGPIO(12, GroveGPIO.OUT)
relay = GroveRelay(5)

SERVO_PIN = 18  

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)  
pwm.start(0)  


MOTION_SENSOR_PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)


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
    
def set_angle(angle):
    duty = 2 + (angle / 18)  # Convert angle (0-180) 
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Stop sending signal
  

def main():
    motion_detected = False
    last_light_time = 0
    pin = 2  
    sensor = GroveLightSensor(pin)
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.rotation = 180
 
    print("Waiting for motion...")
    

    while True:
        if GPIO.input(MOTION_SENSOR_PIN):
            if not motion_detected:
                print("Motion detected!")
                motion_detected = True
                light_value = sensor.read_light()
                timestamp = datetime.utcnow().isoformat()
                print(f"Light Sensor Value: {light_value}")
                telemetry = {'light_value': light_value, 'timestamp': timestamp}
                print("Sending telemetry ", telemetry)
                with open("light_log.json", "a") as f:
                    f.write(json.dumps(telemetry) + "\n")
                try:
                    message = Message(json.dumps( telemetry ))
                    device_client.send_message(message)
                except Exception: 
                    print("Error Sending Light Values: %s",Exception)


                image = io.BytesIO()
                camera.capture(image, 'jpeg')
                image.seek(0)
                with open('/home/tomas/IOT-Project/image.jpg', 'wb') as image_file:
                    print('Taking Photo')
                    image_file.write(image.read())
                image.seek(0)
                results = predictor.classify_image(project_id, iteration_name, image)
                
                for prediction in results.predictions:
                    print(f'{prediction.tag_name}:\t{prediction.probability * 100:.2f}%')

                    if prediction.tag_name.lower() == "dog" and prediction.probability > 0.4:
                        print("Opening door")
                        set_angle(180)  # Trigger servo to open
        
                        
                current_time = time.time()
                if current_time - last_light_time >= 10:
                
                    blynk.virtual_write(0, light_value)  
                    last_light_time = current_time

            
            else:
                if motion_detected:
                    print("Motion ended.")
                    set_angle(0)
                motion_detected = False
            blynk.run()
            time.sleep(5)   



        
 
@blynk.on("V1")
def handle_v1_write(value):
    button_value = value[0]
    print(f'Current swith value: {button_value}')
    if button_value=="1":
        relay.on()
    else:
        relay.off()
  

if __name__ == "__main__":
    main()
 


