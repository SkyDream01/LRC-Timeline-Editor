# lrc.py
import re
from collections import defaultdict

try:
    import pykakasi
    PYKAKASI_AVAILABLE = True
except ImportError:
    PYKAKASI_AVAILABLE = False

class Lrc:
    """负责LRC歌词的解析、编辑和生成，支持双语"""
    def __init__(self):
        self.meta = {"ti": "", "ar": "", "al": ""}
        # 数据结构: [{'ts': float, 'original': "...", 'translated': "..."}, ...]
        self.lyrics = []
        # 罗马音转换器
        self.kks = None
        if PYKAKASI_AVAILABLE:
            try:
                self.kks = pykakasi.kakasi()
            except Exception:
                self.kks = None

    def parse_from_text(self, text: str):
        """从字符串解析LRC内容，智能处理单行和分行双语格式"""
        self.lyrics.clear()
        self.meta = {"ti": "", "ar": "", "al": ""}
        lines = text.split('\n')

        time_map = defaultdict(list)
        unstimed_lyrics = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            meta_match = re.match(r'\[(ti|ar|al):(.*?)\]', line)
            if meta_match:
                key, value = meta_match.groups()
                self.meta[key.strip()] = value.strip()
                continue
            
            # 使用正则表达式捕获时间戳，格式为：[mm:ss.xx] 或 [mm:ss.xxx]
            time_tags_matches = re.findall(r'\[(\d{2,}):(\d{2,})\.(\d{2,3})\]', line)
            # 获取歌词文本：最后一个时间标签之后的内容
            lyric_text = line[line.rfind(']') + 1:].strip() if ']' in line else line

            if time_tags_matches:
                # 处理每个时间标签
                for m, s, fraction in time_tags_matches:
                    # 分钟转换为整数
                    minutes = int(m)
                    # 秒转换为整数
                    seconds = int(s)
                    # 处理小数部分（厘秒）：可能为2位或3位（百分秒或毫秒）
                    # 如果是3位（毫秒），则取前两位作为厘秒（除以10取整），因为LRC精度为0.01秒
                    if len(fraction) == 3:
                        centiseconds = int(fraction) // 10
                    else:
                        centiseconds = int(fraction)
                    # 计算总时间（秒）：分钟*60 + 秒 + 厘秒/100
                    ts = minutes * 60 + seconds + centiseconds / 100.0
                    time_map[ts].append(lyric_text)
            elif lyric_text:
                # 没有时间戳的行
                unstimed_lyrics.append(lyric_text)
        
        # 按时间戳对解析出的歌词行进行排序
        sorted_timestamps = sorted(time_map.keys())
        for ts in sorted_timestamps:
            lyrics_at_ts = time_map[ts]
            original = ""
            translated = ""

            # 如果同一时间戳有多行歌词，通常第一行是原文，第二行是译文
            if len(lyrics_at_ts) >= 2:
                original = lyrics_at_ts[0]
                translated = lyrics_at_ts[1]
            elif len(lyrics_at_ts) == 1:
                # 如果只有一行，尝试用'/'或'|'分割原文和译文
                parts = re.split(r'\s*[/|]\s*', lyrics_at_ts[0], maxsplit=1)
                original = parts[0]
                if len(parts) > 1:
                    translated = parts[1]

            self.lyrics.append({'ts': ts, 'original': original, 'translated': translated})
        
        # 无时间戳的歌词放在最后
        for text in unstimed_lyrics:
            parts = re.split(r'\s*[/|]\s*', text, maxsplit=1)
            original = parts[0]
            translated = parts[1] if len(parts) > 1 else ""
            self.lyrics.append({'ts': None, 'original': original, 'translated': translated})
        
        # 初次加载后不再自动排序
        # self.sort_lyrics()


    def convert_to_romaji(self, text: str) -> str:
        """将日文文本转换为罗马音"""
        if not text or not self.kks:
            return ""
        try:
            result = self.kks.convert(text)
            return " ".join(item["hepburn"] for item in result)
        except Exception:
            return ""

    @staticmethod
    def format_timestamp(ts: float) -> str:
        """将秒数格式化为LRC时间戳字符串 [mm:ss.xx]"""
        minutes = int(ts / 60)
        seconds = int(ts % 60)
        centiseconds = int(round((ts - minutes * 60 - seconds) * 100))
        # 确保厘秒在0-99范围内
        if centiseconds >= 100:
            centiseconds = 99
        elif centiseconds < 0:
            centiseconds = 0
        return f"[{minutes:02d}:{seconds:02d}.{centiseconds:02d}]"

    def to_lrc_string(self, save_as_bilingual_separated=True) -> str:
        """生成LRC格式的字符串，精度为0.01s"""
        lrc_parts = []
        for key, value in self.meta.items():
            if value:
                lrc_parts.append(f"[{key}:{value}]")
        
        # 保存时不再强制排序，按当前表格顺序生成
        # sorted_lyrics = sorted(self.lyrics, key=lambda x: x['ts'] if x['ts'] is not None else float('inf'))

        for line_data in self.lyrics: # 直接使用当前顺序
            ts = line_data['ts']
            original = line_data.get('original', '')
            translated = line_data.get('translated', '')

            if ts is not None:
                time_str = self.format_timestamp(ts)
            else:
                time_str = ""

            if not original and not translated:
                continue

            if translated:
                if save_as_bilingual_separated:
                    lrc_parts.append(f"{time_str}{original}")
                    lrc_parts.append(f"{time_str}{translated}")
                else:
                    lrc_parts.append(f"{time_str}{original} / {translated}")
            else:
                lrc_parts.append(f"{time_str}{original}")
                
        return "\n".join(lrc_parts)

    def sort_lyrics(self):
        """根据时间戳排序歌词列表 (此功能已根据用户要求停用)"""
        # self.lyrics.sort(key=lambda x: x['ts'] if x['ts'] is not None else float('inf'))
        pass
