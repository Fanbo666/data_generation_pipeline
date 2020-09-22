import json
import cv2
import numpy as np

with open(r'D:\DT-cat\image\F58001104827202120004_[0, 90, 9].json','r') as f:
    settings=json.load(f)

points=settings['shapes'][0]['points']

img=cv2.imread(r'D:\DT-cat\image\F58001104827202120004_[0, 90, 9]_10.png')
img_array=np.array(img)
for point in points:
    img_array[point[1]][point[0]]=[255,255,255]

cv2.imshow('img',img_array)
cv2.waitKey(0)
