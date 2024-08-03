import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyautogui
import cv2
import numpy as np
import threading

class ScreenRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")
        self.root.geometry("550x450")
        
        self.is_recording = False
        self.is_paused = False

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 12))

        self.start_button = ttk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=10)

        self.pause_button = ttk.Button(root, text="Pause Recording", command=self.pause_recording)
        self.pause_button.pack(pady=10)

        self.resume_button = ttk.Button(root, text="Resume Recording", command=self.resume_recording)
        self.resume_button.pack(pady=10)

        self.save_button = ttk.Button(root, text="Save Recording", command=self.save_recording)
        self.save_button.pack(pady=10)

        self.info_label = ttk.Label(root, text="")
        self.info_label.pack(pady=10)

        self.frames = []
        self.recording_thread = None

    def start_recording(self):
        if self.is_recording:
            messagebox.showwarning("Warning", "Recording is already in progress.")
            return
        self.is_recording = True
        self.is_paused = False
        self.frames = []
        self.recording_thread = threading.Thread(target=self.record_screen)
        self.recording_thread.start()
        self.info_label.config(text="Recording...")

    def stop_recording(self):
        if not self.is_recording:
            messagebox.showwarning("Warning", "No recording in progress.")
            return
        self.is_recording = False
        self.recording_thread.join()
        self.info_label.config(text="Recording stopped.")

    def pause_recording(self):
        if not self.is_recording:
            messagebox.showwarning("Warning", "No recording in progress.")
            return
        if self.is_paused:
            messagebox.showwarning("Warning", "Recording is already paused.")
            return
        self.is_paused = True
        self.info_label.config(text="Recording paused.")

    def resume_recording(self):
        if not self.is_recording:
            messagebox.showwarning("Warning", "No recording in progress.")
            return
        if not self.is_paused:
            messagebox.showwarning("Warning", "Recording is not paused.")
            return
        self.is_paused = False
        self.info_label.config(text="Recording resumed.")

    def record_screen(self):
        while self.is_recording:
            if not self.is_paused:
                screenshot = pyautogui.screenshot()
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)
                self.frames.append(frame)

    def save_recording(self):
        if not self.frames:
            self.info_label.config(text="No recording to save.")
            messagebox.showwarning("Warning", "No recording to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
        if not file_path:
            return

        height, width, _ = self.frames[0].shape
        video_writer = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'XVID'), 10, (width, height))

        for frame in self.frames:
            video_writer.write(frame)

        video_writer.release()
        self.info_label.config(text=f"Recording saved to {file_path}")
        messagebox.showinfo("Info", f"Recording saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorder(root)
    root.mainloop()
