import time
import cv2
import json
import pathlib
import datetime
import os
import numpy as np

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
"""
pip freeze > requirements.txt
pyinstaller --onefile --clean --icon=icon.ico StreamToFrame.py
"""

if __name__ == '__main__':
    try:
        with open("config.json", 'r') as fp:
            config = json.load(fp)
        rtsp = config["rtsp"]
        image_path = config["ImagePath"]
        video_path = config["VideoPath"]
        save_image = config["SaveImage"]
        save_video = config["SaveVideo"]
        interval = int(config["interval"])

        pathlib.Path(image_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(video_path).mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(rtsp, cv2.CAP_FFMPEG)

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_name = filename = os.path.join(video_path,
                                             datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3] + ".avi")
        out = cv2.VideoWriter(video_name, fourcc, 30.0, (frame_width, frame_height))
        starttime = time.time()
        starttime_live = time.time()
        while True:
            result, image = cap.read()
            if result:
                datetime_now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]
                filename = os.path.join(image_path, datetime_now + ".png")
                now = time.time()
                if (now - starttime) * 1000 > interval:
                    starttime = now
                    if save_image is True:
                        cv2.imwrite(filename, image)
                if (now - starttime_live) * 1000 > 1000:
                    starttime_live = now
                    print(f"Datetime now: {datetime_now}")
                if save_video is True:
                    out.write(image)
            else:
                print("Cannot read and save frame")
    except Exception as e:
        print("Cannot start program")
        print(e)
