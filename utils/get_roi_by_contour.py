import argparse
import json
import shutil
import os
import re

import cv2
import numpy as np

# Filter for feasible contours
FEASIBLE_AREA_MIN = 1000
FEASIBLE_AREA_MAX = 100000

# binary image threshold
UPPER = 255
LOWER = 254

bad_images = list()
bad_image_bin=r'D:\DT-cat_Synthetic_Data_Generation\utils\bad_image_bin'
parser = argparse.ArgumentParser()
parser.add_argument('--config-path', default='D:\\DT-cat_Synthetic_Data_Generation\\config\\settings.json'
					, dest='config_path')
parser.add_argument('--image-path', default=r'D:\DT-cat\image'
					, dest='image_path')

config_path = parser.parse_args().config_path
img_file_path = parser.parse_args().image_path

with open(config_path, 'r') as f:
	all_settings = json.load(f)

IMAGE_SIZE = all_settings['general_settings']['Image_Size']


def calculate_pixels(img):  # return the average pixel value of an image, suggest background image
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img_gray_array = np.array(img_gray, dtype=float)
	img_gray_array_1d = img_gray_array.flatten()
	img_gray_array_avg_pix = sum(img_gray_array_1d) / len(img_gray_array_1d)
	return img_gray_array_avg_pix


def find_ROI_contour(img_path, upper, lower, offset=0, show_result=0):
	img = cv2.imread(img_path)
	img_binary = cv2.Canny(img, lower, upper)
	_, contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	contours = [con for con in contours if FEASIBLE_AREA_MAX > cv2.contourArea(con) > FEASIBLE_AREA_MIN]
	if len(contours) > 0:
		contours = [contours[0]]
	elif len(contours) == 0:
		print('Alert!! We dont find ROi in' + img_path)
		bad_images.append(img_path + '\n')

	if show_result:
		cv2.drawContours(img, contours, -1, 255)
		cv2.imshow('img', img_binary)
		cv2.waitKey(0)
		cv2.imshow('img', img)
		cv2.waitKey(0)

	con_arr = np.array(contours).ravel()
	res = con_arr.reshape(int(len(con_arr) / 2), 2)
	return res

def remove_bad_image():
	for badimg in bad_images:
		for i in range(16):#NUMBEROFFEASBILEEXAMPLE
			shutil.move(badimg.replace('0.png\n','%s.png'%str(i)),bad_image_bin)
			print('hhh')

if __name__ == '__main__':
	# img_file_list = [os.path.join(img_file_path, img_path) for img_path in os.listdir(img_file_path) if
	# 				 '_0.png' in img_path]
	# img_contours = [(img, find_ROI_contour(img, UPPER, LOWER)) for img in img_file_list]
	# for img_con in img_contours:
	# 	if len(img_con[1]) == 0: continue
	# 	img_json = dict({"imageHeight": IMAGE_SIZE[1], "imageWidth": IMAGE_SIZE[0], "imagePath": img_con[0],
	# 				 "shapes": [{"label": re.findall(r'F5800[a-zA-Z0-9]*', img_con[0])
	# 								, "points": img_con[1].tolist()}]})
	# 	with open(img_con[0].replace('_0.png', '.json'), 'w') as f:
	# 		json.dump(img_json, f)
	# 		print("%s processed and saved with %d points found " % (img_con[0], len(img_con[1])))
	#
	#
	# with open(r'..\config\bad_images.txt', 'w') as f:
	# 	f.writelines(bad_images)
	#print(bad_images)
	bad_images=[img+'\n' for img in os.listdir(r'D:\DT-cat_Synthetic_Data_Generation\utils\bad_image_bin')]
	#print(bad_images,len(bad_images))
	bad_imgs_pattern = [os.path.join(r'D:\DT-cat\image',img.replace('_0.png\n','')) for img in bad_images]
	# for i in range(1,16):
	# 	for img in bad_imgs_pattern:
	# 		shutil.move((img+"_"+str(i)+'.png'),r'D:\DT-cat_Synthetic_Data_Generation\utils\bad_image_bin')


