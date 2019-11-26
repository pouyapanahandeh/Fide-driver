------------------------------------------------------------------------------------------
Introduction:

This is the second commit for the face detection. Comparing to the previous one, here I apply the technique to the immigration card. As shown in the output file, you can see the drawn red rectangle declaring the face area.

------------------------------------------------------------------------------------------
**Updates: In the Image_processing&num_extraction.py file, we have achieved the image processing property by first human face detection, capturing the human eyes features and use it as image perspective rotation part. And then defined functions to extract both the string (text) and num (card number) for the authentication property.

------------------------------------------------------------------------------------------
Running environment:

Mac os
Pycharm
Python3
PIL
pytesseract
pandas
opencv-python
numpy>=1.9.2
scipy>=0.15.1
matplotlib>=1.4.3
Pillow>=2.7.0
lxml>=3.5.0

------------------------------------------------------------------------------------------
Method:

Our target dataset would be the Hungarian license card and identification card. Since they are all confidencial data which is hard to get online, we use our immigration card as a sample for testing.

In this version, I used the dlib.get_frontal_face_detector for the face detection and then draw the rectangle within the detected area. It is work perfectly with the current image, while in real case it may happen that the input photo with bad quality (i.e. weird perspective, full of noise and so on).

------------------------------------------------------------------------------------------
** Update: Adding the eyes feature detection and drawn in red points.

------------------------------------------------------------------------------------------
** Update: 
Adding the calculation of tilt angle of eyes + tilt angle of IDcard + Rotation function + Head extraction 
( The save result can be a useful source for the Human_face_detection part, input as image-to-be-checked.)

------------------------------------------------------------------------------------------
** Update: 
Mainly adding the image_to_string function for the more accurate text extration. 

After several trails, we found here the specified language library do matters the results, so in the end we choose the "hun" for the string extraction and "ocd" for the num extraction. 

Our output can be simply one line showing the extracted idetification number for the driver authentication process, and if necessary the information on the card  such as driver's name, birth date and so on for future user database management.

Tested on 5 image types, workes well.


------------------------------------------------------------------------------------------
Output:
In the output files, you can see the up-to-date outputs. (i.e. Face detection, Eyes detection, Rotate&detection, Head Extraction, string_extraction output files(.txt)) 
