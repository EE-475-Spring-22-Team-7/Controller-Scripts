from bluedot.btcomm import BluetoothClient
from cmd_struct import pack_cmd

SSID = 'vcrc_car'
BT_DEV = '/org/bluez/hci0'


bt_client = None

def connect(log):
    global bt_client
    try:
        if bt_client == None or (not bt_client.connected):
            log.info('Connection to RC car...')
            bt_client = BluetoothClient(SSID, data_rx, device=BT_DEV, encoding=None)
            log.info('Connection established to RC Car.')
        return True
    except Exception as e:
        log.info(f'BT connection failed. Exception: "{e}"')
        return False

def data_rx(data):  log.info(f'Recieved BT data: "{data}"')

def send(data, log):
    global bt_client
    if connect(log):
        try:
            cmd = pack_cmd(*data)
            log.info(f'Sending data to RC car: "{cmd.hex(":")}"')
            bt_client.send(cmd)
            return True
        except Exception as e:
            log.info(f'BT Send failed: {e}')
    return False

def main():
    send('move_forward', 3.0)
    log.info('Done!')

if __name__ == '__main__':
    import logging, sys, os
    handler = logging.StreamHandler(stream=sys.stdout)
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    log.addHandler(handler)
    main()
