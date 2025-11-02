import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def organize_files(directory, include_subfolders=False):
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "The selected directory is not valid.")
        return

    files = []
    if include_subfolders:
        for current_folder, _, file_list in os.walk(directory):
            for f in file_list:
                files.append(os.path.join(current_folder, f))
    else:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    total = len(files)
    if total == 0:
        messagebox.showinfo("Empty", "No files found to organize.")
        return

    progress_bar["maximum"] = total
    progress_bar["value"] = 0
    window.update_idletasks()

    moved_files = 0
    for i, file_path in enumerate(files, 1):
        move_file(file_path, directory)
        moved_files += 1
        progress_bar["value"] = i
        lbl_status.config(text=f"Organizing ({i}/{total})")
        window.update_idletasks()

    lbl_status.config(text=f"Done: {moved_files} files organized.")
    messagebox.showinfo("Completed", f"{moved_files} files organized successfully!")

def move_file(file_path, base_directory):
    ext = os.path.splitext(file_path)[1].lower().replace('.', '')
    if ext == '':
        ext = "no_extension"
    dest_folder = os.path.join(base_directory, ext)

    os.makedirs(dest_folder, exist_ok=True)
    try:
        shutil.move(file_path, os.path.join(dest_folder, os.path.basename(file_path)))
    except shutil.Error:
        name, ext2 = os.path.splitext(os.path.basename(file_path))
        new_name = f"{name}_copy{ext2}"
        shutil.move(file_path, os.path.join(dest_folder, new_name))

def select_directory():
    folder = filedialog.askdirectory()
    if folder:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, folder)

def run_organizer():
    directory = entry_directory.get().strip()
    include_subs = var_subfolders.get()
    if directory:
        lbl_status.config(text="Starting organization...")
        progress_bar["value"] = 0
        window.update_idletasks()
        organize_files(directory, include_subfolders=include_subs)
    else:
        messagebox.showwarning("Warning", "Please select a directory.")

window = tk.Tk()
window.title("File Organizer")
window.geometry("440x260")
window.resizable(False, False)

tk.Label(window, text="Select the directory to organize:").pack(pady=10)

frame = tk.Frame(window)
frame.pack()

entry_directory = tk.Entry(frame, width=40)
entry_directory.pack(side=tk.LEFT, padx=5)
btn_browse = tk.Button(frame, text="Browse", command=select_directory)
btn_browse.pack(side=tk.LEFT)

var_subfolders = tk.BooleanVar()
chk_subfolders = tk.Checkbutton(window, text="Include subfolders", variable=var_subfolders)
chk_subfolders.pack(pady=10)

btn_organize = tk.Button(window, text="Organize Files", bg="#4CAF50", fg="white", command=run_organizer)
btn_organize.pack(pady=10)

progress_bar = ttk.Progressbar(window, length=350, mode='determinate')
progress_bar.pack(pady=5)

lbl_status = tk.Label(window, text="")
lbl_status.pack(pady=5)

window.mainloop()