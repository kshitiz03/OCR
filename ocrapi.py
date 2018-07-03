# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 13:31:28 2018

@author: LENOVO
"""
from PIL import Image
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pdf2image import convert_from_path
#from keras.preprocessing import image
import cv2


import PyPDF2
from wand.image import Image
import io
import os


def pdf_page_to_png(src_pdf, resolution = 72,):
    """
    Returns specified PDF page as wand.image.Image png.
    :param PyPDF2.PdfFileReader src_pdf: PDF from which to take pages.
    :param int pagenum: Page number to take.
    :param int resolution: Resolution for resulting png in DPI.
    """
    pagenum=0
    dst_pdf = PyPDF2.PdfFileWriter()
    dst_pdf.addPage(src_pdf.getPage(pagenum))

    pdf_bytes = io.BytesIO()
    dst_pdf.write(pdf_bytes)
    pdf_bytes.seek(0)

    img = Image(file = pdf_bytes, resolution = resolution)
    img.convert("png")

    return img


def ocr_space_file(filename, overlay=False, api_key='0c265702be88957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()

src_filename = "Hackathon4.0Certificate.pdf"

src_pdf = PyPDF2.PdfFileReader(open(src_filename, "rb"))
img = pdf_page_to_png(src_pdf,resolution = 300)
    

img = img.convert('LA')
#img = Image.open('hd-min.jpg').convert('LA')

img.save('greyscale1.png')
'''
img=img.resize((2000,1000),Image.ANTIALIAS)
img.save('hdd.png',quality=80,optimize=True)
#img = image_resize(img, height = 800)'''
test_file = ocr_space_file(filename='greyscale1.png', language='eng')
back_json=json.loads(test_file)

text= back_json.get('ParsedResults')[0].get('ParsedText')
f=open('out1.txt','w')
f.write(text)
f.close()

print(text)
#test_url = ocr_space_url(url='20180702_132002.jpg')