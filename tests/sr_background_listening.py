#NOTE: this example requires PyAudio because it uses the Microphone class

from time import sleep

import speech_recognition as sr

MIC_DEVICE_NAME = 'USB PnP Audio Device'

# this is called from the background thread
def callback(recognizer, audio):
    print('recognizing...')
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said \"{}\"".format(recognizer.recognize_google(audio)))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

print("# LIST MICROPHONES")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

#print("# LIST MICROPHONES")
device_idx = None
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    if MIC_DEVICE_NAME == name[:len(MIC_DEVICE_NAME)]: device_idx = index
assert device_idx, 'Audio Device with name "{}" not found'.format(MIC_DEVICE_NAME)



r = sr.Recognizer()
m = sr.Microphone(device_index=device_idx)
m.CHUNK = 512
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

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


