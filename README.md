# Rock-Paper-Scissors-Detector
As the name suggests, it is a program to recognize the three gestures "Rock", "Paper", "Scissors" from a webcam in real-time. 

It uses Google's "Mediapipe" library for hand recognition and OpenCV for the webcam image. 

After receiving the coordinates of every finger segment (Which can be found here: https://mediapipe.readthedocs.io/en/latest/solutions/hands.html) 
it checks every single finger to see if it is bent or not. 

It does that by comparing the sum of the distance of the points on the finger with the distance between the fingertip and the finger base. 
If it´s not bent, the distance should be about the same, so if the fingertip to finger base distance is much less it knows it´s bent.
