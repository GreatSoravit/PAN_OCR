from PIL import Image, ImageFilter
import utils.logger as logger
from config import *
from typing import Tuple, List
index = 0

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