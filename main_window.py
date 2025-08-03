# main_window.py
import os
import sys
import re
import copy
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView,
    QMenuBar, QFileDialog, QLineEdit, QFormLayout, QSlider, QLabel,
    QStatusBar, QMessageBox, QComboBox, QSizePolicy, QToolBar
)
from PySide6.QtGui import (
    QAction, QKeySequence, QColor, QIcon, QShortcut, QActionGroup,
    QUndoStack, QUndoCommand
)
from PySide6.QtCore import Qt, QUrl, QTimer, QSize
from PySide6.QtMultimedia import QMediaPlayer

import qtawesome as qta

from lrc import Lrc
from player import Player
from i18n import LANG

def resource_path(relative_path):
    """ 获取资源的绝对路径，适用于开发环境和 PyInstaller 打包环境 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class EditCommand(QUndoCommand):
    def __init__(self, main_window, old_lrc, description):
        super().__init__(description)
        self.main_window = main_window
        self.old_lrc = copy.deepcopy(old_lrc)
        self.new_lrc = copy.deepcopy(main_window.lrc)

    def undo(self):
        self.main_window.lrc = self.old_lrc
        self.main_window.update_ui_from_lrc()
        self.main_window.is_dirty = True

    def redo(self):
        self.main_window.lrc = self.new_lrc
        self.main_window.update_ui_from_lrc()
        self.main_window.is_dirty = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lrc = Lrc()
        self.player = Player()
        self.current_audio_file = ""
        self.current_lrc_file = None
        self.save_as_separated_default = True
        self.last_highlighted_row = -1
        self.is_dirty = False

        self.undo_stack = QUndoStack(self)
        self.undo_stack.setUndoLimit(5)

        self.ui_update_timer = QTimer(self)
        self.ui_update_timer.setInterval(10)

        self.setAcceptDrops(True)
        
        self.init_actions()
        self.init_ui()
        self.connect_signals()
        
        self.update_lyrics_table()
        self.update_edit_buttons_state()

    def init_actions(self):
        """初始化所有QAction，方便在菜单和工具栏中复用"""
        # 文件
        self.open_audio_action = QAction(qta.icon('fa5s.music'), LANG["menu_open_audio"], self)
        self.open_lyric_action = QAction(qta.icon('fa5s.file-alt'), LANG["menu_open_lyric"], self)
        self.save_action = QAction(qta.icon('fa5s.save'), LANG["menu_save_lyric"], self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_as_action = QAction(LANG["menu_save_lyric_as"], self)
        self.exit_action = QAction(LANG["menu_exit"], self)

        # 编辑
        self.undo_action = self.undo_stack.createUndoAction(self, LANG["menu_undo"])
        self.redo_action = self.undo_stack.createRedoAction(self, LANG["menu_redo"])
        self.undo_action.setIcon(qta.icon('fa5s.undo'))
        self.redo_action.setIcon(qta.icon('fa5s.redo'))
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)

        # 播放
        self.play_pause_action = QAction(qta.icon('fa5s.play-circle'), LANG['play_button'], self)
        self.stop_action = QAction(qta.icon('fa5s.stop-circle'), LANG['stop_button'], self)
        self.rewind_action = QAction(qta.icon('fa5s.backward'), LANG['rewind_button'], self)
        self.forward_action = QAction(qta.icon('fa5s.forward'), LANG['forward_button'], self)

        # 打轴 Actions
        self.mark_time_action = QAction(LANG['mark_time_button'], self)
        self.mark_time_action.setShortcut(QKeySequence("F8"))

        # 注册快捷键
        self.addAction(self.mark_time_action)


    def init_ui(self):
        """初始化整体UI布局"""
        self.setWindowTitle(LANG["app_title"])
        self.setWindowIcon(QIcon(resource_path('assets/logo.png')))
        self.setGeometry(150, 150, 900, 800)

        self.create_menu()
        self.create_toolbars()

        # 主窗口布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_panel = self.create_left_panel()
        right_panel = self.create_right_panel()

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 3)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(LANG["status_ready"])

    def create_menu(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu(LANG["menu_file"])
        file_menu.addAction(self.open_audio_action)
        file_menu.addAction(self.open_lyric_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # 编辑菜单
        edit_menu = menu_bar.addMenu(LANG["menu_edit"])
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)

        # 设置菜单
        settings_menu = menu_bar.addMenu(LANG["menu_settings"])
        save_format_group = QActionGroup(self)
        save_format_group.setExclusive(True)
        self.save_separated_action = QAction(LANG["setting_save_separated"], self, checkable=True)
        self.save_single_line_action = QAction(LANG["setting_save_single_line"], self, checkable=True)
        
        if self.save_as_separated_default:
            self.save_separated_action.setChecked(True)
        else:
            self.save_single_line_action.setChecked(True)
            
        save_format_menu = settings_menu.addMenu(LANG["setting_default_save_format"])
        save_format_menu.addAction(self.save_separated_action)
        save_format_menu.addAction(self.save_single_line_action)
        save_format_group.addAction(self.save_separated_action)
        save_format_group.addAction(self.save_single_line_action)

        # 帮助菜单
        help_menu = menu_bar.addMenu(LANG["menu_help"])
        about_action = QAction(LANG["menu_about"], self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def create_toolbars(self):
        """创建工具栏"""
        # 文件工具栏
        file_toolbar = QToolBar(LANG["toolbar_file"])
        self.addToolBar(file_toolbar)
        file_toolbar.addAction(self.open_audio_action)
        file_toolbar.addAction(self.open_lyric_action)
        file_toolbar.addAction(self.save_action)

        # 编辑工具栏
        edit_toolbar = QToolBar(LANG["toolbar_edit"])
        self.addToolBar(edit_toolbar)
        edit_toolbar.addAction(self.undo_action)
        edit_toolbar.addAction(self.redo_action)

        # 播放控制工具栏
        playback_toolbar = QToolBar(LANG["toolbar_playback"])
        self.addToolBar(playback_toolbar)
        playback_toolbar.addAction(self.play_pause_action)
        playback_toolbar.addAction(self.stop_action)
        playback_toolbar.addAction(self.rewind_action)
        playback_toolbar.addAction(self.forward_action)
        
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        playback_toolbar.addWidget(self.timeline_slider)
        
        self.time_label = QLabel("00:00.00 / 00:00.00")
        self.time_label.setMinimumWidth(self.fontMetrics().horizontalAdvance("00:00.00 / 00:00.00") + 10)
        playback_toolbar.addWidget(self.time_label)

    def create_left_panel(self):
        """创建左侧控制面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        layout.addWidget(self.create_meta_group())
        layout.addWidget(self.create_secondary_player_controls())
        layout.addWidget(self.create_timeline_controls()) # New group
        layout.addWidget(self.create_edit_controls())
        layout.addStretch()

        return panel

    def create_right_panel(self):
        """创建右侧歌词编辑器面板"""
        lyrics_group = QGroupBox(LANG["tab_editor"])
        lyrics_layout = QVBoxLayout()
        self.lyrics_table = QTableWidget()
        self.setup_lyrics_table()
        lyrics_layout.addWidget(self.lyrics_table)
        lyrics_group.setLayout(lyrics_layout)
        return lyrics_group

    def create_meta_group(self):
        """创建歌曲信息分组"""
        group = QGroupBox(LANG["meta_info_group"])
        layout = QFormLayout(group)
        self.title_edit = QLineEdit()
        self.artist_edit = QLineEdit()
        self.album_edit = QLineEdit()
        layout.addRow(LANG["title"], self.title_edit)
        layout.addRow(LANG["artist"], self.artist_edit)
        layout.addRow(LANG["album"], self.album_edit)
        return group
        
    def create_secondary_player_controls(self):
        """创建播放设置分组"""
        group = QGroupBox(LANG["player_controls_group"])
        layout = QFormLayout(group)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        layout.addRow(LANG["volume_label"], self.volume_slider)

        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "0.75x", "1.0x", "1.5x", "2.0x"])
        self.speed_combo.setCurrentText("1.0x")
        layout.addRow(LANG["speed_label"], self.speed_combo)
        
        return group

    def create_timeline_controls(self):
        """创建打轴操作分组"""
        group = QGroupBox(LANG["timeline_controls_group"])
        layout = QVBoxLayout(group)
        
        self.mark_time_button = QPushButton(LANG["mark_time_button"])
        self.mark_time_button.setIcon(qta.icon('fa5s.map-marker-alt'))
        layout.addWidget(self.mark_time_button)
        
        return group

    def create_edit_controls(self):
        """创建编辑操作分组"""
        group = QGroupBox(LANG["edit_controls_group"])
        layout = QVBoxLayout(group)
        self.add_row_button = QPushButton(LANG["add_row_button"])
        self.remove_row_button = QPushButton(LANG["remove_row_button"])
        self.merge_rows_button = QPushButton(LANG["merge_rows_button"])
        self.split_row_button = QPushButton(LANG["split_row_button"])
        layout.addWidget(self.add_row_button)
        layout.addWidget(self.remove_row_button)
        layout.addWidget(self.merge_rows_button)
        layout.addWidget(self.split_row_button)
        return group

    def connect_signals(self):
        """连接所有信号和槽"""
        # Action-based signals
        self.open_audio_action.triggered.connect(self.open_audio_file)
        self.open_lyric_action.triggered.connect(self.open_lyric_file)
        self.save_action.triggered.connect(self.save_lrc_file)
        self.save_as_action.triggered.connect(self.save_lrc_file_as)
        self.exit_action.triggered.connect(self.close)
        
        self.play_pause_action.triggered.connect(self.toggle_play_pause)
        self.stop_action.triggered.connect(self.player.stop)
        self.rewind_action.triggered.connect(lambda: self.player.set_pos(self.player.get_pos() - 1000))
        self.forward_action.triggered.connect(lambda: self.player.set_pos(self.player.get_pos() + 1000))
        
        # Connect actions to handlers (shortcuts will trigger these)
        self.mark_time_action.triggered.connect(self.mark_timestamp)

        # Widget-based signals
        self.add_row_button.clicked.connect(self.add_row)
        self.remove_row_button.clicked.connect(self.remove_selected_rows)
        self.merge_rows_button.clicked.connect(self.merge_selected_rows)
        self.split_row_button.clicked.connect(self.split_selected_row)
        
        # Connect new buttons
        self.mark_time_button.clicked.connect(self.mark_timestamp)

        self.timeline_slider.sliderMoved.connect(self.player.set_pos)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.speed_combo.currentTextChanged.connect(self.on_speed_changed)
        
        self.lyrics_table.itemDoubleClicked.connect(self.play_from_selection)
        self.lyrics_table.itemChanged.connect(self.sync_table_to_lrc)
        self.lyrics_table.itemSelectionChanged.connect(self.update_edit_buttons_state)

        self.title_edit.editingFinished.connect(lambda: self.create_command("编辑标题"))
        self.artist_edit.editingFinished.connect(lambda: self.create_command("编辑歌手"))
        self.album_edit.editingFinished.connect(lambda: self.create_command("编辑专辑"))
        self.title_edit.textChanged.connect(lambda t: self.lrc.meta.update({'ti': t}))
        self.artist_edit.textChanged.connect(lambda t: self.lrc.meta.update({'ar': t}))
        self.album_edit.textChanged.connect(lambda t: self.lrc.meta.update({'al': t}))

        self.player.durationChanged.connect(self.update_duration)
        self.player.playbackStateChanged.connect(self.handle_player_state_change)
        self.ui_update_timer.timeout.connect(self.update_ui_on_timer)
        
        QShortcut(QKeySequence("Space"), self).activated.connect(self.toggle_play_pause)

    # --- 核心逻辑函数 ---
    
    def create_command(self, description: str):
        old_lrc_snapshot = copy.deepcopy(self.lrc)
        command = EditCommand(self, old_lrc_snapshot, description)
        self.undo_stack.push(command)
        self.is_dirty = True
        
    def closeEvent(self, event):
        if self.is_dirty:
            reply = QMessageBox.question(self, LANG["unsaved_changes_title"],
                                         LANG["unsaved_changes_text"],
                                         QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Save:
                if self.save_lrc_file(): event.accept()
                else: event.ignore()
            elif reply == QMessageBox.StandardButton.Discard: event.accept()
            else: event.ignore()
        else: event.accept()
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(url.toLocalFile().lower().endswith(ext) for url in urls for ext in ['.mp3', '.wav', '.flac', '.m4a', '.ogg', '.lrc', '.txt']):
                event.acceptProposedAction()
                return
        event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            self.status_bar.showMessage(LANG["status_file_dropped"].format(file=os.path.basename(file_path)))
            if any(file_path.lower().endswith(ext) for ext in ['.mp3', '.wav', '.flac', '.m4a', '.ogg']):
                self.open_audio_file(file_path)
            elif any(file_path.lower().endswith(ext) for ext in ['.lrc', '.txt']):
                self.open_lyric_file(file_path)

    def handle_player_state_change(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.ui_update_timer.start()
            self.play_pause_action.setIcon(qta.icon('fa5s.pause-circle'))
            self.play_pause_action.setText(LANG['pause_button'])
        else:
            self.ui_update_timer.stop()
            self.play_pause_action.setIcon(qta.icon('fa5s.play-circle'))
            self.play_pause_action.setText(LANG['play_button'])
            if state == QMediaPlayer.PlaybackState.StoppedState:
                self.timeline_slider.setValue(0)
                self.update_time_label(0, self.player.get_duration())
                self.highlight_current_lyric(-1)

    def toggle_play_pause(self):
        if self.player.is_playing():
            self.player.pause()
        else:
            if self.current_audio_file:
                self.player.play()

    def add_row(self):
        old_lrc_snapshot = copy.deepcopy(self.lrc)
        selected_rows = self.get_selected_rows()
        insert_pos = selected_rows[-1] + 1 if selected_rows else self.lyrics_table.rowCount()
        self.lrc.lyrics.insert(insert_pos, {'ts': None, 'original': '', 'translated': ''})
        self.create_command("添加行")
        self.update_lyrics_table()
        self.lyrics_table.selectRow(insert_pos)

    def remove_selected_rows(self):
        rows = self.get_selected_rows()
        if not rows: return
        reply = QMessageBox.question(self, "确认删除", f"您确定要删除选中的 {len(rows)} 行吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No: return
        
        old_lrc_snapshot = copy.deepcopy(self.lrc)
        for row in reversed(rows):
            del self.lrc.lyrics[row]
        self.create_command("删除行")
        self.update_lyrics_table()

    def merge_selected_rows(self):
        rows = self.get_selected_rows()
        if len(rows) < 2: return

        old_lrc_snapshot = copy.deepcopy(self.lrc)
        base_row_idx = rows[0]
        base_lyric = self.lrc.lyrics[base_row_idx]
        for row_idx in reversed(rows[1:]):
            lyric_to_merge = self.lrc.lyrics.pop(row_idx)
            base_lyric['original'] += " " + lyric_to_merge.get('original', '')
            base_lyric['translated'] += " " + lyric_to_merge.get('translated', '')
        base_lyric['original'] = base_lyric['original'].strip()
        base_lyric['translated'] = base_lyric['translated'].strip()

        self.create_command("合并行")
        self.update_lyrics_table()
        self.lyrics_table.selectRow(base_row_idx)

    def split_selected_row(self):
        rows = self.get_selected_rows()
        if len(rows) != 1: return

        row = rows[0]
        original_text = self.lrc.lyrics[row].get('original', '')
        parts = original_text.split()
        if len(parts) < 2: return

        old_lrc_snapshot = copy.deepcopy(self.lrc)
        self.lrc.lyrics[row]['original'] = parts[0]
        for i, part in enumerate(parts[1:]):
            self.lrc.lyrics.insert(row + i + 1, {'ts': None, 'original': part, 'translated': ''})
            
        self.create_command("拆分行")
        self.update_lyrics_table()

    def mark_timestamp(self):
        rows = self.get_selected_rows()
        if not rows:
            QMessageBox.warning(self, LANG["error_title"], LANG["error_no_selection"])
            return
        
        old_lrc_snapshot = copy.deepcopy(self.lrc)
        current_pos_ms = self.player.get_pos()
        current_ts = current_pos_ms / 1000.0
        for row in rows:
            self.lrc.lyrics[row]['ts'] = current_ts
        
        self.create_command("标记时间戳")
        self.update_lyrics_table()
        # After marking, ensure the same rows remain selected
        self.lyrics_table.blockSignals(True)
        for row in rows:
            self.lyrics_table.selectRow(row)
        self.lyrics_table.blockSignals(False)

    def show_about_dialog(self): 
        QMessageBox.about(self, LANG["about_dialog_title"], LANG["about_dialog_text"])

    def update_save_format_setting(self, is_separated): 
        self.save_as_separated_default = is_separated

    def setup_lyrics_table(self):
        self.lyrics_table.setColumnCount(3)
        self.lyrics_table.setHorizontalHeaderLabels([LANG["lyrics_table_header_time"], LANG["lyrics_table_header_original"], LANG["lyrics_table_header_translated"]])
        self.lyrics_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        header = self.lyrics_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.lyrics_table.setStyleSheet("QTableWidget::item:selected { background-color: #5a98d1; color: white; }")

    def on_volume_changed(self, value):
        self.player.set_volume(value / 100.0)

    def on_speed_changed(self, text):
        rate = float(text.replace('x', ''))
        self.player.set_playback_rate(rate)

    def update_duration(self, duration):
        self.timeline_slider.setRange(0, duration)
        self.update_time_label(self.player.get_pos(), duration)

    def format_time(self, ms):
        if ms < 0: ms = 0
        total_seconds = ms / 1000.0
        minutes = int(total_seconds / 60)
        seconds = int(total_seconds % 60)
        centiseconds = int((total_seconds - minutes * 60 - seconds) * 100)
        return f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

    def update_time_label(self, pos, dur):
        self.time_label.setText(f"{self.format_time(pos)} / {self.format_time(dur)}")

    def update_ui_on_timer(self):
        if self.player.is_playing() and not self.timeline_slider.isSliderDown():
            pos = self.player.get_pos()
            self.timeline_slider.setValue(pos)
            self.update_time_label(pos, self.player.get_duration())
            self.highlight_current_lyric(pos / 1000.0)

    def open_audio_file(self, file_path=None):
        if not file_path: 
            file_path, _ = QFileDialog.getOpenFileName(self, LANG["open_audio_title"], "", LANG["audio_files_filter"])
        if file_path: 
            self.current_audio_file = file_path
            self.player.load(file_path)
            self.status_bar.showMessage(LANG["status_audio_loaded"].format(file=os.path.basename(file_path)))

    def open_lyric_file(self, file_path=None):
        if not file_path: 
            file_path, _ = QFileDialog.getOpenFileName(self, LANG["open_lyric_title"], "", LANG["lyric_files_filter"])
        if file_path:
            try:
                try: 
                    with open(file_path, 'r', encoding='utf-8') as f:
                        f_content = f.read()
                except UnicodeDecodeError: 
                    with open(file_path, 'r', encoding='gbk') as f:
                        f_content = f.read()
                self.lrc.parse_from_text(f_content)
                self.update_ui_from_lrc()
                self.current_lrc_file = file_path
                self.status_bar.showMessage(LANG["status_lyric_loaded"].format(file=os.path.basename(file_path)))
                self.undo_stack.clear()
                self.is_dirty = False
            except Exception as e: 
                QMessageBox.critical(self, LANG["error_title"], LANG["error_open_file"].format(e=e))

    def save_lrc_file(self):
        path = self.current_lrc_file
        if path and os.path.exists(os.path.dirname(path)):
            self.sync_table_to_lrc_before_save()
            try:
                with open(path, 'w', encoding='utf-8') as f: 
                    f.write(self.lrc.to_lrc_string(self.save_as_separated_default))
                self.status_bar.showMessage(LANG["status_lyric_saved"].format(file=path))
                self.is_dirty = False
                return True
            except Exception as e: 
                QMessageBox.critical(self, LANG["error_title"], f"无法保存文件: {e}")
                return False
        else: 
            return self.save_lrc_file_as()

    def save_lrc_file_as(self):
        self.sync_table_to_lrc_before_save()
        path, _ = QFileDialog.getSaveFileName(self, LANG["save_lyric_title"], os.path.dirname(self.current_lrc_file or ""), LANG["lrc_file_filter"])
        if path:
            choice = QMessageBox.question(self, LANG["save_format_prompt_title"], LANG["save_format_prompt_text"], QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Yes)
            if choice == QMessageBox.StandardButton.Cancel: 
                return False
            try:
                with open(path, 'w', encoding='utf-8') as f: 
                    f.write(self.lrc.to_lrc_string(choice == QMessageBox.StandardButton.Yes))
                self.current_lrc_file = path
                self.status_bar.showMessage(LANG["status_lyric_saved"].format(file=path))
                self.is_dirty = False
                return True
            except Exception as e: 
                QMessageBox.critical(self, LANG["error_title"], f"无法保存文件: {e}")
                return False
        return False
    
    def sync_table_to_lrc_before_save(self):
        """A simplified version of sync_table_to_lrc without creating undo commands."""
        for row in range(self.lyrics_table.rowCount()):
            if 0 <= row < len(self.lrc.lyrics):
                ts_str = self.lyrics_table.item(row, 0).text()
                original = self.lyrics_table.item(row, 1).text()
                translated = self.lyrics_table.item(row, 2).text()
                ts = None
                match = re.match(r'(\d+):(\d{2,2})\.(\d{2,2})', ts_str)
                if match: 
                    m, s, cs = map(int, match.groups())
                    ts = m * 60 + s + cs / 100.0
                self.lrc.lyrics[row] = {'ts': ts, 'original': original, 'translated': translated}

    def update_ui_from_lrc(self):
        self.lyrics_table.blockSignals(True)
        self.title_edit.setText(self.lrc.meta.get('ti', ''))
        self.artist_edit.setText(self.lrc.meta.get('ar', ''))
        self.album_edit.setText(self.lrc.meta.get('al', ''))
        self.lyrics_table.blockSignals(False)
        self.update_lyrics_table()

    def check_and_highlight_disordered_timestamps(self):
        last_ts = -1.0
        for i in range(self.lyrics_table.rowCount()):
            item = self.lyrics_table.item(i, 0)
            item.setBackground(QColor("transparent"))
            if not item.text(): 
                continue
            match = re.match(r'(\d+):(\d{2,2})\.(\d{2,2})', item.text())
            if match:
                m, s, cs = map(int, match.groups())
                current_ts = m * 60 + s + cs / 100.0
                if current_ts < last_ts: 
                    item.setBackground(QColor("red"))
                last_ts = current_ts

    def update_lyrics_table(self):
        self.lyrics_table.blockSignals(True)
        self.lyrics_table.setRowCount(len(self.lrc.lyrics))
        for i, line in enumerate(self.lrc.lyrics):
            ts, original, translated = line.get('ts'), line.get('original', ''), line.get('translated', '')
            time_str = self.format_time(ts * 1000) if ts is not None else ""
            self.lyrics_table.setItem(i, 0, QTableWidgetItem(time_str))
            self.lyrics_table.setItem(i, 1, QTableWidgetItem(original))
            self.lyrics_table.setItem(i, 2, QTableWidgetItem(translated))
        self.lyrics_table.resizeRowsToContents()
        self.check_and_highlight_disordered_timestamps()
        self.lyrics_table.blockSignals(False)
        self.update_edit_buttons_state()

    def sync_table_to_lrc(self, item=None):
        if not item: 
            return
        old_lrc_snapshot = copy.deepcopy(self.lrc)
        row = item.row()
        if 0 <= row < len(self.lrc.lyrics):
            ts_str = self.lyrics_table.item(row, 0).text()
            original = self.lyrics_table.item(row, 1).text()
            translated = self.lyrics_table.item(row, 2).text()
            ts = None
            match = re.match(r'(\d+):(\d{2,2})\.(\d{2,2})', ts_str)
            if match: 
                m, s, cs = map(int, match.groups())
                ts = m * 60 + s + cs / 100.0
            self.lrc.lyrics[row] = {'ts': ts, 'original': original, 'translated': translated}
            self.create_command("编辑歌词")
            if item.column() == 0: 
                self.check_and_highlight_disordered_timestamps()

    def highlight_current_lyric(self, current_sec):
        target_idx = -1
        for i, lyric in enumerate(self.lrc.lyrics):
            if lyric.get('ts') is None: 
                continue
            if current_sec >= lyric['ts']: 
                target_idx = i
            else: 
                break
        if target_idx != -1 and self.lyrics_table.selectionModel().currentIndex().row() != target_idx:
            self.lyrics_table.selectRow(target_idx)
            self.lyrics_table.scrollToItem(self.lyrics_table.item(target_idx, 0), QAbstractItemView.ScrollHint.PositionAtCenter)

    def get_selected_rows(self): 
        return sorted(list(set(index.row() for index in self.lyrics_table.selectedIndexes())))

    def update_edit_buttons_state(self):
        count = len(self.get_selected_rows())
        self.remove_row_button.setEnabled(count > 0)
        self.mark_time_action.setEnabled(count > 0)
        self.split_row_button.setEnabled(count == 1)
        self.merge_rows_button.setEnabled(count > 1)
        # Update new buttons
        self.mark_time_button.setEnabled(count > 0)

    def play_from_selection(self, item):
        row = item.row()
        if 0 <= row < len(self.lrc.lyrics):
            lyric = self.lrc.lyrics[row]
            if lyric and lyric.get('ts') is not None:
                self.player.set_pos(int(lyric['ts'] * 1000))
                if not self.player.is_playing(): 
                    self.player.play()