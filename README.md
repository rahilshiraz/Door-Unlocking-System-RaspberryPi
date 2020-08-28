# Door-Unlocking-System-RaspberryPi
Automatic Door Unlocking System with Raspberry Pi using OpenCV, CNN ResNet and LBPH Algorithm

Algorithm for operating face recognition on Raspberry:
1.	Load required models and recognizer files.
2.	Open a loop.
3.	Read PIR sensor.. if person detected>30 times then open camera.
4.	Read Camera.
5.	Run Face Detection and Face Recognition.
6.	Get Person name and print Welcome text.
7.	If person is in known list then trigger dc motor to operate. Wait for a minute and close the door. 
8.	If person is unknown then send notification.
9.	Loop the main function.
