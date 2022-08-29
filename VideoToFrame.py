import cv2
import easygui
import tkinter as tk
from tkinter import filedialog
import os
import pathlib

"""
pip freeze > requirements.txt
pyinstaller --onefile --clean --icon=icon.ico VideoToFrame.py
"""

root = tk.Tk()
root.withdraw()
try:
    video_path = filedialog.askopenfilename(title="Select a video file",
                                            filetypes=[("Video", ".avi"), ("Video", ".mp4"), ("Video", ".mkv"),
                                                       ("All Files", ".*")])
    head, tail = os.path.split(video_path)
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    interval = easygui.enterbox(f"Select interval you want to get image (second)?")
    int_interval = int(interval)
    save_dir = filedialog.askdirectory(title="Select save frame folder?", )
    save_dir = os.path.join(save_dir.replace("/", "\\"), tail + "_frame")
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
    EXTENSION = ".png"
    curr_frame = 0
    image_count = 0
    count = 0
    frame_catch = fps * int_interval
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_catch == 0:
            name = os.path.join(save_dir, f"{image_count:04d}{EXTENSION}")
            cv2.imwrite(name, frame)
            print(f'Successfully written at {int_interval}s')
            image_count += int_interval
        count += 1
    cap.release()
except Exception as e:
    print("Cannot start program")
    print(e)
