
import shutil

import numpy as np
import PIL
from PIL import Image
import os, sys
from scipy.io import loadmat


def get_label_index(label, classes):
    for index in range(len(classes)):
        if label == classes[index]:
            return index
    return -1

def is_label_considered(labels, classes):
    answer = False
    #print(labels)
    if labels != []:
        for label in labels:
            if label in classes:
                answer = True
    return answer

def count_images(path, labels, classes):
    dirs = os.listdir(path)
    #print(labels)
    label_bool = is_label_considered(labels, classes)

    count = 0
    for item in dirs:
        itemPath = os.path.join(path, item) 

        if os.path.isdir(itemPath):
            if labels != []:
                sub_labels = labels.copy()
            else:
                sub_labels = []
            sub_labels.append(item)
            count += count_images(itemPath, sub_labels, classes)
        elif os.path.isfile(itemPath) and label_bool:
            count +=1

    return count

def load_image(path, image_size, x, y, current_index, labels_indexes):
    # Ouverture de l'image
    img = Image.open(path)
    # Conversion de l'image en RGB
    img = img.convert('RGB')
    # Redimensionnement de l'image et écriture dans la variable de retour x 
    img = img.resize((image_size,image_size))
    

    x[current_index] = np.asarray(img)
    # Écriture du label associé dans la variable de retour y
    for label_index in labels_indexes:
        y[current_index, label_index] = 1
    return current_index+1

def load_labels(label_path, image_size,  x, y, current_index, labels_indexes, labels, classes):
    dirs = os.listdir(label_path)
    label_bool = is_label_considered(labels, classes)

    for item in dirs:
        itemPath = os.path.join(label_path, item) 

        if os.path.isdir(itemPath):
            if labels != []:
                sub_labels = labels.copy()
            else:
                sub_labels = []
            sub_labels.append(item)


            sub_label_index = get_label_index(item, classes)
            sub_labels_indexes = labels_indexes.copy()
            if sub_label_index!=-1:
                sub_labels_indexes.append(sub_label_index)

            current_index = load_labels(itemPath, image_size, x, y, current_index, sub_labels_indexes, sub_labels, classes)

        elif os.path.isfile(itemPath) and label_bool:
            current_index = load_image(itemPath, image_size, x, y, current_index, labels_indexes)

    return current_index


def load_data(data_path, classes, dataset='train', image_size=128):
    set_path = os.path.join(data_path, dataset)
    dirs = os.listdir(set_path)


    nb_images = count_images(set_path, [], classes)
    x = np.zeros((nb_images, image_size, image_size, 3))
    y = np.zeros((nb_images, len(classes)))


    
    _ = load_labels(set_path, image_size, x, y, 0, [],[], classes)

    return x, y


def get_string_labels(labels_indexes, classes):
    answer = ""
    labelized = False
    for index in range(len(classes)):
        if int(labels_indexes[index]) == 1:
        	if not labelized:
        		answer =  classes[int(index)]
        		labelized = True
        	else:
        		answer = answer + " + " + classes[int(index)]

    return answer