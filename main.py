

# ===============================================
# 
# Author - Ilya Purtov
# My VK - vk.com/iluxapurtov
# 
# ===============================================


# ======================/ Depenicies /=========================
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import *
from tkinter.scrolledtext import ScrolledText
from ttkthemes import ThemedTk
import mouse
import keyboard
import time
import threading
import sys
# ======================/ Depenicies /=========================




# ======================/ Global Variables /=========================
is_clicker_running = False
is_kl_thread_started = False
# ======================/ Global Variables /=========================


def printToLog(tag, message):
	pass


# ======================/ Init clicker function /=========================
def init_clicker():
	if not is_kl_thread_started:
		log_text.insert(tk.INSERT, "Getting required information...\n")
		log_text.yview("end")
		cps = cps_entry.get()
		bind_key = bind_entry.get()

		if (cps.strip() == "") or (bind_key.strip() == ""):
			showerror(title="Error", message="Invalid cps / bind key")
			return

		try:
			keyboard.parse_hotkey(bind_key)
		except:
			showerror(title="Error", message="Invalid bind key")
			return


		log_text.insert(tk.INSERT, "Initialize key listen thread...\n")
		log_text.yview("end")
		key_l = threading.Thread(target=key_listen, args=(bind_key, ))
		log_text.insert(tk.INSERT, "Starting key listen thread...\n")
		log_text.yview("end")
		key_l.start()
		log_text.insert(tk.INSERT, "Running clicker...\n")
		log_text.yview("end")
		run_clicker(cps)
	else:
		log_text.insert(tk.INSERT, "Clicker already started.\n")
		log_text.yview("end")
# ======================/ Init clicker function /=========================




# ======================/ Key listen function. Running from "init_clicker" function and working in secondary thread /=========================
def key_listen(key):
	global is_clicker_running, is_kl_thread_started
	log_text.insert(tk.INSERT, f"Key listen thread started. Press {key} to start clicker.\n")
	log_text.yview("end")
	is_kl_thread_started = True
	while is_kl_thread_started:
		if keyboard.is_pressed(key):
			log_text.insert(tk.INSERT, f"Key {key} is pressed! Toggling clicker...\n")
			log_text.yview("end")
			is_clicker_running = not is_clicker_running
			log_text.insert(tk.INSERT, "Clicker toggled to {0}!\n".format(str(is_clicker_running)))
			log_text.yview("end")
			if is_clicker_running:
				time.sleep(0.2)
				is_kl_thread_started = False
				init_clicker()
				break
			else:
				time.sleep(0.2)
				continue
	return
# ======================/ Key listen function. Running from "init_clicker" function and working in secondary thread /=========================




# ======================/ Main clicker function. Here clicker is click on the left button of mouse /=========================
def run_clicker(cps):
	global is_clicker_running

	sleeping_time = 1 / int(cps)

	log_text.insert(tk.INSERT, "Clicker was started.\n")
	log_text.yview("end")

	while is_clicker_running:
		mouse.click(button="left")
		time.sleep(sleeping_time)

	return
# ======================/ Main clicker function. Here clicker is click on the left button of mouse /=========================




# ======================/ This function is stopping key listen thread and clicker running function /=========================
def stop_clicker():
	global is_clicker_running, is_kl_thread_started
	log_text.insert(tk.INSERT, "Stopping clicker...\n")
	log_text.yview("end")
	is_clicker_running = False
	is_kl_thread_started = False
# ======================/ This function is stopping key listen thread and clicker running function /=========================




# ======================/ This function is REQUIRED to correctly exit from program, else it will be works after closing tkinter window and overload CPU /=========================
def terminateThreads():
	stop_clicker()
	root.destroy()
	sys.exit(0)
# ======================/ This function is REQUIRED to correctly exit from program, else it will be works after closing tkinter window and overload CPU /=========================




# Creating window
root = ThemedTk(theme="yaru")
root.title("Python clicker")
root.iconbitmap("icon.ico")
root["bg"] = "#fff"
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", terminateThreads)

start_btn_style = ttk.Style().configure("TButton", font=("wasy10", 10, "bold"))




# ======================/ Initializing window components /=========================
main = tk.Frame(root, bg="#fff")

cps_frame = tk.Frame(main, bg="#fff")
cps_label = tk.Label(cps_frame, bg="#fff", text="CPS:", font=("Ubuntu", 10, "bold"))
cps_entry = ttk.Entry(cps_frame, width=30)
cps_entry.insert(tk.INSERT, "5")

bind_frame = tk.Frame(main, bg="#fff")
bind_label = tk.Label(bind_frame, bg="#fff", text="BIND KEY:", font=("Ubuntu", 10, "bold"))
bind_entry = ttk.Entry(bind_frame, width=30)
bind_entry.insert(tk.INSERT, "f9")

start_btn = ttk.Button(main, width=25, text="START", style="TButton", command=init_clicker)
stop_btn = ttk.Button(main, width=25, text="STOP", style="TButton", command=stop_clicker)

log = tk.Frame(root, bg="#fff")
log_text = ScrolledText(
	log,
	bg="#444",
	fg="#f2f2f2",
	height=20,
	width=50,
	font=("Segoe UI", 10),
	padx=10,
	pady=10
)
log_text.insert(tk.INSERT, "There is a clicker log.\n")
log_text.bind("<Key>", lambda e: "break")
# ======================/ Initializing window components /=========================




# ======================/ Placing window components /=========================
main.grid(row=0, column=0, padx=10, pady=10)

cps_frame.grid(row=0, column=0, pady=10)
cps_label.grid(row=0, column=0, sticky="w")
cps_entry.grid(row=1, column=0)

bind_frame.grid(row=1, column=0, pady=10)
bind_label.grid(row=0, column=0, sticky="w")
bind_entry.grid(row=1, column=0)

start_btn.grid(row=2, column=0, padx=10, pady=10)
stop_btn.grid(row=3, column=0, padx=10, pady=10)

log.grid(row=0, column=1)
log_text.pack()
# ======================/ Placing window components /=========================




# Main window loop
root.mainloop()