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

# 使用dlib.get_frontal_face_detector识别人脸
detector = dlib.get_frontal_face_detector( )
image = io.imread("/Users/pingguo/Desktop/identification_recognization/Card_test.jpg")
dets = detector(image, 2)  # 使用detector进行人脸检测 dets为返回的结果

# 将识别的图像可视化
plt.figure()
ax = plt.subplot(111)
ax.imshow(image)
plt.axis("off")
for i, face in enumerate(dets):
    # 在图片中标注人脸，并显示
    left = face.left( )
    top = face.top( )
    right = face.right( )
    bottom = face.bottom( )
    rect = mpatches.Rectangle((left, bottom), right - left, top - bottom,
                              fill=False, edgecolor='red', linewidth=1)
    ax.add_patch(rect)
plt.show( )