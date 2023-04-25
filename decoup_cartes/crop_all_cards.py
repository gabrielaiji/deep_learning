import os, sys
from select_rectangle import RectangleBuilder
from PIL import Image


def search_cards_set(path):
	dirs = os.listdir(path)

	for item in dirs:
		itemPath = os.path.join(path, item)

		if os.path.isdir(itemPath):
			search_cards_set(itemPath)
		else:
			if ("carte" in item) and (not "cropped" in item):
				
				rectangle = RectangleBuilder(itemPath)
				im = Image.open(itemPath)
				crop_rectangle = rectangle.getRect()

				if(crop_rectangle != (0,0,0,0) ):
					nom =  item.split(".")
					new_nom = nom[0]+"_cropped"

					cropped_im = im.crop(crop_rectangle)
					cropped_im.save(path+"/"+new_nom+".png")
					os.remove(itemPath)



def search_cards(global_path):

	dirs = os.listdir( global_path )
	for label in dirs:

		set_path = os.path.join(global_path, label)
		
		search_cards_set(set_path)

search_cards("../data/global/")