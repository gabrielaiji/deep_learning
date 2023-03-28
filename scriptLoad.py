import matplotlib.pyplot as plt

from loadimages import *


labels = ['feu', 'eau']

path = "./data/"

nb_images = 0;
for i in range(len(labels)):
        #dirs = sorted(os.listdir(data_path + dataset + '/' + classes[i]) +"/")
        type_path = path + 'train' + "/" + labels[i] +"/"
        nb_images += count_images(type_path)

x_train, y_train = load_data(path, labels, dataset='train', image_size=128)
print(x_train.shape, y_train.shape)



plt.figure(figsize=(12, 12))
shuffle_indices = np.random.permutation(nb_images)
for i in range(0, 9):
    plt.subplot(3, 3, i+1)
    image = x_train[shuffle_indices[i]]
    plt.title(labels[int(y_train[shuffle_indices[i]])])
    plt.imshow(image/255)

plt.tight_layout()
plt.show()