import cv2
import numpy as np
import pytesseract

def preprocess_image(image):
    image =  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1,1), dtype = "uint8")
    image = cv2.erode(image, kernel, iterations = 1)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    image = cv2.medianBlur(image, 3)
    return image

def read_receipt_from_image(path):
    img = cv2.imread(path)
    img = preprocess_image(img)
    text = pytesseract.image_to_string(img)
    return text
