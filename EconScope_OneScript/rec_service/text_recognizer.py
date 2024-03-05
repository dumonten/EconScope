import os
from paddleocr import PaddleOCR

class TextRecognizer(): 
    DET_DIR_NAME = "detection_model"
    REC_DIR_NAME = "recognition_model"
    CLS_DIR_NAME = "cls_model"
    REC_CHAR_DICT_PATH = "PaddleOCR/ppocr/utils/dict/cyrillic_dict.txt"

    current_directory = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_directory)

    model = PaddleOCR(show_log=False, use_angle_cls = True, use_space_char = True, lang="ru",  
                det_model_dir=parent_path + "/" + DET_DIR_NAME, 
                rec_model_dir=parent_path + "/" + REC_DIR_NAME, 
                cls_model_dir=parent_path + "/" + CLS_DIR_NAME,
                rec_char_dict_path=parent_path + "/" + REC_CHAR_DICT_PATH, 
                use_gpu=True) 

    @classmethod
    def get_text(cls, img): 
        text = cls.model(img, cls=True)
        text = list(map(lambda x: x[1][0], text))
        text = ' '.join(map(str, text))
        return text 
