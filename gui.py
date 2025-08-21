import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading

# Import your automation logic
from whatsapp_script import start_whatsapp_automation  # You’ll create this function next

def run_script():
    file_path = file_path_var.get()
    if not file_path.endswith('.xlsx'):
        messagebox.showerror("Invalid File", "Please select a valid Excel file.")
        return

    def thread_target():
        start_button.config(state=tk.DISABLED)
        log_output.insert(tk.END, f"📁 Starting with file: {file_path}\n")
        start_whatsapp_automation(file_path, log_callback)
        start_button.config(state=tk.NORMAL)

    threading.Thread(target=thread_target).start()

def browse_file():
    path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    file_path_var.set(path)

def log_callback(message):
    log_output.insert(tk.END, message + '\n')
    log_output.see(tk.END)

# Create the window
root = tk.Tk()
root.title("WhatsApp Automation Tool")
root.geometry("600x400")

# Keep the window on top
root.attributes("-topmost", True)

file_path_var = tk.StringVar()

tk.Label(root, text="Select Excel File:").pack(pady=(10, 0))
tk.Entry(root, textvariable=file_path_var, width=60).pack(padx=10)
tk.Button(root, text="Browse", command=browse_file).pack(pady=5)

start_button = tk.Button(root, text="Start Messaging", command=run_script)
start_button.pack(pady=10)

log_output = scrolledtext.ScrolledText(root, height=15)
log_output.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

root.mainloop()
