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

![image](https://github.com/user-attachments/assets/f23459a9-da45-4f69-be10-01537d67dc36)
Did 4 iterations of training

![image](https://github.com/user-attachments/assets/55a5ba5a-c7d8-4b0f-80c9-a9f7f42775ea)
Here was the code for my function app, it didn't work in the end after I added a timestamp and I wasn't able to fix it.
Checks if light value is greater than 100 and if not turns on the relay with a message response.
![image](https://github.com/user-attachments/assets/642fd08c-ee07-40b6-9e95-c8b7dfc8d840)
code for handling response, no longer works.

![image](https://github.com/user-attachments/assets/6394385d-b008-43f6-8fd4-9ea6540d2ac6)
main code loop that runs when motion is detected. reads the light value and sends it as telemtry with a timestamp.
![image](https://github.com/user-attachments/assets/3e08e424-c1a9-467d-8594-6f1450c469f5)
code to display values in blynk.
Predictions check there probabilty and set the servor motor angle to open.
After a while if no motion detected it closes.

![image](https://github.com/user-attachments/assets/26c27641-2aa9-4fc5-a3a2-2ceffa226c51)
code for plotting

## Tools, Technologies and Equipment

VS Code, Rasp berry pi, azure, iot hub, blob, custom vision, maybe phone
Camera, light sensor,servo motor  relay.
Stored data locally in json, plotted and used blynk
![image](https://github.com/user-attachments/assets/98e044c1-ce7c-4672-bacf-43175442522a)



