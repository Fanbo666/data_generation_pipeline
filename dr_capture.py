import sys

import argparse
import json
import numpy as np
import os
import vtk

from utils.vtk_gen import WriteImage, set_texture, set_background_image, uni_rotate

# Number of images generated per feasible angels
NUMBER_OF_SAMPLES = 36

# Number of colors per angles
NUMBER_OF_RANDOM_COLORS = 15

# If we want the image the texture by ourselves
SET_TEXTURE = False


def mkdir(path):
	path = path.strip()
	path = path.rstrip("\\")
	exists = os.path.exists(path)
	if not exists:
		os.makedirs(path)
	else:
		print("add files into existing folder")


def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('--config-path', default='D:\\DT-cat_Synthetic_Data_Generation\\config\\settings.json'
						, dest='config_path')
	config_path = parser.parse_args().config_path
	with open(config_path, 'r') as f:
		all_settings = json.load(f)

	general_settings = all_settings['general_settings']
	module_settings = all_settings['module_settings']
	camera_settings = all_settings['camera_settings']

	model_folder = general_settings['Module_Path']
	background_path = general_settings['BG_Path']
	out_path = general_settings['Save_Path']
	if not os.path.exists(out_path):
		mkdir(out_path)
	model_list = [model.replace('.stl', '') for model in os.listdir(model_folder) if 'stl' in model]
	image_size = general_settings['Image_Size']

	# configuration of Light condition
	light = vtk.vtkLight()
	light.PositionalOff()
	light.SetPosition(300, 0, 470)
	light.SetIntensity(10)  # light intensity we default set it quite high

	ren = vtk.vtkRenderer()
	ren.SetBackground(0.1, 0.2, 0.4)  # Fixed
	ren.AddLight(light)

	# config of the camera position
	ren.GetActiveCamera().SetFocalPoint(1, 1, 1)
	ren.GetActiveCamera().SetPosition(camera_settings["co_ordinate"][0],
									  camera_settings["co_ordinate"][1], camera_settings["co_ordinate"][2])  # 470
	# Here we set x,y to zero which means we face vertical to the surface and adjust the height of camera
	ren.GetActiveCamera().SetViewUp(0, 1, 0)  # fixed

	# Some basic universal configurations
	renWin = vtk.vtkRenderWindow()
	background_ren = set_background_image(background_path)
	renWin.SetSize(image_size[0], image_size[1])  # The same with real image
	background_ren.SetLayer(0)
	background_ren.InteractiveOff()
	ren.SetLayer(1)
	renWin.SetNumberOfLayers(2)
	renWin.AddRenderer(ren)
	renWin.AddRenderer(background_ren)

	ext = ['', '.png', '.jpg', '.ps', '.tiff', '.bmp', '.pnm']
	my_ext = ['.png']
	assert my_ext[0] in ext

	for model_name in model_list:
		assert model_name in module_settings  # At least we are doing the same thing

		model_path = os.path.join(model_folder, model_name + ".stl")
		# Read from stl model
		stlreader = vtk.vtkSTLReader()
		stlreader.SetFileName(model_path.strip())

		# Construct mapper
		mapper = vtk.vtkPolyDataMapper()
		mapper.SetInputConnection(stlreader.GetOutputPort())
		mapper.ScalarVisibilityOff()

		actor = vtk.vtkActor()
		scale_config_module = module_settings[model_name]['scale']
		actor.SetScale(scale_config_module, scale_config_module, scale_config_module)

		# Config Offset
		transform = vtk.vtkTransform()
		offset_module = module_settings[model_name]['offset']
		transform.Translate(offset_module[0], offset_module[1], offset_module[2])  # TODO: Link with offset in json
		actor.SetUserTransform(transform)
		actor.SetMapper(mapper)

		# Read and set texture
		if SET_TEXTURE:
			texture_path = module_settings[model_name]['texture_path']
			module_text = set_texture(stlreader, mapper, texture_path)
			actor.SetTexture(module_text)

		ren.AddActor(actor)
		# TODO: Here we get rotate
		feasible_rotations = module_settings[model_name]['rotate_combination']
		rotate_z = 360 / NUMBER_OF_SAMPLES
		print(feasible_rotations)
		for xyz in feasible_rotations:
			uni_rotate(actor, xyz[0], xyz[1], xyz[2])
			for accu in range(NUMBER_OF_SAMPLES):
				uni_rotate(actor, 0, 0, rotate_z)
				color_list = list()  # We set black as default
				color_list.append([0, 0, 0])
				if module_settings[model_name]['random_color']:
					for _ in range(NUMBER_OF_RANDOM_COLORS):
						#TODO: Color RGB value need to be noticed here.
						r, g, b = np.random.normal(0, 0.1, 1), np.random.normal(0, 0.1, 1), np.random.uniform(0, 0.1, 1)
						color_list.append([r, g, b])
				position_label = str(xyz[:2] + [int(accu * rotate_z) + int(rotate_z)]).replace(' ', '')
				position_label = position_label.replace('[', '')
				position_label = position_label.replace(']', '')
				counter_color = 0
				for color in color_list:
					actor.GetProperty().SetColor(color[0], color[1], color[2])
					renWin.Render()
					file_names = list(map(lambda x: out_path + os.path.sep + str(model_name) + '_' + position_label
													+ '_' + str([str(c) for c in color]) + x, my_ext))
					counter_color += 1
					for f in file_names:
						WriteImage(f, renWin, rgba=False)
						print('3D model --------------------------------> %s' % f)
			uni_rotate(actor, -xyz[0], -xyz[1], -xyz[2])  # put it back as origin
		ren.RemoveActor(actor)


if __name__ == "__main__":
	main(sys.argv)
