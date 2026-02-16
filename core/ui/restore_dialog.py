# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
import json

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTreeWidget, QTreeWidgetItem, QMessageBox, QHeaderView,
    QAbstractItemView, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt


class RestoreDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.logs = []
        self.log_paths = {}
        self.selected_items = []
        self.setWindowTitle("Restore Moved Files")
        self.setMinimumSize(900, 600)
        self.setup_ui()
        self.load_logs()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        instructions = QLabel(
            "Select files to restore. Files will be moved back to their original locations.\n"
            "Note: Original directories must still exist for restoration to succeed."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["", "Date", "Original Path", "New Path", "Size", "Status"])
        self.tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tree.header().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.tree.setAlternatingRowColors(True)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        layout.addWidget(self.tree)

        button_layout = QHBoxLayout()

        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all)
        button_layout.addWidget(self.select_all_btn)

        self.deselect_all_btn = QPushButton("Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all)
        button_layout.addWidget(self.deselect_all_btn)

        button_layout.addStretch()

        self.restore_btn = QPushButton("Restore Selected")
        self.restore_btn.setProperty("class", "warning")
        self.restore_btn.clicked.connect(self.restore_selected)
        button_layout.addWidget(self.restore_btn)

        layout.addLayout(button_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def load_logs(self):
        self.tree.clear()
        self.logs = []
        self.log_paths = {}

        if not os.path.exists(self.parent.state['dupes_folder']):
            return

        for root, dirs, files in os.walk(self.parent.state['dupes_folder']):
            if 'move_log.json' in files:
                log_path = os.path.join(root, 'move_log.json')
                try:
                    with open(log_path, 'r', encoding='utf-8') as f:
                        log_data = json.load(f)

                    existing_files = []
                    for file_info in log_data.get('files', []):
                        if os.path.exists(file_info.get('new_path', '')):
                            existing_files.append(file_info)

                    if not existing_files:
                        try:
                            os.remove(log_path)
                            if not os.listdir(root):
                                os.rmdir(root)
                        except:
                            pass
                        continue

                    log_data['files'] = existing_files
                    log_data['total_files'] = len(existing_files)
                    log_data['total_size'] = sum(f['size'] for f in existing_files)

                    with open(log_path, 'w', encoding='utf-8') as f:
                        json.dump(log_data, f, indent=2, ensure_ascii=False)

                    folder_name = os.path.basename(root)
                    folder_date = log_data.get('timestamp', '')[:10]
                    folder_item = QTreeWidgetItem([
                        f"📁 {folder_name}",
                        folder_date,
                        f"{len(existing_files)} files",
                        f"{self.parent.format_size(log_data['total_size'])}",
                        "",
                        ""
                    ])
                    folder_item.setExpanded(True)
                    folder_item.setData(0, Qt.ItemDataRole.UserRole, {
                        'type': 'folder',
                        'path': root,
                        'log_path': log_path,
                        'log_data': log_data
                    })

                    for i, file_info in enumerate(existing_files):
                        file_item = QTreeWidgetItem([
                            "",
                            file_info.get('timestamp', '')[:10] if i == 0 else "",
                            file_info.get('original_path', ''),
                            file_info.get('new_path', ''),
                            self.parent.format_size(file_info.get('size', 0)),
                            "Available"
                        ])
                        file_item.setData(0, Qt.ItemDataRole.UserRole, {
                            'type': 'file',
                            'original_path': file_info.get('original_path'),
                            'new_path': file_info.get('new_path'),
                            'size': file_info.get('size'),
                            'group_hash': file_info.get('group_hash'),
                            'timestamp': file_info.get('timestamp'),
                            'log_path': log_path,
                            'folder_path': root
                        })
                        file_item.setFlags(file_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                        file_item.setCheckState(0, Qt.CheckState.Unchecked)
                        folder_item.addChild(file_item)

                    self.tree.addTopLevelItem(folder_item)

                except Exception as e:
                    print(f"Error loading log {log_path}: {e}")

        for i in range(1, 6):
            self.tree.resizeColumnToContents(i)

    def select_all(self):
        for i in range(self.tree.topLevelItemCount()):
            folder = self.tree.topLevelItem(i)
            for j in range(folder.childCount()):
                folder.child(j).setCheckState(0, Qt.CheckState.Checked)

    def deselect_all(self):
        for i in range(self.tree.topLevelItemCount()):
            folder = self.tree.topLevelItem(i)
            for j in range(folder.childCount()):
                folder.child(j).setCheckState(0, Qt.CheckState.Unchecked)

    def get_selected_files(self):
        selected = []
        for i in range(self.tree.topLevelItemCount()):
            folder = self.tree.topLevelItem(i)
            for j in range(folder.childCount()):
                item = folder.child(j)
                if item.checkState(0) == Qt.CheckState.Checked:
                    data = item.data(0, Qt.ItemDataRole.UserRole)
                    if data and data.get('type') == 'file':
                        selected.append(data)
        return selected

    def update_log_after_restore(self, log_path, restored_files):
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)

            original_paths = {f['original_path'] for f in restored_files}
            log_data['files'] = [f for f in log_data['files']
                                 if f['original_path'] not in original_paths]

            log_data['total_files'] = len(log_data['files'])
            log_data['total_size'] = sum(f['size'] for f in log_data['files'])

            if not log_data['files']:
                folder_path = os.path.dirname(log_path)
                os.remove(log_path)
                try:
                    if not os.listdir(folder_path):
                        os.rmdir(folder_path)
                except:
                    pass
                return True
            else:
                with open(log_path, 'w', encoding='utf-8') as f:
                    json.dump(log_data, f, indent=2, ensure_ascii=False)
                return False
        except Exception as e:
            print(f"Error updating log {log_path}: {e}")
            return False

    def restore_selected(self):
        selected_files = self.get_selected_files()

        if not selected_files:
            QMessageBox.information(self, "Info", "No files selected for restoration")
            return

        files_by_log = {}
        for file_info in selected_files:
            log_path = file_info.get('log_path')
            if log_path not in files_by_log:
                files_by_log[log_path] = []
            files_by_log[log_path].append(file_info)

        reply = QMessageBox.question(
            self, "Confirm Restoration",
            f"Restore {len(selected_files)} selected files to their original locations?\n\n"
            "This will move files back to where they came from.\n"
            "WARNING: If original files still exist, they will be backed up!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        restored = 0
        failed = 0
        errors = []
        restored_by_log = {}

        for log_path, files in files_by_log.items():
            restored_by_log[log_path] = []

            for file_info in files:
                original_path = file_info.get('original_path')
                new_path = file_info.get('new_path')

                if not os.path.exists(new_path):
                    failed += 1
                    errors.append(f"File not found: {os.path.basename(new_path)}")
                    continue

                original_dir = os.path.dirname(original_path)
                if not os.path.exists(original_dir):
                    failed += 1
                    errors.append(f"Original directory not found: {original_dir}")
                    continue

                try:
                    if os.path.exists(original_path):
                        base, ext = os.path.splitext(original_path)
                        counter = 1
                        backup_path = f"{base}.backup{counter}{ext}"
                        while os.path.exists(backup_path):
                            counter += 1
                            backup_path = f"{base}.backup{counter}{ext}"

                        os.rename(original_path, backup_path)
                        self.parent.status_label.setText(f"Backed up existing file to: {os.path.basename(backup_path)}")

                    os.rename(new_path, original_path)
                    restored += 1
                    restored_by_log[log_path].append(file_info)
                    self.parent.status_label.setText(f"Restored: {os.path.basename(original_path)}")

                except Exception as e:
                    failed += 1
                    errors.append(f"{os.path.basename(original_path)}: {str(e)}")

        for log_path, restored_files in restored_by_log.items():
            if restored_files:
                log_deleted = self.update_log_after_restore(log_path, restored_files)
                if log_deleted:
                    self.parent.status_label.setText(f"Removed empty folder: {os.path.dirname(log_path)}")

        result_msg = f"Files restored: {restored}\nFiles failed: {failed}"
        if errors:
            result_msg += "\n\nErrors:\n" + "\n".join(errors[:10])
            if len(errors) > 10:
                result_msg += f"\n... and {len(errors) - 10} more errors"

        QMessageBox.information(self, "Restoration Complete", result_msg)

        self.load_logs()

        if restored > 0:
            self.parent.status_label.setText(f"Restoration complete. {restored} files restored.")
