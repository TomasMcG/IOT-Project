### IOT-Project

# Automatic Dog Door
#### Student Name: *Tomás McGrath*   Student ID: *20103551*

i am planning on doing a project that detects for a dog and opens a dog door. I might also have it send you a notification. I would use motion sensor and camera for input, have a light and a relay for output. I would use a motion detector for motion, if yes then checks if its dark and turns on light. I will take a picture with the camera and send it to vision to check if its a dog. I will train a dog detections model. I might try to host it with a container. Azure wull manage the mqtt for me. If it is a dog then it will turn ona relay to let the dog go inside and then turn off the relay after a set amount of time of no dog. I might also try to use blynk to access the camera at anytime but that would be an extra thing. I need to learn how to use the motion detector first. Might count the number of times the dog entered the door today. I do only have the camera on one side. Not sure how to display the door opening, Might keep a database of dog images online. Open manually with blynk. Telemetry and data proces in cloud. Claffiication. Motion detection and iamge capture first, control of the servo to open and close. can do in edge or cloud, he geenrally does in clodu first to check it works, then deploy. Should look for pre existing training sets.
Proof of concept. Automated and manual version. Notificaiton of the still picture. DAte time and maybe picture for storing image online. DAte time and link to image. If 2 cameras can check the time between them.

Can do a glitch app.
if motion , stuck oup on cloud and then glitch app to view it, last image taken.

Can do the same with azure as firebase,


## Tools, Technologies and Equipment

VS Code, Rasp berry pi, azure, docker, custom vision, maybe phone
Camera, light sensor, Led light or phone torch, relay.
Maybe firebase for remote storage. 


