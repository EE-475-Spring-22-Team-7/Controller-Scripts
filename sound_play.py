
import pyaudio, wave, struct
from threading import Thread

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

    data = wf.readframes(CHUNK)
    while data != b'':
        # Convert data to ints
        data_in_int = struct.unpack(str(len(data)//2)+'h', data)
        
        # Process data (attenuate)
        data_out_int = []    
        for i in range(len(data_in_int)):
            data_out_int.append(data_in_int[i] // atten)
        
        # Convert back to bytes for output
        data_out_bytes = b''
        for samp in data_out_int:
            data_out_bytes += struct.pack('h',samp)    
        # Srite data
        stream.write(data_out_bytes, exception_on_underflow=True)
        # Read next data
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()