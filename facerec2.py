from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import mysql.connector
from datetime import datetime
import os
import time
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    import winsound
import threading
import math


class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")
        self.root.configure(bg="#0d0d1a")

        self.running = False
        self.marked_today = set()
        self.total_present = 0
        self.pulse_angle = 0
        self.scan_line_y = 0
        self.scan_direction = 1

        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 1.0)
            except:
                self.tts_engine = None
        else:
            self.tts_engine = None

        # ── TOP BANNER ──────────────────────────────────────────────────
        banner = Frame(self.root, height=90, bg="#0d0d1a")
        banner.pack(side=TOP, fill=X)
        banner.pack_propagate(False)

        # Left accent bar
        accent = Frame(banner, width=6, bg="#7c3aed")
        accent.pack(side=LEFT, fill=Y, padx=(18, 0))

        title_block = Frame(banner, bg="#0d0d1a")
        title_block.pack(side=LEFT, padx=14, pady=10)

        Label(title_block,
              text="ATTENDANCE MANAGEMENT SYSTEM",
              font=("Courier New", 22, "bold"),
              fg="#e0d7ff", bg="#0d0d1a").pack(anchor=W)

        Label(title_block,
              text="AI-Powered Face Recognition  •  Real-Time Tracking",
              font=("Courier New", 10),
              fg="#6d5fa0", bg="#0d0d1a").pack(anchor=W)

        # Live clock on right
        self.clock_var = StringVar()
        clock_lbl = Label(banner, textvariable=self.clock_var,
                          font=("Courier New", 13, "bold"),
                          fg="#7c3aed", bg="#0d0d1a")
        clock_lbl.pack(side=RIGHT, padx=24)
        self._tick_clock()

        # Thin separator line
        sep = Frame(self.root, height=2, bg="#7c3aed")
        sep.pack(fill=X)

        # ── MAIN BODY ────────────────────────────────────────────────────
        body = Frame(self.root, bg="#0d0d1a")
        body.pack(fill=BOTH, expand=True, padx=14, pady=10)

        # ── LEFT PANEL (control + status) ────────────────────────────────
        left_panel = Frame(body, bg="#12122a", width=320,
                           highlightbackground="#2a2a4a", highlightthickness=1)
        left_panel.pack(side=LEFT, fill=Y, padx=(0, 10))
        left_panel.pack_propagate(False)

        Label(left_panel, text="⬡  RECOGNITION CORE",
              font=("Courier New", 10, "bold"),
              fg="#7c3aed", bg="#12122a").pack(anchor=W, padx=16, pady=(14, 2))

        Frame(left_panel, height=1, bg="#2a2a4a").pack(fill=X, padx=16, pady=4)

        # Animated canvas (pulse ring)
        self.pulse_canvas = Canvas(left_panel, width=180, height=180,
                                   bg="#12122a", highlightthickness=0)
        self.pulse_canvas.pack(pady=14)
        self._draw_pulse()

        self.status_label = Label(left_panel,
                                  text="READY",
                                  font=("Courier New", 15, "bold"),
                                  fg="#00e5ff", bg="#12122a")
        self.status_label.pack(pady=4)

        self.name_label = Label(left_panel, text="Name : ---",
                                font=("Courier New", 11),
                                fg="#a89fd4", bg="#12122a")
        self.name_label.pack(pady=3)

        self.time_label = Label(left_panel, text="Time  : ---",
                                font=("Courier New", 11),
                                fg="#a89fd4", bg="#12122a")
        self.time_label.pack(pady=3)

        Frame(left_panel, height=1, bg="#2a2a4a").pack(fill=X, padx=16, pady=12)

        # Stat counters
        stats_row = Frame(left_panel, bg="#12122a")
        stats_row.pack(fill=X, padx=16, pady=4)

        self._stat_box(stats_row, "TODAY", "0", "present_count", "#00e5a0", 0)
        self._stat_box(stats_row, "LAST ID", "---", "last_id", "#7c3aed", 1)

        Frame(left_panel, height=1, bg="#2a2a4a").pack(fill=X, padx=16, pady=12)

        # Buttons
        btn_frame = Frame(left_panel, bg="#12122a")
        btn_frame.pack(padx=16, pady=4, fill=X)

        self._neon_button(btn_frame, "▶  TAKE ATTENDANCE",
                          "#00e5a0", self.start_camera).pack(fill=X, pady=5)
        self._neon_button(btn_frame, "■  STOP CAMERA",
                          "#ff4d6d", self.stop_camera).pack(fill=X, pady=5)
        self._neon_button(btn_frame, "↻  REFRESH TABLE",
                          "#7c3aed", self.load_today_attendance).pack(fill=X, pady=5)

        # ── RIGHT PANEL (attendance dashboard) ───────────────────────────
        right_panel = Frame(body, bg="#0d0d1a")
        right_panel.pack(side=LEFT, fill=BOTH, expand=True)

        # Top row: 3 stat cards
        cards_row = Frame(right_panel, bg="#0d0d1a")
        cards_row.pack(fill=X, pady=(0, 10))

        self._big_card(cards_row, "TOTAL PRESENT", "0", "#00e5a0",
                       "present_big", "👤")
        self._big_card(cards_row, "DATE", datetime.now().strftime("%d %b %Y"),
                       "#7c3aed", None, "📅")
        self._big_card(cards_row, "SESSION", "LIVE", "#00e5ff", None, "🎥")

        # Treeview section
        table_frame = Frame(right_panel, bg="#12122a",
                            highlightbackground="#2a2a4a", highlightthickness=1)
        table_frame.pack(fill=BOTH, expand=True)

        hdr = Frame(table_frame, bg="#12122a")
        hdr.pack(fill=X, padx=14, pady=(10, 4))

        Label(hdr, text="⬡  TODAY'S ATTENDANCE LOG",
              font=("Courier New", 11, "bold"),
              fg="#7c3aed", bg="#12122a").pack(side=LEFT)

        self.row_count_lbl = Label(hdr, text="0 records",
                                   font=("Courier New", 10),
                                   fg="#4a4a7a", bg="#12122a")
        self.row_count_lbl.pack(side=RIGHT)

        Frame(table_frame, height=1, bg="#2a2a4a").pack(fill=X, padx=14, pady=2)

        # Style treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                         background="#12122a",
                         foreground="#c8c0e8",
                         fieldbackground="#12122a",
                         rowheight=32,
                         font=("Courier New", 10))
        style.configure("Custom.Treeview.Heading",
                         background="#1e1e3a",
                         foreground="#7c3aed",
                         font=("Courier New", 10, "bold"),
                         relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", "#2a1a5e")],
                  foreground=[("selected", "#e0d7ff")])

        tree_wrap = Frame(table_frame, bg="#12122a")
        tree_wrap.pack(fill=BOTH, expand=True, padx=14, pady=(4, 12))

        scroll_y = Scrollbar(tree_wrap, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x = Scrollbar(tree_wrap, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        cols = ("ID", "Name", "Department", "Time", "Date", "Status", "Source")
        self.attendance_table = ttk.Treeview(
            tree_wrap,
            columns=cols,
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        scroll_y.config(command=self.attendance_table.yview)
        scroll_x.config(command=self.attendance_table.xview)

        col_widths = {"ID": 70, "Name": 160, "Department": 110,
                      "Time": 90, "Date": 100, "Status": 90, "Source": 80}
        for c in cols:
            self.attendance_table.heading(c, text=c)
            self.attendance_table.column(c, width=col_widths[c], anchor=CENTER)

        # Alternating row tags
        self.attendance_table.tag_configure("odd",  background="#14142e")
        self.attendance_table.tag_configure("even", background="#12122a")
        self.attendance_table.tag_configure("new",  background="#1a2e1a",
                                                     foreground="#00e5a0")

        self.attendance_table.pack(fill=BOTH, expand=True)

        # ── OpenCV setup ──────────────────────────────────────────────────
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            self.recognizer.read("classifier.xml")
        except:
            print("classifier.xml not found")

        self.camera_window = None
        self.cap = None

        self.load_today_attendance()

    # ──────────────────────────────────────────────────────────────────────
    # HELPER WIDGETS
    # ──────────────────────────────────────────────────────────────────────

    def _stat_box(self, parent, title, value, attr_name, color, col):
        box = Frame(parent, bg="#1a1a35",
                    highlightbackground=color, highlightthickness=1)
        box.grid(row=0, column=col, padx=5, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        Label(box, text=title, font=("Courier New", 8),
              fg="#6d5fa0", bg="#1a1a35").pack(pady=(6, 0))
        lbl = Label(box, text=value, font=("Courier New", 16, "bold"),
                    fg=color, bg="#1a1a35")
        lbl.pack(pady=(0, 6))
        setattr(self, attr_name + "_lbl", lbl)

    def _big_card(self, parent, title, value, color, attr, icon):
        card = Frame(parent, bg="#12122a",
                     highlightbackground=color, highlightthickness=1)
        card.pack(side=LEFT, expand=True, fill=BOTH, padx=5)

        Label(card, text=icon, font=("Segoe UI Emoji", 18),
              bg="#12122a").pack(pady=(10, 0))
        Label(card, text=title, font=("Courier New", 9),
              fg="#6d5fa0", bg="#12122a").pack()
        lbl = Label(card, text=value, font=("Courier New", 18, "bold"),
                    fg=color, bg="#12122a")
        lbl.pack(pady=(0, 12))
        if attr:
            setattr(self, attr + "_lbl", lbl)

    def _neon_button(self, parent, text, color, command):
        btn = Button(parent, text=text,
                     font=("Courier New", 10, "bold"),
                     bg="#1a1a35", fg=color,
                     activebackground=color, activeforeground="#0d0d1a",
                     relief=FLAT, bd=0, cursor="hand2",
                     highlightbackground=color, highlightthickness=1,
                     padx=10, pady=8,
                     command=command)
        return btn

    # ──────────────────────────────────────────────────────────────────────
    # ANIMATIONS
    # ──────────────────────────────────────────────────────────────────────

    def _draw_pulse(self):
        c = self.pulse_canvas
        c.delete("all")
        cx, cy, r = 90, 90, 60

        # Outer glow rings
        for i in range(3):
            offset = i * 14 + (self.pulse_angle % 14)
            alpha_rings = ["#1a0a3a", "#220d4a", "#2a1060"]
            c.create_oval(cx - r - offset, cy - r - offset,
                          cx + r + offset, cy + r + offset,
                          outline=alpha_rings[i], width=1)

        # Rotating arc
        start = self.pulse_angle % 360
        c.create_arc(cx - r, cy - r, cx + r, cy + r,
                     start=start, extent=220,
                     outline="#7c3aed", width=2, style=ARC)
        c.create_arc(cx - r, cy - r, cx + r, cy + r,
                     start=start + 230, extent=80,
                     outline="#00e5ff", width=1, style=ARC)

        # Center face icon
        face_color = "#00e5a0" if self.running else "#4a4a7a"
        c.create_oval(cx - 22, cy - 26, cx + 22, cy + 18,
                      outline=face_color, width=2)
        # eyes
        c.create_oval(cx - 10, cy - 16, cx - 4, cy - 10,
                      fill=face_color, outline="")
        c.create_oval(cx + 4, cy - 16, cx + 10, cy - 10,
                      fill=face_color, outline="")
        # mouth
        c.create_arc(cx - 10, cy - 4, cx + 10, cy + 10,
                     start=200, extent=140,
                     outline=face_color, width=2, style=ARC)

        self.pulse_angle += 2
        self.root.after(40, self._draw_pulse)

    def _tick_clock(self):
        now = datetime.now().strftime("  %a  %d-%m-%Y   %H:%M:%S  ")
        self.clock_var.set(now)
        self.root.after(1000, self._tick_clock)

    # ──────────────────────────────────────────────────────────────────────
    # LOAD TABLE
    # ──────────────────────────────────────────────────────────────────────

    def load_today_attendance(self):
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="piddii51242", database="mydb"
            )
            cur = conn.cursor()
            cur.execute(
                "SELECT attendance_id, name, department, time, date, attendance, source "
                "FROM attendance WHERE date=%s ORDER BY time DESC",
                (today,)
            )
            rows = cur.fetchall()
            conn.close()

            for item in self.attendance_table.get_children():
                self.attendance_table.delete(item)

            for i, row in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                self.attendance_table.insert("", END, values=row, tags=(tag,))

            count = len(rows)
            self.row_count_lbl.config(text=f"{count} records")
            self._update_count(count)

        except Exception as e:
            print("DB load error:", e)

    def _update_count(self, count):
        self.total_present = count
        if hasattr(self, "present_count_lbl"):
            self.present_count_lbl.config(text=str(count))
        if hasattr(self, "present_big_lbl"):
            self.present_big_lbl.config(text=str(count))

    # ──────────────────────────────────────────────────────────────────────
    # CAMERA
    # ──────────────────────────────────────────────────────────────────────

    def start_camera(self):
        if self.running:
            return

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Camera Error", "Cannot open camera")
            return

        self.running = True

        self.camera_window = Toplevel(self.root)
        self.camera_window.title("Live Camera — Face Recognition")

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        ww = sw // 2
        self.camera_window.geometry(f"{ww}x{sh}+{sw // 2}+0")
        self.camera_window.configure(bg="black")

        self.video_label = Label(self.camera_window, bg="black")
        self.video_label.pack(fill=BOTH, expand=True)
        self.camera_window.protocol("WM_DELETE_WINDOW", self.stop_camera)

        self.status_label.config(text="SCANNING", fg="#00e5ff")
        self.update_frame()

    def stop_camera(self):
        if not self.running:
            return
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        cv2.destroyAllWindows()
        try:
            if self.camera_window and self.camera_window.winfo_exists():
                self.camera_window.destroy()
        except Exception:
            pass
        self.camera_window = None
        self.status_label.config(text="STOPPED", fg="#ff4d6d")

    def update_frame(self):
        if not self.running:
            return
        if not self.camera_window or not self.camera_window.winfo_exists():
            self.running = False
            return
        if not self.cap or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            self.root.after(20, self.update_frame)
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id_, conf = self.recognizer.predict(gray[y:y + h, x:x + w])
            confidence = int(100 * (1 - conf / 300))
            name = self.get_student_name(id_)

            if confidence > 70 and name != "Unknown":
                if id_ not in self.marked_today:
                    self.marked_today.add(id_)  # guard first to avoid double-call
                    self.mark_attendance(id_, name)
                    return  # camera will close via after(); stop drawing

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 229, 160), 2)
                cv2.putText(frame, f"{name}  {confidence}%",
                            (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 229, 160), 2)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 77, 109), 2)
                cv2.putText(frame, "Unknown",
                            (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (255, 77, 109), 2)

        if self.running and self.camera_window and self.camera_window.winfo_exists():
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)
            self.root.after(20, self.update_frame)

    # ──────────────────────────────────────────────────────────────────────
    # DATABASE
    # ──────────────────────────────────────────────────────────────────────

    def get_student_name(self, student_id):
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="piddii51242", database="mydb"
            )
            cur = conn.cursor()
            cur.execute("SELECT name FROM students WHERE student_id=%s",
                        (student_id,))
            result = cur.fetchone()
            conn.close()
            return result[0] if result else "Unknown"
        except:
            return "Unknown"

    def mark_attendance(self, student_id, name):
        today = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M:%S")

        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="piddii51242", database="mydb"
            )
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM attendance WHERE attendance_id=%s AND date=%s",
                (student_id, today)
            )

            if cur.fetchone():
                self.status_label.config(text="ALREADY MARKED", fg="#f59e0b")
                self.name_label.config(text=f"Name : {name}")
                conn.close()
                return

            cur.execute(
                """INSERT INTO attendance
                   (attendance_id, roll, name, department, time, date, attendance, source)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                (student_id, student_id, name, "CSE",
                 now_time, today, "Present", "Face")
            )
            conn.commit()
            conn.close()

            # Update UI labels
            self.status_label.config(text="MARKED ✓", fg="#00e5a0")
            self.name_label.config(text=f"Name : {name}")
            self.time_label.config(text=f"Time  : {now_time}")

            if hasattr(self, "last_id_lbl"):
                self.last_id_lbl.config(text=str(student_id))

            # Insert at top of treeview with highlight
            display_date = datetime.now().strftime("%d-%m-%Y")
            self.attendance_table.insert(
                "", 0,
                values=(student_id, name, "CSE",
                        now_time, display_date, "Present", "Face"),
                tags=("new",)
            )

            # Update counts
            self.total_present += 1
            self._update_count(self.total_present)

            count = len(self.attendance_table.get_children())
            self.row_count_lbl.config(text=f"{count} records")

            # Re-colour alternating rows
            self._restripe()

            # Auto-close camera after 1.5s so user can see the confirmation
            self.root.after(1500, self.stop_camera)

        except Exception as e:
            print("DB insert error:", e)

    def _restripe(self):
        for i, item in enumerate(self.attendance_table.get_children()):
            current_tags = self.attendance_table.item(item, "tags")
            if "new" not in current_tags:
                tag = "even" if i % 2 == 0 else "odd"
                self.attendance_table.item(item, tags=(tag,))


if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognition(root)
    root.mainloop()