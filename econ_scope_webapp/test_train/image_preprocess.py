import sys
import cv2
import numpy as np


def preprocess(img): 
    np.seterr(divide='ignore', invalid='ignore') # 0/0 == 0 - ignore dividing 

    # 1. Create mask and inverted mask for colored areas
    blurred_img = cv2.blur(img,(5,5))
    b,g,r = cv2.split(blurred_img) 
    intensity_arr = (np.fmin(np.fmin(b, g), r) / np.fmax(np.fmax(b, g), r)) * 255 
    _, inverted_mask = cv2.threshold(np.uint8(intensity_arr), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) 
    mask = cv2.bitwise_not(inverted_mask)  

    # 2. Local thresholding of grayscale image
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = cv2.ximgproc.niBlackThreshold(gray_img, 255, cv2.THRESH_BINARY, 41, -0.1, 
                                         binarizationMethod=cv2.ximgproc.BINARIZATION_NICK)

    # 3. Сreate background(text) and foreground(color markings)
    bg = cv2.bitwise_and(text, text, mask = inverted_mask)
    fg = cv2.cvtColor(cv2.bitwise_and(img, img, mask = mask), cv2.COLOR_BGR2GRAY) 
    out = cv2.add(bg, fg)
    
    return out 
