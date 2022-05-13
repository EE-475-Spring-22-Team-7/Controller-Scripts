
from bluedot.btcomm import BluetoothClient
from time import sleep

BT_DEVICE = '/org/bluez/hci0' # Raspberry pi bluez device
RC_CAR_BT_NAME = 'vcrc_car'

rc_conn = None

def rc_rx(data):
    log.info('Recieved data "{}" from RC car'.format(data))
    # TODO how do we handle it?


def connect(timeout=10):
    log.info('Connecting to RC car...')
    for i in range(timeout):
        try:    
            rc_conn = BluetoothClient(RC_CAR_BT_NAME, rc_rx, device=BT_DEVICE)
            log.info('Connected to RC car!')
            return True
        except OSError: pass    
    # Return false if connection fails
    log.info('Connection failed!')
    return False


def send_bytes(data):
    try: 
        rc_conn.send(data)
        return
    except Exception as e:
        log.info('Data transmission to car failed. Excpetion: "{}"'.format(e))
    # Try to reconnect, then send if needed
    log.info('Starting reconnect...')
    if connect(1):
        rc_conn.send(data)


def disconnect():
    try:
        rc_conn.disconnect()
    except Exception as e:
        log.info('Disconnection from RC Car failed. Excpetion: "{}"'.format(e))