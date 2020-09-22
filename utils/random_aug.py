import numpy as np
from skimage import exposure, color, util, transform
import os, sys, argparse
import matplotlib.pyplot as plt

def rand_gray(image):
	rate = np.clip(np.random.randn(1,)+1, 0.2, 1)
	image = color.rgb2gray(image)
	image = color.gray2rgb(image)
	image = exposure.rescale_intensity(image,in_range='image',out_range=(0,rate[0]))
	return image


def rand_crop(image, ratio = 0.8, resize = True):
	shape = image.shape
	height ,width, _ = image.shape
	height_c =int(height*ratio)
	width_c =int(width*ratio)
	position_x = np.random.uniform(high = width - width_c , low = 0)
	position_y = np.random.uniform(high = height - height_c , low = 0)
	image = util.crop(image, ((position_x, width-width_c-position_x),(position_y, height-height_c-position_y),(0,0)))
	if resize:
		image = transform.resize(image, shape)
	return image


def rand_rescale(image, mean_scale=0.9):
	shape = image.shape
	rate = np.clip(np.random.randn(1,)+mean_scale, 0.2, 1)
	image = transform.rescale(image, rate[0], multichannel=True, anti_aliasing = True)
	image = transform.resize(image, shape)
	return image


def rand_noise(image):
	return util.random_noise(image, var = 0.001)


def rand_hue(image):
	pass


def rand_aug(folder, out_path, fold=1):
	images = [image_path for image_path in os.listdir(folder) if image_path.endswith('.jpg')]
	
	for f in range(int(fold)):
		for i, image_path in enumerate(images):
			image = plt.imread(os.path.join(folder,image_path))

			image = rand_gray(image)
			image = rand_crop(image)
			image = rand_rescale(image)
			image = rand_noise(image)

			save_path = os.path.join(out_path, image_path[:-4]+'_aug_{}.jpg'.format(f))
			plt.imsave(save_path, image)
			print(save_path)




def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument("-folder")
	parser.add_argument("-out")
	parser.add_argument("-fold")
	args = parser.parse_args()
	folder = args.folder
	out_path = args.out
	fold = args.fold
	rand_aug(folder, out_path, fold)



if __name__ == "__main__":
	main(sys.argv)