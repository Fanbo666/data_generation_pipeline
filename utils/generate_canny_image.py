import cv2
import os

img_dir=r'D:\DT-cat\image'
img_list=[os.path.join(img_dir,img) for img in os.listdir(img_dir)]
dest=r'D:\DT-cat\image\bin'
os.mkdir(dest)

for img_orin in img_list:

	img=cv2.imread(img_orin)
	img_bin=cv2.Canny(img,0,255)
	save_name = img_orin.replace('png', 'jpg')
	print(save_name+"saveed!!")

	cv2.imwrite(os.path.join(dest,save_name),img_bin)
	#cv2.imwrite(img_orin.replace('.png','bin_.png'),img_bin)
#
