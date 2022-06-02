# RC Car Controller Scripts
Python scripts for the Controller (RaspberryPi) of the remote controlled RC car project.

These scripts have only been tested on a RaspberryPi 4.

## Instalation
To install the controller scripts on a fresh RaspberryPi (Rpi) first install the dependancies:
```
# (Good practice to update all currently installed packages)
sudo apt update
# Install software dependances for the scripts
sudo apt install python3-pyaudio swig libpulse-dev libasound2-dev flac bluetooth pi-bluetooth bluez blueman
# Install required Python libraries
pip install SpeechRecognition google-api-python-client
```

## Configure Audio
For the audo input, plug in a USB microphone. Within the script, the audio device is connected to by name. 
The name of the audio device to use can be set in the main script with the variable `MIC_DEVICE_NAME`. 
If the name of your microphone is unknown, plug it in, and run the script `tests/print_devices.py`. 
All connected audio devices will be printed out.

For the audio output, the default will be the audio connection over the Mini-HDMI display connection. 
We decided it was more convenient to use the analog audio output. 
The audio output for the RPi can be configured with the command `sudo raspi-config`. 
Navigate the menus to: System options -> Audio -> 0 Headphones

## Configure bluetooth
The blueman "Bluetooth Manager" program is required to make the first time connection to the RC car (assuming you are using the HC-05/HC-06 module).
First, you need to know the ssid and passphrase of the bluetooth module on the RC Car. 
(These are easy to set from the serial connection side of the module.) Use blueman to create a new connection to the module. 
It will probabaly say connection failed, but this is okay. Now try one of the BT test scripts: `RC_car_bt.py`. 
If it finishes without error, the connection was a success. 
If the Bluetooth module is something other than "vcrc_car", you can change the name by setting the `SSID` variable in that script.

## Running
Simply run `./main.py` or `python3 main.py`

## Enable Automatic Start
One useful feature is to have the script `main.py` automatically start when the RPi boots. 
This can easialy be implemented with Systemd.

First you have to add a "unit file" so Systemd knows about your script.
We have included a template unit file: `rc_control.service`. To add it to Systemd, copy it to the directory `/etc/systemd/system`.
You will also need to replace instances of "<THIS_DIR>" in the unit file to the directory of `main.py`. 

Finally, enable the service to start on boot. Run:
```
# Enable the "detect network interface up" services
systemctl enable systemd-networkd.service systemd-networkd-wait-online.service
# Enable the controller script service
systemctl enable rc_control
```

When next booted, the script should be running in the background.
To interact with it, use any of the systemctl commands for example:
```
systemctl status rc_control # (Shows the state of the program and print out some of the most recent log)
systemctl stop rc_control
systemctl start rc_control
systemctl restart rc_control
systemctl disable rc_control # (disables start on boot)
```
