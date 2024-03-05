import pytesseract
import cv2
import imutils
import os
import numpy as np
import skimage.measure as measure
from mmdet.apis import init_detector, inference_detector
from pytesseract import Output

class ReceiptDetector:
	model = init_detector(os.path.dirname(__file__) + "/model.py", os.path.dirname(__file__) + "/epoch_110.pth", device="cpu")

	@classmethod
	def detect(cls, image):
		results = inference_detector(cls.model, image)
		mask = results.pred_instances.masks.cpu().numpy()[0]
		contour = cls._binary_mask_to_polygon(mask)
		rect = cls._get_bounding_rectangle(contour)
		warp = cls._perspective_transform(image, rect)
		pre_rotate_warp = cls._preprocess(warp)
		rotated_warp = cls._rotate(pre_rotate_warp)
		return rotated_warp
    
	@staticmethod
	def _binary_mask_to_polygon(mask):
		padded_mask = np.pad(mask, pad_width=1, mode="constant", constant_values=0)
		contours = measure.find_contours(padded_mask, 0.5)
		contours = np.subtract(contours, 1)
		for i, contour in enumerate(contours):
			for j, element in enumerate(contour):
				contours[i][j][0], contours[i][j][1] = element[1], element[0]
		return contours[0]

	@staticmethod
	def _get_bounding_rectangle(contour):
		min_x = np.min(contour[:, 0])
		min_y = np.min(contour[:, 1])
		max_x = np.max(contour[:, 0])
		max_y = np.max(contour[:, 1])
		rect = np.zeros((4, 2), dtype=np.float32)
		rect[0] = np.array([min_x, min_y])
		rect[1] = np.array([max_x, min_y])
		rect[2] = np.array([max_x, max_y])
		rect[3] = np.array([min_x, max_y])
		return rect

	@staticmethod
	def _perspective_transform(image, rect):
		(tl, tr, br, bl) = rect
		width_bottom = np.sqrt((br[0] - bl[0]) ** 2 + (br[1] - bl[1]) ** 2)
		width_top = np.sqrt((tr[0] - tl[0]) ** 2 + (tr[1] - tl[1]) ** 2)
		height_right = np.sqrt((tr[0] - br[0]) ** 2 + (tr[1] - br[1]) ** 2)
		height_left = np.sqrt((tl[0] - bl[0]) ** 2 + (tl[1] - bl[1]) ** 2)
		width = max(int(width_bottom), int(width_top))
		height = max(int(height_right), int(height_left))
		destination = np.array([
			[0, 0],
			[width - 1, 0],
			[width - 1, height - 1],
			[0, height - 1],
		], dtype=np.float32)
		transform_matrix = cv2.getPerspectiveTransform(rect, destination)
		warp = cv2.warpPerspective(image, transform_matrix, (width, height))
		return warp
	
	@staticmethod
	def _preprocess(image): 
		# 0/0 == 0 - ignore dividing 
		np.seterr(divide='ignore', invalid='ignore') 

		# 1. Create mask and inverted mask for colored areas
		blurred_img = cv2.blur(image, (5, 5))
		b, g, r = cv2.split(blurred_img) 
		intensity_arr = (np.fmin(np.fmin(b, g), r) / np.fmax(np.fmax(b, g), r)) * 255 
		_, inverted_mask = cv2.threshold(np.uint8(intensity_arr), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) 
		mask = cv2.bitwise_not(inverted_mask)  

		# 2. Local thresholding of grayscale image
		gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		text = cv2.ximgproc.niBlackThreshold(gray_img, 255, cv2.THRESH_BINARY, 41, -0.1, 
											binarizationMethod=cv2.ximgproc.BINARIZATION_NICK)

		# 3. Сreate background(text) and foreground(color markings)
		bg = cv2.bitwise_and(text, text, mask = inverted_mask)
		fg = cv2.cvtColor(cv2.bitwise_and(image, image, mask = mask), cv2.COLOR_BGR2GRAY) 
		out = cv2.add(bg, fg)
		
		return out
	
	@staticmethod
	def _rotate(receipt_image):
		results = pytesseract.image_to_osd(receipt_image, output_type=Output.DICT)
		rotated = imutils.rotate_bound(receipt_image, angle=results["rotate"])
		return rotated

















