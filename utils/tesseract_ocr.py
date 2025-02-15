from utils.ocr import OCR
import pyocr
import pyocr.builders
import sys
from PIL import Image
from typing import Tuple

class TesseractOCR(OCR):

    def initialize(self):
        ''' Initialize Tesseract and load it up for speed '''
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No tools found, do you have Tesseract installed?")
            sys.exit(1)
        self.tool = tools[0]
        self.langs = self.tool.get_available_languages()
        
    def ocr_one_image(self, area, image, lang,  threadList=-1, threadNum=None):
        print("Starting image...")
        ''' If input languages is english or thai then use langs[0] as eng train data and lang[1] as thai train data'''
        if(lang=='eng'):
            txt = self.tool.image_to_string(image, lang=self.langs[0], builder=pyocr.builders.TextBuilder())
        else:
            txt = self.tool.image_to_string(image, lang=self.langs[1], builder=pyocr.builders.TextBuilder())
        
        print("==RESULT==" + str(area) + "\n" + txt + "\n==========================")
        
        if threadList != -1:
            threadList[threadNum] = txt
            
        return txt
