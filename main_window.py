# main_window.py
import os
import sys
import re
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView,
    QMenuBar, QFileDialog, QLineEdit, QFormLayout, QSlider, QLabel,
    QStatusBar, QMessageBox, QComboBox, QSizePolicy
)
from PySide6.QtGui import QAction, QKeySequence, QColor, QIcon, QShortcut
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lrc = Lrc()
        self.player = Player()
        self.current_audio_file = ""
        self.last_highlighted_row = -1

        self.ui_update_timer = QTimer(self)
        self.ui_update_timer.setInterval(33)

        self.init_ui()
        self.connect_signals()
        self.update_lyrics_table()

    def init_ui(self):
        self.setWindowTitle(LANG["app_title"])
        self.setWindowIcon(QIcon(resource_path('assets/logo.png')))
        self.setGeometry(150, 150, 1200, 800)
        self.create_menu()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        top_panel_layout = QHBoxLayout()
        meta_group = self.create_meta_group()
        player_group = self.create_player_controls()
        top_panel_layout.addWidget(meta_group, 1)
        top_panel_layout.addWidget(player_group, 2)

        lyrics_group = QGroupBox(LANG["tab_editor"])
        lyrics_layout = QHBoxLayout()
        self.lyrics_table = QTableWidget()
        self.setup_lyrics_table()
        lyrics_layout.addWidget(self.lyrics_table)
        lyrics_group.setLayout(lyrics_layout)

        bottom_panel_layout = QHBoxLayout()
        edit_group = self.create_edit_controls()
        timeline_group = self.create_timeline_controls()
        bottom_panel_layout.addWidget(edit_group)
        bottom_panel_layout.addWidget(timeline_group)
        bottom_panel_layout.addStretch()

        main_layout.addLayout(top_panel_layout, 0)
        main_layout.addWidget(lyrics_group, 1)
        main_layout.addLayout(bottom_panel_layout, 0)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(LANG["status_ready"])

    def create_menu(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu(LANG["menu_file"])
        open_audio_action = QAction(LANG["menu_open_audio"], self)
        open_lyric_action = QAction(LANG["menu_open_lyric"], self)
        save_action = QAction(LANG["menu_save_lyric"], self)
        exit_action = QAction(LANG["menu_exit"], self)
        open_audio_action.triggered.connect(self.open_audio_file)
        open_lyric_action.triggered.connect(self.open_lyric_file)
        save_action.triggered.connect(self.save_lrc_file)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(open_audio_action)
        file_menu.addAction(open_lyric_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu(LANG["menu_help"])
        about_action = QAction(LANG["menu_about"], self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        QMessageBox.about(self, LANG["about_dialog_title"], LANG["about_dialog_text"])

    def create_meta_group(self):
        group = QGroupBox(LANG["meta_info_group"])
        layout = QFormLayout()
        self.title_edit = QLineEdit()
        self.artist_edit = QLineEdit()
        self.album_edit = QLineEdit()
        layout.addRow(LANG["title"], self.title_edit)
        layout.addRow(LANG["artist"], self.artist_edit)
        layout.addRow(LANG["album"], self.album_edit)
        group.setLayout(layout)
        return group

    def create_player_controls(self):
        group = QGroupBox(LANG["player_controls_group"])
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        controls_layout = QHBoxLayout()
        self.play_pause_button = QPushButton()
        self.stop_button = QPushButton(qta.icon('fa5s.stop-circle', color='white'), f" {LANG['stop_button']}")
        self.rewind_button = QPushButton(qta.icon('fa5s.backward', color='white'), f" {LANG['rewind_button']}")
        self.forward_button = QPushButton(qta.icon('fa5s.forward', color='white'), f" {LANG['forward_button']}")

        for btn in [self.play_pause_button, self.stop_button, self.rewind_button, self.forward_button]:
            icon_size = int(btn.fontMetrics().height() * 1.2)
            btn.setIconSize(QSize(icon_size, icon_size))
            btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        controls_layout.addWidget(self.play_pause_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addStretch()
        controls_layout.addWidget(self.rewind_button)
        controls_layout.addWidget(self.forward_button)

        timeline_layout = QHBoxLayout()
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_label = QLabel("00:00.00 / 00:00.00")
        self.time_label.setMinimumWidth(self.fontMetrics().horizontalAdvance("00:00.00 / 00:00.00") + 10)
        timeline_layout.addWidget(self.timeline_slider)
        timeline_layout.addWidget(self.time_label)

        extra_controls_layout = QHBoxLayout()
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setFixedWidth(120) 
        self.volume_label = QLabel(f"{self.volume_slider.value()}%")

        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "0.75x", "1.0x", "1.5x", "2.0x"])
        self.speed_combo.setCurrentText("1.0x")

        extra_controls_layout.addWidget(QLabel(LANG["volume_label"]))
        extra_controls_layout.addWidget(self.volume_slider)
        extra_controls_layout.addWidget(self.volume_label)
        extra_controls_layout.addStretch()
        extra_controls_layout.addWidget(QLabel(LANG["speed_label"]))
        extra_controls_layout.addWidget(self.speed_combo)

        main_layout.addLayout(controls_layout)
        main_layout.addLayout(timeline_layout)
        main_layout.addLayout(extra_controls_layout)
        group.setLayout(main_layout)
        return group
    
    def toggle_play_pause(self):
        if self.player.is_playing():
            self.player.pause()
        else:
            if self.current_audio_file:
                self.player.play()

    def setup_lyrics_table(self):
        self.lyrics_table.setColumnCount(3)
        self.lyrics_table.setHorizontalHeaderLabels([
            LANG["lyrics_table_header_time"],
            LANG["lyrics_table_header_original"],
            LANG["lyrics_table_header_translated"]
        ])
        self.lyrics_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        header = self.lyrics_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        # --- 修改点 1: 添加样式表以定义选中行的颜色 ---
        self.lyrics_table.setStyleSheet("""
            QTableWidget::item:selected {
                background-color: #5a98d1;
                color: white;
            }
        """)

    def create_edit_controls(self):
        group = QGroupBox(LANG["edit_controls_group"])
        layout = QHBoxLayout()
        self.add_row_button = QPushButton(LANG["add_row_button"])
        self.remove_row_button = QPushButton(LANG["remove_row_button"])
        self.merge_rows_button = QPushButton(LANG["merge_rows_button"])
        self.split_row_button = QPushButton(LANG["split_row_button"])
        layout.addWidget(self.add_row_button)
        layout.addWidget(self.remove_row_button)
        layout.addWidget(self.merge_rows_button)
        layout.addWidget(self.split_row_button)
        group.setLayout(layout)
        return group

    def create_timeline_controls(self):
        group = QGroupBox(LANG["timeline_controls_group"])
        layout = QHBoxLayout()
        self.mark_time_button = QPushButton(LANG["mark_time_button"])
        layout.addWidget(self.mark_time_button)
        group.setLayout(layout)
        return group

    def connect_signals(self):
        self.ui_update_timer.timeout.connect(self.update_ui_on_timer)
        self.player.durationChanged.connect(self.update_duration)
        self.player.playbackStateChanged.connect(self.handle_player_state_change)
        
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.stop_button.clicked.connect(self.player.stop)
        
        self.timeline_slider.sliderMoved.connect(self.player.set_pos)
        self.rewind_button.clicked.connect(lambda: self.player.set_pos(self.player.get_pos() - 1000))
        self.forward_button.clicked.connect(lambda: self.player.set_pos(self.player.get_pos() + 1000))

        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.speed_combo.currentTextChanged.connect(self.on_speed_changed)
        self.add_row_button.clicked.connect(self.add_row)
        self.remove_row_button.clicked.connect(self.remove_selected_rows)
        self.merge_rows_button.clicked.connect(self.merge_selected_rows)
        self.split_row_button.clicked.connect(self.split_selected_row)
        self.mark_time_button.clicked.connect(self.mark_timestamp)
        self.lyrics_table.itemDoubleClicked.connect(self.play_from_selection)
        self.lyrics_table.itemChanged.connect(self.sync_table_to_lrc)
        self.title_edit.textChanged.connect(lambda t: self.lrc.meta.update({'ti': t}))
        self.artist_edit.textChanged.connect(lambda t: self.lrc.meta.update({'ar': t}))
        self.album_edit.textChanged.connect(lambda t: self.lrc.meta.update({'al': t}))

        QShortcut(QKeySequence("F8"), self).activated.connect(self.mark_timestamp)
        QShortcut(QKeySequence("Ctrl+T"), self).activated.connect(self.mark_timestamp)
        QShortcut(QKeySequence("Space"), self).activated.connect(self.toggle_play_pause)

    def update_ui_on_timer(self):
        if self.player.is_playing() and not self.timeline_slider.isSliderDown():
            position = self.player.get_pos()
            self.timeline_slider.setValue(position)
            self.update_time_label(position, self.player.get_duration())
            self.highlight_current_lyric(position / 1000.0)

    def handle_player_state_change(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.ui_update_timer.start()
            self.play_pause_button.setIcon(qta.icon('fa5s.pause-circle', color='white'))
            self.play_pause_button.setText(f" {LANG['pause_button']}")
        else:
            self.ui_update_timer.stop()
            self.play_pause_button.setIcon(qta.icon('fa5s.play-circle', color='white'))
            self.play_pause_button.setText(f" {LANG['play_button']}")
            if state == QMediaPlayer.PlaybackState.StoppedState:
                self.timeline_slider.setValue(0)
                self.update_time_label(0, self.player.get_duration())
                self.highlight_current_lyric(-1) # 清除高亮

    def open_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, LANG["open_audio_title"], "", LANG["audio_files_filter"])
        if file_path:
            self.current_audio_file = file_path
            self.player.load(file_path)
            self.status_bar.showMessage(LANG["status_audio_loaded"].format(file=os.path.basename(file_path)))

    def open_lyric_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, LANG["open_lyric_title"], "", LANG["lyric_files_filter"])
        if file_path:
            try:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='gbk') as f:
                        file_content = f.read()

                self.lrc.parse_from_text(file_content)
                self.update_ui_from_lrc()
                self.status_bar.showMessage(LANG["status_lyric_loaded"])
            except Exception as e:
                QMessageBox.critical(self, LANG["error_title"], LANG["error_open_file"].format(e=e))

    def save_lrc_file(self):
        self.sync_table_to_lrc()
        file_path, _ = QFileDialog.getSaveFileName(self, LANG["save_lyric_title"], "", LANG["lrc_file_filter"])
        if file_path:
            choice = QMessageBox.question(self, "选择保存格式",
                                          "您想如何保存双语歌词？\n- 'Yes' 保存为分行格式\n- 'No' 保存为单行'/'分隔格式",
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                                          QMessageBox.StandardButton.Yes)
            if choice == QMessageBox.StandardButton.Cancel:
                return
            save_as_separated = (choice == QMessageBox.StandardButton.Yes)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.lrc.to_lrc_string(save_as_bilingual_separated=save_as_separated))
            self.status_bar.showMessage(LANG["status_lyric_saved"].format(file=file_path))

    def update_ui_from_lrc(self):
        self.title_edit.setText(self.lrc.meta.get('ti', ''))
        self.artist_edit.setText(self.lrc.meta.get('ar', ''))
        self.album_edit.setText(self.lrc.meta.get('al', ''))
        self.update_lyrics_table()

    def update_lyrics_table(self):
        self.lyrics_table.blockSignals(True)
        self.lyrics_table.setRowCount(len(self.lrc.lyrics))
        for i, line in enumerate(self.lrc.lyrics):
            ts, original, translated = line.get('ts'), line.get('original', ''), line.get('translated', '')
            if ts is not None:
                minutes = int(ts / 60)
                seconds = int(ts % 60)
                centiseconds = int((ts - minutes * 60 - seconds) * 100)
                time_str = f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
            else:
                time_str = ""
            time_item = QTableWidgetItem(time_str)
            time_item.setFlags(time_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.lyrics_table.setItem(i, 0, time_item)
            self.lyrics_table.setItem(i, 1, QTableWidgetItem(original))
            self.lyrics_table.setItem(i, 2, QTableWidgetItem(translated))
        self.lyrics_table.resizeRowsToContents()
        self.lyrics_table.blockSignals(False)

    def sync_table_to_lrc(self, item=None):
        self.lrc.lyrics.clear()
        for i in range(self.lyrics_table.rowCount()):
            time_str_item = self.lyrics_table.item(i, 0)
            original_item = self.lyrics_table.item(i, 1)
            translated_item = self.lyrics_table.item(i, 2)
            
            time_str = time_str_item.text() if time_str_item else ""
            original = original_item.text() if original_item else ""
            translated = translated_item.text() if translated_item else ""
            
            ts = None
            match = re.match(r'(\d+):(\d{2,2})\.(\d{2,2})', time_str)
            if match:
                m, s, cs = map(int, match.groups())
                ts = m * 60 + s + cs / 100.0
            
            self.lrc.lyrics.append({'ts': ts, 'original': original, 'translated': translated})

        if item and item.column() == 0:
             self.lrc.sort_lyrics()
             self.update_lyrics_table()

    def on_volume_changed(self, value):
        self.player.set_volume(value / 100.0)
        self.volume_label.setText(f"{value}%")

    def on_speed_changed(self, text):
        rate = float(text.replace('x', ''))
        self.player.set_playback_rate(rate)

    def update_duration(self, duration):
        self.timeline_slider.setRange(0, duration)
        self.update_time_label(self.player.get_pos(), duration)
        self.handle_player_state_change(self.player._player.playbackState())

    def format_time(self, ms):
        if ms < 0: ms = 0
        total_seconds = ms / 1000.0
        minutes = int(total_seconds / 60)
        seconds = int(total_seconds % 60)
        centiseconds = int((total_seconds - minutes * 60 - seconds) * 100)
        return f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

    def update_time_label(self, pos, dur):
        pos_str = self.format_time(pos)
        dur_str = self.format_time(dur)
        self.time_label.setText(f"{pos_str} / {dur_str}")

    # --- 修改点 2: 替换整个函数 ---
    def highlight_current_lyric(self, current_sec):
        current_line_idx = -1
        # 在有时间戳的歌词中查找当前行
        sorted_lyrics = [lyric for lyric in self.lrc.lyrics if lyric['ts'] is not None]
        for i, lyric_line in enumerate(sorted_lyrics):
            if current_sec >= lyric_line['ts']:
                current_line_idx = i
            else:
                break
        
        # 如果找到了当前播放的歌词行
        if current_line_idx != -1:
            try:
                # 找到它在原始lyrics列表中的索引
                target_lyric = sorted_lyrics[current_line_idx]
                original_index = -1
                for idx, lyric in enumerate(self.lrc.lyrics):
                    if lyric is target_lyric:
                        original_index = idx
                        break
                
                # 如果索引有效，则滚动并选中该行
                if original_index != -1:
                    # 避免重复选中，仅在需要时操作
                    if self.lyrics_table.selectionModel().currentIndex().row() != original_index:
                        self.lyrics_table.scrollToItem(self.lyrics_table.item(original_index, 0), QAbstractItemView.ScrollHint.PositionAtCenter)
                        self.lyrics_table.selectRow(original_index)

            except (ValueError, IndexError):
                # 如果出现意外错误，清除选择
                self.lyrics_table.clearSelection()
        else:
            # 如果没有正在播放的行 (例如歌曲停止或未开始)，清除选择
            if current_sec < 0:
                self.lyrics_table.clearSelection()

    def get_selected_rows(self):
        return sorted(list(set(index.row() for index in self.lyrics_table.selectedIndexes())))

    def add_row(self):
        selected_rows = self.get_selected_rows()
        insert_pos = selected_rows[-1] + 1 if selected_rows else self.lyrics_table.rowCount()
        self.lyrics_table.blockSignals(True)
        self.lyrics_table.insertRow(insert_pos)
        self.lyrics_table.setItem(insert_pos, 0, QTableWidgetItem(""))
        self.lyrics_table.setItem(insert_pos, 1, QTableWidgetItem(""))
        self.lyrics_table.setItem(insert_pos, 2, QTableWidgetItem(""))
        self.lyrics_table.blockSignals(False)
        self.sync_table_to_lrc()

    def remove_selected_rows(self):
        rows = self.get_selected_rows()
        if not rows:
            QMessageBox.warning(self, LANG["error_title"], LANG["error_no_selection"])
            return
        
        reply = QMessageBox.question(self, "确认删除", f"您确定要删除选中的 {len(rows)} 行吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return

        self.lyrics_table.blockSignals(True)
        for row in reversed(rows):
            self.lyrics_table.removeRow(row)
        self.lyrics_table.blockSignals(False)
        self.sync_table_to_lrc()

    def merge_selected_rows(self):
        rows = self.get_selected_rows()
        if len(rows) < 2:
            QMessageBox.warning(self, LANG["error_title"], LANG["error_need_two_rows"])
            return
        
        self.lyrics_table.blockSignals(True)
        base_row = rows[0]
        base_orig_item = self.lyrics_table.item(base_row, 1)
        base_trans_item = self.lyrics_table.item(base_row, 2)

        base_orig = base_orig_item.text() if base_orig_item else ""
        base_trans = base_trans_item.text() if base_trans_item else ""

        for row in rows[1:]:
            orig_item = self.lyrics_table.item(row, 1)
            trans_item = self.lyrics_table.item(row, 2)
            if orig_item:
                base_orig += " " + orig_item.text()
            if trans_item:
                base_trans += " " + trans_item.text()

        if base_orig_item: base_orig_item.setText(base_orig.strip())
        if base_trans_item: base_trans_item.setText(base_trans.strip())

        for row in reversed(rows[1:]):
            self.lyrics_table.removeRow(row)
        self.lyrics_table.blockSignals(False)
        self.sync_table_to_lrc()

    def split_selected_row(self):
        rows = self.get_selected_rows()
        if len(rows) != 1:
            QMessageBox.warning(self, LANG["error_title"], LANG["error_need_one_row"])
            return
        
        row = rows[0]
        original_item = self.lyrics_table.item(row, 1)
        if not original_item: return

        original = original_item.text()
        parts = original.split()
        if len(parts) > 1:
            self.lyrics_table.blockSignals(True)
            original_item.setText(parts[0])
            for i, part in enumerate(parts[1:]):
                new_row_idx = row + i + 1
                self.lyrics_table.insertRow(new_row_idx)
                self.lyrics_table.setItem(new_row_idx, 0, QTableWidgetItem(""))
                self.lyrics_table.setItem(new_row_idx, 1, QTableWidgetItem(part))
                self.lyrics_table.setItem(new_row_idx, 2, QTableWidgetItem(""))
            self.lyrics_table.blockSignals(False)
            self.sync_table_to_lrc()

    def mark_timestamp(self):
        rows = self.get_selected_rows()
        if not rows:
            QMessageBox.warning(self, LANG["error_title"], LANG["error_no_selection"])
            return
        
        current_pos_ms = self.player.get_pos()
        
        self.lyrics_table.blockSignals(True)
        for row in rows:
            time_str = self.format_time(current_pos_ms)
            self.lyrics_table.item(row, 0).setText(time_str)
        self.lyrics_table.blockSignals(False)
        
        self.sync_table_to_lrc(self.lyrics_table.item(rows[0], 0))
        
        if len(rows) == 1:
            next_row = rows[0] + 1
            if next_row < self.lyrics_table.rowCount():
                self.lyrics_table.selectRow(next_row)

    def play_from_selection(self, item):
        row = item.row()
        if 0 <= row < len(self.lrc.lyrics):
            lyric_data = self.lrc.lyrics[row]
            if lyric_data and lyric_data['ts'] is not None:
                timestamp_ms = lyric_data['ts'] * 1000
                self.player.set_pos(int(timestamp_ms))
                self.toggle_play_pause()