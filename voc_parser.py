import xml.etree.ElementTree as ET
import os

classes = []

def convert_annotation(file_path, training_file):
    in_file = open(file_path)
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        cls = obj.find('name').text

        if cls not in classes:
            classes.append(cls)

        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        training_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

annotation_files = []
image_files = []

for file in os.listdir('data/annotations'):
    annotation_files.append(file)

for file in os.listdir('data/images'):
    image_files.append(file)

print(f'Detected: {len(annotation_files)} annotation files')
print(f'Detected: {len(image_files)} image files')

training_file = open('training_file.txt', 'w')

missed_annotations = 0
success_annotations = 0

for image_file in image_files:
    file_name = image_file.split('.')[0]
    annotation_file = f'{file_name}.xml'

    if annotation_file in annotation_files:
        training_file.write(f'data/images/{image_file}')
        convert_annotation(f'data/annotations/{annotation_file}', training_file)    
        training_file.write('\n')
        success_annotations += 1
    else:
        missed_annotations += 1
print()
print(f'Finished processing {success_annotations} files\n\
A total of {missed_annotations} annotation files were missing and were skipped\n\n\
The following classes were added to detection:')
for cls in classes:
    print(f'- {cls}')
training_file.close()
