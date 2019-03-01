from yolo import YOLO
from PIL import Image
import json

if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    configuration = config['model']

    yolo = YOLO(**configuration)
    while True:
        img = input('Input image filename:')
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(image)
            r_image.show()
    yolo.close_session()
