
import tensorflow as tf
from scipy import misc
import numpy as np
import os
from PIL import Image
import argparse 
from math import ceil
import sys
import skimage

cur_dir = os.getcwd()


def rotate_func(image):
    angle = np.random.uniform(low=-90, high=90.0)
    return skimage.transform.rotate(image, angle, resize=True)

def rotate(image):
    image = tf.numpy_function(rotate_func, [image], tf.uint8)
    image = tf.image.crop_to_bounding_box(image,60,80,360,480)
    return image

def resize(image):
    resized = tf.image.resize(image, (640, 480), 1)
    resized.set_shape([640,480,3])
    return resized

def read_image(filename_queue):
    reader = tf.WholeFileReader()
    key,value = reader.read(filename_queue)
    image = tf.image.decode_jpeg(value)
    return key, image

def inputs(path):
  
    filenames = [os.path.join(path, file) for file in os.listdir(path) if ".jpg" in file]
    filename_queue = tf.train.string_input_producer(filenames)
    filename,read_input = read_image(filename_queue)
    image = rotate(read_input)
    image = resize(image)

    return filename, image

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-folder")
    parser.add_argument("-fold")
    args = parser.parse_args()
    path = args.folder
    n = int(args.fold)

    with tf.Graph().as_default():
        image = inputs(path)
        init = tf.initialize_all_variables()
        sess = tf.Session()
        sess.run(init)
        tf.train.start_queue_runners(sess=sess)

        img_num = len([file for file in os.listdir(path) if ".jpg" in file])

        for i in range(n*img_num):
            filename, img = sess.run(image)
            print (filename)
            img = Image.fromarray(img, "RGB")
            img.save(os.path.join(str(filename)[2:-6]+ "_" + str(ceil((i+1)/img_num)) +'.jpg'))

if __name__ == "__main__":
    main(sys.argv)



