# File Integrity Monitor

A Python-based file integrity monitoring tool that uses SHA-256 hashing to detect modified, deleted, and new files.

## Features

- Select a folder using a graphical interface.
- Calculate SHA-256 hashes for files.
- Maintain a separate baseline for each monitored folder.
- Detect modified, deleted, and new files.
- Display scan results in the GUI.
- Handle scanning without selecting a folder.

## How It Works

1. Select a folder with **Browse**.
2. Click **Scan**.
3. On the first scan of a folder, a baseline is created for that folder.
4. Later scans of the same folder are compared with its own baseline.
5. The application reports modified, deleted, and new files.

Each folder is identified using a hash of its resolved path, so different monitored folders can have separate baseline files.

## Technologies

- Python
- Tkinter
- SHA-256
- JSON
- pathlib

## Run the GUI

```bash
python file_integrity_monitor.py
```

## Project Structure

```text
File-Integrity-Monitor/
├── file_integrity_monitor.py
├── File_Integrity_Monitor.ipynb
├── README.md
└── .gitignore
```

The `baselines/` directory is created automatically when the application runs and is ignored by Git.

## Note

The current implementation scans files directly inside the selected folder. Subfolders are not recursively scanned.
