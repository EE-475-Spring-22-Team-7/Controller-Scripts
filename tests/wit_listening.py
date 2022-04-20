#NOTE: this example requires PyAudio because it uses the Microphone class

from time import sleep
import json

import speech_recognition as sr

MIC_DEVICE_NAME = 'USB PnP Audio Device'

API_KEY='NZBO2AMYDUSMDX2BI7POKYA3BGVSEHPU'

# this is called from the background thread
def callback(recognizer, audio):
    print('recognizing...')
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        result = recognizer.recognize_wit(audio, key=API_KEY, show_all=True)
        print('Wit response:')
        print(json.dumps(result, indent=2))
        #print(result)
        print()
    except sr.UnknownValueError:
        print("Wit could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit service; {0}".format(e))


#print("# LIST MICROPHONES")
device_idx = None
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    if MIC_DEVICE_NAME == name[:len(MIC_DEVICE_NAME)]: device_idx = index
assert device_idx, 'Audio Device with name "{}" not found'.format(MIC_DEVICE_NAME)

r = sr.Recognizer()
m = sr.Microphone(device_index=device_idx)
m.CHUNK = 512

print('RATE = {r}, CHUNK = {c}'.format(r=m.SAMPLE_RATE, c=m.CHUNK))

# Calibration
with m as source:
    r.adjust_for_ambient_noise(source)
#r.energy_threshold = 120
r.dynamic_energy_threshold = False
#r.operation_timeout = 3.0
print('Mic index = {mi}, detection threshold = {th}'.format(mi=device_idx, th=r.energy_threshold))

print('listenig started...')
# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

try:
    while True: sleep(0.1)
except KeyboardInterrupt:
    stop_listening(wait_for_stop=False)
    print('\nlistening stopped.')
    for _ in range(10): sleep(0.1)


