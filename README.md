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
numpy>=1.20
cvxpy>=1
psutils
```

## Usage

Connect the raspberry pi to a TV via HDMI and a usb webcam.

Connect to the webserver and coaches page on your phone/mobile device. ie `http://10.42.0.1:8000/coaches`

The `record` button will record the livestream for a default of 5secs.
The `reset` button will return to the livestream view.
The `replay` button will replay or continue to play the last recorded video/paused video.
The `pause` button will pause the last recorded video.

## Configuration

A `config.ini` file is available to set some defaults. TBD when/if the UI will be able to modify the default settings.

```bash
[DEFAULT]
host_port = 8000
replay_wait_duration = 0
replay_duration = 2
replay_playback_rate = 0.25
```
