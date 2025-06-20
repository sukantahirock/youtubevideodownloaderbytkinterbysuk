import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import subprocess
import os

def download_video():
    link = entry_link.get().strip()
    quality = quality_var.get()

    if not link:
        messagebox.showwarning("⚠️ Warning", "YouTube লিঙ্ক দিন!")
        return

    folder = filedialog.askdirectory()
    if not folder:
        return

    try:
        status_label.config(text="⬇️ ডাউনলোড চলছে...", fg="blue")
        root.update_idletasks()

        # ফাইল নাম প্যাটার্ন
        output_path = os.path.join(folder, '%(title)s.%(ext)s')

        # yt-dlp command (only video with selected quality)
        command = [
            'yt-dlp',
            '-f', f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
            '--merge-output-format', 'mp4',
            '-o', output_path,
            link
        ]

        subprocess.run(command, check=True)

        status_label.config(text="✅ ভিডিও ডাউনলোড শেষ!", fg="green")
        messagebox.showinfo("Success", f"ভিডিও সফলভাবে {quality}p রেজোলিউশনে ডাউনলোড হয়েছে!")

    except subprocess.CalledProcessError as e:
        status_label.config(text="❌ ডাউনলোড ব্যর্থ", fg="red")
        messagebox.showerror("Error", f"yt-dlp ত্রুটি: {e}")
    except Exception as e:
        status_label.config(text="❌ সমস্যা হয়েছে", fg="red")
        messagebox.showerror("Error", str(e))

# GUI
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("500x300")
root.resizable(False, False)

tk.Label(root, text="YouTube লিঙ্ক দিন:", font=("Helvetica", 12)).pack(pady=10)
entry_link = tk.Entry(root, width=50, font=("Helvetica", 12))
entry_link.pack(pady=5)

# Quality select
quality_var = tk.StringVar(value="720")
tk.Label(root, text="ভিডিও কোয়ালিটি নির্বাচন করুন:", font=("Helvetica", 11)).pack(pady=(10, 0))
quality_combo = ttk.Combobox(root, textvariable=quality_var, values=["1080", "720", "480", "360", "240"], state="readonly")
quality_combo.pack()

# Download button
tk.Button(root, text="🎬 ভিডিও ডাউনলোড করো", command=download_video,
          bg="#1E90FF", fg="white", font=("Helvetica", 12)).pack(pady=20)

status_label = tk.Label(root, text="", font=("Helvetica", 10))
status_label.pack()

root.mainloop()
