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


# 身份证号码识别
def identity_OCR(pic_path):
    # 读取所需图片
    img1 = cv2.imread(pic_path)
    # 裁切脸的部分
    crop_img = img1[1439:2327, 791:1631]
    # 灰度图像
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # threshing if needed
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # Do median blurring to remove noise
    remove_noise = cv2.medianBlur(gray, 3)

    # 粉卡序列号裁切
    card_num_area = img1[899:1067, 2459:3119]

    code = pytesseract.image_to_string(card_num_area)
    print("The detected num is:" + str(code))
    # cv2.imshow('check',img2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    identity_OCR('/Users/pingguo/Desktop/identification_recognization/Card_test.jpg')