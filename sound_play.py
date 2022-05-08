import pyaudio, wave, struct
from threading import Thread
import array
import sys

SPEAKER_DEVICE_NAME = 'samplerate' # Honestly, no idea why this is it's name

CHUNK = 512

MIN_SHORT = -2**15
MAX_SHORT = 2**15-1

def background_play(fname, atten=1):
    t = Thread(target=foreground_play, args=(fname, atten))
    #t.daemon=True
    t.start()

def foreground_play(fname, atten=1):
    p = pyaudio.PyAudio()
    # Select audio device by name
    device_idx = None
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i) 
        # print(f'Found device "{dev_info["name"]}"')
        if SPEAKER_DEVICE_NAME == dev_info['name'][:len(SPEAKER_DEVICE_NAME)]:
            device_idx = i
            break
    assert device_idx, f'Audio Device with name prefix "{SPEAKER_DEVICE_NAME}" not found'

    wf = wave.open(fname, 'rb') # Open waveform file

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    output_device_index=device_idx,
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read initial data
    data = array.array('h')
    data.frombytes(wf.readframes(CHUNK))
    while len(data) != 0:
        # Process data: attenuate, and saturate if needed
        for i in range(len(data)):
            data[i] = max(min( int(data[i] / atten), MAX_SHORT), MIN_SHORT)

        # Write out data
        stream.write(data.tobytes(), exception_on_underflow=False)

        # Get next data chunk
        data = array.array('h')
        data.frombytes(wf.readframes(CHUNK))

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        foreground_play(sys.argv[1], float(sys.argv[2]))
    else:
        foreground_play(sys.argv[1])