import pyaudio
import wave
import sys

MIC_DEVICE_NAME = 'USB PnP Audio Device'

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

# Find audio device index
device_idx = None
for i in range(p.get_device_count()):
    if MIC_DEVICE_NAME == p.get_device_info_by_index(i)['name'][:len(MIC_DEVICE_NAME)]:
        device_idx = i
assert device_idx, 'Audio Device with name "{}" not found'.format(MIC_DEVICE_NAME)

stream = p.open(format=p.get_format_from_width(WIDTH),
                input_device_index=device_idx,
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
