Introduction:

This is the initial commit for the human face detection. Here we use 2 images online for testing. Later we can verify the output by adding sample of real life case such as selfies.



Running environment:

Mac os
Pycharm
Python3
PIL
numpy>=1.9.2


Method:

Our target dataset would be simply the driver's selfie. 

In this version, I am using the face_recognition library in python. Achieving by learning the encodings from known image (in our case, it could be the driver's image), then detect the face in the image with certain position. Marked with bold edges around the detected face. Comparing the distance of the encoding matrices then finding the argmin of two sets.

In the next generation, I am going to do the face detection on identication card. In the end, the result here will be the known_image_dataset, while the result of identication detection will be the dataset which need to be learned and checked.



Output:
In the face_recognition_output.png file, we can see the rectangle box drawing the recognized face. 





