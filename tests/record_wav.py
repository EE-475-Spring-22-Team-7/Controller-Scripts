import pyaudio
import wave
import sys

MIC_DEVICE_INDEX = 2  # The USB Mic Audio Device index

CHUNK = 512
WIDTH = 2
CHANNELS = 1
RATE = 44100

# ATTEN_FACTOR = 1

if len(sys.argv) < 2:
    print("Records to a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(WIDTH)
wf.setframerate(RATE)

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                input_device_index=MIC_DEVICE_INDEX,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print()
print('### RECORDING STARTED...')
try:
    while True:
        data_in = stream.read(CHUNK, exception_on_overflow=False)
        wf.writeframes(data_in)
except KeyboardInterrupt:
    print('\n### DONE!')
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()