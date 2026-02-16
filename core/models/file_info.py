import os
from datetime import datetime


class FileInfo:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.size = 0
        self.size_str = ""
        self.hash = ""
        self.mod_time = 0
        self.date_str = ""
        self.selected = False
        self.is_main = False

        try:
            stat = os.stat(path)
            self.size = stat.st_size
            self.size_str = self._format_size(self.size)
            self.mod_time = stat.st_mtime
            self.date_str = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
        except (OSError, IOError):
            pass

    @staticmethod
    def _format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
