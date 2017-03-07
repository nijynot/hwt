import scipy.misc as sm
import numpy as np
from PIL import Image
#import time
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

def imageToArray(image):
    return np.asarray(image, dtype="int32")

def arrayToImage(data):
    # Removes all negative values
    # Can't save negative values for some reason
    return Image.fromarray(data).convert('L')

def initWm(shape):
    # Column hwt
    # Init first rows of Wm
    Wm = np.zeros(shape[0]).reshape(1, shape[0])
    Wm[0][0] = np.sqrt(2) / 2
    Wm[0][1] = np.sqrt(2) / 2
    
    # Add rows to W
    for x in range(1, int(shape[0]/2)):
        a = np.zeros(shape[0])
        a[2*x] = (np.sqrt(2) / 2)
        a[(2*x) + 1] = (np.sqrt(2) / 2)
        Wm = np.concatenate((Wm, [a]), axis=0)
 
    for x in range(0, int(shape[0]/2)):
        a = np.zeros(shape[0])
        a[2*x] = (np.negative(np.sqrt(2) / 2))
        a[(2*x) + 1] = (np.sqrt(2) / 2)
        Wm = np.concatenate((Wm, [a]), axis=0)
    return Wm

def initWn(shape):
    # Row hwt
    # Init first rows of Wn
    Wn = np.zeros(shape[1]).reshape(1, shape[1])
    Wn[0][0] = np.sqrt(2) / 2
    Wn[0][1] = np.sqrt(2) / 2
    
    # Add rows to Wn
    for x in range(1, int(shape[1]/2)):
        a = np.zeros(shape[1])
        a[2*x] = (np.sqrt(2) / 2)
        a[(2*x) + 1] = (np.sqrt(2) / 2)
        Wn = np.concatenate((Wn, [a]), axis=0)
 
    for x in range(0, int(shape[1]/2)):
        a = np.zeros(shape[1])
        a[2*x] = (np.negative(np.sqrt(2) / 2))
        a[(2*x) + 1] = (np.sqrt(2) / 2)
        Wn = np.concatenate((Wn, [a]), axis=0)
    return Wn

def compress(data):
    #data = imageToArray(image)
    Wm = initWm(data.shape)
    Wn = initWn(data.shape)
    
    newData = np.dot(Wm, data)
    newData = np.dot(newData, np.transpose(Wn))
    return newData

def decompress(data):
    Wm = initWm(data.shape)
    Wn = initWn(data.shape)
    
    newData = np.dot(data, Wn)
    newData = np.dot(np.transpose(Wm), newData)
    return newData

#def averageImage(data):
#    a2 = np.zeros((shape[0], shape[1]))
#    for i in range(data.shape[0]):
#        for j in range(data.shape[1]):
#            if j % 2 == 0:
#                a2[i,j], a2[i,j+1] = (data[i,j+1] + data[i,j])/2, (data[i,j+1] - data[i,j])/2
#            else:
#                continue
            
def average(data):
    rows = data.shape[0]
    columns = data.shape[1]
    A = np.zeros((rows, columns))
    for i in range(int(rows/2)):
        for j in range(int(columns/2)):
            A[i, j] = 2*(data[2*i, 2*j] + data[2*i, 2*j + 1] + data[2*i + 1, 2*j] + data[2*i + 1, 2*j + 1])/4
            A[i, j + int(columns/2)] = 2*(-1*data[2*i, 2*j] + data[2*i, 2*j + 1] - data[2*i + 1, 2*j] + data[2*i + 1, 2*j + 1])/4
            A[i + int(rows/2), j] = 2*(-1*data[2*i, 2*j] - data[2*i, 2*j + 1] + data[2*i + 1, 2*j] + data[2*i + 1, 2*j + 1])/4
            A[i + int(rows/2), j + int(columns/2)] = 2*(-1*data[2*i, 2*j] + data[2*i, 2*j + 1] + data[2*i + 1, 2*j] - data[2*i + 1, 2*j + 1])/4
    return A

# Paths
dir = path.dirname(__file__)
kvinna = path.join(dir, 'kvinna.jpg')

# image is the image
# data is the grayscale
image = loadImage(kvinna)
data = trim(imageToArray(image))

#time(average(data))
#time(compress(data))
