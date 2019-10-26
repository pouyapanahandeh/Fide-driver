Code for Image detection.
Using the face_recognition library
By learning the encodings from known image (in our case, it could be the driver's image), then detect the face in the image with certain position. Comparing the distance of the encoding matrices and find the argmin of two sets.
In the output, we can see the rectangle box drawing the recognized face.
