import os
# from pathlib import Path
from typing import Tuple
from numba import njit
# from decrypt import _decrypt_image

# from key import key_system
import numpy as np
import cv2 as cv

@njit
def f(x: float) -> float:
    return ((x + 1) % 2) - 1

@njit
def normalize(x: float | int | np.uint8) -> float:
    return (x - 128) / 128

@njit
def denormalize(x: float | int | np.uint8) -> float:
    return (x * 128) + 128

@njit
def file(path: str):
    from os.path import exists
    if not exists(path):
        raise ValueError("Path doesn't exist")
    return path

@njit
def KeyGeneration(key, c1_value, c2_value, y1_value, y2_value):
    listOfKey = []
    tempvalue = 0
    for i in range(16):
        if(i == 0):
            tempvalue = (ord(key[i])) + (c1_value * y1_value) + (c2_value * y2_value)
            listOfKey.append(((tempvalue+1) % 2) - 1)
        elif(i == 1):
            tempvalue = (ord(key[i])) + (c1_value * listOfKey[i-1]) + (c2_value * y1_value)
            listOfKey.append(((tempvalue+1) % 2) - 1)
        elif(i > 1):
            tempvalue = (ord(key[i]))+ (c1_value * listOfKey[i-1]) + (c2_value * listOfKey[i-2])
            listOfKey.append(((tempvalue+1) % 2) - 1)
    
    c1prime = listOfKey[14]
    c2prime = listOfKey[15]
    
    return c1prime, c2prime

@njit
def encrypte_image(src_img: cv.typing.MatLike, encoded_img: np.ndarray[np.uint8], coeff1: float, coeff2: float, prev_val: float, prev_prev_val: float,
                  return_output=False) -> Tuple[np.ndarray[np.uint8], float, float]:
    last_val = prev_val
    second_last_val = prev_prev_val

    for r_idx in range(src_img.shape[0]):
        for c_idx in range(src_img.shape[1]):
            for ch_idx in range(src_img.shape[2]):
                pixel_val = src_img[r_idx, c_idx, ch_idx]
                encoded_val = f(normalize(pixel_val) + coeff1 * last_val + coeff2 * second_last_val)

                denorm_val = denormalize(encoded_val)
                while True:
                    temp_encoded_pixel = int(denorm_val)
                    decrypted_pixel, temp_dec_last_val, temp_dec_second_last_val = decypte_for_test(temp_encoded_pixel, coeff1, coeff2, last_val, second_last_val)
                    denorm_val = (denorm_val + pixel_val - decrypted_pixel) % 256
                    # print("val: ", pixel_val)
                    # print("decrypt: ", decrypted_pixel)
                    if pixel_val - decrypted_pixel == 0:
                        # print("----------------------------------------")
                        break

                last_val = temp_dec_last_val
                second_last_val = temp_dec_second_last_val

                encoded_img[r_idx, c_idx, ch_idx] = int(denorm_val)

    return encoded_img

@njit
def decypte_for_test(input_byte: int, coeff1: float, coeff2: float, prev_val: float, prev_prev_val: float) -> tuple[int, float, float]:
    last_val = prev_val
    second_last_val = prev_prev_val

    normalized_val = normalize(input_byte)

    decoded_val = f(normalized_val - coeff1 * last_val - coeff2 * second_last_val)

    second_last_val = last_val
    last_val = normalized_val

    return int(denormalize(decoded_val)), last_val, second_last_val

@njit
def decrypte_image(encoded_image: cv.typing.MatLike, decoded_image: np.ndarray[np.uint8], coeff1: float, coeff2: float, prev_val: float, prev_prev_val: float, return_output=False) -> tuple[np.ndarray[np.uint8], float, float]:
    last_val = prev_val
    second_last_val = prev_prev_val

    for r_idx in range(encoded_image.shape[0]):
        for c_idx in range(encoded_image.shape[1]):
            for ch_idx in range(encoded_image.shape[2]):
                encoded_pixel = encoded_image[r_idx, c_idx, ch_idx]
                normalized_val = normalize(encoded_pixel)

                decrypted_val = f(normalized_val - coeff1 * last_val - coeff2 * second_last_val)

                decoded_image[r_idx, c_idx, ch_idx] = int(denormalize(decrypted_val))
                second_last_val = last_val
                last_val = normalized_val

    return decoded_image



# dirname = os.path.join(os.path.dirname(__file__))
# imagepath = "python\image\original_forest.jpg"
# dest = "encrypted_image.jpg"
# c1 = -0.85
# c2 = 0.24
# y1 = -0.7
# y2 = 0.29
# key = "FsD(#uWmB%zLmv<w"
# c1prime, c2prime = KeyGeneration(key, c1, c2, y1, y2)
# print(c1prime, c2prime)

# image = cv.imread(imagepath)
# cipher_image = np.zeros_like(image, dtype=np.uint8)
# # encrypted_img ,_,_ = _encrypt_image(img, tmp_img, MAIN_ALGO_C1, MAIN_ALGO_C2,MAIN_ALGO_Y_MINUS_1 ,MAIN_ALGO_Y_MINUS_2 , returnVal=False)

# encrypted_image, new_y_minus_1, new_y_minus_2 = encrypte_image(image, cipher_image, c1prime, c2prime, y1, y2)

# cv.imwrite(dest, encrypted_image)

# plain_image = np.zeros_like(cipher_image, dtype=np.uint8)
# decrypted_image, new_y_minus_1, new_y_minus_2 = decrypte_image(cipher_image, plain_image, c1prime, c2prime, y1, y2)
# cv.imwrite("decrypted_image.jpg", decrypted_image)