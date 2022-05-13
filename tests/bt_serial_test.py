import serial
from time import sleep

ser = serial.Serial('/dev/ttyS0', 9600, bytesize=8, timeout=0.5);
ser.write(b'AT')
sleep(0.5)

print('Got serial response "{r}"'.format(r=str(ser.read(64))))

# For minicom serial connection, run "minicom -D /dev/ttyS0 -b 9600"

