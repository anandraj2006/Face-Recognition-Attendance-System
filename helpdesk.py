from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import webbrowser
import urllib.parse


class Help_desk:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.root.configure(bg="white")
        
        img_frame = Frame(self.root,height=150,bd=0,bg="white", highlightthickness=0)
        img_frame.pack(side=TOP, fill=X)
        img_frame.grid_rowconfigure(0, weight=1)
        img_frame.grid_columnconfigure(0, weight=1)
        img_frame.grid_columnconfigure(1, weight=1)
        img_frame.grid_columnconfigure(2, weight=1)

        # img1
        img=Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\home.png")
        img=img.resize((510,150),Image.LANCZOS)
        self.photoimage=ImageTk.PhotoImage(img)

        f_label=Label(img_frame,image=self.photoimage,bd=0, highlightthickness=0)
        f_label.grid(row=0, column=0, sticky="nsew")

        # img2
        img1=Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\home.png")
        img1=img1.resize((510,150),Image.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img1)

        f_label1=Label(img_frame,image=self.photoimage1,bd=0, highlightthickness=0)
        f_label1.grid(row=0, column=1, sticky="nsew")

        # img3
        img2=Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\home.png")
        img2=img2.resize((510,150),Image.LANCZOS)
        self.photoimage2=ImageTk.PhotoImage(img2)

        f_label2=Label(img_frame,image=self.photoimage2,bd=0, highlightthickness=0)
        f_label2.grid(row=0, column=2, sticky="nsew")

        # bg_img
        img3=Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\bgimg.jpeg")
        img3=img3.resize((1530,690),Image.LANCZOS)
        self.photoimage3=ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimage3,bd=0,highlightthickness=0)
        bg_img.place(x=0,y=150,relwidth=1,relheight=1)

        title_lbl=Label(bg_img,text="HELP DESK ", font=("times new roman",30,"bold"),bg="white",fg="purple",justify="center")
        title_lbl.pack(fill=X)
        
        # ================= MAIN CONTAINER (FULL BORDER) =================
        container = Frame(bg_img, bg="white", bd=3, relief=RIDGE)
        container.place(x=10, y=60, width=1250, height=420)

        # ================= LEFT FRAME =================
        left_frame = Frame(container, bg="white")
        left_frame.place(x=10, y=10, width=400, height=400)

        img_help = Image.open(
            r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\helpdesk1.jpeg"
        )
        img_help = img_help.resize((360, 360), Image.LANCZOS)
        self.help_img = ImageTk.PhotoImage(img_help)

        Label(left_frame, image=self.help_img, bg="white").pack(pady=20)
        Label(
            left_frame,
            text="We are here to help you",
            font=("Segoe UI", 14, "bold"),
            bg="white"
        ).pack()

        # ================= RIGHT FRAME =================
        right_frame = Frame(container, bg="white")
        right_frame.place(x=420, y=10, width=820, height=400)

        # ---------- Common Issues ----------
        Label(
            right_frame,
            text="Common Issues",
            font=("Segoe UI", 18, "bold"),
            fg="#0b3d91",
            bg="white"
        ).place(x=10, y=5)

        issues = (
            "• Camera not opening\n"
            "• Face not detected properly\n"
            "• Attendance not marked\n"
            "• Training data error\n"
            "• CSV import/export issue\n"
            "• Database connection problem"
        )

        Label(
            right_frame,
            text=issues,
            font=("Segoe UI", 12),
            bg="white",
            justify=LEFT
        ).place(x=10, y=40)

        # ---------- Issue Category ----------
        Label(
            right_frame,
            text="Issue Category",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).place(x=10, y=170)

        self.issue_category = ttk.Combobox(
            right_frame,
            state="readonly",
            width=30,
            font=("Segoe UI", 11)
        )
        self.issue_category["values"] = (
            "Camera Issue",
            "Face Detection Problem",
            "Attendance Issue",
            "Training Error",
            "CSV / Database Issue",
            "Other"
        )
        self.issue_category.current(0)
        self.issue_category.place(x=10, y=200)

        # ---------- Issue Description ----------
        Label(
            right_frame,
            text="Describe your issue",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).place(x=10, y=230)

        self.issue_text = Text(
            right_frame,
            width=60,
            height=4.2,
            font=("Segoe UI", 11),
            bd=2,
            relief=GROOVE
        )
        self.issue_text.place(x=10, y=260)

        # ---------- Send Buttons ----------
        Button(
            right_frame,
            text="Send via Email",
            font=("Segoe UI", 12, "bold"),
            bg="#2563eb",
            fg="white",
            cursor="hand2",
            command=self.send_email
        ).place(x=10, y=360, width=180, height=40)

        Button(
            right_frame,
            text="Send via WhatsApp",
            font=("Segoe UI", 12, "bold"),
            bg="#22c55e",
            fg="white",
            cursor="hand2",
            command=self.send_whatsapp
        ).place(x=200, y=360, width=200, height=40)

        # ---------- Contact Box ----------
        contact_frame = Frame(right_frame, bg="#f9fafb", bd=2, relief=RIDGE)
        contact_frame.place(x=520, y=40, width=270, height=160)

        Label(
            contact_frame,
            text="Contact Support",
            font=("Segoe UI", 16, "bold"),
            bg="#f9fafb"
        ).pack(pady=10)

        email_lbl = Label(
            contact_frame,
            text="📧 anandraj.141520@gmail.com",
            fg="blue",
            bg="#f9fafb",
            cursor="hand2"
        )
        email_lbl.pack()
        email_lbl.bind(
            "<Button-1>",
            lambda e: webbrowser.open(
                "https://mail.google.com/mail/?view=cm&fs=1&to=anandraj.141520@gmail.com"
            )
        )


        Label(
            contact_frame,
            text="📞 +91 74548 30370",
            bg="#f9fafb"
        ).pack(pady=5)

        whatsapp_lbl = Label(
            contact_frame,
            text="💬 WhatsApp Support",
            fg="green",
            bg="#f9fafb",
            cursor="hand2"
        )
        whatsapp_lbl.pack()
        whatsapp_lbl.bind(
            "<Button-1>",
            lambda e: webbrowser.open(
                "https://wa.me/917454830370"
            )
        )


    # ================= FUNCTIONS =================
    def send_email(self):
        category = self.issue_category.get()
        issue = self.issue_text.get("1.0", END).strip()

        if not issue:
            messagebox.showerror("Error", "Please describe your issue")
            return

        subject = urllib.parse.quote(f"Help Desk Issue - {category}")
        body = urllib.parse.quote(
            f"Issue Category: {category}\n\n"
            f"Issue Description:\n{issue}"
        )

        gmail_url = (
            "https://mail.google.com/mail/?view=cm&fs=1"
            f"&to=anandraj.141520@gmail.com"
            f"&subject={subject}"
            f"&body={body}"
        )

        webbrowser.open(gmail_url)


    def send_whatsapp(self):
        category = self.issue_category.get()
        issue = self.issue_text.get("1.0", END).strip()

        if not issue:
            messagebox.showerror("Error", "Please describe your issue")
            return

        message = urllib.parse.quote(
            f"Issue Category: {category}\n\nIssue:\n{issue}"
        )

        webbrowser.open(
            f"https://wa.me/917454830370?text={message}"
        )


if __name__ == "__main__":
    root = Tk()
    obj = Help_desk(root)
    root.mainloop()
