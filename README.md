### IOT-Project

# Automatic Dog Door
#### Student Name: *Tomás McGrath*   Student ID: *20103551*

I did a dog door sensor, it scans for motion and then records the light value and timestamps and sends it to azure , it processses and should come back from functionapp with a response to turn relay on or off.
I broke it at the end by accident when I added a timestamp value to the json.
Relay was supposed to simulate light coming on when its dark so a better photo could be taken.
Camera takes a picture and sends it to custom vision , if chance is greater than 40 that its a dog then turn on motor to simulate opening door. 
After a while door closes.
I have blynk displaying light values, I have a blob for the timestamp and light value and then I plot them.
![image](https://github.com/user-attachments/assets/0ead296d-ba2c-4bb9-a0f9-48c1eec4a2b4)
Output of running the app.

![image](https://github.com/user-attachments/assets/e48714f2-942e-4713-a415-8ab781e2e1d1
)Light values displayed over time.

![image](https://github.com/user-attachments/assets/bd6677a2-d8da-44f3-957a-d79c0be9c887)
Log file

![image](https://github.com/user-attachments/assets/e2ccdad8-a5af-4f7d-8e02-a29c98a9964f)
folder

## Tools, Technologies and Equipment

VS Code, Rasp berry pi, azure, iot hub, blob, custom vision, maybe phone
Camera, light sensor,servo motor  relay.
Stored data locally in json, plotted and used blynk
![image](https://github.com/user-attachments/assets/98e044c1-ce7c-4672-bacf-43175442522a)



