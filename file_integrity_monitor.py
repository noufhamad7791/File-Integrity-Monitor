import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import hashlib
import json

window = tk.Tk()
window.title("File Integrity Monitor")
window.geometry("600x700")
window.configure(bg="#1e1e2f")


def choose_folder():
    folder_path = filedialog.askdirectory()

    if folder_path:
        folder_label.config(text=folder_path)
        scan_button.config(text="Scan")


def scan_folder():
    folder_path = folder_label.cget("text")

    if folder_path == "No folder selected":
        results_label.config(text="Please select a folder first.")
        return

    results_label.config(text="Scanning...")
    window.update()

    folder = Path(folder_path)
    current_hashes = {}

    for file in folder.iterdir():
        if file.is_file():
            sha256_hash = hashlib.sha256()

            with open(file, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)

            current_hashes[file.name] = sha256_hash.hexdigest()

    baselines_folder = Path("baselines")
    baselines_folder.mkdir(exist_ok=True)

    folder_id = hashlib.sha256(
        str(folder.resolve()).encode()
    ).hexdigest()

    baseline_path = baselines_folder / f"{folder_id}.json"

    if not baseline_path.exists():
        with open(baseline_path, "w") as f:
            json.dump(current_hashes, f, indent=4)

    with open(baseline_path, "r") as f:
        saved_hashes = json.load(f)

    modified_files = []
    deleted_files = []
    new_files = []

    for file in current_hashes:
        if file not in saved_hashes:
            new_files.append(file)

        elif current_hashes[file] != saved_hashes[file]:
            modified_files.append(file)

    for file in saved_hashes:
        if file not in current_hashes:
            deleted_files.append(file)

    results_text = "Modified Files:\n"

    if modified_files:
        for file in modified_files:
            results_text += f"- {file}\n"
    else:
        results_text += "None\n"

    results_text += "\nDeleted Files:\n"

    if deleted_files:
        for file in deleted_files:
            results_text += f"- {file}\n"
    else:
        results_text += "None\n"

    results_text += "\nNew Files:\n"

    if new_files:
        for file in new_files:
            results_text += f"- {file}\n"
    else:
        results_text += "None\n"

    results_label.config(
        text=results_text,
        justify="left",
        anchor="w"
    )

    scan_button.config(text="✓ Scanned")


title = tk.Label(
    window,
    text="File Integrity Monitor",
    font=("Arial", 22, "bold"),
    bg="#1e1e2f",
    fg="white"
)
title.pack(pady=30)

browse_button = tk.Button(
    window,
    text="Browse",
    command=choose_folder,
    bg="#489ee9",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8,
    relief="flat",
    cursor="hand2"
)
browse_button.pack(pady=10)

folder_label = tk.Label(
    window,
    text="No folder selected",
    font=("Arial", 11),
    bg="#1e1e2f",
    fg="white"
)
folder_label.pack(pady=10)

results_label = tk.Label(
    window,
    text="Scan Results",
    font=("Arial", 12),
    bg="#2a2a3d",
    fg="white",
    width=55,
    height=12,
    justify="left",
    anchor="nw",
    padx=20,
    pady=15
)
results_label.pack(pady=20)

scan_button = tk.Button(
    window,
    text="Scan",
    command=scan_folder,
    bg="#489ee9",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8,
    relief="flat",
    cursor="hand2"
)
scan_button.pack(pady=10)

window.mainloop()
