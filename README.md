# LRC Timeline Editor

<div align="center">

[English](./README.md) · [中文](./README-zh.md)

</div>

**LRC Timeline Editor** is a desktop application crafted for music enthusiasts and lyric translators. It offers an efficient and intuitive tool for creating and calibrating bilingual LRC lyric files. By seamlessly integrating audio playback with timestamp editing, you can precisely tag every line of lyric, making professional-grade lyric creation easier than ever.

## ✨ Key Features

  * **Broad Audio Support**: Load various popular audio formats like `mp3`, `wav`, `flac`, `m4a`, and `ogg` to use as a timeline reference.
  * **Intelligent Lyric Parsing**:
      * Easily open existing `LRC` or `TXT` files. The application intelligently recognizes single-line and multi-line bilingual formats.
      * Automatically handles `UTF-8` and `GBK` encodings to prevent garbled text issues.
      * When saving, you can choose to merge bilingual lyrics into a single line or keep them as separate lines to suit different players.
  * **Precise Playback Control**:
      * Full playback functionality including play, pause, stop, and seeking.
      * Use the slider or hotkeys for precise 1-second rewinds and forwards.
      * Dynamically adjust playback speed and volume for easier, slow-paced calibration.
  * **Efficient Lyric Editing**:
      * Intuitively edit timestamps, original lyrics, and translated lyrics in a table view.
      * Flexible editing options including adding, deleting, merging, and splitting lyric lines.
  * **One-Click Timestamping**:
      * While audio is playing, use the `F8` hotkey or a button to mark the current timestamp for the selected lyric line.
      * Double-click any lyric line to start playback from its corresponding timestamp for quick verification.
  * **Real-time Highlighting & Scrolling**:
      * During playback, the current lyric line is automatically highlighted and scrolled to the center of the view, keeping your focus where it needs to be.
  * **Metadata Support**:
      * Edit the song's title, artist, and album information at any time, and save it directly into the LRC file.

## 🚀 Getting Started

1.  **Install Dependencies**:
    Make sure you have all the necessary libraries installed in your Python environment. The recommended way is to use `pip` with the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application**:
    Execute `main.py` to launch the LRC Timeline Editor.

    ```bash
    python main.py
    ```

## 📂 Project Structure

```
LRC Timeline Editor/
├── assets/
│   └── logo.png
├── main.py             # Application entry point
├── main_window.py      # Main window UI and core logic
├── player.py           # Audio player class encapsulating QMediaPlayer
├── lrc.py              # Handles parsing, processing, and generating LRC files
├── i18n.py             # Internationalization texts for the UI
├── README.md           # English documentation
└── README-zh.md        # Chinese documentation
```
