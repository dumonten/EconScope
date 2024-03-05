import cv2
from paddleocr import PaddleOCR
from image_preprocess import preprocess

parent_path = "/home/dumonten/Documents/GitHub/EconScope/econ_scope_webapp/test_train"
img_path = parent_path + '/image.jpg'

ocr = PaddleOCR(show_log=False, use_angle_cls = True, use_space_char = True, lang="ru",
                det_model_dir=parent_path + "/detection_model",
                rec_model_dir=parent_path + "/recognition_model",
                cls_model_dir=parent_path + "/cls_model",
                rec_char_dict_path=parent_path + "/PaddleOCR/ppocr/utils/dict/cyrillic_dict.txt",
                use_gpu=True)

img = cv2.imread(img_path)
print(img.shape) 
result = ocr.ocr(img, cls=True)
result = list(map(lambda x: x[1][0], result))
result = ' '.join(map(str, result))

print(result)
