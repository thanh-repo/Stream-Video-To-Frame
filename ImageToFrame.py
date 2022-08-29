import cv2
import easygui
import tkinter as tk
from tkinter import filedialog
import os
import pathlib

"""
pip freeze > requirements.txt
pyinstaller --onefile --clean --icon=icon.ico ImageToFrame.py
"""


root = tk.Tk()
root.withdraw()
try:
    video_path = filedialog.askopenfilename(title="Select a video file",
                                            filetypes=[("Video", ".avi"), ("Video", ".mp4"), ("Video", ".mkv"),
                                                       ("All Files", ".*")])
    head, tail = os.path.split(video_path)
    cap = cv2.VideoCapture(video_path)
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    KPS = easygui.enterbox(f"Video source frame per second: {fps}.\nNumber of frame per second do you want to save?")
    save_dir = filedialog.askdirectory(title="Select save frame folder?", )
    save_dir = os.path.join(save_dir.replace("/", "\\"), tail)
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
    EXTENSION = ".png"
    print(f"Video source frame per second: {fps}")
    hop = round(fps / int(KPS))
    curr_frame = 0
    image_count = 0
    while (True):
        ret, frame = cap.read()
        if not ret:
            break
        if curr_frame % hop == 0:
            name = os.path.join(save_dir, f"{image_count:09d}{EXTENSION}")

            cv2.imwrite(name, frame)
            print(f"Save frame at: {curr_frame}")
            image_count += 1
        curr_frame += 1
    cap.release()
except Exception as e:
    print("Cannot start program")
    print(e)
