import cv2
import os
import numpy as np


show = True
FEASIBLE_AREA_MIN = 1000
FEASIBLE_AREA_MAX = 100000
original_image_folder = r'D:\DT-cat-image-for-ROI'

labels = ["F58001104805002120001","F58001104805003210004","F58001104805003240003",
		  "F58001104821701010008","F58001104827202120004","F58001104949503200002"]

imgs = [os.path.join(original_image_folder,img) for img in os.listdir(original_image_folder)]


for image in imgs:
	if r'_0.png' in image:
		padding=list()
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
		H,W,_=img.shape
		for h in range(H):
			for w in range(W):
				if (cv2.pointPolygonTest(contours,(w,h),False)) == -1:
					padding.append((h,w))

		for image_name in [image.replace(r'_0.png',r'_%d.png'%i) for i in range(1,21)]:
			color_img = cv2.imread(image_name)
			for p in padding:
				color_img[p[0]][p[1]] = [0,0,0]

			cv2.imwrite(image_name,color_img)



