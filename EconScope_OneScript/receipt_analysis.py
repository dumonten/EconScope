import cv2
import argparse
import os
from seg_service import ReceiptDetector
from rec_service import TextRecognizer
from gpt_service import Gpt
import json

def load_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not load the image at {image_path}")
        return None

    return image

def main():
    parser = argparse.ArgumentParser(description='Load an image into a cv2 numpy array.')
    parser.add_argument('-i', '--image', type=str, help='Path to the image file')

    args = parser.parse_args()

    if args.image:
        image_path = args.image
    else:
        default_dir = 'example_images'
        default_image = '1.jpg'
        image_path = os.path.join(default_dir, default_image)

    image = load_image(image_path)

    if image is not None:
        image = ReceiptDetector.detect(image)
        text = TextRecognizer.get_text(image)
        analysis = Gpt.receipt_ask(text)
        print(analysis)

if __name__ == "__main__":
    main()
