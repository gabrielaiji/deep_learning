from loadimages import count_images
import os, sys
import numpy as np
import shutil
from math import ceil

def get_partition_borders(nb_elements, percentages):
	borders = [0 for k in range(len(percentages)-1) ]

	borders[0] = ceil(nb_elements * percentages[0])
	for i in range(1, len(percentages) -1):
		borders[i] = borders[i-1] + ceil(nb_elements * percentages[i])

	return borders

def get_index_partition(borders, current_index, shuffle_indices):
	temp_border = 0
	shuffle_indice = shuffle_indices[current_index]
	while temp_border < len(borders) and shuffle_indice > borders[temp_border]:
		temp_border+=1

	return temp_border

def partition_move_file(data_path, origin_partition, new_partitions, local_dire_path, item_name, borders, current_index, shuffle_indices):
	original_path = os.path.join(data_path, os.path.join(origin_partition, os.path.join(local_dire_path, item_name)))
	
	partition_path = new_partitions[get_index_partition(borders, current_index, shuffle_indices)]
	new_path = os.path.join(data_path, os.path.join(partition_path, local_dire_path))

	if not os.path.isdir(new_path):
		os.makedirs(new_path)

	shutil.copyfile(original_path, os.path.join(new_path, item_name))


def partition_sub_type(data_path, origin_partition, new_partitions, borders, current_type, shuffle_indices, current_index):
	type_path = os.path.join(data_path, os.path.join(origin_partition,current_type))
	dirs = os.listdir(type_path)

	for item in dirs:
		itemPath = os.path.join(type_path, item)

		if os.path.isfile(itemPath):
			partition_move_file(data_path, origin_partition, new_partitions, current_type, item, borders, current_index, shuffle_indices)
			current_index +=1
		elif os.path.isdir(itemPath):
			current_sub_type = os.path.join(current_type, item)
			current_index = partition_sub_type(data_path, origin_partition, new_partitions, borders, current_sub_type, shuffle_indices, current_index)
		else:
			print("Unknown : " + itemPath)

	return current_index

def partition_type(data_path, origin_partition, new_partitions, percentages, current_type):
	type_path = os.path.join(data_path, os.path.join(origin_partition,current_type))
	nb_images = count_images(type_path)

	shuffle_indices = np.random.permutation(nb_images)
	borders = get_partition_borders(nb_images, percentages)

	current_index = 0

	dirs = os.listdir(type_path)
	for item in dirs:
		itemPath = os.path.join(type_path, item) 


		if os.path.isfile(itemPath):
			partition_move_file(data_path, origin_partition, new_partitions, current_type, item, borders, current_index, shuffle_indices)
			current_index +=1
		elif os.path.isdir(itemPath):
			current_sub_type = os.path.join(current_type, item)
			current_index = partition_sub_type(data_path, origin_partition, new_partitions, borders, current_sub_type, shuffle_indices, current_index)
		else:
			print("Unknown : " + itemPath)


def partition_data(data_path, origin_partition, new_partitions, percentages):
	original_path = os.path.join(data_path, origin_partition)	

	dirs = os.listdir(original_path)
	for item in dirs:
		itemPath = os.path.join(original_path, item)

		if os.path.isdir(itemPath):
			partition_type(data_path, origin_partition, new_partitions, percentages, item)
		else:
			print("Not dir : " + itemPath)





path = "./data/"

origin_partition = "global/"
new_partitions = ["validation/", "test/", "train/"]
percentages = [0.10, 0.10, 0.80]

partition_data(path, origin_partition, new_partitions, percentages)