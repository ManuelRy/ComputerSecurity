//image capture
document.addEventListener("DOMContentLoaded", function() {
  const uploadDefaultRadio = document.getElementById("uploadDefault");
  const captureImageRadio = document.getElementById("captureImage");
  const uploadSection = document.getElementById("uploadSection");
  const captureSection = document.getElementById("captureSection");
  const imageUploadInput = document.getElementById("imageUpload");
  const captureButton = document.getElementById("captureButton");
  const cameraPreview = document.getElementById("cameraPreview");
  const imagePreviewSection = document.getElementById("imagePreviewSection");
  const imagePreview = document.getElementById("imagePreview");
  const previewButton = document.getElementById("previewButton");
  const submitButton = document.getElementById("submitButton");

  let stream; // Variable to store camera stream

  // Toggle visibility based on radio button selection
  uploadDefaultRadio.addEventListener("change", function() {
      if (uploadDefaultRadio.checked) {
          uploadSection.style.display = "block";
          captureSection.style.display = "none";
          stopCamera(); // Stop camera when switching to upload option
      }
  });

  captureImageRadio.addEventListener("change", function() {
      if (captureImageRadio.checked) {
          uploadSection.style.display = "none";
          captureSection.style.display = "block";
          startCamera(); // Start camera when switching to capture option
      }
  });

  // Capture image from camera
  captureButton.addEventListener("click", function() {
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      const scaleFactor = 0.5; // Adjust this value to resize the image
      const videoWidth = cameraPreview.videoWidth * scaleFactor;
      const videoHeight = cameraPreview.videoHeight * scaleFactor;
      canvas.width = videoWidth;
      canvas.height = videoHeight;
      context.drawImage(cameraPreview, 0, 0, videoWidth, videoHeight);
      const imageDataUrl = canvas.toDataURL('image/jpeg');
      imagePreview.src = imageDataUrl;
      imagePreviewSection.style.display = "block";
      previewButton.style.display = "inline-block";
      submitButton.style.display = "none";
  });

  // Access the camera and start the video stream
  function startCamera() {
      navigator.mediaDevices.getUserMedia({ video: true })
          .then(function(cameraStream) {
              stream = cameraStream;
              cameraPreview.srcObject = cameraStream;
          })
          .catch(function(error) {
              console.error('Error accessing the camera:', error);
          });
  }

  // Stop the camera stream
  function stopCamera() {
      if (stream) {
          stream.getTracks().forEach(track => track.stop());
          cameraPreview.srcObject = null;
      }
  }

  // Preview the captured image
  previewButton.addEventListener("click", function() {
      imagePreviewSection.style.display = "none";
      previewButton.style.display = "none";
      submitButton.style.display = "inline-block";
  });

  // Handle form submission
  const encryptionForm = document.getElementById("encryptionForm");
  encryptionForm.addEventListener("submit", function(event) {
      // Perform encryption or decryption based on form data
      event.preventDefault();
      // Example: retrieve key text and selected operation
      const keyText = document.getElementById("keyText").value;
      const operation = document.getElementById("operationSelect").value;
      console.log("Key Text:", keyText);
      console.log("Operation:", operation);
      // Implement your encryption/decryption logic here
      // Once done, you can submit the form or display the result as required
      // encryptionForm.submit();
  });
});




  //video recording
  document.addEventListener("DOMContentLoaded", function() {
    const uploadDefaultRadio = document.getElementById("uploadDefault");
    const recordVideoRadio = document.getElementById("recordVideo");
    const uploadSection = document.getElementById("uploadSection");
    const recordSection = document.getElementById("recordSection");
    const videoUploadInput = document.getElementById("videoUpload");
    const recordButton = document.getElementById("recordButton");
    const stopRecordButton = document.getElementById("stopRecordButton");
    const cameraPreview = document.getElementById("cameraPreview");
    const durationDisplay = document.getElementById("durationDisplay");

    let mediaRecorder;
    let recordedChunks = [];
    let startTime;
    let durationInterval;

    // Toggle visibility based on radio button selection
    uploadDefaultRadio.addEventListener("change", function() {
        if (uploadDefaultRadio.checked) {
            uploadSection.style.display = "block";
            recordSection.style.display = "none";
            stopRecording();
        }
    });

    recordVideoRadio.addEventListener("change", function() {
        if (recordVideoRadio.checked) {
            uploadSection.style.display = "none";
            recordSection.style.display = "block";
        }
    });

    // Start recording video
    recordButton.addEventListener("click", startRecording);

    // Stop recording video
    stopRecordButton.addEventListener("click", stopRecording);

    // Handle video recording
    function startRecording() {
        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then(function(stream) {
                cameraPreview.srcObject = stream;
                mediaRecorder = new MediaRecorder(stream);
                recordedChunks = [];
                startTime = Date.now();
                durationInterval = setInterval(updateDuration, 1000);
                mediaRecorder.ondataavailable = function(event) {
                    recordedChunks.push(event.data);
                };
                mediaRecorder.onstop = function() {
                    clearInterval(durationInterval);
                    const recordedBlob = new Blob(recordedChunks, { type: 'video/webm' });
                    const recordedUrl = URL.createObjectURL(recordedBlob);
                    const recordedDuration = Math.ceil((Date.now() - startTime) / 1000);
                    durationDisplay.textContent = `Recorded Duration: ${recordedDuration} seconds`;
                    cameraPreview.srcObject = null;
                    cameraPreview.src = recordedUrl;
                    cameraPreview.controls = true;
                };
                mediaRecorder.start();
                recordButton.style.display = "none";
                stopRecordButton.style.display = "block";
            })
            .catch(function(error) {
                console.error('Error accessing the camera:', error);
            });
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            clearInterval(durationInterval);
            recordButton.style.display = "block";
            stopRecordButton.style.display = "none";
        }
    }

    function updateDuration() {
        const recordedDuration = Math.ceil((Date.now() - startTime) / 1000);
        durationDisplay.textContent = `Recording Duration: ${recordedDuration} seconds`;
    }
});


//audio recording
document.addEventListener("DOMContentLoaded", function() {
  const uploadDefaultRadio = document.getElementById("uploadDefault");
  const recordAudioRadio = document.getElementById("recordAudio");
  const uploadSection = document.getElementById("uploadSection");
  const recordSection = document.getElementById("recordSection");
  const audioUploadInput = document.getElementById("audioUpload");
  const recordButton = document.getElementById("recordButton");
  const stopRecordButton = document.getElementById("stopRecordButton");
  const audioPreview = document.getElementById("audioPreview");
  const durationDisplay = document.getElementById("durationDisplay");

  let mediaRecorder;
  let audioChunks = [];
  let startTime;

  // Toggle visibility based on radio button selection
  uploadDefaultRadio.addEventListener("change", function() {
      if (uploadDefaultRadio.checked) {
          uploadSection.style.display = "block";
          recordSection.style.display = "none";
          stopRecording();
      }
  });

  recordAudioRadio.addEventListener("change", function() {
      if (recordAudioRadio.checked) {
          uploadSection.style.display = "none";
          recordSection.style.display = "block";
      }
  });

  // Start recording audio
  recordButton.addEventListener("click", startRecording);

  // Stop recording audio
  stopRecordButton.addEventListener("click", stopRecording);

  // Handle audio recording
  function startRecording() {
      navigator.mediaDevices.getUserMedia({ audio: true })
          .then(function(stream) {
              mediaRecorder = new MediaRecorder(stream);
              startTime = Date.now();
              durationDisplay.textContent = "Recording...";
              mediaRecorder.ondataavailable = function(event) {
                  audioChunks.push(event.data);
              };
              mediaRecorder.onstop = function() {
                  const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                  const audioUrl = URL.createObjectURL(audioBlob);
                  audioPreview.src = audioUrl;
                  const recordedDuration = Math.ceil((Date.now() - startTime) / 1000);
                  durationDisplay.textContent = `Recorded ${recordedDuration} seconds`;
              };
              mediaRecorder.start();
              recordButton.style.display = "none";
              stopRecordButton.style.display = "block";
          })
          .catch(function(error) {
              console.error('Error accessing the microphone:', error);
          });
  }

  function stopRecording() {
      if (mediaRecorder && mediaRecorder.state !== 'inactive') {
          mediaRecorder.stop();
          recordButton.style.display = "block";
          stopRecordButton.style.display = "none";
      }
  }
});
