import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    a = np.zeros([512,512],dtype = 'uint16')
    
    data = np.load("array.npy")
    b=a//256
    c=a%256
    print(a)
    print(a.dtype)
    print(data.dtype)
    print(b.dtype)
    print(c.dtype)
    b= b.astype('uint8')
    c= c.astype('uint8')
    print(b.dtype)
    print(c.dtype)
