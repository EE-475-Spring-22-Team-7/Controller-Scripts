import pyaudio

p = pyaudio.PyAudio()

# List all audio devices
print()
print('### AUDIO DEVICES: ')
for i in range(p.get_device_count()):
    print(str(i)+': ', p.get_device_info_by_index(i)['name'],
          ' input chans = '+str(p.get_device_info_by_index(i)['maxInputChannels']),
          ' output chans = '+str(p.get_device_info_by_index(i)['maxOutputChannels']),
          ' SR = '+str(p.get_device_info_by_index(i)['defaultSampleRate']))
print()
