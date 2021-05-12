from google.cloud import vision
from google.cloud import translate_v3beta1 as translate
from google.oauth2 import service_account
import io, os

image_base_path = 'images'
#image_path = os.path.join(image_base_path, 'image_test.png')
<<<<<<< HEAD
#image_path = os.path.join(image_base_path, 'manga001.jpg')
image_path = os.path.join(image_base_path, 'totemo.PNG')
=======
#image_path = os.path.join(image_base_path, 'manga001.jpg') #'merchant.PNG'

import sys

#print 'Number of arguments:', len(sys.argv), 'arguments.'


image_path = os.path.join(image_base_path, str(sys.argv[1]))
>>>>>>> 32dfd9091504a532c1121fc64abb96e84b3be34c


def pic_to_text(image_path):

    with io.open(image_path, 'rb') as image_file :
        image = image_file.read()

    image = vision.Image(content=image)
    credentials = service_account.Credentials.from_service_account_file('SM-2021-4a699763da54.json')
    #108303079256104612485
    client = vision.ImageAnnotatorClient(credentials = credentials)

    response = client.text_detection(image=image)

    #texts = response.text_annotations

    texts = response.full_text_annotation

    print(response)
    return texts





print(pic_to_text(image_path))
