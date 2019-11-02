Here is the code for Image detection.

I am using the face_recognition library in python. Achieving by learning the encodings from known image (in our case, it could be the driver's image), then detect the face in the image with certain position. Marked with bold edges around the detected face. Comparing the distance of the encoding matrices then finding the argmin of two sets.

In the face_recognition_output.png file, we can see the rectangle box drawing the recognized face.
