Introduction:

This is the second commit for the face detection. Comparing to the previous one, here I apply the technique to the immigration card. As shown in the output file, you can see the drawn red rectangle declaring the face area.


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


Method:

Our target dataset would be the Hungarian license card and identification card. Since they are all confidencial data which is hard to get online, we use our immigration card as a sample for testing.

In this version, I used the dlib.get_frontal_face_detector for the face detection and then draw the rectangle within the detected area. It is work perfectly with the current image, while in real case it may happen that the input photo with bad quality (i.e. weird perspective, full of noise and so on).

** Update: Adding the eyes feature detection and drawn in red points.

In the next generation, I am going to find way for calculating the desired rotation angle.

Output:
In the output files, you can see the up-to-date outputs. (i.e. face detection, eyes detection) 
