import cv2
import os
import shutil
import json
import numpy as np

from skimage import feature

img_json_path=r'C:\Users\Z0042n1j\Desktop\DT-CAT\test_img'
imgs = [os.path.join(img_json_path,file) for file in os.listdir(img_json_path)]

for img in imgs:
	img_origin=cv2.imread(img)
	img_bin=cv2.Canny(img_origin,0,1)
	cv2.imwrite(img.replace('jpg','png'),img_bin)

# file_pattern=[file.replace('.json','')
# 			  for file in os.listdir(img_json_path) if 'json' in file]
#
# file_full_path=[os.path.join(img_json_path,file) for file in file_pattern]
#
# for file in file_full_path:
# 	with open(file+'.json') as f:
# 		json_config = json.load(f)
# 	name = json_config['shapes'][0]['label']+'_'+str(np.random.randint(0,1000000))
# 	os.rename(file+'.png',os.path.join(img_json_path,name+'.jpg'))
#


