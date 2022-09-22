from flask import Flask, request, jsonify
from flask_restful import Api,Resource

# from PIL import Image
# import pytesseract

import cv2
import pytesseract
from pytesseract import Output
from PIL import Image
import numpy as np

app = Flask(__name__)
api = Api(app)

# class WeatherCity(Resource):
#     def get(self):
#         pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
#         # img_path = r'test.jpg'
#         # img_path = r'test.jpeg'
#         img_path = r'id.jpg'
#         txtImg = Image.open(img_path)
#         text = pytesseract.image_to_string(txtImg, 'eng+tha').replace(' ','')
#         return text



@app.route("/im_size", methods=["POST"])
def process_image():
    file = request.files['image']
    # Read the image via file.stream

    # img = Image.open(file.stream)
    imgCv = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    
    img_gray = cv2.cvtColor(imgCv, cv2.COLOR_BGR2GRAY)
    img_thresholding = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    custom_config = r'-l tha+eng --dpi 400 --oem 1'
    # custom_config = r'-l tha+eng --dpi 400 --oem 1 -clanguage_model_ngram_space_delimited_language=1'


    # data = pytesseract.image_to_data(img_thresholding,config=custom_config, output_type=Output.DICT)
    # totalBox = len(data['text'])
    # for i in range(totalBox):
    #     (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
    #     img = cv2.rectangle(img_thresholding, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # cv2.imshow('img', img)
    # cv2.waitKey(0)


    text = pytesseract.image_to_string(img_thresholding, config=custom_config)
    return text

class WeatherCity(Resource):
    def get(self):
        # img_path = r'test.jpeg'
        img_path = r'test.jpg'
        # img_path = r'id.jpg'
        img = cv2.imread(img_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_thresholding = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        custom_config = r'-l tha+eng --dpi 400 --oem 1 -c language_model_ngram_space_delimited_language=1'

        text = pytesseract.image_to_string(img_thresholding, config=custom_config)

        # data = pytesseract.image_to_data(img_thresholding,config=custom_config, output_type=Output.DICT)
        # keys = list(data.keys())
        # totalBox = len(data['text'])
        # for i in range(totalBox):
        #     (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        #     img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # cv2.imshow('img', img_thresholding)
        # cv2.waitKey(0)

        # print(''.join(data['text']))



        return text

api.add_resource(WeatherCity,"/cardid")

if __name__ == "__main__":
    app.run(debug=True)