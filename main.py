#!/usr/bin/env python3 

# Top Level RC Car Controller Script

from time import sleep
import json
import logging, sys, os
import speech_recognition as sr
from bluedot.btcomm import BluetoothClient
from cmd_struct import pack_cmd
import RC_car_bt as bt

# Exit on SIGTERM
import signal
def sigterm_handler(_signo, _stack_frame): exit(0)
signal.signal(signal.SIGTERM, sigterm_handler)

from sound_play import *

# Microphone audio device name
MIC_DEVICE_NAME = 'USB PnP Audio Device'

# Wit API Key
#API_KEY='NZBO2AMYDUSMDX2BI7POKYA3BGVSEHPU' # Version 1
#API_KEY='MT5MPJBOAEZEKIWJU2POKXAGU5V2ILTQ' # Version 2
API_KEY='3X2AUX3KXFN63HOMNOKIGHG2LUHRUH3T' # Version 2.1

CONF_THRESH = 0.4

DEFAULT_DIST = 3 # feet
DEFAULT_ROTATION = 90 # degrees

# Defile logger
handler = logging.StreamHandler(stream=sys.stdout)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(handler)

def wit_recognize_callback(recognizer, audio):    
    background_play('./sounds/ding.wav')
    log.info('interpreting speech...')
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        result = recognizer.recognize_wit(audio, key=API_KEY, show_all=True)
        log.info('Wit response:')
        log.info(json.dumps(result, indent=2))
        #log.info(result)
        log.info('')
        cmd_result = interpret_wit_result(result)
        if cmd_result:
            # success = bt_send(cmd_result)
            success = bt.send(cmd_result, log)

        # Play sounds!
        if cmd_result and success:
            foreground_play('./sounds/fast-happy-ding.wav');
        else:
            foreground_play('./sounds/sad-dings.wav');
    except sr.UnknownValueError as e:
        handle_sr_value_error(e)
    except sr.RequestError as e:
        handle_api_req_error(e)

def handle_sr_value_error(err):
    log.info("Wit could not understand audio")
    foreground_play('./sounds/buzz-ding.wav')

def handle_api_req_error(err):
    log.info("Could not request results from Wit service: {0}".format(err))
    foreground_play('./sounds/buzz-ding.wav')

def interpret_wit_result(d):
    try:
        if not 'intent' in d['entities']:
            log.info('ERROR: No intent result')
            return None
        if d['entities']['intent'][0]['confidence'] < CONF_THRESH:
            log.info('ERROR: intent confidence low')
            return None
        cmd_intent = d['entities']['intent'][0]['value']

        speed_cmd = None
        if 'speed' in d['entities']:
            if d['entities']['speed'][0]['confidence'] >= CONF_THRESH:
                val = d['entities']['speed'][0]['value'].upper()
                log.info('>>> RC COMMAND >>>   UPDATE TO {} SPEED'.format(val))
                speed_cmd = val.lower()+'_speed'
        
        cmd_type = None
        cmd_val = None
        if cmd_intent == 'move_forward':
            distance = DEFAULT_DIST
            if 'distance' in d['entities']:
                distance = handle_distance(d['entities']['distance'][0])
            if distance == None:
                log.info('ERROR: invalid distance')
                return None
            log.info('>>> RC COMMAND >>>   MOVE FORWARD {} FEET'.format(distance))
            cmd_type = 'move_forward'
            cmd_val = distance
        
        elif cmd_intent == 'move_backward':
            distance = DEFAULT_DIST
            if 'distance' in d['entities']:
                distance = handle_distance(d['entities']['distance'][0])
            if distance == None:
                log.info('ERROR: invalid distance')
                return None
            log.info('>>> RC COMMAND >>>   MOVE BACKWARD {} FEET'.format(distance))
            cmd_type = 'move_backward'
            cmd_val = distance
        
        elif cmd_intent == 'rotate_right':
            angle = DEFAULT_ROTATION
            if 'angle' in d['entities']:
                angle = handle_angle(d['entities']['angle'][0])
            if angle == None:
                log.info('ERROR: invalid angle')
                return None
            log.info('>>> RC COMMAND >>>   ROTATE RIGHT {} DEGREES'.format(angle))
            cmd_type = 'rotate_right'
            cmd_val = angle
        
        elif cmd_intent == 'rotate_left':
            angle = DEFAULT_ROTATION
            if 'angle' in d['entities']:
                angle = handle_angle(d['entities']['angle'][0])
            if angle == None:
                log.info('ERROR: invalid angle')
                return None
            log.info('>>> RC COMMAND >>>   ROTATE LEFT {} DEGREES'.format(angle))
            cmd_type = 'rotate_left'
            cmd_val = angle
        
        elif cmd_intent == 'rotate_back':
            log.info('>>> RC COMMAND >>>   ROTATE LEFT {} DEGREES'.format(180))
            cmd_type = 'rotate_around'
        
        elif cmd_intent == 'cancel':
            log.info('>>> RC COMMAND >>>   CANCEL')
            cmd_type = 'cancel'
        
        elif cmd_intent == 'continue':
            log.info('>>> RC COMMAND >>>   CONTINUE')
            cmd_type = 'continue'
        
        else:
            log.info('ERROR: intent "{}" not recognized'.format(cmd_intent))

        if cmd_val != None:
            if speed_cmd != None:
                return (cmd_type, cmd_val, speed_cmd)
            return (cmd_type, cmd_val)
        return (cmd_type,)

    except KeyError as e:
        log.info('result dictionary key error: "{}"'.format(e))
        return False

def handle_distance(d):
    if d['confidence'] < CONF_THRESH:
        log.info('ERROR: distance confidence low')
        return None
    value = d['value']
    if d['unit'] == 'foot':
        pass # 1 foot in a foot :)
    elif d['unit'] == 'inch':
        value /= 12 # 12 inches in a foot
    else:
        log.info('ERROR: invalid distance unit "{}"'.format(d['unit']))
        return None
    return round(value, 1) # Round to 0.1 feet

def handle_angle(d):
    if d['confidence'] < CONF_THRESH:
        log.info('ERROR: distance confidence low')
        return None
    try:
        value = int(d['value']) # Directly convert to int
    except: 
        return None
    return round(value) # Round to 1 degree for now


def initialize_recognizer():
    #log.info("# LIST MICROPHONES")
    device_idx = None
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        #log.info("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
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

    log.info('Mic index = {mi}, detection threshold = {th}'.format(mi=device_idx, th=r.energy_threshold))
    return (r, m)

def wait_for_ping(hostname, time=60):
    for i in range(time):
        # Done if hostname can be pinged
        if os.system(f'ping -c 1 {hostname} >> /dev/null') == 0:
            log.info(f'hostname "{hostname}" found after {i+1} tries.')
            return
        sleep(1) # Wait 1 sec between pings
    log.info(f'hostname "{hostname}" could not be pinged for {time} seconds')
    raise Exception # Error if timeout

def main():
    try:
        (r, m) = initialize_recognizer()

        background_play('./sounds/ding.wav')
        wait_for_ping('wit.ai', 120) # Try for 2 minutes to ping wit service
        bt.connect(log) # Connect to Bluetooth if available (OK if doesn't connect)
        foreground_play('./sounds/happy-ding-2.wav') # Connection success


        log.info('listening started...')
        stop_listening = r.listen_in_background(m, wit_recognize_callback) # start listening in the background
        # "stop_listening" is now a function that, when called, stops background listening
        
        ### MAIN CONTOL LOOP
        while True: sleep(0.1) # Do nothing
        ###

    except KeyboardInterrupt: pass # Skips to "finally"
    except Exception as e:
        # Some unexpected error! Crash!        
        foreground_play('./sounds/breaking-glass.wav', 2)
        log.info('### EXCEPTION! : '+str(e))
        os._exit(1) # Exit without "finally"!
    
    finally: # Play the graceful exit sound
        log.info('')
        stop_listening(wait_for_stop=False)
        log.info('listening stopped.')
        background_play('./sounds/buzz-ding.wav', 1.5)
        sleep(1) # wait for things to close        

if __name__ == '__main__':
    main()
