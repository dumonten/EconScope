import cv2
import argparse
import os
from seg_service import ReceiptDetector
from rec_service import TextRecognizer
from gpt_service import Gpt

def load_image(image_path):
    """
    Function to load an image from a given path.

    Parameters:
    - image_path (str): Path to the image file.

    Returns:
    - image (numpy.ndarray): The loaded image as a numpy array.
    """
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not load the image at {image_path}")
        return None

    return image

def main():
    """
    Main function to execute the script.

    This function parses command-line arguments, loads an image, processes it through receipt detection, text recognition, and analysis,
    and prints the analysis result.
    """
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
