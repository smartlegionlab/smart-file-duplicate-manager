# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
import shutil
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QProgressBar, QPushButton, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class MoveProgressDialog(QDialog):
    def __init__(self, groups, target_folder, dry_run=False, parent=None):
        super().__init__(parent)
        self.groups = groups
        self.target_folder = target_folder
        self.dry_run = dry_run
        self.parent_ref = parent

        self.total_files = 0
        self.total_size = 0
        for group in groups:
            for file in group.files:
                if file.selected and not file.is_main:
                    self.total_files += 1
                    self.total_size += file.size

        self.moved_count = 0
        self.space_freed = 0
        self.errors = []
        self.moved_files = []
        self.cancelled = False
        self.current = 0

        self.setup_ui()
        self.center_dialog()

        QTimer.singleShot(100, self.move_files)

    def setup_ui(self):
        self.setWindowTitle("Moving Files")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setFixedHeight(150)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("Moving Duplicate Files")
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.info_label = QLabel(f"Moving: 0 of {self.total_files} files")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.total_files)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        hl = QHBoxLayout()
        hl.addStretch()
        hl.addWidget(self.cancel_button)
        hl.addStretch()
        layout.addLayout(hl)

    def center_dialog(self):
        if self.parent_ref:
            x = self.parent_ref.x() + (self.parent_ref.width() - self.width()) // 2
            y = self.parent_ref.y() + (self.parent_ref.height() - self.height()) // 2
            self.move(x, y)

    def move_files(self):
        for group in self.groups:
            if self.cancelled:
                break

            main_file = group.main_file
            if not main_file:
                continue

            for file in group.files:
                if self.cancelled:
                    break

                if not (file.selected and not file.is_main):
                    continue

                self.current += 1

                if not self.dry_run:
                    try:
                        if not os.path.exists(file.path):
                            self.errors.append(f"{file.name}: not found")
                            self.update_progress()
                            continue

                        ext = os.path.splitext(main_file.path)[1]
                        base = os.path.splitext(os.path.basename(main_file.path))[0]
                        new_name = f"{base}_{self.current}{ext}"
                        new_path = os.path.join(self.target_folder, new_name)

                        counter = 1
                        while os.path.exists(new_path):
                            new_name = f"{base}_{self.current}_{counter}{ext}"
                            new_path = os.path.join(self.target_folder, new_name)
                            counter += 1

                        shutil.move(file.path, new_path)

                        self.moved_count += 1
                        self.space_freed += file.size
                        self.moved_files.append({
                            'original_path': file.path,
                            'new_path': new_path,
                            'size': file.size,
                            'group_hash': group.hash,
                            'timestamp': datetime.now().isoformat(),
                            'original_name': file.name
                        })

                    except Exception as e:
                        self.errors.append(f"{file.name}: {str(e)}")

                self.update_progress()

        if not self.dry_run and self.moved_files:
            self.save_move_log()

        self.show_result()

    def update_progress(self):
        self.progress_bar.setValue(self.current)
        freed_str = self._format_size(self.space_freed)
        self.info_label.setText(f"Moving: {self.current} of {self.total_files} files ({freed_str} freed)")
        QApplication.processEvents()

    def show_result(self):
        if self.space_freed < 0:
            self.space_freed = 0

        freed_str = self._format_size(self.space_freed)

        result_msg = f"Files moved: {self.moved_count}\nSpace freed: {freed_str}"

        if self.dry_run:
            result_msg = f"TEST MODE - no files were actually moved\n\n{result_msg}"

        if self.errors:
            result_msg += "\n\nErrors:\n" + "\n".join(self.errors[:10])
            if len(self.errors) > 10:
                result_msg += f"\n... and {len(self.errors) - 10} more errors"

        if self.parent_ref:
            self.parent_ref.status_label.setText(f"Moved {self.moved_count} files, freed {freed_str}")
            self.parent_ref.reset_all()

        self.accept()

        QMessageBox.information(self.parent_ref, "Move Complete", result_msg)

    def on_cancel(self):
        if self.moved_count == self.total_files:
            self.accept()
        else:
            reply = QMessageBox.question(
                self, "Confirm Cancel",
                "Stop moving files?\n\nSome files may have already been moved.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.cancelled = True
                self.cancel_button.setEnabled(False)
                self.info_label.setText("Cancelling...")
                QApplication.processEvents()

    def save_move_log(self):
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'target_folder': self.target_folder,
            'files': self.moved_files,
            'total_files': len(self.moved_files),
            'total_size': sum(f['size'] for f in self.moved_files)
        }

        log_filename = os.path.join(self.target_folder, 'move_log.json')
        try:
            with open(log_filename, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save move log: {e}")

    @staticmethod
    def _format_size(size):
        if size <= 0:
            return "0 B"
        if size < 1024:
            return f"{size} B"

        units = ['KB', 'MB', 'GB', 'TB', 'PB']
        size_float = float(size)

        for unit in units:
            size_float /= 1024.0
            if size_float < 1024.0:
                return f"{size_float:.1f} {unit}"

        return f"{size_float:.1f} PB"