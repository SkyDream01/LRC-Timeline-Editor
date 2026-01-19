# i18n.py
# 存储所有UI界面文本

LOCALE_CN = {
    "app_title": "LRC Timeline Editor",
    "menu_file": "文件(&F)",
    "menu_edit": "编辑(&E)",
    "menu_help": "帮助(&H)",
    "menu_settings": "设置(&T)",
    "menu_about": "关于(&A)",
    "menu_open_audio": "打开音频(&A)",
    "menu_open_lyric": "打开歌词文本/LRC(&L)",
    "menu_save_lyric": "保存LRC文件(&S)",
    "menu_save_lyric_as": "另存为(&A)...",
    "menu_exit": "退出(&X)",
    "menu_undo": "撤销(&U)",
    "menu_redo": "重做(&R)",

    "toolbar_file": "文件操作",
    "toolbar_edit": "编辑操作",
    "toolbar_playback": "播放控制",

    "setting_default_save_format": "默认双语保存格式",
    "setting_save_separated": "分行保存 (推荐)",
    "setting_save_single_line": "单行'/'分隔保存",
    "setting_language": "语言 / Language",

    "about_dialog_title": "关于 LRC Timeline Editor",
    "about_dialog_text": (
        "<h3>LRC Timeline Editor</h3>"
        "<p>一个用于创建和校准双语LRC歌词的工具。</p>"
        "<p>版本: 1.5.0 </p>"
        "<p>项目主页: <a href='https://github.com/SkyDream01/LRC-Timeline-Editor'>https://github.com/SkyDream01/LRC-Timeline-Editor</a></p>"
        "<p>这是一个开源项目，欢迎贡献！</p>"
    ),
    
    "tab_editor": "歌词编辑器",
    
    "meta_info_group": "歌曲信息",
    "title": "歌名:",
    "artist": "歌手:",
    "album": "专辑:",
    
    "player_controls_group": "播放设置",
    "play_button": "播放",
    "pause_button": "暂停",
    "stop_button": "停止",
    "rewind_button": "<< 1s",
    "forward_button": "1s >>",
    "volume_label": "音量:",
    "speed_label": "速度:",

    "lyrics_table_header_time": "时间戳",
    "lyrics_table_header_original": "原文歌词",
    "lyrics_table_header_translated": "译文歌词",

    "edit_controls_group": "编辑操作",
    "add_row_button": "增添一行",
    "remove_row_button": "删除选中行",
    "merge_rows_button": "合并选中行",
    "split_row_button": "拆分选中行",

    "timeline_controls_group": "打轴操作",
    "mark_time_button": "标记时间戳",
    
    "save_format_prompt_title": "选择保存格式",
    "save_format_prompt_text": "您想如何保存双语歌词？\n- 'Yes' 保存为分行格式\n- 'No' 保存为单行'/'分隔格式",
    
    "unsaved_changes_title": "未保存的更改",
    "unsaved_changes_text": "您有未保存的更改。您想在退出前保存它们吗？",
    
    "status_ready": "就绪",
    "status_audio_loaded": "音频已加载: {file}",
    "status_lyric_loaded": "歌词已加载: {file}",
    "status_file_dropped": "已加载文件: {file}",
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
    "error_need_two_rows": "此操作需要选择两行或更多行。",
    "confirm_delete_title": "确认删除",
    "confirm_delete_text": "您确定要删除选中的 {rows} 行吗？",
    "shortcuts_action": "快捷键列表",
    "shortcuts_dialog_title": "快捷键列表",
    "replay_line_action": "重听当前行",
    "replay_line_tooltip": "重听当前行 (F5)",
    "control_console": "控制台",
    "add_row_tooltip": "在下方插入新行",
    "remove_row_tooltip": "删除选中行",
    "merge_rows_tooltip": "合并选中行",
    "split_row_tooltip": "拆分选中行",
    "error_unknown": "未知错误: {e}\n请检查文件格式或报告此错误。",
    "error_save_system": "无法保存文件（系统错误）: {e}",
    "error_save_unknown": "保存文件时发生未知错误: {e}",
    "menu_view": "视图(&V)",
    "view_show_translated": "显示译文列",
    "view_romaji_tooltips": "罗马音提示",
    "romaji_tooltip_unavailable": "（罗马音功能不可用）",
    
    # Undo Command Descriptions
    "undo_edit_title": "编辑标题",
    "undo_edit_artist": "编辑歌手",
    "undo_edit_album": "编辑专辑",
    "undo_add_row": "添加行",
    "undo_remove_row": "删除行",
    "undo_merge_rows": "合并行",
    "undo_split_row": "拆分行",
    "undo_mark_timestamp": "标记时间戳",
    "undo_edit_lyric": "编辑歌词",

    "shortcuts_dialog_content": """
        <b>播放控制:</b><br>
        Space: 播放/暂停<br>
        F5: 重听当前行<br><br>
        
        <b>打轴操作:</b><br>
        F8: 标记时间戳并跳转下一行<br><br>
        
        <b>编辑操作:</b><br>
        Ctrl+Enter: 插入新行<br>
        Ctrl+Del: 删除选中行<br>
        Ctrl+J: 合并选中行<br>
        Ctrl+K: 拆分选中行<br>
        Ctrl+S: 保存文件<br>
        Ctrl+Z: 撤销<br>
        Ctrl+Y: 重做
        """
}

LOCALE_EN = {
    "app_title": "LRC Timeline Editor",
    "menu_file": "File(&F)",
    "menu_edit": "Edit(&E)",
    "menu_help": "Help(&H)",
    "menu_settings": "Settings(&T)",
    "menu_about": "About(&A)",
    "menu_open_audio": "Open Audio(&A)",
    "menu_open_lyric": "Open Lyrics/LRC(&L)",
    "menu_save_lyric": "Save LRC(&S)",
    "menu_save_lyric_as": "Save As(&A)...",
    "menu_exit": "Exit(&X)",
    "menu_undo": "Undo(&U)",
    "menu_redo": "Redo(&R)",

    "toolbar_file": "File Ops",
    "toolbar_edit": "Edit Ops",
    "toolbar_playback": "Playback",

    "setting_default_save_format": "Bilingual Save Format",
    "setting_save_separated": "Separate Lines (Recommended)",
    "setting_save_single_line": "Single Line with '/'",
    "setting_language": "Language / 语言",

    "about_dialog_title": "About LRC Timeline Editor",
    "about_dialog_text": (
        "<h3>LRC Timeline Editor</h3>"
        "<p>A tool for creating and calibrating bilingual LRC lyrics.</p>"
        "<p>Version: 1.5.0 </p>"
        "<p>Homepage: <a href='https://github.com/SkyDream01/LRC-Timeline-Editor'>https://github.com/SkyDream01/LRC-Timeline-Editor</a></p>"
        "<p>This is an open source project. Contributions welcome!</p>"
    ),
    
    "tab_editor": "Lyric Editor",
    
    "meta_info_group": "Song Info",
    "title": "Title:",
    "artist": "Artist:",
    "album": "Album:",
    
    "player_controls_group": "Playback Settings",
    "play_button": "Play",
    "pause_button": "Pause",
    "stop_button": "Stop",
    "rewind_button": "<< 1s",
    "forward_button": "1s >>",
    "volume_label": "Vol:",
    "speed_label": "Spd:",

    "lyrics_table_header_time": "Timestamp",
    "lyrics_table_header_original": "Original",
    "lyrics_table_header_translated": "Translation",

    "edit_controls_group": "Edit Actions",
    "add_row_button": "Add Row",
    "remove_row_button": "Remove Rows",
    "merge_rows_button": "Merge Rows",
    "split_row_button": "Split Row",

    "timeline_controls_group": "Timeline Actions",
    "mark_time_button": "Mark Timestamp",
    
    "save_format_prompt_title": "Select Save Format",
    "save_format_prompt_text": "How to save bilingual lyrics?\n- 'Yes' for Separate Lines\n- 'No' for Single Line with '/'",
    
    "unsaved_changes_title": "Unsaved Changes",
    "unsaved_changes_text": "You have unsaved changes. Save before exit?",
    
    "status_ready": "Ready",
    "status_audio_loaded": "Audio Loaded: {file}",
    "status_lyric_loaded": "Lyrics Loaded: {file}",
    "status_file_dropped": "File Dropped: {file}",
    "status_lyric_saved": "Lyrics Saved: {file}",
    
    "open_audio_title": "Select Audio File",
    "open_lyric_title": "Select Lyrics File",
    "save_lyric_title": "Save LRC File",
    
    "audio_files_filter": "Audio Files (*.mp3 *.wav *.flac *.m4a *.ogg)",
    "lyric_files_filter": "Lyric/Text Files (*.lrc *.txt)",
    "lrc_file_filter": "LRC Files (*.lrc)",

    "error_title": "Error",
    "error_open_file": "Cannot open/parse file: {e}",
    "error_no_selection": "Please select a row first.",
    "error_need_one_row": "Please select exactly one row.",
    "error_need_two_rows": "Please select two or more rows.",
    "confirm_delete_title": "Confirm Delete",
    "confirm_delete_text": "Delete selected {rows} rows?",
    "shortcuts_action": "Shortcuts",
    "shortcuts_dialog_title": "Shortcuts",
    "replay_line_action": "Replay Line",
    "replay_line_tooltip": "Replay Current Line (F5)",
    "control_console": "Console",
    "add_row_tooltip": "Insert new row below",
    "remove_row_tooltip": "Delete selected rows",
    "merge_rows_tooltip": "Merge selected rows",
    "split_row_tooltip": "Split selected row",
    "error_unknown": "Unknown Error: {e}\nPlease check file format.",
    "error_save_system": "Save failed (System): {e}",
    "error_save_unknown": "Save failed (Unknown): {e}",
    "menu_view": "View(&V)",
    "view_show_translated": "Show Translation Column",
    "view_romaji_tooltips": "Romaji Tooltips",
    "romaji_tooltip_unavailable": "(Unavailable)",

    # Undo Command Descriptions
    "undo_edit_title": "Edit Title",
    "undo_edit_artist": "Edit Artist",
    "undo_edit_album": "Edit Album",
    "undo_add_row": "Add Row",
    "undo_remove_row": "Remove Rows",
    "undo_merge_rows": "Merge Rows",
    "undo_split_row": "Split Row",
    "undo_mark_timestamp": "Mark Timestamp",
    "undo_edit_lyric": "Edit Lyric",

    "shortcuts_dialog_content": """
        <b>Playback:</b><br>
        Space: Play/Pause<br>
        F5: Replay Current Line<br><br>
        
        <b>Timeline:</b><br>
        F8: Mark Timestamp & Next Line<br><br>
        
        <b>Editing:</b><br>
        Ctrl+Enter: Insert Row<br>
        Ctrl+Del: Delete Rows<br>
        Ctrl+J: Merge Rows<br>
        Ctrl+K: Split Row<br>
        Ctrl+S: Save File<br>
        Ctrl+Z: Undo<br>
        Ctrl+Y: Redo
        """
}

# 默认语言 (Default Language)
LANG = {}
LANG.update(LOCALE_CN)

def set_language(lang_code):
    """切换语言 / Switch Language"""
    LANG.clear()
    if lang_code == "en_US":
        LANG.update(LOCALE_EN)
    else:
        LANG.update(LOCALE_CN)
