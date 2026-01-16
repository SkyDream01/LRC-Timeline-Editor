# LRC Timeline Editor

<br/>

**A professional tool for creating and calibrating bilingual LRC lyrics.**
<br/>
**专为双语LRC歌词制作与校准打造的专业工具。**

<br/>

[English](#-english) | [中文说明](#-中文说明)

</div>

---

<div id="english"></div>

## 📖 English

**LRC Timeline Editor** is a desktop application crafted for music enthusiasts and lyric translators. It offers an efficient and intuitive tool for creating and calibrating bilingual LRC lyric files. By seamlessly integrating audio playback with timestamp editing, you can precisely tag every line of lyric, making professional-grade lyric creation easier than ever.

### ✨ Key Features

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

### 🚀 Getting Started

1.  **Install Dependencies**
    Make sure you have all the necessary libraries installed in your Python environment.

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application**
    Execute `main.py` to launch the LRC Timeline Editor.

    ```bash
    python main.py
    ```

### 📂 Project Structure

```text
LRC Timeline Editor/
├── assets/
│   └── logo.png
├── main.py             # Application entry point
├── main_window.py      # Main window UI and core logic
├── player.py           # Audio player class encapsulating QMediaPlayer
├── lrc.py              # Handles parsing, processing, and generating LRC files
├── i18n.py             # Internationalization texts for the UI
└── README.md           # Documentation

```

---

<div id="chinese"></div>

## 🇨🇳 中文说明

**LRC Timeline Editor** 是一款专为音乐爱好者和歌词译者打造的桌面应用，旨在提供一个高效、直观的双语LRC歌词制作和校准工具。通过将音频播放与时间戳编辑无缝结合，您可以精确地为每一句歌词打上时间标签，轻松创作出专业级的歌词文件。

### ✨ 核心功能

* **广泛的音频支持**: 可加载 `mp3`, `wav`, `flac`, `m4a`, `ogg` 等多种主流音频格式，作为歌词制作的时间基准。
* **智能歌词解析**:
* 轻松打开现有的 `LRC` 或 `TXT` 文件，程序能智能识别单行或分行的双语歌词格式。
* 自动处理 `UTF-8` 和 `GBK` 编码，避免乱码烦恼。
* 保存时，您可以选择将双语歌词合并为一行或保持分行格式，满足不同播放器的需求。


* **精准播放控制**:
* 包含完整的播放、暂停、停止和跳转功能。
* 通过滑动条或快捷键，实现1秒精度的快进与快退。
* 支持播放速度和音量的动态调整，便于慢速校准。


* **高效歌词编辑**:
* 在直观的表格中，批量编辑时间戳、原文和译文。
* 提供增加、删除、合并、拆分歌词行等多种实用编辑功能，操作灵活。


* **一键“打轴”**:
* 在音频播放时，使用 `F8` 快捷键或点击按钮，即可为当前选中的歌词行标记时间戳。
* 双击任意一行歌词，即可从该行对应的时间点开始播放，方便快速核对。


* **实时高亮与滚动**:
* 播放过程中，当前歌词行会在表格中自动高亮显示并滚动到视野中央，让您始终聚焦于当前位置。


* **元数据支持**:
* 可随时编辑歌曲的标题、歌手和专辑信息，并保存至LRC文件中。



### 🚀 如何开始

1. **安装依赖**
请确保您的Python环境中已安装所有必要的库。推荐使用 `pip` 根据 `requirements.txt` 文件一键安装。
```bash
pip install -r requirements.txt

```


2. **启动应用**
执行 `main.py` 即可启动LRC Timeline Editor。
```bash
python main.py

```



### 📂 项目结构

```text
LRC Timeline Editor/
├── assets/
│   └── logo.png
├── main.py             # 应用程序入口
├── main_window.py      # 主窗口界面与核心逻辑
├── player.py           # 封装了 QMediaPlayer 的音频播放器
├── lrc.py              # 负责 LRC 文件的解析、处理和生成
├── i18n.py             # UI 界面的国际化文本
└── README.md           # 说明文档

```
