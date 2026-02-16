# Copyright (©) 2026, Alexander Suvorov. All rights reserved.


class DuplicateGroup:
    def __init__(self, hash_value):
        self.hash = hash_value
        self.id = f"{hash_value[:8]}..."
        self.files = []
        self.size = 0
        self.size_str = ""
        self.file_count = 0
        self.main_file = None

    def add_file(self, file_info):
        self.files.append(file_info)
        self.file_count = len(self.files)
        if self.files:
            self.size = self.files[0].size
            self.size_str = self.files[0].size_str

    def set_main_file(self, file_info):
        for f in self.files:
            f.is_main = (f.path == file_info.path)
        self.main_file = file_info
