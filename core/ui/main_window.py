# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox,
    QTreeWidget, QTreeWidgetItem, QProgressBar, QMessageBox,
    QFileDialog, QSplitter, QHeaderView, QAbstractItemView,
    QGroupBox, QGridLayout, QScrollArea, QSpinBox, QDialog,
    QTextEdit, QDialogButtonBox, QMenu, QApplication, QFrame
)
from PyQt6.QtCore import Qt, QRegularExpression, QPoint, QSettings
from PyQt6.QtGui import QFont, QAction, QKeySequence, QRegularExpressionValidator, QColor

from core.models.config import Config
from core.models.dupe_group import DuplicateGroup
from core.models.file_info import FileInfo
from core.ui.dark_theme import ModernStyle
from core.ui.restore_dialog import RestoreDialog
from core.ui.scan_worker import ScanWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.state = {
            'root_path': str(Path.home()),
            'dupes_folder': str(Path.home() / 'duplicates'),
            'strategy': 'oldest',
            'min_size': 0,
            'max_size': 1 << 40,
            'include_ext': '',
            'exclude_ext': '',
            'threads': os.cpu_count() or 4,
            'dry_run': False,
            'groups': [],
            'filtered_groups': [],
            'total_files': 0,
            'total_size': 0,
            'duplicate_cnt': 0,
            'duplicate_sum': 0,
            'scan_time': 0,
            'is_scanning': False
        }
        self.config = Config()

        self.current_group = None
        self.scan_worker = None

        self.scan_settings_visible = True
        self.group_details_visible = False

        self.setup_ui()
        self.setup_menu()

    def closeEvent(self, event):

        if self.state['is_scanning']:
            reply = QMessageBox.question(
                self, "Confirm Exit",
                "Scan is in progress. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                event.ignore()
                return

        if self.state['groups']:
            reply = QMessageBox.question(
                self, "Confirm Exit",
                "Unsaved scan results will be lost. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                event.ignore()
                return

        event.accept()

    def setup_ui(self):
        self.setWindowTitle(f"{self.config.app_name} v{self.config.version}")
        self.setMinimumSize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(3)

        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setHandleWidth(5)
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.setStyleSheet("QSplitter::handle { background-color: #404040; }")

        left_panel = self.create_left_panel()
        left_panel.setMinimumWidth(250)
        left_panel.setMaximumWidth(400)
        self.main_splitter.addWidget(left_panel)

        self.right_splitter = QSplitter(Qt.Orientation.Vertical)
        self.right_splitter.setHandleWidth(5)
        self.right_splitter.setChildrenCollapsible(False)
        self.right_splitter.setStyleSheet("QSplitter::handle { background-color: #404040; }")

        center_panel = self.create_center_panel()
        self.right_splitter.addWidget(center_panel)

        self.bottom_panel = self.create_bottom_panel()
        self.bottom_panel.setVisible(False)
        self.right_splitter.addWidget(self.bottom_panel)

        self.right_splitter.setSizes([500, 500])

        self.main_splitter.addWidget(self.right_splitter)

        self.main_splitter.setSizes([300, 600])

        main_layout.addWidget(self.main_splitter, 1)

        progress_panel = self.create_progress_panel()
        main_layout.addWidget(progress_panel)

        status_panel = self.create_status_panel()
        main_layout.addWidget(status_panel)

    def create_left_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(5, 5, 5, 5)

        scan_group_header = QWidget()
        scan_group_header_layout = QHBoxLayout(scan_group_header)
        scan_group_header_layout.setContentsMargins(5, 5, 5, 5)

        scan_group_title = QLabel("Scan Settings")
        title_font = QFont()
        title_font.setBold(True)
        scan_group_title.setFont(title_font)

        scan_group_header_layout.addWidget(scan_group_title)
        scan_group_header_layout.addStretch()

        layout.addWidget(scan_group_header)

        self.scan_settings_widget = QWidget()
        scan_layout = QVBoxLayout(self.scan_settings_widget)
        scan_layout.setSpacing(8)
        scan_layout.setContentsMargins(5, 5, 5, 5)

        path_label = QLabel("Path:")
        self.path_edit = QLineEdit()
        self.path_edit.setText(self.state['root_path'])
        self.path_edit.textChanged.connect(lambda t: self.state.update({'root_path': t}))
        self.path_edit.setToolTip(self.state['root_path'])

        path_btn = QPushButton()
        path_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DirIcon))
        path_btn.setMaximumWidth(30)
        path_btn.clicked.connect(self.browse_scan_folder)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(path_btn)
        scan_layout.addWidget(path_label)
        scan_layout.addLayout(path_layout)

        dupes_label = QLabel("Duplicates Folder:")
        self.dupes_folder_edit = QLineEdit()
        self.dupes_folder_edit.setText(self.state['dupes_folder'])
        self.dupes_folder_edit.textChanged.connect(lambda t: self.state.update({'dupes_folder': t}))

        dupes_btn = QPushButton()
        dupes_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DirIcon))
        dupes_btn.setMaximumWidth(30)
        dupes_btn.clicked.connect(self.browse_dupes_folder)

        dupes_layout = QHBoxLayout()
        dupes_layout.addWidget(self.dupes_folder_edit)
        dupes_layout.addWidget(dupes_btn)
        scan_layout.addWidget(dupes_label)
        scan_layout.addLayout(dupes_layout)

        strategy_label = QLabel("Strategy:")
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems([
            "oldest", "newest", "smallest", "largest",
            "shortest path", "longest path"
        ])
        self.strategy_combo.setCurrentText("oldest")
        self.strategy_combo.currentTextChanged.connect(self.on_strategy_changed)
        scan_layout.addWidget(strategy_label)
        scan_layout.addWidget(self.strategy_combo)

        self.dry_run_check = QCheckBox("Test mode (don't move files)")
        self.dry_run_check.toggled.connect(self.on_test_mode_changed)
        scan_layout.addWidget(self.dry_run_check)

        scan_btn_layout = QHBoxLayout()
        self.scan_btn = QPushButton("Start Scan")
        self.scan_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_MediaPlay))
        self.scan_btn.setProperty("class", "primary")
        self.scan_btn.clicked.connect(self.start_scan)
        self.scan_btn.setToolTip("Start scanning for duplicates (Ctrl+R)")

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogCancelButton))
        self.cancel_btn.setVisible(False)
        self.cancel_btn.clicked.connect(self.cancel_scan)
        self.cancel_btn.setToolTip("Cancel current scan (Ctrl+Shift+C)")

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_BrowserReload))
        self.reset_btn.clicked.connect(self.reset_all)
        self.reset_btn.setToolTip("Reset all scan results (Ctrl+X)")

        scan_btn_layout.addWidget(self.scan_btn)
        scan_btn_layout.addWidget(self.cancel_btn)
        scan_btn_layout.addWidget(self.reset_btn)
        scan_layout.addLayout(scan_btn_layout)

        layout.addWidget(self.scan_settings_widget)

        filters_group = QGroupBox("Filters")
        filters_layout = QGridLayout(filters_group)
        filters_layout.setSpacing(8)

        filters_layout.addWidget(QLabel("Min size (bytes):"), 0, 0)
        self.min_size_edit = QLineEdit()
        self.min_size_edit.setPlaceholderText("0")
        self.min_size_edit.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*")))
        self.min_size_edit.textChanged.connect(
            lambda t: self.state.update({'min_size': int(t) if t else 0})
        )
        filters_layout.addWidget(self.min_size_edit, 0, 1)

        filters_layout.addWidget(QLabel("Max size (bytes):"), 1, 0)
        self.max_size_edit = QLineEdit()
        self.max_size_edit.setPlaceholderText("No limit")
        self.max_size_edit.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*")))
        self.max_size_edit.textChanged.connect(
            lambda t: self.state.update({'max_size': int(t) if t else 1 << 40})
        )
        filters_layout.addWidget(self.max_size_edit, 1, 1)

        filters_layout.addWidget(QLabel("Include:"), 2, 0)
        self.include_edit = QLineEdit()
        self.include_edit.setPlaceholderText(".jpg,.png")
        self.include_edit.textChanged.connect(lambda t: self.state.update({'include_ext': t}))
        filters_layout.addWidget(self.include_edit, 2, 1)

        filters_layout.addWidget(QLabel("Exclude:"), 3, 0)
        self.exclude_edit = QLineEdit()
        self.exclude_edit.setPlaceholderText(".tmp,.log")
        self.exclude_edit.textChanged.connect(lambda t: self.state.update({'exclude_ext': t}))
        filters_layout.addWidget(self.exclude_edit, 3, 1)

        filters_layout.addWidget(QLabel("Threads:"), 4, 0)
        self.threads_spin = QSpinBox()
        self.threads_spin.setMinimum(1)
        self.threads_spin.setMaximum(os.cpu_count() * 4 or 16)
        self.threads_spin.setValue(self.state['threads'])
        self.threads_spin.valueChanged.connect(lambda v: self.state.update({'threads': v}))
        filters_layout.addWidget(self.threads_spin, 4, 1)

        layout.addWidget(filters_group)
        layout.addStretch()

        return panel

    def create_center_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Filter by filename...")
        self.search_edit.textChanged.connect(self.filter_groups)
        search_layout.addWidget(self.search_edit)
        layout.addLayout(search_layout)

        stats_layout = QHBoxLayout()
        self.stats_total_label = QLabel("Files: -")
        self.stats_dupes_label = QLabel("Duplicates: -")
        self.stats_groups_label = QLabel("Groups: -")
        self.stats_space_label = QLabel("Space: -")
        self.stats_time_label = QLabel("Time: -")

        stats_layout.addWidget(self.stats_total_label)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.stats_dupes_label)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.stats_groups_label)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.stats_space_label)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.stats_time_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        self.groups_tree = QTreeWidget()
        self.groups_tree.setHeaderLabels(["Group", "Size", "Copies"])
        self.groups_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.groups_tree.setAlternatingRowColors(True)
        self.groups_tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.groups_tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.groups_tree.itemSelectionChanged.connect(self.on_group_selected)
        layout.addWidget(self.groups_tree, 1)

        actions_layout = QHBoxLayout()

        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogApplyButton))
        self.select_all_btn.clicked.connect(self.select_all_duplicates)
        actions_layout.addWidget(self.select_all_btn)

        self.deselect_all_btn = QPushButton("Deselect All")
        self.deselect_all_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogResetButton))
        self.deselect_all_btn.clicked.connect(self.deselect_all)
        actions_layout.addWidget(self.deselect_all_btn)

        actions_layout.addStretch()

        self.move_btn = QPushButton("Move Selected")
        self.move_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ArrowRight))
        self.move_btn.setProperty("class", "warning")
        self.move_btn.setEnabled(False)
        self.move_btn.clicked.connect(lambda: self.process_duplicates("move"))
        actions_layout.addWidget(self.move_btn)

        layout.addLayout(actions_layout)

        return panel

    def create_bottom_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)

        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.right_title = QLabel("Group Details")
        title_font = QFont()
        title_font.setBold(True)
        self.right_title.setFont(title_font)

        self.toggle_details_btn = QPushButton("▼")
        self.toggle_details_btn.setToolTip("Toggle Group Details panel")
        self.toggle_details_btn.clicked.connect(self.toggle_group_details)

        header_layout.addWidget(self.right_title)
        header_layout.addStretch()
        header_layout.addWidget(self.toggle_details_btn)

        layout.addWidget(header_widget)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #404040; max-height: 1px;")
        layout.addWidget(separator)

        info_layout = QHBoxLayout()
        self.group_size_label = QLabel("Size: -")
        info_layout.addWidget(self.group_size_label)
        info_layout.addWidget(QLabel("|"))
        self.group_copies_label = QLabel("Copies: -")
        info_layout.addWidget(self.group_copies_label)
        info_layout.addWidget(QLabel("|"))
        self.group_total_label = QLabel("Total: -")
        info_layout.addWidget(self.group_total_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)

        self.files_tree = QTreeWidget()
        self.files_tree.setHeaderLabels(["", "File Name", "Size", "Date"])
        self.files_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.files_tree.setAlternatingRowColors(True)
        self.files_tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.files_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.files_tree.customContextMenuRequested.connect(self.show_file_context_menu)
        self.files_tree.itemChanged.connect(self.on_file_check_changed)
        self.files_tree.itemDoubleClicked.connect(self.on_file_double_clicked)
        layout.addWidget(self.files_tree, 1)

        return panel

    def create_progress_panel(self):
        panel = QWidget()
        panel.setMaximumHeight(40)
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(10, 2, 10, 2)

        layout.addWidget(QLabel("Progress:"))

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        return panel

    def create_status_panel(self):
        panel = QWidget()
        panel.setMaximumHeight(25)
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(10, 0, 10, 2)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {ModernStyle.FG_MEDIUM};")
        layout.addWidget(self.status_label)

        self.scanning_indicator = QLabel("")
        self.scanning_indicator.setMaximumWidth(16)
        layout.addWidget(self.scanning_indicator)

        layout.addStretch()

        return panel

    def toggle_group_details(self):
        self.group_details_visible = not self.group_details_visible
        self.bottom_panel.setVisible(self.group_details_visible)
        self.toggle_details_btn.setText("▼" if self.group_details_visible else "▶")
        self.toggle_details_btn.setToolTip(
            "Show Group Details" if not self.group_details_visible else "Hide Group Details")

        if self.group_details_visible:
            self.right_splitter.setSizes([500, 500])
        else:
            self.right_splitter.setSizes([1000, 0])

    def setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")
        select_scan_action = QAction("&Select Scan Folder...", self)
        select_scan_action.setShortcut(QKeySequence("Ctrl+Shift+O"))
        select_scan_action.triggered.connect(self.browse_scan_folder)
        file_menu.addAction(select_scan_action)

        select_dupes_action = QAction("Select &Duplicates Folder...", self)
        select_dupes_action.setShortcut(QKeySequence("Ctrl+Shift+D"))
        select_dupes_action.triggered.connect(self.browse_dupes_folder)
        file_menu.addAction(select_dupes_action)

        file_menu.addSeparator()
        start_scan_action = QAction("&Start Scan", self)
        start_scan_action.setShortcut(QKeySequence("Ctrl+R"))
        start_scan_action.triggered.connect(self.start_scan)
        file_menu.addAction(start_scan_action)

        cancel_scan_action = QAction("&Cancel Scan", self)
        cancel_scan_action.setShortcut(QKeySequence("Ctrl+Shift+C"))
        cancel_scan_action.triggered.connect(self.cancel_scan)
        file_menu.addAction(cancel_scan_action)

        reset_action = QAction("&Reset", self)
        reset_action.setShortcut(QKeySequence("Ctrl+X"))
        reset_action.triggered.connect(self.reset_all)
        file_menu.addAction(reset_action)

        file_menu.addSeparator()
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("&Edit")
        select_all_action = QAction("Select &All Duplicates", self)
        select_all_action.setShortcut(QKeySequence("Ctrl+A"))
        select_all_action.triggered.connect(self.select_all_duplicates)
        edit_menu.addAction(select_all_action)

        deselect_all_action = QAction("&Deselect All", self)
        deselect_all_action.setShortcut(QKeySequence("Ctrl+Shift+A"))
        deselect_all_action.triggered.connect(self.deselect_all)
        edit_menu.addAction(deselect_all_action)

        edit_menu.addSeparator()
        self.test_mode_action = QAction("&Test Mode", self)
        self.test_mode_action.setCheckable(True)
        self.test_mode_action.setShortcut(QKeySequence("Ctrl+T"))
        self.test_mode_action.triggered.connect(self.on_test_mode_menu)
        edit_menu.addAction(self.test_mode_action)

        view_menu = menubar.addMenu("&View")
        stats_action = QAction("Show &Statistics", self)
        stats_action.setShortcut(QKeySequence("Ctrl+I"))
        stats_action.triggered.connect(self.show_statistics)
        view_menu.addAction(stats_action)

        clear_search_action = QAction("&Clear Search", self)
        clear_search_action.setShortcut(QKeySequence("Ctrl+L"))
        clear_search_action.triggered.connect(lambda: self.search_edit.clear())
        view_menu.addAction(clear_search_action)

        tools_menu = menubar.addMenu("&Tools")
        move_action = QAction("&Move Selected Files", self)
        move_action.setShortcut(QKeySequence("Ctrl+M"))
        move_action.triggered.connect(lambda: self.process_duplicates("move"))
        tools_menu.addAction(move_action)

        tools_menu.addSeparator()
        restore_action = QAction("&Restore Files...", self)
        restore_action.setShortcut(QKeySequence("Ctrl+Shift+R"))
        restore_action.triggered.connect(self.show_restore_dialog)
        tools_menu.addAction(restore_action)

        tools_menu.addSeparator()
        open_folder_action = QAction("&Open Dupes Folder", self)
        open_folder_action.setShortcut(QKeySequence("Ctrl+Shift+F"))
        open_folder_action.triggered.connect(self.open_dupes_folder)
        tools_menu.addAction(open_folder_action)

        help_menu = menubar.addMenu("&Help")
        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.setShortcut(QKeySequence("Ctrl+/"))
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)

        help_menu.addSeparator()
        about_action = QAction("&About", self)
        about_action.setShortcut(QKeySequence("Ctrl+H"))
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        docs_action = QAction("&Documentation", self)
        docs_action.setShortcut(QKeySequence("F1"))
        docs_action.triggered.connect(self.open_documentation)
        help_menu.addAction(docs_action)

        help_menu.addSeparator()
        report_action = QAction("&Report Issue", self)
        report_action.setShortcut(QKeySequence("Ctrl+Shift+I"))
        report_action.triggered.connect(self.report_issue)
        help_menu.addAction(report_action)

        license_action = QAction("&License", self)
        license_action.setShortcut(QKeySequence("Ctrl+Alt+L"))
        license_action.triggered.connect(self.show_license)
        help_menu.addAction(license_action)

    def browse_scan_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Scan Folder", self.state['root_path']
        )
        if folder:
            self.path_edit.setText(folder)
            self.state['root_path'] = folder
            self.path_edit.setToolTip(folder)
            self.status_label.setText(f"Scan folder set to: {folder}")

    def browse_dupes_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Duplicates Folder", self.state['dupes_folder']
        )
        if folder:
            self.dupes_folder_edit.setText(folder)
            self.state['dupes_folder'] = folder
            self.status_label.setText(f"Duplicates folder set to: {folder}")

    def on_strategy_changed(self, text):
        if text == "shortest path":
            self.state['strategy'] = "shortest"
        elif text == "longest path":
            self.state['strategy'] = "longest"
        else:
            self.state['strategy'] = text
        self.status_label.setText(f"Strategy changed to: {text}")

    def on_test_mode_changed(self, checked):
        self.state['dry_run'] = checked
        self.test_mode_action.setChecked(checked)
        status = "enabled" if checked else "disabled"
        self.status_label.setText(f"Test mode {status}")

    def on_test_mode_menu(self, checked):
        self.state['dry_run'] = checked
        self.dry_run_check.setChecked(checked)
        status = "enabled" if checked else "disabled"
        self.status_label.setText(f"Test mode {status}")

    def start_scan(self):
        if self.state['is_scanning']:
            return

        if not os.path.exists(self.state['root_path']):
            QMessageBox.critical(self, "Error", "Scan folder does not exist!")
            return

        reply = QMessageBox.question(
            self, "Confirm Scan",
            f"Start scanning folder:\n{self.state['root_path']}\n\nThis may take some "
            f"time depending on the number of files.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self.scan_btn.setEnabled(False)
        self.reset_btn.setEnabled(False)
        self.move_btn.setEnabled(False)
        self.cancel_btn.setVisible(True)
        self.select_all_btn.setEnabled(False)
        self.deselect_all_btn.setEnabled(False)
        self.dry_run_check.setEnabled(False)

        self.state['is_scanning'] = True
        self.state['groups'] = []
        self.state['filtered_groups'] = []
        self.state['total_files'] = 0
        self.state['total_size'] = 0
        self.state['duplicate_cnt'] = 0
        self.state['duplicate_sum'] = 0

        self.current_group = None
        self.groups_tree.clear()
        self.files_tree.clear()
        self.right_title.setText("Group Details")
        self.group_size_label.setText("Size: -")
        self.group_copies_label.setText("Copies: -")
        self.group_total_label.setText("Total: -")

        self.progress_bar.setValue(0)
        self.status_label.setText("Scanning started...")
        self.scanning_indicator.setText("⏳")

        self.scan_worker = ScanWorker(
            self.state['root_path'],
            self.state['dupes_folder'],
            self.state['min_size'],
            self.state['max_size'],
            self.state['include_ext'],
            self.state['exclude_ext'],
            self.state['threads']
        )

        self.scan_worker.progress_updated.connect(self.on_scan_progress)
        self.scan_worker.scan_finished.connect(self.on_scan_finished)
        self.scan_worker.scan_error.connect(self.on_scan_error)

        self.scan_worker.start()

    def cancel_scan(self):
        if self.scan_worker and self.scan_worker.isRunning():
            reply = QMessageBox.question(
                self, "Confirm Cancel",
                "Cancel current scan?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

            self.scan_worker.stop()
            self.scan_worker.wait()
            self.scan_worker = None

        self.state['is_scanning'] = False
        self.scan_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
        self.cancel_btn.setVisible(False)
        self.select_all_btn.setEnabled(True)
        self.deselect_all_btn.setEnabled(True)
        self.dry_run_check.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Scan cancelled")
        self.scanning_indicator.setText("")

    def on_scan_progress(self, current, total, message):
        if total > 0:
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
        self.status_label.setText(message)

    def on_scan_finished(self, results, scan_time):
        self.state['is_scanning'] = False
        self.state['scan_time'] = scan_time
        self.state['groups'] = []

        for hash_value, file_data in results.items():
            if len(file_data) > 1:
                group = DuplicateGroup(hash_value)

                for path, size, mod_time in file_data:
                    file_info = FileInfo(path)
                    file_info.size = size
                    file_info.size_str = FileInfo._format_size(size)
                    file_info.hash = hash_value
                    file_info.mod_time = mod_time
                    file_info.date_str = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M")
                    group.add_file(file_info)

                main_file = self.select_main_file(group.files)
                group.set_main_file(main_file)

                for file in group.files:
                    if file != main_file:
                        file.selected = True

                self.state['groups'].append(group)
                self.state['duplicate_cnt'] += len(group.files) - 1
                self.state['duplicate_sum'] += (len(group.files) - 1) * group.size
                self.state['total_files'] += len(group.files)
                self.state['total_size'] += group.size * len(group.files)

        self.state['groups'].sort(key=lambda g: g.size * g.file_count, reverse=True)
        self.state['filtered_groups'] = self.state['groups']

        self.refresh_ui()

        self.scan_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
        self.cancel_btn.setVisible(False)
        self.select_all_btn.setEnabled(True)
        self.deselect_all_btn.setEnabled(True)
        self.dry_run_check.setEnabled(True)

        if self.state['groups']:
            self.move_btn.setEnabled(True)

        self.progress_bar.setValue(self.progress_bar.maximum())
        status_msg = f"Scan complete. Found {len(self.state['groups'])} duplicate groups in {scan_time:.1f}s"
        self.status_label.setText(status_msg)
        self.scanning_indicator.setText("")

    def on_scan_error(self, error_msg):
        QMessageBox.critical(self, "Scan Error", f"An error occurred during scan:\n{error_msg}")
        self.status_label.setText(f"Scan error: {error_msg}")
        self.scanning_indicator.setText("")
        self.cancel_scan()

    def refresh_ui(self):
        self.groups_tree.clear()

        for group in self.state['filtered_groups']:
            item = QTreeWidgetItem([
                f"{group.id} ({group.files[0].name})",
                group.size_str,
                str(group.file_count)
            ])
            item.setData(0, Qt.ItemDataRole.UserRole, group)
            self.groups_tree.addTopLevelItem(item)

        self.stats_total_label.setText(
            f"Files: {self.state['total_files']} ({self.format_size(self.state['total_size'])})"
        )
        self.stats_dupes_label.setText(f"Duplicates: {self.state['duplicate_cnt']}")
        self.stats_groups_label.setText(f"Groups: {len(self.state['groups'])}")
        self.stats_space_label.setText(
            f"Space: {self.format_size(self.state['duplicate_sum'])}"
        )
        self.stats_time_label.setText(
            f"Time: {self.state['scan_time']:.1f}s"
        )

    def filter_groups(self, text):
        if not text:
            self.state['filtered_groups'] = self.state['groups']
        else:
            text_lower = text.lower()
            filtered = []
            for group in self.state['groups']:
                for file in group.files:
                    if text_lower in file.name.lower():
                        filtered.append(group)
                        break
            self.state['filtered_groups'] = filtered

        self.refresh_ui()

    def on_group_selected(self):
        selected = self.groups_tree.selectedItems()
        if not selected:
            self.current_group = None
            self.files_tree.clear()
            self.right_title.setText("Group Details")
            self.group_size_label.setText("Size: -")
            self.group_copies_label.setText("Copies: -")
            self.group_total_label.setText("Total: -")
            return

        group = selected[0].data(0, Qt.ItemDataRole.UserRole)
        self.current_group = group

        if not self.group_details_visible:
            self.toggle_group_details()

        self.right_title.setText(f"Group: {group.id}")
        self.group_size_label.setText(f"Size: {group.size_str}")
        self.group_copies_label.setText(f"Copies: {group.file_count}")
        self.group_total_label.setText(f"Total: {self.format_size(group.size * group.file_count)}")

        self.files_tree.clear()

        for file in group.files:
            item = QTreeWidgetItem()
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(0, Qt.CheckState.Checked if file.selected else Qt.CheckState.Unchecked)
            item.setText(1, file.name)
            item.setText(2, file.size_str)
            item.setText(3, file.date_str)
            item.setData(0, Qt.ItemDataRole.UserRole, file)
            item.setToolTip(1, file.path)

            if file.is_main:
                item.setIcon(1, self.style().standardIcon(self.style().StandardPixmap.SP_DialogApplyButton))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(0, Qt.CheckState.Unchecked)
                item.setBackground(1, QColor(42, 130, 218, 50))

            self.files_tree.addTopLevelItem(item)

        self.files_tree.resizeColumnToContents(0)
        self.files_tree.resizeColumnToContents(2)
        self.files_tree.resizeColumnToContents(3)

    def on_file_check_changed(self, item, column):
        if column != 0:
            return

        file = item.data(0, Qt.ItemDataRole.UserRole)
        if file and not file.is_main:
            file.selected = (item.checkState(0) == Qt.CheckState.Checked)

    def show_file_context_menu(self, position: QPoint):
        item = self.files_tree.itemAt(position)
        if not item:
            return

        file = item.data(0, Qt.ItemDataRole.UserRole)
        if not file:
            return

        menu = QMenu()

        details_action = menu.addAction("File Details")
        details_action.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogDetailedView))
        details_action.triggered.connect(lambda: self.show_file_details(file))

        copy_path_action = menu.addAction("Copy Full Path")
        copy_path_action.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_FileLinkIcon))
        copy_path_action.triggered.connect(lambda: self.copy_to_clipboard(file.path))

        menu.addSeparator()

        open_folder_action = menu.addAction("Open Containing Folder")
        open_folder_action.triggered.connect(lambda: self.open_file_folder(file))

        menu.addSeparator()

        if not file.is_main:
            set_main_action = menu.addAction("Set as Main File")
            set_main_action.triggered.connect(lambda: self.set_file_as_main(file))

        if file.selected:
            deselect_action = menu.addAction("Deselect")
            deselect_action.triggered.connect(lambda: self.toggle_file_selection(file, False))
        else:
            select_action = menu.addAction("Select")
            select_action.triggered.connect(lambda: self.toggle_file_selection(file, True))

        menu.addSeparator()

        select_all_in_group = menu.addAction("Select All in Group")
        select_all_in_group.triggered.connect(self.select_all_in_group)

        deselect_all_in_group = menu.addAction("Deselect All in Group")
        deselect_all_in_group.triggered.connect(self.deselect_all_in_group)

        menu.exec(self.files_tree.viewport().mapToGlobal(position))

    def open_file_folder(self, file):
        folder = os.path.dirname(file.path)
        if os.path.exists(folder):
            if sys.platform == 'win32':
                os.startfile(folder)
            elif sys.platform == 'darwin':
                subprocess.run(['open', folder])
            else:
                subprocess.run(['xdg-open', folder])

    def set_file_as_main(self, file):
        if not self.current_group or file not in self.current_group.files:
            return

        for f in self.current_group.files:
            f.is_main = (f.path == file.path)
        self.current_group.main_file = file

        self.on_group_selected()
        self.status_label.setText(f"Main file changed to: {file.name}")

    def toggle_file_selection(self, file, selected):
        if file.is_main:
            return

        file.selected = selected
        self.on_group_selected()

    def select_main_file(self, files):
        strategy = self.state['strategy']
        if strategy == "newest":
            return max(files, key=lambda f: f.mod_time)
        elif strategy == "oldest":
            return min(files, key=lambda f: f.mod_time)
        elif strategy == "smallest":
            return min(files, key=lambda f: f.size)
        elif strategy == "largest":
            return max(files, key=lambda f: f.size)
        elif strategy == "shortest":
            return min(files, key=lambda f: len(f.path))
        elif strategy == "longest":
            return max(files, key=lambda f: len(f.path))
        return min(files, key=lambda f: f.mod_time)

    def select_all_in_group(self):
        if not self.current_group:
            QMessageBox.warning(self, "Warning", "No group selected")
            return

        reply = QMessageBox.question(
            self, "Confirm Selection",
            "Select all duplicates in this group?\n\nThe main file will remain unselected.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        for file in self.current_group.files:
            if not file.is_main:
                file.selected = True

        self.on_group_selected()
        self.status_label.setText("Selected all duplicates in current group")

    def deselect_all_in_group(self):
        if not self.current_group:
            QMessageBox.warning(self, "Warning", "No group selected")
            return

        reply = QMessageBox.question(
            self, "Confirm Deselection",
            "Deselect all duplicates in this group?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        for file in self.current_group.files:
            if not file.is_main:
                file.selected = False

        self.on_group_selected()
        self.status_label.setText("Deselected all duplicates in current group")

    def select_all_duplicates(self):
        if not self.state['groups']:
            return

        reply = QMessageBox.question(
            self, "Confirm Selection",
            f"Select all duplicate files across {len(self.state['groups'])} groups?\n\nMain files will remain unselected.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        selected_count = 0
        for group in self.state['groups']:
            for file in group.files:
                if not file.is_main:
                    file.selected = True
                    selected_count += 1

        if self.current_group:
            self.on_group_selected()

        self.status_label.setText(
            f"Selected {selected_count} duplicate files across {len(self.state['groups'])} groups")
        QMessageBox.information(
            self, "Success",
            f"Selected {selected_count} duplicate files across {len(self.state['groups'])} groups"
        )

    def deselect_all(self):
        if not self.state['groups']:
            return

        reply = QMessageBox.question(
            self, "Confirm Deselection",
            f"Deselect all duplicate files across {len(self.state['groups'])} groups?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        for group in self.state['groups']:
            for file in group.files:
                if not file.is_main:
                    file.selected = False

        if self.current_group:
            self.on_group_selected()

        self.status_label.setText("All duplicates deselected")
        QMessageBox.information(self, "Success", "All files deselected")

    def save_move_log(self, moved_files, target_folder):
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
            return log_filename
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to save move log: {e}")
            return None

    def process_duplicates(self, action):
        if not self.state['groups']:
            QMessageBox.information(self, "Info", "No duplicates to process")
            return

        total_selected = 0
        for group in self.state['groups']:
            for file in group.files:
                if file.selected:
                    total_selected += 1

        if total_selected == 0:
            QMessageBox.information(
                self, "Info",
                "No files selected for processing. Use 'Select All' button or manually select files."
            )
            return

        action_name = "Move"
        action_past = "moved"

        reply = QMessageBox.question(
            self, f"Confirm {action_name}",
            f"{action_name} {total_selected} selected duplicate files?\n\n"
            f"Files will be {action_past} to: {self.state['dupes_folder']}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        target_folder = None
        if not self.state['dry_run']:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            target_folder = os.path.join(self.state['dupes_folder'], timestamp)
            try:
                os.makedirs(target_folder, exist_ok=True)
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Failed to create dated folder: {e}")
                return

        processed = 0
        saved = 0
        errors = []
        moved_files = []

        for group in self.state['groups']:
            main_file = group.main_file or self.select_main_file(group.files)

            for i, file in enumerate(group.files):
                if file.path == main_file.path or not file.selected:
                    continue

                if not self.state['dry_run']:
                    try:
                        ext = os.path.splitext(main_file.path)[1]
                        base = os.path.splitext(os.path.basename(main_file.path))[0]
                        new_name = f"{base}_{i + 1}{ext}"
                        new_path = os.path.join(target_folder, new_name)

                        counter = 1
                        while os.path.exists(new_path):
                            new_name = f"{base}_{i + 1}_{counter}{ext}"
                            new_path = os.path.join(target_folder, new_name)
                            counter += 1

                        os.rename(file.path, new_path)

                        moved_files.append({
                            'original_path': file.path,
                            'new_path': new_path,
                            'size': file.size,
                            'group_hash': group.hash,
                            'timestamp': datetime.now().isoformat()
                        })

                        processed += 1
                        saved += group.size

                    except (OSError, IOError) as e:
                        errors.append(f"{file.name}: {e}")

        log_file = None
        if moved_files and not self.state['dry_run']:
            log_file = self.save_move_log(moved_files, target_folder)

        result_msg = (
            f"Files {action_past}: {processed}\n"
            f"Space freed: {self.format_size(saved)}"
        )

        if log_file:
            result_msg += f"\n\nMove log saved to:\n{log_file}"

        if errors:
            result_msg += "\n\nErrors:\n" + "\n".join(errors)

        if self.state['dry_run']:
            result_msg = f"TEST MODE - no files were actually {action_past}\n\n{result_msg}"

        QMessageBox.information(self, "Done", result_msg)
        self.status_label.setText(f"Processing complete. {processed} files {action_past}.")

        self.reset_all()

    def open_dupes_folder(self):
        folder = self.state['dupes_folder']
        if not os.path.exists(folder):
            QMessageBox.information(
                self, "Info",
                "Duplicates folder does not exist yet. Please run a scan first."
            )
            return

        if sys.platform == 'win32':
            os.startfile(folder)
        elif sys.platform == 'darwin':
            subprocess.run(['open', folder])
        else:
            subprocess.run(['xdg-open', folder])

    def show_restore_dialog(self):
        dialog = RestoreDialog(self)
        dialog.exec()

    def reset_all(self):
        self.state['groups'] = []
        self.state['filtered_groups'] = []
        self.state['total_files'] = 0
        self.state['total_size'] = 0
        self.state['duplicate_cnt'] = 0
        self.state['duplicate_sum'] = 0
        self.state['scan_time'] = 0
        self.state['is_scanning'] = False

        self.current_group = None
        if hasattr(self, 'search_edit'):
            self.search_edit.clear()

        self.groups_tree.clear()
        self.files_tree.clear()

        self.right_title.setText("Group Details")
        self.group_size_label.setText("Size: -")
        self.group_copies_label.setText("Copies: -")
        self.group_total_label.setText("Total: -")

        self.stats_total_label.setText("Files: -")
        self.stats_dupes_label.setText("Duplicates: -")
        self.stats_groups_label.setText("Groups: -")
        self.stats_space_label.setText("Space: -")
        self.stats_time_label.setText("Time: -")

        self.progress_bar.setValue(0)

        self.move_btn.setEnabled(False)
        self.scan_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
        self.cancel_btn.setVisible(False)
        self.select_all_btn.setEnabled(True)
        self.deselect_all_btn.setEnabled(True)
        self.dry_run_check.setEnabled(True)

        self.status_label.setText("Ready - all data reset")

    def show_statistics(self):
        if not self.state['groups']:
            QMessageBox.information(self, "Statistics", "No scan data available")
            return

        stats = (
            f"Total Files: {self.state['total_files']} "
            f"({self.format_size(self.state['total_size'])})\n"
            f"Duplicate Groups: {len(self.state['groups'])}\n"
            f"Duplicate Files: {self.state['duplicate_cnt']}\n"
            f"Space to Free: {self.format_size(self.state['duplicate_sum'])}\n"
            f"Scan Time: {self.state['scan_time']:.1f}s"
        )

        QMessageBox.information(self, "Detailed Statistics", stats)

    def show_shortcuts(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Keyboard Shortcuts")
        msg.setText(self.config.shortcuts_text)
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About Smart File Duplicate Manager")
        dialog.setMinimumSize(600, 500)

        layout = QVBoxLayout(dialog)

        title = QLabel("Smart File Duplicate Manager")
        title.setStyleSheet("""
            QLabel {
                color: #2a82da;
            }
        """)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        version = QLabel(f"Version {self.config.version}")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)

        about_label = QLabel()
        about_label.setText(self.config.about_text)
        about_label.setTextFormat(Qt.TextFormat.RichText)
        about_label.setOpenExternalLinks(True)
        about_label.setWordWrap(True)
        scroll = QScrollArea()
        scroll.setWidget(about_label)
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(350)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        layout.addWidget(scroll)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.exec()

    def open_documentation(self):
        import webbrowser
        webbrowser.open(self.config.doc_url)

    def report_issue(self):
        import webbrowser
        webbrowser.open(self.config.issue_url)

    def show_license(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("License")
        dialog.setMinimumSize(600, 500)

        layout = QVBoxLayout(dialog)

        title = QLabel("BSD 3-Clause License")
        title.setStyleSheet("""
                    QLabel {
                        color: #2a82da;
                    }
                """)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)

        license_text = self.load_license_from_file()
        if license_text:
            text_edit.setPlainText(license_text)
        else:
            text_edit.setPlainText(self.config.license_text)

        text_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        text_edit.setMinimumHeight(350)
        layout.addWidget(text_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.exec()

    def load_license_from_file(self):
        try:
            possible_paths = [
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'LICENSE'),
                os.path.join(os.path.dirname(os.path.dirname(__file__)), 'LICENSE'),
                os.path.join(os.path.dirname(__file__), 'LICENSE'),
                os.path.join(os.getcwd(), 'LICENSE')
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        return f.read()

            return None
        except Exception:
            return None

    @staticmethod
    def format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def show_file_details(self, file):
        if not file:
            return

        details = f"""
        <b style="color: #2a82da;">File Details:</b><br><br>

        <b style="color: #2a82da;">Name:</b> {file.name}<br>
        <b style="color: #2a82da;">Full Path:</b><br>
        <span style='font-family: monospace; word-wrap: break-word;'>{file.path}</span><br><br>

        <b style="color: #2a82da;">Size:</b> {file.size_str} ({file.size:,} bytes)<br>
        <b style="color: #2a82da;">Hash:</b> {file.hash if file.hash else 'Not calculated'}<br>
        <b style="color: #2a82da;">Modified:</b> {file.date_str}<br>

        <b style="color: #2a82da;">Group Hash:</b> {file.hash[:16] if file.hash else 'N/A'}<br>
        <b style="color: #2a82da;">Is Main File:</b> {'Yes' if file.is_main else 'No'}<br>
        <b style="color: #2a82da;">Selected:</b> {'Yes' if file.selected else 'No'}<br>
        """

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("File Details")
        msg_box.setText(details)
        msg_box.setTextFormat(Qt.TextFormat.RichText)

        copy_btn = msg_box.addButton("Copy Path", QMessageBox.ButtonRole.ActionRole)
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(file.path))

        msg_box.addButton(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.status_label.setText("Path copied to clipboard")

    def on_file_double_clicked(self, item, column):
        file = item.data(0, Qt.ItemDataRole.UserRole)
        if file:
            self.show_file_details(file)
