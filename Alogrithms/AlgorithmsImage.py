import math
from PIL import Image

def normalized(value):  
    return (value - 128) / 128

def denormalized(value): 
    return round((value * 128) + 128) 

# Key generation algorithms for Chaos Encryption Algorithms
def KeyGeneration(key, c1_value, c2_value, y1_value, y2_value):
    listOfKey = []
    tempvalue = 0
    for i in range(16):
        if(i == 0):
            tempvalue = ord(key[i]) + (c1_value * y1_value) + (c2_value * y2_value)
            listOfKey.append((tempvalue+1)%2 - 1)
        elif(i == 1):
            tempvalue = ord(key[i]) + (c1_value * listOfKey[i-1]) + (c2_value * y1_value)
            listOfKey.append((tempvalue+1)%2 - 1)
        elif(i > 1):
            tempvalue = ord(key[i]) + (c1_value * listOfKey[i-1]) + (c2_value * listOfKey[i-2])
            listOfKey.append((tempvalue+1)%2 - 1)
            
    return listOfKey

# encryption algorithms for Chaos Encryption Algorithms
def encryption(image_pixel_value, height, width, selected_rgb, c1prime, c2prime, y1, y2):
    pixel_value_list = []
    tempvalue = 0
    i = 0
    for h in range(height):
        for w in range(width):
            if(i == 0):
                tempvalue = normalized(image_pixel_value[w, h][selected_rgb]) + (c1prime * y1) + (c2prime * y2)
                pixel_value_list.append((tempvalue+1)%2 - 1)
            elif(i == 1):
                tempvalue = normalized(image_pixel_value[w, h][selected_rgb]) + (c1prime * pixel_value_list[i-1]) + (c2prime * y1)
                pixel_value_list.append((tempvalue+1)%2 - 1)
            elif(i > 1):
                tempvalue = normalized(image_pixel_value[w, h][selected_rgb]) + (c1prime * pixel_value_list[i-1]) + (c2prime * pixel_value_list[i-2])
                pixel_value_list.append((tempvalue+1)%2 - 1)
            i += 1
    return pixel_value_list

# decryption algorithms for Chaos Encryption Algorithms
def decryption(image_pixel_value, c1prime, c2prime, y1, y2):
    cyphertextlist = []
    tempvalue = 0
    for i in range(len(image_pixel_value)):
        if(i == 0):
            tempvalue = image_pixel_value[i] - (c1prime * y1) - (c2prime * y2)
            cyphertextlist.append((tempvalue+1)%2 - 1)
        elif(i == 1):
            tempvalue = image_pixel_value[i] - (c1prime * image_pixel_value[i-1]) - (c2prime * y1)
            cyphertextlist.append((tempvalue+1)%2 - 1)
        elif(i > 1):
            tempvalue = image_pixel_value[i] - (c1prime * image_pixel_value[i-1]) - (c2prime * image_pixel_value[i-2])
            cyphertextlist.append((tempvalue+1)%2 - 1)
    return cyphertextlist

# Turning all of value create by encryption or decryption to charactor
def denormalized_list(list):
    temp = []
    for i in range(len(list)):
        temp.append(denormalized(list[i]))
    return temp