
import os, sys


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


def count_image(nb_images, labels_indexes):
    for label_index in labels_indexes:
        nb_images[label_index] += 1
    return nb_images

def count_labels(label_path, nb_images, labels_indexes, labels, classes):
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

            nb_images = count_labels(itemPath, nb_images, sub_labels_indexes, sub_labels, classes)

        elif os.path.isfile(itemPath) and label_bool:
            nb_images = count_image(nb_images, labels_indexes)

    return nb_images


def count_partition(data_path, dataset, classes):
    set_path = os.path.join(data_path, dataset)
    dirs = os.listdir(set_path)


    nb_images = [0 for k in range(len(classes))]
    
    nb_images = count_labels(set_path, nb_images, [], [], classes)

    return nb_images


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


Classes = ['acier', 'combat', 'dragon', 'eau', 'feu', 'fée', 'glace', 'insecte', 'normal', 'plante', 'poison', 'psy', 'roche', 'sol', 'spectre', 'tenebres', 'vol', 'électrique']
data_sets = ["train", "validation", "test"]

data_path = "./data/"



nb_images = count_partition(data_path, "global", Classes)

import numpy as np
index = np.argsort(nb_images)

for i in range(len(Classes)):
	print("{0:11} : {1}".format(Classes[index[i]], str(nb_images[index[i]])))

print("{0:11} : {1}".format("'Total' : ", str(sum(nb_images))))

