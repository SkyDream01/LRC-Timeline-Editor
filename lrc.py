# lrc.py
import re
from collections import defaultdict

class Lrc:
    """负责LRC歌词的解析、编辑和生成，支持双语"""
    def __init__(self):
        self.meta = {"ti": "", "ar": "", "al": ""}
        # 数据结构: [{'ts': float, 'original': "...", 'translated': "..."}, ...]
        self.lyrics = []

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
            
            # 使用一个更通用的正则表达式来捕获时间戳
            time_tags_matches = re.findall(r'\[(\d{2,}):(\d{2,})\.(\d{2,3})\]', line)
            lyric_text = line[line.rfind(']') + 1:].strip() if ']' in line else line

            if time_tags_matches:
                for m, s, ms_str in time_tags_matches:
                    # 将毫秒部分统一处理成厘秒（截断或补齐）
                    if len(ms_str) > 2:
                        cs = int(ms_str[:2]) # 截断为厘秒
                    else:
                        cs = int(ms_str)
                    ts = int(m) * 60 + int(s) + cs / 100.0
                    time_map[ts].append(lyric_text)
            elif lyric_text:
                unstimed_lyrics.append(lyric_text)
        
        # 按时间戳对解析出的歌词行进行排序
        sorted_timestamps = sorted(time_map.keys())
        for ts in sorted_timestamps:
            lyrics_at_ts = time_map[ts]
            original = ""
            translated = ""

            if len(lyrics_at_ts) == 1:
                parts = re.split(r'\s*[/|]\s*', lyrics_at_ts[0], maxsplit=1)
                original = parts[0]
                if len(parts) > 1:
                    translated = parts[1]
            elif len(lyrics_at_ts) >= 2:
                original = lyrics_at_ts[0]
                translated = lyrics_at_ts[1]

            self.lyrics.append({'ts': ts, 'original': original, 'translated': translated})
        
        # 无时间戳的歌词放在最后
        for text in unstimed_lyrics:
            parts = re.split(r'\s*[/|]\s*', text, maxsplit=1)
            original = parts[0]
            translated = parts[1] if len(parts) > 1 else ""
            self.lyrics.append({'ts': None, 'original': original, 'translated': translated})
        
        # 初次加载后不再自动排序
        # self.sort_lyrics()


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
                minutes = int(ts / 60)
                seconds = int(ts % 60)
                centiseconds = int((ts - minutes * 60 - seconds) * 100)
                time_str = f"[{minutes:02d}:{seconds:02d}.{centiseconds:02d}]"
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