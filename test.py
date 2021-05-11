from google.cloud import vision
from google.cloud import translate_v3beta1 as translate
from google.oauth2 import service_account
import io, os
import cv2
import matplotlib.pyplot as plt


image_base_path = 'images'
#image_path = os.path.join(image_base_path, 'image_test.png')
#image_path = os.path.join(image_base_path, 'manga001.jpg')
#image_path = os.path.join(image_base_path, 'chinito.png')
image_path = os.path.join(image_base_path, 'totemo.PNG')


def pic_to_text(image_path):

    with io.open(image_path, 'rb') as image_file :
        image = image_file.read()

    image = vision.Image(content=image)
    credentials = service_account.Credentials.from_service_account_file('SM-2021-4a699763da54.json')
    #108303079256104612485
    client = vision.ImageAnnotatorClient(credentials = credentials)

    response = client.text_detection(image=image)

    #texts = response.text_annotations

    texts = response.full_text_annotation.text

    return response.full_text_annotation

def draw_rectangle(img, bbox):

    cv2.rectangle(img,bbox[0],bbox[1],(255,0,0),3)

    return img

def text_translate(text, locale = 'ja'):

    if locale is None:
        locale = 'ja'
    
    credentials = service_account.Credentials.from_service_account_file('SM-2021-4a699763da54.json')
    client = translate.TranslationServiceClient(credentials = credentials)

    # Designates the data center location that you want to use
    location = "us-central1"

    # Set glossary resource name
    name = client.glossary_path(project_id, location, glossary_name)

    # Set language codes
    language_codes_set = translate.Glossary.LanguageCodesSet(
        language_codes=languages
    )

    gcs_source = translate.GcsSource(input_uri=glossary_uri)

    input_config = translate.GlossaryInputConfig(gcs_source=gcs_source)

    # Set glossary resource information
    glossary = translate.Glossary(
        name=name, language_codes_set=language_codes_set, input_config=input_config
    )    


text = pic_to_text(image_path)

#print(text)

print(type(text.pages))

bounds = []
bounds = []
for page in text.pages:
    
    for block in page.blocks:
        b = []
        """
        for paragraph in block.paragraphs:
            for word in paragraph.words:
                for symbol in word.symbols:
                    
        """

        for verti in block.bounding_box.vertices:

            b.append((verti.x, verti.y))

        bounds.append(b)
        #print(block.bounding_box)


#print(text.pages.blocks)
print(bounds)

image = cv2.imread(image_path)
image_rect = image
for b in bounds:
    image_rect = draw_rectangle(image_rect, [b[0], b[2]])


cv2.imwrite('test.png', image_rect)


