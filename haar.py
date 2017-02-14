import scipy.misc as sm
import numpy as np
from PIL import Image
from os import path

print('==================')

def loadImage(image):
    try:
        # L for grayscale, LA saves 2 color channels
        i = Image.open(image).convert('L')
        return i
    except OSError: # Checking for different possible errors in the input file
        print ('This is not a jpg image! Input has to be a jpg image!')
        return False
    except FileNotFoundError: # Another check for error in the input file
        print ('No image was found! Input file has to be in the same directory as this code is!')
        return False

def imgToArray(img):
    return np.asarray(img, dtype="int32")

def trim(arr):
    shape = np.shape(arr)
    if shape[0] % 2 != 0:
        if shape[1] % 2 != 0:
            return np.delete(np.delete(arr, shape[0] - 1, 0), shape[1] - 1, 1)
        else:
            return np.delete(arr, shape[0] - 1, 0)
    elif shape[1] % 2 != 0: 
        return np.delete(arr, shape[1] - 1, 1)
    else:
        return arr

# Paths
dir = path.dirname(__file__)
kvinna = path.join(dir, 'kvinna.jpg')

# Img to array
img = loadImage(kvinna)
data = trim(imgToArray(img))
shape = np.shape(data)

W = np.zeros(600).reshape(1,600)
W[0][0] = np.sqrt(2) / 2
W[0][1] = np.sqrt(2) / 2

Wn = np.zeros(478).reshape(1,478)
Wn[0][0] = np.sqrt(2) / 2
Wn[0][1] = np.sqrt(2) / 2

for x in range(1, 300):
    a = np.zeros(600)
    a[2*x] = (np.sqrt(2) / 2)
    a[(2*x) + 1] = (np.sqrt(2) / 2)
    W = np.concatenate((W, [a]), axis=0)
 
for x in range(0, 300):
    a = np.zeros(600)
    a[2*x] = (np.negative(np.sqrt(2) / 2))
    a[(2*x) + 1] = (np.sqrt(2) / 2)
    W = np.concatenate((W, [a]), axis=0)

for x in range(1, 239):
    a = np.zeros(478)
    a[2*x] = (np.sqrt(2) / 2)
    a[(2*x) + 1] = (np.sqrt(2) / 2)
    Wn = np.concatenate((Wn, [a]), axis=0)
 
for x in range(0, 239):
    a = np.zeros(478)
    a[2*x] = (np.negative(np.sqrt(2) / 2))
    a[(2*x) + 1] = (np.sqrt(2) / 2)
    Wn = np.concatenate((Wn, [a]), axis=0)

def compressImage(data):
    #for x in range(0, 478):
    newData = np.dot(W, data)
    
    #for x in range(0, 600):
    newData = np.dot(newData, np.transpose(Wn))
    return newData

def arrayToImage(data):
    return Image.fromarray(data).convert('L')
    
    
#for x in range(0, 478):
#data = np.dot(W, data)

#for x in range(0, 600):
#data = np.dot(data, np.transpose(Wn))
    
#compressedImg = Image.fromarray(data).convert('L')

data = compressImage(data)
data = compressImage(data)

#arrayToImage(data).show()

Wt = np.transpose(W);
Wnt = np.transpose(Wn);


def decompressImage(data):
    #for x in range(0, 478):
    newData = np.dot(Wt, data)
    
    #for x in range(0, 600):
    newData = np.dot(newData, np.transpose(Wnt))
    return newData
data = decompressImage(data)
a = decompressImage(data)

#img = arrayToImage(data)

#averagedData[0][0] = np.mean([data[0][1], data[0][2]]);

def averageImage(data):
    a2 = np.zeros((600, 478))
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if j % 2 == 0:
                a2[i,j], a2[i,j+1] = (data[i,j+1] + data[i,j])/2, (data[i,j+1] - data[i,j])/2
            else:
                continue

#for y in range(600):
#    for x in range(1, 237):
#        averagedData[y][x] = np.mean([data[y][x], data[y][x + 1]])
#    for x in range(1, 237):
#        averagedData[y][236 + x] = (data[y][x + 1] - data[y][x])/2




