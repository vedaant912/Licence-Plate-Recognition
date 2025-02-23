import os
import shutil

def move_files(image_folder, annotation_folder, output_dir, image_list, split):

    for img in image_list:

        image_path = os.path.join(image_folder, img)
        annotation_path = os.path.join(annotation_folder, img.replace('.png', '.txt'))


        # move images
        shutil.move(image_path, os.path.join(output_dir, 'images',split, img))
        shutil.move(annotation_path, os.path.join(output_dir, 'annotations', split, img.replace('.png','.txt')))