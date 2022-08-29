import time
import cv2
import json
import pathlib
import datetime
import os

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
        save_path = config["path"]
        interval = int(int(config["interval"]) / 1000)
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
        cap = cv2.VideoCapture(rtsp, cv2.CAP_FFMPEG)
        while True:
            result, image = cap.read()
            if result:
                filename = os.path.join(save_path,
                                        datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3] + ".png")
                cv2.imwrite(filename, image)
                print(f"Saved to: {filename}")
            else:
                print("Cannot read and save frame")
            time.sleep(interval)
    except Exception as e:
        print("Cannot start program")
        print(e)
