#!/usr/bin/env python3 

# Top Level RC Car Controller Script

from time import sleep
import json
import speech_recognition as sr

from sound_play import *

# Microphone audio device name
MIC_DEVICE_NAME = 'USB PnP Audio Device'

# Wit API Key
#API_KEY='NZBO2AMYDUSMDX2BI7POKYA3BGVSEHPU' # Version 1
#API_KEY='MT5MPJBOAEZEKIWJU2POKXAGU5V2ILTQ' # Version 2
API_KEY='3X2AUX3KXFN63HOMNOKIGHG2LUHRUH3T' # Version 2.1

CONF_THRESH = 0.4

DEFAULT_DIST = 3 # feet
DEFAULT_ROTATION = 45 # degrees

def wit_recognize_callback(recognizer, audio):
    background_play('./sounds/ding.wav', 1)
    print('interpreting speech...')
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        result = recognizer.recognize_wit(audio, key=API_KEY, show_all=True)
        print('Wit response:')
        print(json.dumps(result, indent=2))
        #print(result)
        print()
        success = interpret_wit_result(result)
        # Play sounds!
        if success:
            foreground_play('./sounds/fast-happy-ding.wav');
        else:
            foreground_play('./sounds/sad-dings.wav');
    except sr.UnknownValueError as e:
        handle_sr_value_error(e)
    except sr.RequestError as e:
        handle_api_req_error(e)

def handle_sr_value_error(err):
    print("Wit could not understand audio")
    foreground_play('./sounds/buzz-ding.wav')

def handle_api_req_error(err):
    print("Could not request results from Wit service: {0}".format(err))
    foreground_play('./sounds/buzz-ding.wav')

def interpret_wit_result(d):
    try:
        if not 'intent' in d['entities']:
            print('ERROR: No intent result')
            return False
        if d['entities']['intent'][0]['confidence'] < CONF_THRESH:
            print('ERROR: intent confidence low')
            return False
        cmd_intent = d['entities']['intent'][0]['value']

        if 'speed' in d['entities']:
            if d['entities']['speed'][0]['confidence'] >= CONF_THRESH:
                val = d['entities']['speed'][0]['value'].upper()
                print('>>> RC COMMAND >>>   UPDATE TO {} SPEED'.format(val))
        
        if cmd_intent == 'move_forward':
            distance = DEFAULT_DIST
            if 'distance' in d['entities']:
                distance = handle_distance(d['entities']['distance'][0])
            if distance == None:
                print('ERROR: invalid distance')
                return False
            print('>>> RC COMMAND >>>   MOVE FORWARD {} FEET'.format(distance))
        
        elif cmd_intent == 'move_backward':
            distance = DEFAULT_DIST
            if 'distance' in d['entities']:
                distance = handle_distance(d['entities']['distance'][0])
            if distance == None:
                print('ERROR: invalid distance')
                return False
            print('>>> RC COMMAND >>>   MOVE BACKWARD {} FEET'.format(distance))
        
        elif cmd_intent == 'rotate_right':
            angle = DEFAULT_ROTATION
            if 'angle' in d['entities']:
                angle = handle_angle(d['entities']['angle'][0])
            if angle == None:
                print('ERROR: invalid angle')
                return False
            print('>>> RC COMMAND >>>   ROTATE RIGHT {} DEGREES'.format(angle))
        
        elif cmd_intent == 'rotate_left':
            angle = DEFAULT_ROTATION
            if 'angle' in d['entities']:
                angle = handle_angle(d['entities']['angle'][0])
            if angle == None:
                print('ERROR: invalid angle')
                return False
            print('>>> RC COMMAND >>>   ROTATE LEFT {} DEGREES'.format(angle))
        
        elif cmd_intent == 'rotate_back':
            print('>>> RC COMMAND >>>   ROTATE LEFT {} DEGREES'.format(180))
        
        elif cmd_intent == 'cancel':
            print('>>> RC COMMAND >>>   CANCEL')
        
        elif cmd_intent == 'continue':
            print('>>> RC COMMAND >>>   CONTINUE')
        
        else:
            print('ERROR: intent "{}" not recognized'.format(cmd_intent))

        return True

    except KeyError as e:
        print('result dictionary key error: "{}"'.format(e))
        return False

def handle_distance(d):
    if d['confidence'] < CONF_THRESH:
        print('ERROR: distance confidence low')
        return None
    value = d['value']
    if d['unit'] == 'foot':
        pass # 1 foot in a foot :)
    elif d['unit'] == 'inch':
        value /= 12 # 12 inches in a foot
    else:
        print('ERROR: invalid distance unit "{}"'.format(d['unit']))
        return None
    return round(value, 1) # Round to 0.1 feet

def handle_angle(d):
    if d['confidence'] < CONF_THRESH:
        print('ERROR: distance confidence low')
        return None
    try:
        value = int(d['value']) # Directly convert to int
    except: 
        return None
    return round(value) # Round to 1 degree for now


def initialize_recognizer():
    #print("# LIST MICROPHONES")
    device_idx = None
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        #print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
        if MIC_DEVICE_NAME == name[:len(MIC_DEVICE_NAME)]: # If start of device name matches name string
            device_idx = index
            break
    assert device_idx, 'Audio Device with name prefix "{}" not found'.format(MIC_DEVICE_NAME)
    
    r = sr.Recognizer()    
    m = sr.Microphone(device_index=device_idx)
    m.CHUNK = 512 # Set chunk size (RPi has trouble with sizes larger than this)

    # Audio calibration
    with m as source:
        r.adjust_for_ambient_noise(source)
    r.dynamic_energy_threshold = False
    r.energy_threshold = 130
    #r.operation_timeout = 3.0

    print('Mic index = {mi}, detection threshold = {th}'.format(mi=device_idx, th=r.energy_threshold))
    return (r, m)

def main():
    try:
        (r, m) = initialize_recognizer()
        foreground_play('./sounds/happy-ding-2.wav')
        print('listening started...')    
        stop_listening = r.listen_in_background(m, wit_recognize_callback) # start listening in the background
        # "stop_listening" is now a function that, when called, stops background listening
        
        ### MAIN CONTOL LOOP
        while True: sleep(0.1) # Do nothing
        ###

    except KeyboardInterrupt:
        print()
        stop_listening(wait_for_stop=False)
        print('listening stopped.')
        background_play('./sounds/buzz-ding.wav', 1.5)
        sleep(1) # wait for things to close
        exit(0)
    except:
        # Some unexpected error! Crash!
        foreground_play('./sounds/breaking-glass.wav')
        exit(1)

if __name__ == '__main__':
    main()
