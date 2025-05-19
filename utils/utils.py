import os
import shutil
from pathlib import Path
import yaml

def move_files(image_folder, annotation_folder, output_dir, image_list, split):

    for img in image_list:

        image_path = os.path.join(image_folder, img)
        annotation_path = os.path.join(annotation_folder, img.replace('.png', '.txt'))


        # move images
        shutil.move(image_path, os.path.join(output_dir, 'images',split, img))
        shutil.move(annotation_path, os.path.join(output_dir, 'annotations', split, img.replace('.png','.txt')))

def convert_bbox(size, box):
    x_min, y_min, x_max, y_max = box
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]

    x = (x_min + x_max) / 2.0 * dw
    y = (y_min + y_max) / 2.0 * dh
    w = (x_max - x_min) * dw
    h = (y_max - y_min) * dh

    return x, y, w, h

def read_yaml(path_to_yamnl: Path):

    try:
        with open(path_to_yamnl, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            return content
    except FileNotFoundError as e:
            raise e
    
if __name__ == '__main__':
     
     print(read_yaml('./params.yaml'))
