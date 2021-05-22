from google.cloud import vision
from google.cloud import translate_v3 as translate
from google.oauth2 import service_account
import io, os
import textwrap as tr
from PIL import ImageFont, ImageDraw, Image



image_base_path = 'images'
#image_path = os.path.join(image_base_path, 'image_test.png')
#image_path = os.path.join(image_base_path, 'error.PNG')
#image_path = os.path.join(image_base_path, '.PNG')
#image_path = os.path.join(image_base_path, 'tonarynojp.png')
#image_path = os.path.join(image_base_path, 'totemo.PNG')
#image_path = os.path.join(image_base_path, 'medic.PNG')
#image_path = os.path.join(image_base_path, 'pointing.PNG')
#image_path = os.path.join(image_base_path, 'notebookMiniLeft.PNG')
#image_path = os.path.join(image_base_path, 'notebookMini.PNG')
#<<image_path = os.path.join(image_base_path, 'fashion.PNG')
#image_path = os.path.join(image_base_path, 'chaseTag.PNG')
#image_path = os.path.join(image_base_path, 'chaseTag2.PNG')
#image_path = os.path.join(image_base_path, 'soldat.PNG')
#image_path = os.path.join(image_base_path, 'chino.PNG')
#image_path = os.path.join(image_base_path, 'coreano.PNG')
image_path = os.path.join(image_base_path, 'ingles.PNG')




def pic_to_text(image_path):

    with io.open(image_path, 'rb') as image_file :
        image = image_file.read()

    image = vision.Image(content=image)
    credentials = service_account.Credentials.from_service_account_file('SM-2021-4a699763da54.json')
    #108303079256104612485
    client = vision.ImageAnnotatorClient(credentials = credentials)

    response = client.text_detection(image=image)

    texts = response.text_annotations

    #texts = response.full_text_annotation.text

    return texts



def drawRect(img, topLeftCoord, bottomRigthCoord, color=(255,255,255)):
    
    img.rectangle([topLeftCoord, bottomRigthCoord],fill=color)

    return img

def rewriteText(img, topLeftCoord, bottomRigthCoord, text, color=(255,255,255)):
    
    img.rectangle([topLeftCoord, bottomRigthCoord],fill=color)
  

    rectWidth = bottomRigthCoord[0]-topLeftCoord[0]
    #print("rectWidth: ", rectWidth)
    rectHeight = bottomRigthCoord[1]-topLeftCoord[1]

    area = rectWidth * rectHeight
    l = len(text)


    exit = False
    fontSize = 1
    letterWidth = 0
    letterHeight = 0
    while not exit:
        font = ImageFont.truetype(font='fonts/courierPrime.ttf', size=fontSize)

        textWidth, textHeight = img.textsize(text, font=font)
        letterWidth, letterHeight = img.textsize('a', font=font)

        lArea = letterHeight * letterWidth
        tArea = lArea * l * 2
        if tArea < area:
            fontSize = fontSize + 1
        else:
            font = ImageFont.truetype(font='fonts/courierPrime.ttf', size=fontSize - 1)
            exit = True
    #print("real Widht: ", textWidth)
    #print("real letter Widht: ", letterWidth)

    wrapped_text = tr.wrap(text, width=int(rectWidth/letterWidth), break_long_words=True)
    
    print(wrapped_text)
    wi = 0
    for el in wrapped_text:
        wid,he = img.textsize(text = el, font = font)
        if wid > wi:
            wi = wid
    
    blankspace = (rectWidth - wi)

    for i, line in enumerate(wrapped_text):
        textY = int(topLeftCoord[1] + i * fontSize)
        textX = int(topLeftCoord[0] + blankspace)
        print('i: ', i , ', textX: ', textX, ', textY: ', textY)
        img.text((textX,textY), line, fill=(0,0,0),  font=font)

    return img

def translate_text2(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    credentials = service_account.Credentials.from_service_account_file('SM-2021-4a699763da54.json')
    translate_client = translate.Client(credentials = credentials)

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result["translatedText"]

text = pic_to_text(image_path)

#print(text)

bounds = []


    
for block in text:
    b = []
    

    #print(block)
    for verti in block.bounding_poly.vertices:

        b.append((verti.x, verti.y))

    #bounds.append(b)
    bounds.append({"text" : block.description, "bounds" : b})

    #print(block.bounding_box)

rectBounds = {'topLeft': bounds[0]['bounds'][0], 'bottomRight': bounds[0]['bounds'][2]} 
#print(text.pages.blocks)
print(bounds)

#image = cv2.imread(image_path)
#image_rect = image
image = Image.open(image_path)
image_rect = ImageDraw.Draw(image)

"""
for b in bounds:
    image_rect = draw_rectangle(image_rect, [b["bounds"][0], b["bounds"][2]], b["text"])
"""

#image_rect = draw_rectangle(image_rect, [ bounds[0]['bounds'][0] ,  bounds[0]['bounds'][2] ],  translate_text2('es', bounds[0]['text']) ,  color=(255,255,255))


image_rect = rewriteText(image_rect,  rectBounds['topLeft'] ,  rectBounds['bottomRight'] , translate_text2('es', bounds[0]['text']))
#image_rect = drawRect(image_rect,  rectBounds['topLeft'] ,  rectBounds['bottomRight'] )


#cv2.imwrite('test.png', image_rect)
image.save('test.png')


