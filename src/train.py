import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np
import threading

# Project root (one level up from src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PICTURES_DIR = os.path.join(BASE_DIR, "pictures")
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "src", "models")


class Train:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')
        root.title("Face Recognition Attendance System")

        title_lb1 = tk.Label(self.root, text="TRAIN DATA SET", font=("verdana", 35, "bold"), bg="white", fg="#8b008b")
        title_lb1.place(x=0, y=128, width=1350, height=60)

        img_frame = Frame(self.root, height=150, bd=0, bg="white", highlightthickness=0)
        img_frame.pack(side=TOP, fill=X)
        img_frame.grid_rowconfigure(0, weight=1)
        img_frame.grid_columnconfigure(0, weight=1)
        img_frame.grid_columnconfigure(1, weight=1)
        img_frame.grid_columnconfigure(2, weight=1)

        # img1
        img = Image.open(os.path.join(PICTURES_DIR, "home.png"))
        img = img.resize((510, 150), Image.LANCZOS)
        self.photoimage = ImageTk.PhotoImage(img)
        f_label = Label(img_frame, image=self.photoimage, bd=0, highlightthickness=0)
        f_label.grid(row=0, column=0, sticky="nsew")

        # img2
        img1 = Image.open(os.path.join(PICTURES_DIR, "home.png"))
        img1 = img1.resize((510, 150), Image.LANCZOS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        f_label1 = Label(img_frame, image=self.photoimage1, bd=0, highlightthickness=0)
        f_label1.grid(row=0, column=1, sticky="nsew")

        # img3
        img2 = Image.open(os.path.join(PICTURES_DIR, "home.png"))
        img2 = img2.resize((510, 150), Image.LANCZOS)
        self.photoimage2 = ImageTk.PhotoImage(img2)
        f_label2 = Label(img_frame, image=self.photoimage2, bd=0, highlightthickness=0)
        f_label2.grid(row=0, column=2, sticky="nsew")

        # bg_img
        img3 = Image.open(os.path.join(PICTURES_DIR, "bgimg.jpeg"))
        img3 = img3.resize((1530, 690), Image.LANCZOS)
        self.photoimage3 = ImageTk.PhotoImage(img3)
        bg_img = Label(self.root, image=self.photoimage3, bd=0, highlightthickness=0)
        bg_img.place(x=0, y=150, relwidth=1, relheight=1)

        title_lbl = Label(bg_img, text="TRAIN DATA ", font=("times new roman", 30, "bold"), bg="white", fg="purple", justify="center")
        title_lbl.pack(fill=X)

        img4 = Image.open(os.path.join(PICTURES_DIR, "traindata1.jpeg"))
        img4 = img4.resize((350, 350), Image.LANCZOS)
        self.photoimage4 = ImageTk.PhotoImage(img4)

        b1 = Button(bg_img, image=self.photoimage4, cursor="hand2", command=self.start_training)
        b1.place(x=450, y=100, width=350, height=350)

        b1_1 = Button(bg_img, text="Train Data", cursor="hand2", font=("times new roman", 12, "bold"), bg="royalblue3", fg="white", command=self.start_training)
        b1_1.place(x=527, y=385, width=200, height=50)

        # Progress Bar
        self.progress = ttk.Progressbar(bg_img, orient=HORIZONTAL, length=300, mode="determinate", maximum=100)
        self.status_label = Label(bg_img, text="", font=("Segoe UI", 11, "bold"), bg="white", fg="black")
        self.train_button = b1_1

    def start_training(self):
        self.train_button.config(state=DISABLED, bg="lightgray", fg="gray")
        self.progress.place(x=480, y=70)
        self.status_label.place(x=20, y=55)
        self.progress["value"] = 0
        self.status_label.config(text="Training started... Please wait", fg="blue")
        thread = threading.Thread(target=self.train_classifier)
        thread.start()

    def hide_progress(self):
        self.progress.place_forget()
        self.status_label.place_forget()

    def train_classifier(self):
        try:
            if not os.path.exists(DATA_DIR):
                self.root.after(0, lambda: messagebox.showerror("Error", "Data folder not found"))
                self.root.after(0, lambda: self.train_button.config(state=NORMAL))
                return

            faces = []
            ids = []
            image_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".jpg") or f.endswith(".png")]
            total_images = len(image_files)

            if total_images == 0:
                self.root.after(0, lambda: messagebox.showerror("Error", "No images found for training"))
                self.root.after(0, lambda: self.train_button.config(state=NORMAL))
                return

            count = 0
            for image_name in image_files:
                image_path = os.path.join(DATA_DIR, image_name)
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                try:
                    id = int(image_name.split(".")[1])
                except:
                    continue
                faces.append(img)
                ids.append(id)
                count += 1
                progress_percent = int((count / total_images) * 100)
                self.root.after(0, lambda p=progress_percent: self.update_progress(p))

            ids = np.array(ids)
            recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
            recognizer.train(faces, ids)

            # Save classifier in src/models/
            classifier_path = os.path.join(MODELS_DIR, "classifier.xml")
            recognizer.save(classifier_path)

            self.root.after(0, self.training_done, len(faces))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.train_button.config(state=NORMAL))

    def update_progress(self, value):
        self.progress["value"] = value
        self.status_label.config(text=f"Training... {value}% completed", fg="blue")

    def training_done(self, total_faces):
        self.progress["value"] = 100
        self.status_label.config(text="Training Completed Successfully!", fg="green")
        self.train_button.config(state=NORMAL, bg="royalblue3", fg="white", activebackground="royalblue4")
        messagebox.showinfo("Success", f"Training completed successfully!\nTotal Faces Trained: {total_faces}")
        self.progress.place_forget()
        self.status_label.place_forget()


if __name__ == "__main__":
    root = tk.Tk()
    obj = Train(root)
    root.mainloop()
