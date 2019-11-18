#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Sat Oct 26 17:28:35 2019
    
    @author: liusirui
    """

from importlib import reload
import pytesseract
import cv2
import matplotlib.pyplot as plt
import dlib
import matplotlib.patches as mpatches
from skimage import io, draw, transform, color
import numpy as np
import pandas as pd
import re
from PIL import Image
import pytesseract

# Using dlib.get_frontal_face_detector to detect the human face
detector = dlib.get_frontal_face_detector( )
image = io.imread("/Users/pingguo/Desktop/identification_recognization/Card_test.jpg")
# Save result in dets
dets = detector(image, 2)  

# Draw the detected rectangle
plt.figure()
ax = plt.subplot(111)
ax.imshow(image)
plt.axis("off")
for i, face in enumerate(dets):
    # draw the human face
    left = face.left( )
    top = face.top( )
    right = face.right( )
    bottom = face.bottom( )
    rect = mpatches.Rectangle((left, bottom), right - left, top - bottom,
                              fill=False, edgecolor='red', linewidth=1)
    ax.add_patch(rect)
plt.show( )

# Detecting the eyes
predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
detected_landmarks = predictor(image, dets[0]).parts( )
landmarks = np.array([[p.x, p.y] for p in detected_landmarks])

# Draw the eyes 
plt.figure( )
ax = plt.subplot(111)
ax.imshow(image)
plt.axis("off")
plt.plot(landmarks[0:4, 0], landmarks[0:4, 1], 'ro')
for ii in np.arange(4):
    plt.text(landmarks[ii, 0] - 10, landmarks[ii, 1] - 15, ii)
plt.show( )    