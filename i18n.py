# i18n.py
# 存储所有UI界面文本

LANG = {
    "app_title": "LRC Timeline Editor",
    "menu_file": "文件(&F)",
    "menu_help": "帮助(&H)",
    "menu_about": "关于(&A)",
    "menu_open_audio": "打开音频(&A)",
    "menu_open_lyric": "打开歌词文本/LRC(&L)",
    "menu_save_lyric": "保存LRC文件(&S)",
    "menu_exit": "退出(&X)",

    "about_dialog_title": "关于 LRC Timeline Editor",
    "about_dialog_text": (
        "<h3>LRC Timeline Editor</h3>"
        "<p>一个用于创建和校准双语LRC歌词的工具。</p>"
        "<p>版本: 1.0.0</p>"
        "<p>项目主页: <a href='https://github.com/SkyDream01/LRC-Timeline-Editor'>https://github.com/SkyDream01/LRC-Timeline-Editor</a></p>"
        "<p>这是一个开源项目，欢迎贡献！</p>"
    ),
    
    "tab_editor": "歌词编辑器",
    
    "meta_info_group": "歌曲信息",
    "title": "歌名:",
    "artist": "歌手:",
    "album": "专辑:",
    
    "player_controls_group": "播放控制",
    "play_button": "播放",
    "pause_button": "暂停",
    "stop_button": "停止",
    "rewind_button": "<< 1s",
    "forward_button": "1s >>",
    "volume_label": "音量",
    "speed_label": "速度",

    "lyrics_table_header_time": "时间戳",
    "lyrics_table_header_original": "原文歌词",
    "lyrics_table_header_translated": "译文歌词",

    "edit_controls_group": "编辑操作",
    "add_row_button": "增添一行",
    "remove_row_button": "删除选中行",
    "merge_rows_button": "合并选中行",
    "split_row_button": "拆分选中行",

    "timeline_controls_group": "打轴操作",
    "mark_time_button": "标记时间 (F8)",
    
    "status_ready": "就绪",
    "status_audio_loaded": "音频已加载: {file}",
    "status_lyric_loaded": "歌词已加载",
    "status_lyric_saved": "歌词已保存到: {file}",
    
    "open_audio_title": "选择一个音频文件",
    "open_lyric_title": "选择一个歌词文件",
    "save_lyric_title": "保存 LRC 文件",
    
    "audio_files_filter": "音频文件 (*.mp3 *.wav *.flac *.m4a *.ogg)",
    "lyric_files_filter": "歌词和文本文件 (*.lrc *.txt)",
    "lrc_file_filter": "LRC 文件 (*.lrc)",

    "error_title": "错误",
    "error_open_file": "无法打开或解析文件: {e}",
    "error_no_selection": "请先在表格中选择一行。",
    "error_need_one_row": "此操作需要且仅能选择一行。",
    "error_need_two_rows": "此操作需要选择两行或更多行。"
}