import numrosa
import pyaudio
import wave 
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5 
THRESHOLD = 300

audioChannel = pyaudio.PyAudio()

stream = audioChannel.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print("Listening")

try:
    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)

        volume = np.linalg.norm(audio_data)
        
        if volume > THRESHOLD:
            print("Sound detected! Volume:", int(volume))
        else:
            print("No Sound")  
except KeyboardInterrupt:
            print("Stopping")

stream.stop_stream()
stream.close()
p.terminate()
