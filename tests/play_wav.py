"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys
import struct

CHUNK = 512

ATTEN_FACTOR = 4

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                # output_device_index=11,
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)


data = wf.readframes(CHUNK)

print('### PLAYBACK STARTED!')
while data != b'':
    # Convert data to ints
    data_in_int = struct.unpack(str(len(data)//2)+'h', data)
    
    # Process data (attenuate)
    data_out_int = []    
    for i in range(len(data_in_int)):
        data_out_int.append(data_in_int[i] // ATTEN_FACTOR)
    
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
print('### PLAYBACK STOPPED.')

p.terminate()
