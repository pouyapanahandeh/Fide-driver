------------------------------------------------------------------------------------------
Introduction:

This is the initial commit for the identification number extraction.


------------------------------------------------------------------------------------------
Running environment:

Mac os
Pycharm
Python3
PIL
pytesseract
opencv-python
numpy>=1.9.2
scipy>=0.15.1
matplotlib>=1.4.3
Pillow>=2.7.0
lxml>=3.5.0


------------------------------------------------------------------------------------------
Method:

Our target dataset would be the Hungarian license card and identification card. Since they are all confidencial data which is hard to get online, we use our immigration card as a sample for testing.

In this version, I used the pytesseract lib for the string extraction (mainly for the numbers), by manully define the cropping area to get the specific necessary information.

In the next generation, I am going to enhance the image processing procedure for more general image form. By adding functions such as detecting face area, rotation if necessary, cropping by math calculation according to pixel status and so on. 


------------------------------------------------------------------------------------------
Output:
In the uploaded picture, you can see the detected identification number in the terminal. 
