from bluedot.btcomm import BluetoothClient
from time import sleep
from cmd_struct import pack_cmd

def data_rx(data):
	print(f'Recieved response: "{data}"')

print('Connecting...')
c = BluetoothClient('vcrc_car', data_rx, 
	device='/org/bluez/hci0', encoding=None) # Sending bytes!
print('Connected!')

cmd = pack_cmd('move_backward', 3.0)
c.send(cmd)
print(f'cmd "{cmd.hex(":")}" sent!')

try: 
	print('(Hit ctrl+C to stop...)')
	while True: sleep(1)
except KeyboardInterrupt: print()
c.disconnect()
