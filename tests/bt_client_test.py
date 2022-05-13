from bluedot.btcomm import BluetoothClient
from time import sleep

def RX(data):
	print('Recieved response: "{}"'.format(data))

print('Connecting...')
c = BluetoothClient('vcrc_car', RX, device='/org/bluez/hci0')
print('Connected!')

c.send('HELLO FORM RPI BT!\r\n')

print('Waiting responses:')
while(True): sleep(1)

