from PIL import Image, ImageFilter, ImageOps
import utils.logger as logger
import cv2
from config import *
from typing import Tuple, List

import sys
import numpy as np
import tempfile
index = 0
IMAGE_SIZE = 1024
BINARY_THREHOLD = 180
def crop_image(image, area:Tuple, nameplate_type, index) -> object:
    ''' Uses PIL to crop an image, given its area.
    Input:
        image - PIL opened image
        Area - Coordinates in tuple (xmin, ymax, xmax, ymin) format '''
    img1 = Image.open(image)
    img1 = img1.convert('L')
    cropped_image = img1.crop(area)
    cropped_image.save('cropimgs/'+str(index)+'_'+nameplate_type+".jpg", "JPEG", dpi=(300,300))
    
    #basewidth = 200
    #wpercent = (basewidth/float(img.size[0]))
    #hsize = int((float(img.size[1])*float(wpercent)))
    #cropped_image = img.resize((basewidth,hsize), Image.ANTIALIAS)
    #global i
    #print(nameplate_type)
    #i += 1
    return cropped_image

def locate_asset(self, image, classifier, lines="") -> List:
    ''' Determines where an asset is in the picture, returning
     a set of coordinates, for the top left, top right, bottom
     left, and bottom right of the tag
     Returns:
     [(area, image)]
         Area is the coordinates of the bounding box
         Image is the image, opened by PIL.'''
    cropped_images = []
    nameplate_list = []
    global index
    #print(lines)
    for line in str(lines).split('\n'):
        #print(line)
        if  "left_x" in line:
            #print(line)
            nameplate_type, area = classifier.extract_info(line)
            # Open image
            cropped_images.append((area, crop_image(image, area, nameplate_type, index)))
            nameplate_list.append(nameplate_type)
    if cropped_images == []:
        logger.bad("No label found in image.")
    else:
        logger.good("Found " + str(len(cropped_images)) + " label(s) in image.")
    index +=1
    return nameplate_list, cropped_images

def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y

    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename

def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3

def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41,3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    #img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image