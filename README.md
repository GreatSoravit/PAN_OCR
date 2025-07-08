![OCR](OCR.png?raw=true "Title")

# PAN_OCR (custom for Thai National ID Card)
This program reproduce from pan_ocr by Karan Purohit which I modify and adjust to use with Thai Natioanl ID Card.

To understand the building process please read his blog [here.](https://medium.com/saarthi-ai/how-to-build-your-own-ocr-a5bb91b622ba)

The program structure use Darknet to identify specific text section of ID card, then cropped those sections while pass to Tesseract as the ocr engine to extract text in Thai and English language before save to csv file for further use.

As labeling images for train data, I use [VoTT](https://github.com/microsoft/VoTT) to label each section of image, then generate as yolo anchors boxes format to use when training.

<img src="https://github.com/GreatSoravit/PAN_OCR/blob/master/1_VoTT_blur.png" width=75% height=75%>

Darknet use yolov4 model object detection with custom weight which obtain by train model with ID card data label with pre-train weight to recognize specific section.
The train data use total 69 images with transformation library [Albumentations](https://github.com/albumentations-team/albumentations) to produce transform images to increase training size from original 23 images.



[Tesseract](https://github.com/tesseract-ocr/tesseract) and [Pytesseract](https://github.com/madmaze/pytesseract) required to install to run this OCR.

The object detection with anchor boxes with label name for specific area.

<img src="https://github.com/GreatSoravit/PAN_OCR/blob/master/4_predictions_blur.jpg" width=75% height=75%>

The cropped images will generate in cropimgs folder as below.

<img src="https://github.com/GreatSoravit/PAN_OCR/blob/master/2_Crop.png" width=50% height=50%>

The result will generate in output folder as csv file.

<img src="https://github.com/GreatSoravit/PAN_OCR/blob/master/3_Result_blur.png" width=75% height=75%>

# Main components and Command
- darknet.exe
- data folder for darknet
- yolo custom file weight that obtained from train data by darknet
- Tesseract.exe and it component such as eng.traineddata and tha.traineddata
- idcards folder to contain target Thai National ID Card for text extraction
- cropimgs folder to contain list of crop images generate by program
- output folder to contain output csv file

To run the OCR follow this command.

``` pan.py -d -t ```

# Limitation
- The output file has a last column that annotate some column name is not in the right format which may cause by object detection not fully detect text area. 
- The train data size for detect text area is small which affect model not able to fully detect text section in some case. The model for area detection could be improved by increasing training size with high quality and various images.
- While the misspelled in text extraction not fully accurate may not be annotated by any algorithm as it occur by model unable to detect text correctly.
- The tesseract may not able to extract text accurately due to some image conditions such as low quality, glare or reflection, and wrong angle of card layout. Also, the tesseract model might not completely recognize thai text. If the image of ID card took properly it could help in text recognition while the tesseract model could be improved accuracy by training model with specific thai font data.
