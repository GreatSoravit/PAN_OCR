#!/bin/bash

from config import *
from utils.darknet_classify_image import *
from utils.tesseract_ocr import *
import utils.logger as logger
import sys
import time
import os
import re
import string
PYTHON_VERSION = sys.version_info[0]
OS_VERSION = os.name

import pandas as pd
class PanOCR():
    ''' Finds and determines if given image contains required text and where it is. '''
    from utils.locate_asset import locate_asset

    def init_vars(self):
        try:
            self.DARKNET = DARKNET
            self.TESSERACT = TESSERACT
            return 0
        except:
            return -1
        
    def init_classifier(self):
        ''' Initializes the classifier '''
        try:
            if self.DARKNET:
                # Get a child process for speed considerations
                logger.good("Initializing Darknet")
                self.classifier = DarknetClassifier()
            if self.classifier == None or self.classifier == -1:
                return -1
            return 0
        except:
            return -1
        
    def init_ocr(self):
        ''' Initializes the OCR engine '''
        try:
            if self.TESSERACT:
                logger.good("Initializing Tesseract")
                self.OCR = TesseractOCR()
            if self.OCR == None or self.OCR == -1:
                return -1
            return 0
        except:
            return -1
        
    def init_tabComplete(self):
        ''' Initializes the tab completer '''
        try:
            if OS_VERSION == "posix":
                global tabCompleter
                global readline
                from utils.PythonCompleter import tabCompleter
                import readline
                comp = tabCompleter()
                # we want to treat '/' as part of a word, so override the delimiters
                readline.set_completer_delims(' \t\n;')
                readline.parse_and_bind("tab: complete")
                readline.set_completer(comp.pathCompleter)
                if not comp:
                    return -1
            return 0
        except:
            return -1

    def prompt_input(self):
        
            filename = str(input(" Specify File >>> "))

    def initialize(self):
        if self.init_vars() != 0:
            logger.fatal("Init vars")
        if self.init_tabComplete() != 0:
            logger.fatal("Init tabcomplete")
        if self.init_classifier() != 0:
            logger.fatal("Init Classifier")
        if self.init_ocr() != 0:
            logger.fatal("Init OCR")       
            
            
    def find_and_classify(self, filename):
        ''' find the required text field from given image and read it through tesseract.
            Results are stored in a dicionary. '''
        start = time.time()

        #------------------------------Classify Image----------------------------------------#
        logger.good("Classifying Image")
        coords = self.classifier.classify_image(filename)
        time1 = time.time()
        print("Classify Time: " + str(time1-start))
        # ----------------------------Crop Image-------------------------------------------#
        logger.good("Finding required text")
        nameplate_list, cropped_images = self.locate_asset(filename, self.classifier, lines=coords)
        time2 = time.time()
        #----------------------------Perform OCR-------------------------------------------#
        
        ocr_results = None
        
        if cropped_images == []:
            logger.bad("No text found!")
            return None      
        else:
            logger.good("Performing OCR")
            ocr_results = self.OCR.ocr(cropped_images, nameplate_list)
            #print(ocr_results)
            text_name,text_result =[],[]
            
            fil=filename+'-ocr'
            #with open(fil, 'w+') as f:
            for i in range(len(ocr_results)):
                            text_name.append(nameplate_list[i])
                            text_result.append(ocr_results[i][1])
                            
            #k.insert(0,'Filename')
            #v.insert(0,filename)
            raw_text=dict(zip(text_name, text_result))
        
        time3 = time.time()
        print("OCR Time: " + str(time3-time2))

        end = time.time()
        logger.good("Elapsed: " + str(end-start))

        return raw_text
    
        #----------------------------------------------------------------#
    def text_preprocessing(self, data):
        final_data = []
        for txt in data:
            txt['error'] = ''
            #address
            txt['address'] = txt['address'].replace('\n', ' ')
            #name
            txt['name'] = re.sub(f'[{re.escape(string.punctuation)}]', '', txt['name'])
            fullname_th = list(filter(lambda x: x != '', txt['name'].split(' ')))
            if (len(fullname_th) == 3):
                sex = fullname_th[0]
                txt['name'] = fullname_th[1]
                txt['surname_th'] = fullname_th[2]
                #ocr might not deliver accurate text, so need to identify and double check
                title_girl = [r'.ญ',r'ดญ']
                title_boy = [r'.ช',r'ดช']
                title_women = [r'.ส',r'นส']
                match_girl = False
                match_boy = False
                match_women = False
                
                for title in title_girl:
                    if(re.findall(title,sex) != []):
                        match_girl = True
                
                for title in title_boy:
                    if(re.findall(title,sex) != []):
                        match_boy = True
                
                for title in title_women:
                    if(re.findall(title,sex) != []):
                        match_women = True
                
                if(match_boy):
                    txt['title'] = 'ด.ช.'
                elif(match_girl):
                    txt['title'] = 'ด.ญ.'
                elif(match_women):
                    txt['title'] = 'น.ส.'
                else:
                    if(sex[-1]=='ย'): 
                        txt['title'] = 'นาย' 
                    elif(sex[-1]=='ง'): 
                        txt['title'] = 'นาง'
            else:
                txt['name'] = fullname_th[0]
                txt['surname_th'] = fullname_th[-1]
                txt['error'] += 'NameTH '

            #engname
            fullname_eng = txt['name_eng'].split('\n')
            if(len(fullname_eng) == 2):
                txt['name_eng'] = fullname_eng[0].split(' ')[-1]
                txt['surname_eng'] = fullname_eng[1].split(' ')[-1]
            else:
                txt['name_eng'] = fullname_eng[0].split(' ')[-1]
                txt['surname_eng'] = fullname_eng[-1].split(' ')[-1]
                txt['error'] += 'NameEN '

            #birthdate
            date_regex = r'\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b'
            txt['birthdate'] = txt['birthdate'].split('\n')[-1]
            txt['birthdate'] = re.sub(f'[{re.escape(string.punctuation)}]', '', txt['birthdate'])
            date_matches = [(match.start(), match.end()) for match in re.finditer(date_regex, txt['birthdate'])]
            if (not date_matches):
                txt['error'] += 'Birthdate '
            else:
                txt['birthdate'] = txt['birthdate'][date_matches[0][0]:date_matches[0][1]]

            #religion
            try:
                txt['religion'] = txt['religion'].split(' ')[-1]
            except:
                txt['religion'] = ''
                txt['error'] += 'Religion '
            #id
            txt['id'] = str(txt['id'].replace(' ',''))
            if(len(txt['id']) != 13):
                txt['error'] += 'ID '

            final_data.append(txt)
            #print(txt)
        
        return final_data
        
    def __init__(self):
        ''' Run PanOCR '''
        self.initialize()

if __name__ == "__main__":
        extracter = PanOCR()
        tim = time.time()
        
        data=[]
        for filename in os.listdir('idcards'):
            print(filename)
            filename='idcards/'+filename
            result=extracter.find_and_classify(filename)
            #print(df1)
            #df=df.append(df1)
            if result==None:
                continue
            else:
                data.append(result)
        
        #------------------------------Text Preprocessing----------------------------------------#
        finish_data = extracter.text_preprocessing(data)
        
        #print((data))
        #finish_data=[]

        #print(finish_data)
        #------------------------------Transfer text to Data Frame-------------------------------#
        df = pd.DataFrame(finish_data)
        column_order = ['id', 'name_eng', 'surname_eng', 'title', 'name', 'surname_th', 'birthdate', 'religion', 'address', 'error' ]
        df = df.reindex(columns=column_order)
        
        #------------------------------Save file to csv------------------------------------------#
        df.to_csv (r'output/ocr_result_pan.csv', encoding='utf-8',index = None, header=True,sep='\t')
        
        en = time.time()
        print('TOTAL TIME TAKEN',str(en-tim))
