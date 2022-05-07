import pyaudio, wave, struct
from threading import Thread
import array
import sys

CHUNK = 512

MIN_SHORT = -2**15
MAX_SHORT = 2**15-1

def background_play(fname, atten=1):
    t = Thread(target=foreground_play, args=(fname, atten))
    #t.daemon=True
    t.start()

def foreground_play(fname, atten=1):
    wf = wave.open(fname, 'rb')

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    #output_device_index=11,
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
            # data[i] = min( int(data[i] / atten), MIN_SHORT)
            # data[i] = int(data[i] / atten)

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