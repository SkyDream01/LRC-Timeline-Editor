# player.py
from PyQt5.QtCore import QObject, QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class Player(QObject):
    """封装 QMediaPlayer 提供播放控制"""
    # 自定义信号，供应用程序的其他部分连接
    positionChanged = pyqtSignal(int)
    durationChanged = pyqtSignal(int)
    stateChanged = pyqtSignal(QMediaPlayer.State)

    def __init__(self):
        super().__init__()
        self._player = QMediaPlayer()

        # 将 QMediaPlayer 的内置信号连接到内部的代理槽函数
        self._player.positionChanged.connect(self._on_position_changed)
        self._player.durationChanged.connect(self._on_duration_changed)
        self._player.stateChanged.connect(self._on_state_changed)

    # --- 内部代理槽函数 (Private Slots) ---
    # 这些方法接收来自 QMediaPlayer 的原始信号

    def _on_position_changed(self, position: int):
        # 然后，它们再发射我们自定义的信号，供程序的其他部分使用
        self.positionChanged.emit(position)

    def _on_duration_changed(self, duration: int):
        self.durationChanged.emit(duration)
        
    def _on_state_changed(self, state: QMediaPlayer.State):
        self.stateChanged.emit(state)

    # --- 公共控制方法 ---
    # 这部分代码保持不变

    def load(self, file_path: str):
        """加载音频文件"""
        url = QUrl.fromLocalFile(file_path)
        content = QMediaContent(url)
        self._player.setMedia(content)

    def play(self):
        self._player.play()

    def pause(self):
        self._player.pause()

    def stop(self):
        self._player.stop()

    def get_pos(self) -> int:
        """获取当前播放位置（毫秒）"""
        return self._player.position()

    def set_pos(self, position: int):
        """设置播放位置（毫秒）"""
        self._player.setPosition(position)
    
    def get_duration(self) -> int:
        """获取总时长（毫秒）"""
        return self._player.duration()
    
    def is_playing(self) -> bool:
        """判断是否正在播放"""
        return self._player.state() == QMediaPlayer.PlayingState

    def set_volume(self, volume: int):
        """设置音量 (0-100)"""
        self._player.setVolume(volume)

    def set_playback_rate(self, rate: float):
        """设置播放速度"""
        self._player.setPlaybackRate(rate)