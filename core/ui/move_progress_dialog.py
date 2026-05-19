# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QProgressBar, QPushButton, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class MoveProgressDialog(QDialog):
    cancelled = pyqtSignal()

    def __init__(self, total_files: int, total_size: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Moving Files")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setFixedHeight(200)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title_label = QLabel("Moving Duplicate Files")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.info_label = QLabel(f"Moving {total_files} files ({self._format_size(total_size)})...")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(total_files)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        self.current_file_label = QLabel("Preparing...")
        self.current_file_label.setWordWrap(True)
        self.current_file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_file_label.setStyleSheet("color: #808080; font-size: 10px;")
        layout.addWidget(self.current_file_label)

        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.center_dialog()

    def center_dialog(self):
        if self.parent():
            x = self.parent().x() + (self.parent().width() - self.width()) // 2
            y = self.parent().y() + (self.parent().height() - self.height()) // 2
            self.move(x, y)

    def update_progress(self, current: int, total: int, current_file: str, space_freed: int):
        if space_freed < 0:
            space_freed = 0

        if current > self.progress_bar.maximum():
            self.progress_bar.setMaximum(current)

        self.progress_bar.setValue(current)

        freed_str = self._format_size(space_freed)
        self.info_label.setText(f"Moving: {current} of {total} files ({freed_str} freed)")

        filename = os.path.basename(current_file)
        self.current_file_label.setText(f"Current: {filename}")
        QApplication.processEvents()

    def update_complete(self, moved: int, space_freed: int):
        if space_freed < 0:
            space_freed = 0

        self.progress_bar.setValue(moved)
        freed_str = self._format_size(space_freed)
        self.info_label.setText(f"Complete! Moved {moved} files, freed {freed_str}")
        self.current_file_label.setText("Operation completed successfully")
        self.cancel_button.setText("Close")
        self.cancel_button.setEnabled(True)

    def on_cancel(self):
        if self.progress_bar.value() == self.progress_bar.maximum():
            self.accept()
        else:
            reply = QMessageBox.question(
                self, "Confirm Cancel",
                "Stop moving files?\n\nSome files may have already been moved.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.cancelled.emit()
                self.reject()

    @staticmethod
    def _format_size(size):
        if size < 0:
            return "0 B"
        if size == 0:
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
