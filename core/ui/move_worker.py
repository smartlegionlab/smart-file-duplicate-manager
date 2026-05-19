# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
import shutil
import json
import threading
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal


class MoveWorker(QThread):
    progress_updated = pyqtSignal(int, int, int)
    move_completed = pyqtSignal(int, int, list)
    move_error = pyqtSignal(str)

    def __init__(self, groups, target_folder, dry_run=False):
        super().__init__()
        self.groups = groups
        self.target_folder = target_folder
        self.dry_run = dry_run
        self.is_running = True
        self._lock = threading.Lock()
        self._moved_count = 0
        self._space_freed = 0
        self._errors = []
        self._moved_files = []

    def stop(self):
        self.is_running = False

    def run(self):
        try:
            total_selected = 0
            for group in self.groups:
                for file in group.files:
                    if file.selected and not file.is_main:
                        total_selected += 1

            if total_selected == 0:
                self.move_completed.emit(0, 0, [])
                return

            current = 0

            for group in self.groups:
                if not self.is_running:
                    break

                main_file = group.main_file
                if not main_file:
                    continue

                for file in group.files:
                    if not self.is_running:
                        break

                    if not (file.selected and not file.is_main):
                        continue

                    current += 1

                    if not self.dry_run:
                        try:
                            if not os.path.exists(file.path):
                                with self._lock:
                                    self._errors.append(f"{file.name}: file not found")
                                self.progress_updated.emit(current, total_selected, self._space_freed)
                                continue

                            original_size = file.size
                            if original_size <= 0:
                                with self._lock:
                                    self._errors.append(f"{file.name}: invalid file size ({original_size})")
                                self.progress_updated.emit(current, total_selected, self._space_freed)
                                continue

                            ext = os.path.splitext(main_file.path)[1]
                            base = os.path.splitext(os.path.basename(main_file.path))[0]
                            new_name = f"{base}_{current}{ext}"
                            new_path = os.path.join(self.target_folder, new_name)

                            counter = 1
                            while os.path.exists(new_path):
                                new_name = f"{base}_{current}_{counter}{ext}"
                                new_path = os.path.join(self.target_folder, new_name)
                                counter += 1

                            shutil.move(file.path, new_path)

                            if not os.path.exists(new_path):
                                raise Exception("File was not moved successfully")

                            with self._lock:
                                self._moved_count += 1
                                self._space_freed += original_size
                                self._moved_files.append({
                                    'original_path': file.path,
                                    'new_path': new_path,
                                    'size': original_size,
                                    'group_hash': group.hash,
                                    'timestamp': datetime.now().isoformat(),
                                    'original_name': file.name
                                })

                        except Exception as e:
                            with self._lock:
                                self._errors.append(f"{file.name}: {str(e)}")

                    with self._lock:
                        current_freed = self._space_freed
                    self.progress_updated.emit(current, total_selected, current_freed)

            if not self.dry_run and self._moved_files:
                self.save_move_log()

            with self._lock:
                final_moved = self._moved_count
                final_freed = self._space_freed
                final_errors = self._errors.copy()

            self.move_completed.emit(final_moved, final_freed, final_errors)

        except Exception as e:
            self.move_error.emit(str(e))

    def save_move_log(self):
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'target_folder': self.target_folder,
            'files': self._moved_files,
            'total_files': len(self._moved_files),
            'total_size': sum(f['size'] for f in self._moved_files)
        }

        log_filename = os.path.join(self.target_folder, 'move_log.json')
        try:
            with open(log_filename, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save move log: {e}")
