<div align="center">

[English](./README.md) · [中文](./README-zh.md)

</div>

# LRC Timeline Editor

This is a desktop application for editing LRC lyric files, specially designed for creating and calibrating bilingual lyrics. It provides a visual interface to synchronize audio playback with the adjustment of lyric timestamps.

## Key Features

  * **Audio Loading**: Supports loading various audio formats (mp3, wav, flac, m4a, ogg) as a reference for the timeline.
  * **Lyric File Handling**:
      * Opens existing LRC or TXT files and intelligently parses single-line or multi-line bilingual formats.
      * Supports lyric files in both UTF-8 and GBK encodings.
      * Saves edited lyrics as standard LRC files, with the option to save bilingual lyrics in separate lines or a single line format.
  * **Playback Control**:
      * Full play, pause, and stop functionality.
      * Precise time seeking (forward/rewind 1s) via a slider or buttons.
      * Adjustable playback speed and volume.
  * **Lyric Editing**:
      * Intuitively edit timestamps, original, and translated lyrics in a table.
      * Easily add, delete, merge, or split lyric lines.
  * **Timeline Tagging (Timestamping)**:
      * While playing audio, use a hotkey (F8) or a button to mark the current timestamp for the selected lyric line.
      * Double-click a lyric line to start playback from its timestamp.
  * **Real-time Highlighting**: As the audio plays, the current lyric line is highlighted in the table, which also scrolls automatically.
  * **Metadata Editing**: Supports editing the song's title, artist, and album information.

## How to Run

1.  **Install Dependencies**:
    Install all necessary libraries using pip. Please refer to the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application**:
    Execute the `main.py` file to start the application.

    ```bash
    python main.py
    ```

## Project File Structure

  * `main.py`: The entry point of the application.
  * `main_window.py`: Implements the main window UI and core logic.
  * `player.py`: A player class that encapsulates `QMediaPlayer` for audio playback.
  * `lrc.py`: Responsible for parsing, processing, and generating LRC files.
  * `i18n.py`: Stores all UI text for internationalization.
  * `styles.qss`: (Optional) A QSS file for defining the application's styles.

