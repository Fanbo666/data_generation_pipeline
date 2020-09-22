import cv2
import os
import numpy as np


show = True
FEASIBLE_AREA_MIN = 1000
FEASIBLE_AREA_MAX = 100000
original_image_folder = r'D:\DT-CAT-IMAGE\syn_vs_real\0'

labels = ["F58001104805002120001","F58001104805003210004","F58001104805003240003",
		  "F58001104821701010008","F58001104827202120004","F58001104949503200002"]

imgs = [os.path.join(original_image_folder,img) for img in os.listdir(original_image_folder)]


for image in imgs:
	padding = list()
	img = cv2.imread(image)
	bin_img = cv2.Canny(img, threshold1=0, threshold2=255)
	_, contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	contours = [con for con in contours if FEASIBLE_AREA_MAX > cv2.contourArea(con) > FEASIBLE_AREA_MIN]

	if len(contours) > 0:
		contours = contours[0]
	else:
		continue
	#
	# if show:
	# 	img_con = cv2.drawContours(img, contours, 3, 255)
	# 	cv2.imshow('ss', img_con)
	# 	cv2.waitKey(0)

	contours = np.array(contours)
	H, W, _ = img.shape
	for h in range(H):
		for w in range(W):
			if (cv2.pointPolygonTest(contours, (w, h), False)) == -1:
				img[h][w] = [0,0,0]
	cv2.imwrite(image,img)
	# cv2.imshow('test',img)
	# cv2.waitKey(0)

