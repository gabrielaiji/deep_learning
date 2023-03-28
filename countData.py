import os, sys



def countRecFiles(path):
	dirs = os.listdir( path )

	count = 0
	for item in dirs:
		itemPath = os.path.join(path, item)	

		if os.path.isdir(itemPath):
			count += countRecFiles(itemPath)
		elif os.path.isfile(itemPath):
			count +=1
		else:
			print("Unknown : " + path+item)

	return count


originPath = "./data/global/"
dirs = os.listdir( originPath )

#dirs = filter(os.path.isdir, os.listdir(path))

countTotal = 0
for item in dirs:
	itemPath = os.path.join(originPath, item)

	if os.path.isdir(itemPath):
		#print(typePath)
		countType = countRecFiles(itemPath)

		#print(item +"\t: \t"+ str(countType))
		#"Location: {0:20} Revision {1}".format(Location, Revision)

		print("{0:11} : {1}".format(item, str(countType)))
		countTotal += countType
	else:
		print("Not type : " + item)

print("Total : "+ str(countTotal))