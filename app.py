import subprocess
from flask import Flask, url_for, redirect, render_template, request, jsonify
from PIL import Image
import soundfile as sf
import Alogrithms.texten2 as choas
import Alogrithms.image_encryption as Image
import Alogrithms.AlgorithmsAudio as ad
import cv2 as cv
import numpy as np
import Alogrithms.video_encryption as Video
import ffmpeg 
from pydub import AudioSegment
# import Alogrithms.AlgorithmsImage as ig

app = Flask(__name__)

#-------------------------vairable----------------------
# key = "ChhorngKy1234JOL"
# key = "aaaaaaaaaaaaaaaa"
# key = "sjfeikookppasjdf"
# key = "#$042asfdf5ygh(("
key = "aaaaaaaaaaaaaaaa"

c1 = -0.85
c2 = 0.24
y1 = -0.7
y2 = -0.29
#-------------------------vairable----------------------

@app.route('/')
def index():
    return render_template('index.html')

# for text encryption website
@app.route('/text')
def text():
    return render_template('/text/index.html')

@app.route('/choas', methods=["POST", "GET"])
def encypted():
    if request.method == "POST":
        key_value = request.form['Textvalue']
        en_or_de = request.form['en_or_de']
        lastTwoC = choas.KeyGeneration(key, c1, c2, y1, y2)
        c1prime = lastTwoC[0]
        c2prime = lastTwoC[1]
        
        if en_or_de == '1':
            Choas_output = choas.encrypt_text(key_value, c1prime, c2prime, y1, y2)
        elif en_or_de == '2':
            Choas_output = choas.decrypt_text(key_value, c1prime, c2prime, y1, y2)
        
        data = {
            "value" : Choas_output,
            "en_or_de": en_or_de
        }
        
        return render_template('/text/index.html', data=data)
    else:
        return render_template('/text/index.html')
#---------end of text website-------------

# for image encryption website
@app.route('/image')
def image():
    return render_template('/image/index.html')

@app.route('/imageEncryption', methods=["POST", "GET"])
def imageEncrypt():
    if request.method == "POST":
        imageget = request.files['image']
        image_choose = request.form['en_or_de']
        
        imageget.save('ComputerSecurity/static/assets/uploads/' + imageget.filename)
       
        imagepath = "ComputerSecurity/static/assets/uploads/" + imageget.filename
        c1prime, c2prime = Image.KeyGeneration(key, c1, c2, y1, y2)
        print(c1prime, c2prime)

        image = cv.imread(imagepath)
        
        if image_choose == '1':
            cipher_image = np.zeros(image.shape, dtype=np.uint8)
            encrypted_image = Image.encrypte_image(image, cipher_image, c1prime, c2prime, y1, y2)
            cv.imwrite("ComputerSecurity/static/assets/uploads/encrypted.png", encrypted_image)
        elif image_choose == '2':
            plain_image = np.zeros(image.shape, dtype=np.uint8)
            decrypted_image = Image.decrypte_image(image, plain_image, c1prime, c2prime, y1, y2)
            cv.imwrite("ComputerSecurity/static/assets/uploads/decrypted.png", decrypted_image)
            
        print("Process Complete")
    
        data = {
           "path": image,
           "en_or_de": image_choose
        }
        
        return render_template('/image/index.html', data=data)
    else:
        return render_template('/image/index.html')
    
#---------end of image website-------------

# for audio encryption website
@app.route('/audio')
def audio():
     return render_template('/audio/index.html')
 
@app.route('/audioEncrypt', methods=["POST", "GET"])
def audioEncrypt():
    if request.method == "POST":
        audio = request.files['audio']
        audio_choose = request.form['en_or_de']
        audio_path = 'ComputerSecurity/static/assets/audio/' + audio.filename
        audio.save(audio_path)
        if not audio.filename.endswith('.wav'):
            # Convert the audio file to .wav format
            audio = AudioSegment.from_file(audio_path)
            audio_path = audio_path.rsplit('.', 1)[0] + '.wav'
            audio.export(audio_path, format='wav')
        c1prime, c2prime= ad.KeyGeneration(key, c1, c2, y1, y2)
        
        data, samplerate = sf.read(audio_path)  # Use audio_path here
        
        if audio_choose == '1':
            new_data = ad.encryption(data, c1prime, c2prime, y1, y2)
            sf.write('ComputerSecurity/static/assets/audio/encrypted.wav', new_data, samplerate)
        elif audio_choose == '2':
            de_data = ad.decryption(data, c1prime, c2prime, y1, y2)
            sf.write('ComputerSecurity/static/assets/audio/decrypted.wav', de_data, samplerate)

        data = {
           "en_or_de": audio_choose
        }
        
        return render_template('/audio/index.html', data=data)
    else:
        return render_template('/audio/index.html')

#---------end of audio website-------------

# for video encryption website
@app.route('/video')
def video():
     return render_template('/video/index.html')
 
@app.route('/videoEncrypt', methods=["POST", "GET"])
def videoEncrypt():
    if request.method == "POST":
        video = request.files['video']
        video_choose = request.form['en_or_de']
        video_path = 'ComputerSecurity/static/assets/video/' + video.filename
        video.save(video_path)
        
        # Check if the video file is in .mp4 format
        if video.filename.endswith('.mp4'):
            # Convert the video file to .mkv format with ffv1 codec
            output_path = video_path.rsplit('.', 1)[0] + '.mkv'
            subprocess.run(['ffmpeg', '-y', '-i', video_path, '-c:v', 'ffv1', output_path])
            video_path = output_path


        c1prime, c2prime= Video.KeyGeneration(key, c1, c2, y1, y2)
             
        if video_choose == '1':
            # Destinations for the encrypted video
            destmkv =  "ComputerSecurity/static/assets/video/encrypted_video.mkv"
            destwebm =  "ComputerSecurity/static/assets/video/encrypted_video.webm"
            cap = cv.VideoCapture(video_path)
            fps = int(cap.get(cv.CAP_PROP_FPS))
            width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
            # create an empty video file
            encrypted_video = cv.VideoWriter(destmkv, cv.VideoWriter.fourcc(*"FFV1"), fps, (width, height), True)
            last = y1
            second_last = y2
            count = 0
            # Encrypt the video by reading each frame and encrypting it
            while cap.isOpened():
                haveFrame, frame = cap.read()
                if not haveFrame:
                    break
                if count == 0:
                    tmp_frame = np.zeros(frame.shape, dtype=np.uint8)

                encrypted_frame, last, second_last = Video.encrypt_image(frame, tmp_frame, c1prime, c2prime, last, second_last)

                encrypted_video.write(encrypted_frame)
                
                count += 1
                print(count)

            cap.release()
            encrypted_video.release()
            # convert the encrypted video to webm format to diplay it in the browser
            Video.convert_to_vp9(destmkv, destwebm)
            
        elif video_choose == '2':
            # destination of the decrypted video
            destmkv =  "ComputerSecurity/static/assets/video/decrypted_video.mkv"
            destwebm =  "ComputerSecurity/static/assets/video/decrypted_video.webm"
            
            cap = cv.VideoCapture(video_path)
            fps = int(cap.get(cv.CAP_PROP_FPS))
            width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
            # create an empty video file
            decrypted_video = cv.VideoWriter(destmkv, cv.VideoWriter.fourcc(*"ffv1"), fps, (width, height), True)
            
            last = y1
            second_last = y2

            count = 0
            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    break

                if count == 0:
                    tmp_frame = np.zeros(frame.shape, dtype=np.uint8)
                encrypted_frame, last, second_last = Video.decrypt_image(frame, tmp_frame, c1prime, c2prime, last, second_last)
                decrypted_video.write(encrypted_frame)
                
                count += 1
                print(count)

            cap.release()
            decrypted_video.release()
            
            Video.convert_to_vp9(destmkv, destwebm)
            
        data = {
            "en_or_de": video_choose
        }
        
        return render_template('/video/index.html', data=data)
    else:
        return render_template('/video/index.html')

#---------end of audio website-------------

#for running all of the route
if __name__ == "__main__":
    app.run(debug=True)
#---------end----------