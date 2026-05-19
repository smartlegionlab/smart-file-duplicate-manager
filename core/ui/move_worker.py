# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
import shutil
import time
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal


class MoveWorker(QThread):
    progress_updated = pyqtSignal(int, int, str, int)
    move_completed = pyqtSignal(int, int, list)
    move_error = pyqtSignal(str)

    def __init__(self, groups, target_folder, dry_run=False):
        super().__init__()
        self.groups = groups
        self.target_folder = target_folder
        self.dry_run = dry_run
        self.is_running = True

    def stop(self):
        self.is_running = False

    def run(self):
        start_time = time.time()
        moved_count = 0
        space_freed = 0
        errors = []
        moved_files = []

        total_selected = 0
        for group in self.groups:
            for file in group.files:
                if file.selected and not file.is_main:
                    total_selected += 1

        current = 0

        try:
            for group in self.groups:
                if not self.is_running:
                    break

                main_file = group.main_file
                if not main_file:
                    continue

                for file in group.files:
                    if not self.is_running:
                        break

                    if file.selected and not file.is_main:
                        current += 1

                        if not self.dry_run:
                            try:
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

                                moved_count += 1
                                space_freed += file.size

                                moved_files.append({
                                    'original_path': file.path,
                                    'new_path': new_path,
                                    'size': file.size,
                                    'group_hash': group.hash,
                                    'timestamp': datetime.now().isoformat()
                                })

                            except Exception as e:
                                errors.append(f"{file.name}: {str(e)}")

                        self.progress_updated.emit(current, total_selected, file.path, space_freed)

            if not self.dry_run and moved_files:
                self.save_move_log(moved_files, self.target_folder)

            self.move_completed.emit(moved_count, space_freed, errors)

        except Exception as e:
            self.move_error.emit(str(e))

    def save_move_log(self, moved_files, target_folder):
        import json
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'target_folder': target_folder,
            'files': moved_files,
            'total_files': len(moved_files),
            'total_size': sum(f['size'] for f in moved_files)
        }

        log_filename = os.path.join(target_folder, 'move_log.json')
        try:
            with open(log_filename, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save move log: {e}")
