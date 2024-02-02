import numpy as np
import skimage.measure as measure
import cv2
import base64
import json
import pickle
from mmdet.apis import init_detector, inference_detector


def im2json(mes):
    return json.dumps({"uuid": mes["uuid"], "image": mes["image"].decode("latin-1")}).encode("latin-1")


def json2im(mes):
    load = json.loads(mes.decode("latin-1"))
    return {"uuid": load["uuid"], "image": load["image"].encode("latin-1")}
  

def close_contour(contour):
  if not np.array_equal(contour[0], contour[-1]):
    contour = np.vstack((contour, contour[0]))
  return contour


def binary_mask_to_polygon(binary_mask, tolerance=0):
  padded_binary_mask = np.pad(binary_mask, pad_width=1, mode='constant', constant_values=0)
  contours = measure.find_contours(padded_binary_mask, 0.5)
  contours = np.subtract(contours, 1)
  for i, contour in enumerate(contours):
      for j, element in enumerate(contour):
        contours[i][j][0], contours[i][j][1] = element[1], element[0]

  return contours

model = init_detector("model.py", "epoch_110.pth", device="cpu")

def crop_image(image):
	results = inference_detector(model, image)

	mask = results.pred_instances.masks.cpu().numpy()[0]
	c = binary_mask_to_polygon(mask)

	rect = np.zeros((4, 2), dtype = "float32")
	c = c[0]
	min_x = np.min(c[:, 0])
	min_y = np.min(c[:, 1])
	max_x = np.max(c[:, 0])
	max_y = np.max(c[:, 1])


	rect[0] = np.array([min_x, min_y])
	rect[1] = np.array([max_x, min_y])
	rect[2] = np.array([max_x, max_y])
	rect[3] = np.array([min_x, max_y])

	(tl, tr, br, bl) = rect
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

	maxWidth = max(int(widthA), int(widthB))
	maxHeight = max(int(heightA), int(heightB))

	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")

	M = cv2.getPerspectiveTransform(rect, dst)
	warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

	return warp
