![OCR](OCR.png?raw=true "Title")

# PAN_OCR (custom for Thai National ID Card)
This program reproduce from pan_ocr by Karan Purohit by modify and adjust to use with Thai Natioanl ID Card.
To understand the building process please read his blog [here.](https://medium.com/saarthi-ai/how-to-build-your-own-ocr-a5bb91b622ba)

The program structure use Darknet to identify specific text section of ID card, then cropped those sections while pass to Tesseract as the ocr engine to extract text in Thai and English language before save to csv file for further use.

Darknet use yolov4 model object detection with custom weight which obtain by train model with ID card data label with pre-train weight to recognize specific section.
The train data use total 69 images with transformation library [Albumentations](https://github.com/albumentations-team/albumentations) to produce transform images to increase training size from original 23 images.

As for labeling images for train data, I use [VoTT](https://github.com/microsoft/VoTT) to label each section of image, then generate as yolo anchors boxes format to use when train with Darknet.

[VoTT](1_VoTT.png)

[Tesseract](https://github.com/tesseract-ocr/tesseract) and [Pytesseract](https://github.com/madmaze/pytesseract) required to install to run this OCR.

The main folder consist of
- darknet.exe
- data folder for darknet
- yolo custom file weight that obtained from train data by darknet
- Tesseract.exe and it component such as eng.traineddata and tha.traineddata
- idcards folder to contain target Thai National ID Card
- cropimgs folder to contain list of crop images generate by program
- output folder to contain output csv file

To run the OCR follow this command.

``` pan.py -d -t ```

The cropped images will generate in cropimgs folder as below.

[Crop](2_Crop.png)

The result will generate in output folder as csv file.

[Result](3_Result.png)
