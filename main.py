import pyaudio
import aubio
import numpy as np
import math
import os

from collections import deque

def freq_to_note_name(frequency):

    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    if frequency <= 0:
        return None
    
    midi_note = 69 + 12 * math.log2(frequency / 440.0)
    midi_note = int(round(midi_note))
    octave = (midi_note // 12) - 1
    note_name = NOTE_NAMES[midi_note % 12]
    return f"{note_name}{octave}"

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 5 
THRESHOLD = 700

samplerate = 44100
win_s = 2048          # window size for fft
hop_s = 512    

audioChannel = pyaudio.PyAudio()

stream = audioChannel.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print("Listening")

pitchDetector = aubio.pitch("yinfft", win_s, hop_s, samplerate)
pitchDetector.set_unit("Hz")
pitchDetector.set_silence(-35)

pitchHistory = deque(maxlen=5)

try:
    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)
        audio_data = audio_data.astype(np.float32) / 32768.0
        pitch = pitchDetector(audio_data)[0]
        if pitch > 0:
            pitchHistory.append(pitch)
            smoothedPitch = sum(pitchHistory) / len(pitchHistory)
            note = freq_to_note_name(smoothedPitch)
            os.system("clear")
            print(f"Detected pitch: {pitch:.2f} Hz, Note: {note}")

except KeyboardInterrupt:
            print("Stopping")

stream.stop_stream()
stream.close()
audioChannel.terminate()
