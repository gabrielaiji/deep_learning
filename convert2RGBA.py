from PIL import Image
import os, sys

def convert_sub_dir(path):
	dirs = os.listdir(path)

	for item in dirs:
		itemPath = os.path.join(path, item)

		if os.path.isdir(itemPath):
			convert_sub_dir(itemPath)

		elif os.path.isfile(itemPath):
			img = Image.open(itemPath)
			if img.format == 'PNG':
				if img.mode != 'RGBA':
					names = itemPath.split(".")
					print(names)
					img.convert("RGBA").save("./"+names[1]+"_rgba.png")
					os.remove(itemPath)
					print("Converted "+itemPath)



path = "./data/global/"
convert_sub_dir(path)