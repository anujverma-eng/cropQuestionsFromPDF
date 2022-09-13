import fitz,re
from PIL import Image
import cv2
import numpy as np

doc = fitz.open('Final  formate.pdf')
page = doc.load_page(0)
page.get_pixmap().save('pageImage.png')

#img = Image.open('pageImage.png')
img = cv2.imread('pageImage.png')
x,y,w,h = cv2.selectROI(img)
print(x,y,w,h)

mat = fitz.Matrix(10,10)
page.get_pixmap(clip=(x,y,x+w,y+h),matrix= mat).save('roi1.png')