#!/usr/bin/python
from threading import Lock
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from adhoc_capture import start_video
from adhoc_capture import setup_camera
from adhoc_capture import play_recorded_video
from prep_ip import get_ip
import cv2
import fcntl
import glob
import os
import time

def del_old_videos():
    try:
        print("[INFO] deleting old videos")
        files = glob.glob('%s/replays/*.mp4' % SCRIPT_PATH)
        for f in files:
            os.remove(f)

    except Exception as e:
        print("[ERROR] deleting old_videos")
        print(e)


def lock_camera():
    lock_file = open("/tmp/vasta.lock", "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # If we acquire the lock, execute the method
        return setup_camera()
    except BlockingIOError:
        # Lock is already held by another worker, skip execution
        pass
    finally:
        lock_file.close()

# threading seems to work better than None
async_mode = 'threading'

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
HOST_IP = get_ip()
HOST_PORT = '8000'
REPLAY_WAIT_DURATION = 2
REPLAY_DURATION = 4.5
REPLAY_PLAYBACK_RATE = 0.25
thread = None
thread_lock = Lock()
app = Flask(__name__, static_folder=SCRIPT_PATH + '/replays')
socketio = SocketIO(app, async_mode=async_mode)
camera = lock_camera()

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # replace frame with flipped to mirror
            #flipped = cv2.flip(frame,1)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/coaches")
def coaches():
    return render_template("coaches.html", async_mode=socketio.async_mode)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def index():
    return render_template("index.html", async_mode=socketio.async_mode)

@socketio.on("record_message")
def handle_broadcast(data):
    recording_img = "<img id=\"video\" width=\"75%\" src=\"replays/css/recording1.png\">"
    emit("record_response", {"data": recording_img }, broadcast=True)
    replay_filename = start_video(camera, REPLAY_DURATION)
    print('created replay: %s' % replay_filename)
    time.sleep(REPLAY_WAIT_DURATION)

    vsettings = '<video id="video" width="77%"'
    vsrc = ' src="http://%s:%s/replays/%s" controls muted></video>' % (HOST_IP, HOST_PORT, replay_filename)
    jsscript = """
    <script id="replay" type="text/javascript">
    document.getElementById("video").defaultPlaybackRate = %s;
    document.getElementById("video").playbackRate = %s;
    document.getElementById("video").play();
    </script>
    """ % (REPLAY_PLAYBACK_RATE, REPLAY_PLAYBACK_RATE)
    emit("record_response", {"data": vsettings + vsrc + jsscript}, broadcast=True)

@socketio.on("reset_message")
def handle_reset_broadcast(data):
    print('resetting page...')
    emit("reset_response", {"data": "reset sent"}, broadcast=True)

@socketio.on("replay_message")
def handle_replay_broadcast(data):
    print('replaying video...')
    emit("replay_response", {"data": "replay sent"}, broadcast=True)

@socketio.on("pause_message")
def handle_pause_broadcast(data):
    print('pausing video...')
    emit("pause_response", {"data": "pause sent"}, broadcast=True)


if __name__ == "__main__":
    del_old_videos()
    HOST_IP = get_ip()
    socketio.run(app, port=HOST_PORT, host=HOST_IP, allow_unsafe_werkzeug=True)
