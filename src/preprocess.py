import os
import cv2

class Preprocess:

    def __init__(self, input_folder, output_folder):
        
        self.input_folder = input_folder
        self.output_folder = output_folder

    def process_images(self):

        os.makedir(self.output_folder, exist_ok=True)

        for img_name in os.listdir(self.input_folder):
            
            img_path = os.path.join(self.input_folder, img_name)
            image = cv2.imread(img_path)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
            output_path = os.path.join(self.output_folder, img_name)
            cv2.imwrite(output_path, blurred)

if __name__ == '__main__':

    process = Preprocess('./dataset/images/','./dataset/processed_images/')
    process.process_images()