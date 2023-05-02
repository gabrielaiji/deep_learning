import shutil

import numpy as np
import PIL
from PIL import Image
import os, sys
from scipy.io import loadmat

def count_images(path):
    dirs = os.listdir( path )

    count = 0
    for item in dirs:
        itemPath = os.path.join(path, item) 

        if os.path.isdir(itemPath):
            count += count_images(itemPath + "/")
        elif os.path.isfile(itemPath):
            count +=1

    return count

def load_image(path, image_size, x, y, current_index, idx_class):
    # Ouverture de l'image
    img = Image.open(path)
    # Conversion de l'image en RGB
    img = img.convert('RGB')
    # Redimensionnement de l'image et écriture dans la variable de retour x 
    img = img.resize((image_size,image_size))
    

    x[current_index] = np.asarray(img)
    # Écriture du label associé dans la variable de retour y
    y[current_index] = idx_class
    return current_index+1

def load_sub_type(type_path, image_size,  x, y, current_index, idx_class):
    dirs = os.listdir(type_path)

    for item in dirs:
        itemPath = os.path.join(type_path, item)

        if os.path.isdir(itemPath):
            current_index = load_sub_type(itemPath, image_size, x, y, current_index, idx_class)

        elif os.path.isfile(itemPath):
            current_index = load_image(itemPath, image_size, x, y, current_index, idx_class)
        else:
            print("Unknown : " + itemPath)

    return current_index


def load_data(data_path, classes, dataset='train', image_size=128):
    
    nb_images = 0;
    for i in range(len(classes)):
        #dirs = sorted(os.listdir(data_path + dataset + '/' + classes[i]) +"/")
        type_path = data_path + dataset + "/" + classes[i] +"/"
        nb_images += count_images(type_path)

    x = np.zeros((nb_images, image_size, image_size, 3))
    y = np.zeros((nb_images, 1))

    current_index = 0

    for idx_class in range(len(classes)):
        type_path = data_path + dataset + "/" + classes[idx_class] +"/"
        dirs = sorted(os.listdir(type_path))

        #nb_images_type = count_images(type_path)

        for item in dirs:
            #item = dirs[idx_img]
            itemPath = os.path.join(type_path, item) 

            if os.path.isfile(itemPath):
                current_index = load_image(itemPath, image_size, x, y, current_index, idx_class)
            elif os.path.isdir(itemPath):
                current_index = load_sub_type(itemPath, image_size, x, y, current_index, idx_class)

    return x, y
