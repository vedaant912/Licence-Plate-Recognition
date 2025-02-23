import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to 
# the sys.path.
sys.path.append(parent)


import os
import cv2
from tqdm import tqdm
import xml.etree.ElementTree as ET
import random
from utils.utils import move_files
import shutil


class Preprocess:

    def __init__(self, input_folder, output_folder):
        
        self.input_folder = input_folder
        self.output_folder = output_folder

    def process_images(self):

        os.makedirs(self.output_folder, exist_ok=True)

        for img_name in os.listdir(self.input_folder):
            
            img_path = os.path.join(self.input_folder, img_name)
            image = cv2.imread(img_path)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
            output_path = os.path.join(self.output_folder, img_name)
            cv2.imwrite(output_path, blurred)

    def convert_bbox(self, size, box):

        x_min, y_min, x_max, y_max = box
        dw = 1.0 / size[0]
        dh = 1.0 / size[1]

        x = (x_min + x_max) / 2.0 * dw
        y = (y_min + y_max) / 2.0 * dh
        w = (x_max - x_min) * dw
        h = (y_max - y_min) * dh

        return x, y, w, h

    def xml_to_yolo_format(self, xml_folder, output_folder):

        os.makedirs(output_folder, exist_ok=True)

        class_mapping = {'licence': 0}

        for xml_file in tqdm(os.listdir(xml_folder)):
            
            if not xml_file.endswith('.xml'):
                continue

            tree = ET.parse(os.path.join(xml_folder, xml_file))
            root = tree.getroot()

            image_name = root.find('filename').text.replace('.png', '')
            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)

            yolo_annotations = []
            for obj in root.findall('object'):
                cls = obj.find('name').text
                if cls not in class_mapping:
                    continue

                cls_id = class_mapping[cls]
                bbox = obj.find('bndbox')
                x_min = int(bbox.find('xmin').text)
                y_min = int(bbox.find('ymin').text)
                x_max = int(bbox.find('xmax').text)
                y_max = int(bbox.find('ymax').text)

                x, y, w, h = self.convert_bbox((width, height), (x_min, y_min, x_max, y_max))
                yolo_annotations.append(f"{cls_id} {x: .6f} {y: .6f} {w: .6f} {h: .6f}")

            with open(os.path.join(output_folder, f"{image_name}.txt"), "w") as f:
                f.write('\n'.join(yolo_annotations))

    def split_dataset(self):

        image_folder = 'dataset/processed_images/'
        annotation_folder = 'dataset/yolo_annotations/'
        output_dir = 'dataset/inputs/'
        splits = ['train','valid']

        if os.listdir(os.path.join(output_dir, 'images')):
            print('Training Data Already Exists!!!')
        else:
            train_ratio = 0.8

            for split in splits:
                os.makedirs(os.path.join(output_dir, "images", split), exist_ok=True)
                os.makedirs(os.path.join(output_dir, "annotations", split), exist_ok=True)

            # Get all image files
            images = [f for f in os.listdir(image_folder) if f.endswith(".png")]
            random.shuffle(images)

            # Split into train and validation sets
            split_index = int(len(images) * train_ratio)
            train_images = images[:split_index]
            valid_images = images[split_index:]


            move_files(image_folder, annotation_folder, output_dir, train_images, splits[0])
            move_files(image_folder, annotation_folder, output_dir, valid_images, splits[1])

        shutil.rmtree(image_folder)
        shutil.rmtree(annotation_folder)
        

if __name__ == '__main__':

    process = Preprocess('./dataset/images/','./dataset/processed_images/')
    process.process_images()
    process.xml_to_yolo_format('./dataset/annotations/','./dataset/yolo_annotations/')
    process.split_dataset()