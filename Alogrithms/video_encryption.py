import os
# from pathlib import Path
from typing import Tuple
from numba import njit
# from decrypt import _decrypt_image

# from key import key_system
import numpy as np
import cv2 as cv
import ffmpeg 

@njit
def f(x: float) -> float:
    return ((x + 1) % 2) - 1
@njit
def normalize(x: float | int | np.uint8) -> float:
    return (x - 128) / 128
 

# [-1.002, 1.00023]

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
def convert_to_h265(input_file, output_file):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, vcodec='libx265')
        .run()
    )


@njit
def convert_to_ffv1(input_file, output_file):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, vcodec='ffv1')
        .run()
    )


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
def encrypt_image(image: cv.typing.MatLike, cipher_image: np.ndarray[np.uint8], c1: float, c2: float, y_minus_1: float, y_minus_2: float,
                               ) -> Tuple[np.ndarray[np.uint8], float, float]:
    current = y_minus_1
    previous = y_minus_2

    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            for channel in range(image.shape[2]):
                pixel_value = image[row, col, channel]
                
                encrypted_value = f(normalize(pixel_value) + c1 * current + c2 * previous)
                denormalized_value = denormalize(encrypted_value)
                
                i = 0
                while True:
                    tmp_cipher_pixel = int(denormalized_value)
                    decrypted_pixel, tmp_decrypt_current, tmp_decrypt_previous = decrypt_for_test(tmp_cipher_pixel, c1, c2, current, previous)

                    denormalized_value = (denormalized_value + pixel_value - decrypted_pixel) % 256
                    i = i + 1
                    if pixel_value - decrypted_pixel == 0:
                        break

                current = tmp_decrypt_current
                previous = tmp_decrypt_previous

                cipher_image[row, col, channel] = int(denormalized_value)

    return cipher_image, current, previous

@njit
def decrypt_for_test(input_byte: int, coeff1: float, coeff2: float, prev_val: float, prev_prev_val: float) -> tuple[int, float, float]:
    current_val = prev_val
    previous_val = prev_prev_val

    normalized_val = normalize(input_byte)

    decoded_val = f(normalized_val - coeff1 * current_val - coeff2 * previous_val)

    previous_val = current_val
    current_val = normalized_val

    return int(denormalize(decoded_val)), current_val, previous_val

@njit
def decrypt_image(cipher_image: cv.typing.MatLike, plain_image: np.ndarray[np.uint8], c1: float, c2: float, y_minus_1: float, y_minus_2: float) -> tuple[np.ndarray[np.uint8], float, float]:
    current = y_minus_1
    previous = y_minus_2

    for row in range(cipher_image.shape[0]):
        for col in range(cipher_image.shape[1]):
            for channel in range(cipher_image.shape[2]):
                cipher_pixel = cipher_image[row, col, channel]
                normalized = normalize(cipher_pixel)

                decrypted = f(normalized - c1 * current - c2 * previous)

                plain_image[row, col, channel] = int(denormalize(decrypted))
                previous = current
                current = normalized

    return plain_image, current, previous


# c1 = -0.85
# c2 = 0.24
# y1 = -0.7
# y2 = -0.29

# #c1 = -0.85
# #c2 = 0.24
# #y1 = -0.7
# #y2 = 0.29
# # key = "FsD(#uWmB%zLmv<w"
# key =   'aaaaaaaaaaaaaaaaa'
# c1prime, c2prime = KeyGeneration(key, c1, c2, y1, y2)

# print(c1prime, c2prime)
# file_path = "0226.mkv"
# # file_path = "file/0226.mp4"

# dest =  "encrypted_video.mkv"
# # dest =  "file/encrypted_video.mp4"
# # file_path_decrypt = "file/encrypted_video.mp4"



# cap = cv.VideoCapture(file_path)
# fps = int(cap.get(cv.CAP_PROP_FPS))
# width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# encrypted_video = cv.VideoWriter(dest, cv.VideoWriter.fourcc(*"FFV1"), fps, (width, height), True)
# # encrypted_video = cv.VideoWriter(dest, cv.VideoWriter.fourcc(*"H264"), fps, (width, height), True)

# last = y1
# second_last = y2

# count = 0
# while cap.isOpened():
#     ret, frame = cap.read()

#     if not ret:
#         break
#     if count == 0:
#         tmp_frame = np.zeros(frame.shape, dtype=np.uint8)

#     encrypted_frame, last, second_last = encrypt_image(frame, tmp_frame, c1prime, c2prime, last, second_last)

#     encrypted_video.write(encrypted_frame)

#     count += 1
#     print(count)

# cap.release()
# encrypted_video.release()
#             # print("done")




# # file_path1 = "file/encrypted_video.mp4"
# file_path1 = "encrypted_video.mkv"
# # dest1 =  "file/decrypted_video.mp4"
# dest1 =  "decrypted_video.mkv"

# cap = cv.VideoCapture(file_path1)
# fps = int(cap.get(cv.CAP_PROP_FPS))
# width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# decrypted_video = cv.VideoWriter(dest1, cv.VideoWriter.fourcc(*"ffv1"), fps, (width, height), True)
# # decrypted_video = cv.VideoWriter(dest1, cv.VideoWriter.fourcc(*"H264"), fps, (width, height), True) 
# last = y1
# second_last = y2

# count = 0
# while cap.isOpened():
#     ret, frame = cap.read()

#     if not ret:
#         break

#     if count == 0:
#         tmp_frame = np.zeros(frame.shape, dtype=np.uint8)
#     encrypted_frame, last, second_last = decrypt_image(frame, tmp_frame, c1prime, c2prime, last, second_last)
#     decrypted_video.write(encrypted_frame)

#     count += 1
#     print(count)

# cap.release()
# decrypted_video.release()
