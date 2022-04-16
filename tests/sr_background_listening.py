# NOTE: this example requires PyAudio because it uses the Microphone class

import time

import speech_recognition as sr


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

mic_idx = 2

r = sr.Recognizer()
m = sr.Microphone(device_index=mic_idx)
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

r.energy_threshold = 120
r.operation_timeout = 3.0
r.dynamic_energy_threshold = False
print('Mic index = {mi}, detection threshold = {th}'.format(mi=mic_idx, th=r.energy_threshold))
print('listenig started...')

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
stop_listening(wait_for_stop=False)

# do some more unrelated things
while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping
