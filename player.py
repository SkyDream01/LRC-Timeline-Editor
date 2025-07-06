# player.py
from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class Player(QObject):
    """封装 QMediaPlayer 提供播放控制"""
    positionChanged = Signal(int)
    durationChanged = Signal(int)
    playbackStateChanged = Signal(QMediaPlayer.PlaybackState)

    def __init__(self):
        super().__init__()
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)

        # 修正点: 使用 lambda 明确地重新发射信号，以避免C++签名冲突
        self._player.positionChanged.connect(lambda pos: self.positionChanged.emit(pos))
        self._player.durationChanged.connect(lambda dur: self.durationChanged.emit(dur))
        self._player.playbackStateChanged.connect(lambda state: self.playbackStateChanged.emit(state))

    def load(self, file_path: str):
        """加载音频文件"""
        url = QUrl.fromLocalFile(file_path)
        self._player.setSource(url)

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
        return self._player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    def set_volume(self, volume: float):
        """设置音量 (0.0 到 1.0)"""
        self._audio_output.setVolume(volume)

    def set_playback_rate(self, rate: float):
        """设置播放速度"""
        self._player.setPlaybackRate(rate)