import cv2
import pytesseract
from ultralytics import YOLO

model = YOLO('model/best.pt')

def detect_plate_text(image_path):

    results = model(image_path)[0]
    for box in results.boxes:

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        plate_crop = cv2.imread(image_path)[y1:y2, x1:x2]

        if plate_crop.size == 0:
            continue

        text = pytesseract.image_to_string(plate_crop, config='--psm 7')
        cleaned = ''.join(filter(str.isalnum, text))
        if cleaned:
            return cleaned.upper()
        
    return None