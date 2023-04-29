import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import speech_recognition as sr
import threading
import os

ICON = os.path.join(os.getcwd(), "mic.ico")
FONT_LARGE = ("Helvetica", 24)
FONT_MEDIUM = ("Helvetica", 18)
FONT_SMALL = ("Helvetica", 12)
BG_COLOR = "#F0F0F0"
BUTTON_COLOR = "#808000"
LABEL_COLOR = "#333333"
ERROR_COLOR = "#FF0000"
WIDTH = 1280
HEIGHT = 720


class VoiceToTextConverter:
    def __init__(self, master):
        self.master = master
        self.master.geometry(f"{WIDTH}x{HEIGHT}")
        self.master.title("Voice To Text Converter")
        self.master.iconbitmap(ICON)
        self.master.config(bg=BG_COLOR)
        self.r = sr.Recognizer()
        self.speech_text = tk.StringVar()
        self.status = tk.StringVar()
        self.icon = tk.PhotoImage(file=ICON)
        self.master.call('wm', 'iconphoto', self.master._w, self.icon)
        self.master.title("Copyritht© 2023 AMIT RAJ(U20CC011)")
        self.label_title = ttk.Label(
            self.master,
            text="Voice To Text Converter",
            font=FONT_LARGE,
            foreground=LABEL_COLOR,
            background=BG_COLOR,
        )
        self.label_title.pack(pady=(30, 0))

        self.label_instruction = ttk.Label(
            self.master,
            text="Press below button and start speaking...",
            font=FONT_MEDIUM,
            foreground=LABEL_COLOR,
            background=BG_COLOR,
        )
        self.label_instruction.pack(pady=(50, 0))

        self.button_listen = ttk.Button(
            self.master,
            text="LISTEN",
            command=self.start_thread,
            style="Listen.TButton",
        )
        self.button_listen.pack(pady=(50, 0))

        self.label_speech_text = ttk.Label(
            self.master,
            textvariable=self.speech_text,
            font=FONT_SMALL,
            foreground=LABEL_COLOR,
            background=BG_COLOR,
        )
        self.label_speech_text.pack(pady=(20, 0))

        self.label_status = ttk.Label(
            self.master,
            textvariable=self.status,
            font=FONT_SMALL,
            foreground=LABEL_COLOR,
            background=BG_COLOR,
        )
        self.label_status.pack(pady=(20, 0))

        self.style = ttk.Style()
        self.style.configure(
            "Listen.TButton",
            font=FONT_MEDIUM,
            background=BUTTON_COLOR,
            foreground=LABEL_COLOR,
            padding=(10, 10),
            borderwidth=0,
        )

    def start_thread(self):
        self.button_listen.config(state=tk.DISABLED)
        self.label_instruction.config(text="Listening...")
        self.status.set("")
        self.speech_text.set("")
        t = threading.Thread(target=self.recognize_speech)
        t.start()

    def recognize_speech(self):
        with sr.Microphone() as source:
            try:
                audio = self.r.listen(source, timeout=5.0)
                self.label_instruction.config(text="Processing...")
                text = self.r.recognize_google(audio)
                self.speech_text.set(text)
                self.status.set("Success!")
            except sr.WaitTimeoutError:
                self.status.set("Timeout error. Please try again.")
            except sr.UnknownValueError:
                self.status.set("Sorry, I could not understand what you said.")
            except sr.RequestError:
                self.status.set("Sorry, there was an error with your request. Please try again.")
            except Exception as e:
                self.status.set(f"Sorry, an error occurred: {str(e)}")
            finally:
                self.button_listen.config(state=tk.NORMAL)
                self.label_instruction.config(text="Press the button and start speaking...")
root = tk.Tk()
app = VoiceToTextConverter(root)
root.mainloop()

