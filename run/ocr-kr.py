# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:28:58 2018

@author: LENOVO
"""
import numpy as np
import requests
import json
import os
import PIL



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


def read_text(filename):
    text_json = ocr_space_file(filename)
    text = json.loads(text_json)
    text = text['ParsedResults'][0].get('ParsedText')
    return text


def preprocess_image(filename):
    image = PIL.Image.open(filename)
    w,h=image.size
    image= image.resize((int((400*w)/100),int((400*h)/100)))
    image=image.convert('L')
    filename = filename.split('.')[0]+'_grey.jpeg'
    
    image.save(filename)
    return filename


def save_file(filename_open):
    filename_saved = filename_open.split('.')[0] + '.txt'
    with open(filename_saved, mode = 'a') as f:
        filename_open = preprocess_image(filename_open)
        text = read_text(filename_open)
        os.remove(filename_open)
        f.write(text)        

items = os.listdir()
for item in items:
    try:
        name = item.split('.')[1]
        if name == 'png' or name == 'jpeg' or name == 'jpg' or name == 'tiff' or name == 'PNG' or name == 'JPEG' or name == 'JPG' or name == 'TIFF':
            save_file(item)
    except:
        print('error' + item)