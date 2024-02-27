import math
from pydub import AudioSegment
# Key generation algorithms for Chaos Encryption Algorithms
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

# encryption algorithms for Chaos Encryption Algorithms
def encryption(audio_data, c1prime, c2prime, y1, y2):    
    encrypted_audio_data_list = []
    tempvalue = 0
    for i in range(len(audio_data)):
        if(i == 0):
            tempvalue = audio_data[i] + (c1prime * y1) + (c2prime * y2)
            encrypted_audio_data_list.append(((tempvalue+1) % 2) - 1)
        elif(i == 1):
            tempvalue = audio_data[i]  + (c1prime * encrypted_audio_data_list[i-1]) + (c2prime * y1)
            encrypted_audio_data_list.append(((tempvalue+1) % 2) - 1)
        elif(i > 1):
            tempvalue = audio_data[i]  + (c1prime * encrypted_audio_data_list[i-1]) + (c2prime * encrypted_audio_data_list[i-2])
            encrypted_audio_data_list.append(((tempvalue+1) % 2) - 1)
    return encrypted_audio_data_list

# decryption algorithms for Chaos Encryption Algorithms
def decryption(audio_data, c1prime, c2prime, y1, y2):
    decrypted_audio_data_list = []
    tempvalue = 0
    for i in range(len(audio_data)):
        if(i == 0):
            tempvalue = audio_data[i] - (c1prime * y1) - (c2prime * y2)
            decrypted_audio_data_list.append(((tempvalue+1) % 2) - 1)
        elif(i == 1):
            tempvalue = audio_data[i] - (c1prime * audio_data[i-1]) - (c2prime * y1)
            decrypted_audio_data_list.append(((tempvalue+1) % 2) - 1)
        elif(i > 1):
            tempvalue = audio_data[i] - (c1prime * audio_data[i-1]) - (c2prime * audio_data[i-2])
            decrypted_audio_data_list.append(((tempvalue+1) % 2) - 1)
    return decrypted_audio_data_list

from pydub import AudioSegment

def convert_m4a_to_wav(input_file_path, output_file_path):
    audio = AudioSegment.from_file(input_file_path, format="m4a")
    audio.export(output_file_path, format="wav")