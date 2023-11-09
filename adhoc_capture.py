import cv2
import os
import glob
import time
import shutil

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


def get_current_time(start_time):
    current = round(time.time())
    diff = round(current - start_time)
    return diff


def setup_camera():
    print("[INFO] starting cv2.VideoCapture(0)")
    cap = cv2.VideoCapture(0)
    # 1080p
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # 720p
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    print("init size: %s" % int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("fps: %s" % int(cap.get(cv2.CAP_PROP_FPS)))

    return cap


def play_recorded_video(replay_file):
    cap = cv2.VideoCapture(replay_file)

    return cap


def start_video(cap, duration=5, start=True):
    print("[INFO] in setup_video, duration=%s" % duration)
    replay_file_path = "%s/replays" % SCRIPT_PATH
    if not os.path.exists(replay_file_path):
        os.mkdir(replay_file_path)

    if start:
        size = (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )

        start_time = round(time.time())
        print("[INFO] %s starting new video_out" % start_time)
        replay_file = "replay-%s.mp4" % start_time

        # ffmpeg -codecs
        fourcc = cv2.VideoWriter_fourcc(*"avc1")
        video_out = cv2.VideoWriter("replays/" + replay_file, fourcc, 30, size)
        recording = True

        while recording:
            ret, frame = cap.read()
            # flipped/mirrored
            #flipped = cv2.flip(frame,1)
            video_out.write(frame)

            diff = get_current_time(start_time)
            if diff >= duration:
                print("[INFO] %s releasing video_out" % start_time)
                video_out.release()
                recording = False

        return replay_file
