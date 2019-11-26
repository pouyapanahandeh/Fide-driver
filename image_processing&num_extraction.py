#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Sat Oct 26 17:28:35 2019

"""
import os
import shlex
import subprocess
import sys
import tempfile
from errno import ENOENT
from glob import iglob
from os.path import realpath, normpath, normcase
import matplotlib.pyplot as plt
import dlib
import matplotlib.patches as mpatches
from pytesseract.pytesseract import subprocess_args, TesseractNotFoundError, timeout_manager, \
    TesseractError, get_errors, numpy_installed
from skimage import io, draw, transform, color
import numpy as np
import pandas as pd
from PIL import Image
import glob

tesseract_cmd = '/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
RGB_MODE = 'RGB'
SUPPORTED_FORMATS = {
    'JPEG', 'PNG', 'PBM', 'PGM', 'PPM', 'TIFF', 'BMP', 'GIF'
}

detected_num_list = []


def twopointcor(point1, point2):
    """point1 = (x1,y1),point2 = (x2,y2)"""
    deltxy = point2 - point1
    corner = np.arctan(deltxy[1] / deltxy[0]) * 180 / np.pi
    return corner


def IDcorner(landmarks):
    """landmarks:检测的人脸5个特征点
    """
    corner20 = twopointcor(landmarks[2, :], landmarks[0, :])
    corner = np.mean([corner20])
    return corner


def rotateIdcard(image):
    "image :需要处理的图像"
    # dlib.get_frontal_face_detector
    detector = dlib.get_frontal_face_detector( )
    dets = detector(image, 2)  
    
    predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
    detected_landmarks = predictor(image, dets[0]).parts( )
    landmarks = np.array([[p.x, p.y] for p in detected_landmarks])
    corner = IDcorner(landmarks)
   
    image2 = transform.rotate(image, corner, clip=False)
    image2 = np.uint8(image2 * 255)
    
    det = detector(image2, 2)
    return image2, det


def run_tesseract(input_filename,
                  output_filename_base,
                  extension,
                  lang,
                  config='',
                  nice=0,
                  timeout=0):
    cmd_args = []

    if not sys.platform.startswith('win32') and nice != 0:
        cmd_args += ('nice', '-n', str(nice))

    cmd_args += (tesseract_cmd, input_filename, output_filename_base)

    if lang is not None:
        cmd_args += ('-l', lang)

    if config:
        cmd_args += shlex.split(config)

    if extension and extension not in {'box', 'osd', 'tsv'}:
        cmd_args.append(extension)

    try:
        proc = subprocess.Popen(cmd_args, **subprocess_args())
    except OSError as e:
        if e.errno != ENOENT:
            raise e
        raise TesseractNotFoundError()

    with timeout_manager(proc, timeout) as error_string:
        if proc.returncode:
            raise TesseractError(proc.returncode, get_errors(error_string))


def prepare(image):
    if numpy_installed and isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    if not isinstance(image, Image.Image):
        raise TypeError('Unsupported image object')

    extension = 'PNG' if not image.format else image.format
    if extension not in SUPPORTED_FORMATS:
        raise TypeError('Unsupported image format/type')

    if not image.mode.startswith(RGB_MODE):
        image = image.convert(RGB_MODE)

    if 'A' in image.getbands():
        # discard and replace the alpha channel with white background
        background = Image.new(RGB_MODE, image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
        image = background

    image.format = extension
    return image, extension

def save_image(image):
    with tempfile.NamedTemporaryFile(prefix='tess_', delete=False) as f:
        temp_name = f.name

    if isinstance(image, str):
        return temp_name, realpath(normpath(normcase(image)))

    image, extension = prepare(image)
    input_file_name = temp_name + os.extsep + extension
    image.save(input_file_name, format=extension, **image.info)
    return temp_name, input_file_name


def cleanup(temp_name):
    """ Tries to remove temp files by filename wildcard path. """
    for filename in iglob(temp_name + '*' if temp_name else temp_name):
        try:
            os.remove(filename)
        except OSError as e:
            if e.errno != ENOENT:
                raise e

def run_and_get_output(image,
                       extension='',
                       lang=None,
                       config='',
                       nice=0,
                       timeout=0,
                       return_bytes=False):

    temp_name, input_filename = '', ''
    try:
        temp_name, input_filename = save_image(image)
        kwargs = {
            'input_filename': input_filename,
            'output_filename_base': temp_name + '_out',
            'extension': extension,
            'lang': lang,
            'config': config,
            'nice': nice,
            'timeout': timeout
        }

        run_tesseract(**kwargs)
        filename = kwargs['output_filename_base'] + os.extsep + extension
        with open(filename, 'rb') as output_file:
            if return_bytes:
                return output_file.read()
            return output_file.read().decode('utf-8').strip()
    finally:
        cleanup(temp_name)

class Output:
    BYTES = 'bytes'
    DATAFRAME = 'data.frame'
    DICT = 'dict'
    STRING = 'string'


def image_to_string(image,
                    lang=None,
                    config='',
                    nice=0,

                    output_type=Output.STRING,
                    timeout=0):
    """
    Returns the result of a Tesseract OCR run on the provided image to string
    """
    args = [image, 'txt', lang, config, nice, timeout]

    return {
        Output.BYTES: lambda: run_and_get_output(*(args + [True])),
        Output.DICT: lambda: {'text': run_and_get_output(*args)},
        Output.STRING: lambda: run_and_get_output(*args),
    }[output_type]()


if __name__ == '__main__':
    # cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    # cv2.imshow('image',image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    #dlib.get_frontal_face_detector
    detector = dlib.get_frontal_face_detector( )

    image = io.imread('/Users/pingguo/Desktop/Software Tech/identification_recognization/data/Card_test.jpg')
    dets = detector(image, 2)  

    
    for i, face in enumerate(dets):
        
        left = face.left( )
        top = face.top( )
        right = face.right( )
        bottom = face.bottom( )
        rect = mpatches.Rectangle((left, bottom), right - left, top - bottom,
                                  fill=False, edgecolor='red', linewidth=1)

    
    predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
    detected_landmarks = predictor(image, dets[0]).parts( )
    landmarks = np.array([[p.x, p.y] for p in detected_landmarks])

    
    # plt.figure( )
    # ax = plt.subplot(111)
    # ax.imshow(image)
    # plt.axis("off")
    plt.plot(landmarks[0:4, 0], landmarks[0:4, 1], 'ro')
    for ii in np.arange(4):
        plt.text(landmarks[ii, 0] - 10, landmarks[ii, 1] - 15, ii)
    # plt.show( )

    
    corner10 = twopointcor(landmarks[1, :], landmarks[0, :])
    corner23 = twopointcor(landmarks[3, :], landmarks[2, :])
    corner20 = twopointcor(landmarks[2, :], landmarks[0, :])
    corner = np.mean([corner10, corner23, corner20])
    # print(corner10)
    # print(corner23)
    # print(corner20)
    # print(corner)

    corner = IDcorner(landmarks)
 
    image2, dets = rotateIdcard(image)
    left = dets[0].left( )
    top = dets[0].top( )
    right = dets[0].right( )
    bottom = dets[0].bottom( )
    rect = mpatches.Rectangle((left, bottom), (right - left), (top - bottom),
                              fill=False, edgecolor='red', linewidth=1)
    # ax.add_patch(rect)

    width = right - left
    high = top - bottom
    left2 = np.uint(left - 0.3 * width)
    bottom2 = np.uint(bottom + 0.4 * width)
    rect = mpatches.Rectangle((left2, bottom2), 1.6 * width, 1.8 * high,
                              fill=False, edgecolor='blue', linewidth=1)
    # ax.add_patch(rect)
    # plt.show( )

   
    top2 = np.uint(bottom2 + 1.8 * high)
    right2 = np.uint(left2 + 1.6 * width)
    image3 = image2[top2:bottom2, left2:right2, :]
    # plt.imshow(image3)
    # plt.axis("off")
    # plt.show( )

    num = image_to_string(image2, lang='osd')
    text = image_to_string(image2, lang='hun')
    # text = pytesseract.image_to_string(image2)

    # print(text)

    textlist = text.split("\n")
    textdf = pd.DataFrame({"text": textlist})
    textdf["textlen"] = textdf.text.apply(len)
    textdf = textdf[textdf.textlen>1].reset_index(drop=True)
    print(textdf)

    numlist = num.split("\n")
    numdf = pd.DataFrame({"num": numlist})
    numdf["numlen"] = numdf.num.apply(len)
    numdf = numdf[numdf.numlen>1].reset_index(drop=True)

    # textdf.loc[textdf"textlen"] == 9, "text"]
    detected_num = numdf.loc[numdf['numlen'] == 9, 'num'].iloc[0]
    print("Detected identification number is: ", detected_num )


