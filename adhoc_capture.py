import cv2
import os
import glob
import time
import shutil
import sys
from subprocess import Popen
from get_cameras import camera_indexes

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


def get_current_time(start_time):
    current = round(time.time())
    diff = round(current - start_time)
    return diff


def setup_camera():
    cameras = camera_indexes()
    main_camera = cameras[0]
    print("[INFO] starting cv2.VideoCapture(%s)" % main_camera)
    cap = cv2.VideoCapture(main_camera)
    print("init size: %s" % int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("fps: %s" % int(cap.get(cv2.CAP_PROP_FPS)))

    return cap


def setup_second_camera():
    cameras = camera_indexes()
    second_camera = cameras[-1]
    print("[INFO] starting cv2.VideoCapture(%s)" % second_camera)
    cap = cv2.VideoCapture(second_camera)
    print("init size: %s" % int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("fps: %s" % int(cap.get(cv2.CAP_PROP_FPS)))

    return cap


def record_ffmpeg(filename, duration=3, camera='/dev/video0'):
    ffmpeg_opts = '-framerate 30 -i %s -video_size 1280x720 -an' % (camera)
    cmd = 'ffmpeg %s -t %s ./replays/%s' % (ffmpeg_opts, duration, filename)
    p = Popen(cmd, shell=True)
    p.wait()

def play_recorded_video(replay_file):
    cap = cv2.VideoCapture(replay_file)

    return cap


def start_main_video(cap, duration=3):
    print("[INFO] in setup_video, duration=%s" % duration)
    replay_file_path = "%s/replays" % SCRIPT_PATH
    if not os.path.exists(replay_file_path):
        os.mkdir(replay_file_path)

    start_time = round(time.time())
    print("[INFO] %s starting new video_out" % start_time)
    replay_file = "replay-%s.mp4" % start_time

    cap.release()
    cameras = camera_indexes()
    camera = '/dev/video' + str(cameras[0])
    record_ffmpeg(replay_file, duration, camera)

    cap.open(cameras[0])

    return replay_file
