import pyaudio, wave, struct
from threading import Thread
import array

CHUNK = 512

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
        # Process data: attenuate
        for i in range(len(data)):
            data[i] = int(data[i] / atten)

        # Write out data
        stream.write(data.tobytes(), exception_on_underflow=False)

        # Get next data chunk
        data = array.array('h')
        data.frombytes(wf.readframes(CHUNK))

    stream.stop_stream()
    stream.close()
    p.terminate()
