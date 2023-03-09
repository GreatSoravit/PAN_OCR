from abc import ABC, abstractmethod
from typing import List
import threading

class OCR(ABC):
    @abstractmethod
    def initialize(self):
        ''' Initialize the OCR '''
        pass

    @abstractmethod
    def ocr_one_image(self, images:List) -> List:
        ''' OCR an image.
        Input: An array of (area, image)s, opened by PIL and pre-processed
        Return: An array of (area, message), where the message is from OCR'''
        pass

    def ocr(self, images:List, nameplate:List) -> List:
        '''Sends an opened image to Azure's cognitive services.
        Input: images (tuple(area, image))
        Returns the results from Tesseract.'''
        threads = []
        threadResults = ["" for i in range(len(images))]
        threadNum = 0
        results = []
        for idx, image in enumerate(images):
            #t = threading.Thread(target=self.ocr_one_image, args=(image[0], image[1]), kwargs={'threadList':threadResults, 'threadNum':threadNum})
            if(nameplate[idx]=='address' or nameplate[idx]=='name' or nameplate[idx]=='religion'):
                t = threading.Thread(target=self.ocr_one_image, args=(image[0], image[1], 'tha'), kwargs={'threadList':threadResults, 'threadNum':threadNum})
                #results.append(self.ocr_one_image(image[0], image[1], 'tha'))
            else:
                t = threading.Thread(target=self.ocr_one_image, args=(image[0], image[1], 'eng'), kwargs={'threadList':threadResults, 'threadNum':threadNum})
                #results.append(self.ocr_one_image(image[0], image[1], 'eng'))
            t.start()
            threads.append(t)
            threadNum += 1
            
        for t in threads:
            t.join()

        for i, result in enumerate(threadResults):
            results.append((images[i][0], result))
        return results

    def __init__(self):
        self.initialize()
