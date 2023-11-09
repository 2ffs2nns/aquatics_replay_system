# aquatics_replay_system

Video system based on Raspberry Pi to record and playback starts and turns.

## Startup

Decided to use `/etc/xdg/lxsession/LXDE-pi/autostart` as the startup config.

```bash
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi

@xset s off
@xset -dpms
@xset s noblank
@unclutter -idle 0

@/usr/bin/python /home/vjo/main.py &
@/usr/bin/python /home/vjo/run_chromium.py
```

## Requirements

Using Flask and OpenCV. Here is the `requirements.txt` file.

```bash
flask
flask-socketio
opencv-python==4.5.3.56
numpy
```

## Usage

Connect the raspberry pi to a TV via HDMI and a usb webcam.

Connect to the webserver and coaches page on your phone/mobile device. ie `http://192.168.1.10:5000/coaches`

The `record` button will record the livestream for a default of 5secs.
The `reset` button will return to the livestream view.
The `replay` button will replay the last recorded video.
