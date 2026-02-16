import os
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox,
    QTreeWidget, QTreeWidgetItem, QProgressBar, QMessageBox,
    QFileDialog, QSplitter, QFrame, QHeaderView, QAbstractItemView,
    QGroupBox, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction, QKeySequence

from core.models.config import Config
from core.models.dupe_group import DuplicateGroup
from core.models.file_info import FileInfo
from core.ui.dark_theme import ModernStyle
from core.workers.scan_worker import ScanWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.state = {
            'root_path': str(Path.home()),
            'dupes_folder': str(Path.home() / 'duplicates'),
            'strategy': 'oldest',
            'priority_folder': '',
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

        self.setup_ui()
        self.setup_menu()

    def setup_ui(self):
        self.setWindowTitle(f"{self.config.app_name} v{self.config.version}")
        self.setMinimumSize(1200, 700)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)

        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        left_panel = self.create_left_panel()
        left_scroll.setWidget(left_panel)
        left_scroll.setMaximumWidth(350)

        center_right_splitter = QSplitter(Qt.Orientation.Horizontal)
        center_right_splitter.setHandleWidth(1)
        center_right_splitter.setChildrenCollapsible(False)

        center_scroll = QScrollArea()
        center_scroll.setWidgetResizable(True)
        center_scroll.setFrameShape(QFrame.Shape.NoFrame)
        center_panel = self.create_center_panel()
        center_scroll.setWidget(center_panel)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setFrameShape(QFrame.Shape.NoFrame)
        right_panel = self.create_right_panel()
        right_scroll.setWidget(right_panel)

        center_right_splitter.addWidget(center_scroll)
        center_right_splitter.addWidget(right_scroll)
        center_right_splitter.setSizes([500, 500])

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setHandleWidth(1)
        main_splitter.setChildrenCollapsible(False)
        main_splitter.addWidget(left_scroll)
        main_splitter.addWidget(center_right_splitter)
        main_splitter.setSizes([300, 900])

        content_layout.addWidget(main_splitter)

        progress_panel = self.create_progress_panel()

        main_layout.addWidget(content)
        main_layout.addWidget(progress_panel)

        self.statusBar().showMessage("Ready")

    def create_left_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        title = QLabel(f"{self.config.app_name}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(ModernStyle.FONT_SIZE_TITLE)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        scan_group = QGroupBox("Scan Settings")
        scan_layout = QVBoxLayout(scan_group)
        scan_layout.setSpacing(8)

        path_label = QLabel("Path:")
        self.path_edit = QLineEdit()
        self.path_edit.setText(self.state['root_path'])
        self.path_edit.textChanged.connect(lambda t: self.state.update({'root_path': t}))

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
            "shortest path", "longest path", "priority folder"
        ])
        self.strategy_combo.setCurrentText("oldest")
        self.strategy_combo.currentTextChanged.connect(self.on_strategy_changed)
        scan_layout.addWidget(strategy_label)
        scan_layout.addWidget(self.strategy_combo)

        priority_label = QLabel("Priority folder:")
        self.priority_edit = QLineEdit()
        self.priority_edit.setPlaceholderText("Priority folder")
        self.priority_edit.textChanged.connect(lambda t: self.state.update({'priority_folder': t}))

        priority_btn = QPushButton()
        priority_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DirIcon))
        priority_btn.setMaximumWidth(30)
        priority_btn.clicked.connect(self.browse_priority_folder)

        priority_layout = QHBoxLayout()
        priority_layout.addWidget(self.priority_edit)
        priority_layout.addWidget(priority_btn)
        scan_layout.addWidget(priority_label)
        scan_layout.addLayout(priority_layout)

        scan_btn_layout = QHBoxLayout()
        self.scan_btn = QPushButton("Start Scan")
        self.scan_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_MediaPlay))
        self.scan_btn.setProperty("class", "primary")
        self.scan_btn.clicked.connect(self.start_scan)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogCancelButton))
        self.cancel_btn.setVisible(False)
        self.cancel_btn.clicked.connect(self.cancel_scan)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_BrowserReload))
        self.reset_btn.clicked.connect(self.reset_all)

        scan_btn_layout.addWidget(self.scan_btn)
        scan_btn_layout.addWidget(self.cancel_btn)
        scan_btn_layout.addWidget(self.reset_btn)
        scan_layout.addLayout(scan_btn_layout)

        layout.addWidget(scan_group)

        filters_group = QGroupBox("Filters")
        filters_layout = QGridLayout(filters_group)
        filters_layout.setSpacing(8)

        filters_layout.addWidget(QLabel("Min size (bytes):"), 0, 0)
        self.min_size_edit = QLineEdit()
        self.min_size_edit.setPlaceholderText("0")
        self.min_size_edit.textChanged.connect(
            lambda t: self.state.update({'min_size': int(t) if t else 0})
        )
        filters_layout.addWidget(self.min_size_edit, 0, 1)

        filters_layout.addWidget(QLabel("Max size (bytes):"), 1, 0)
        self.max_size_edit = QLineEdit()
        self.max_size_edit.setPlaceholderText("No limit")
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
        self.threads_edit = QLineEdit()
        self.threads_edit.setText(str(self.state['threads']))
        self.threads_edit.textChanged.connect(
            lambda t: self.state.update({'threads': int(t) if t else os.cpu_count()})
        )
        filters_layout.addWidget(self.threads_edit, 4, 1)

        self.dry_run_check = QCheckBox("Test mode (don't move/delete files)")
        self.dry_run_check.toggled.connect(lambda b: self.state.update({'dry_run': b}))
        filters_layout.addWidget(self.dry_run_check, 5, 0, 1, 2)

        layout.addWidget(filters_group)

        layout.addStretch()
        return panel

    def create_center_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(5)

        title = QLabel("Duplicate Groups")
        title_font = QFont()
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by filename...")
        self.search_edit.textChanged.connect(self.filter_groups)
        layout.addWidget(self.search_edit)

        self.select_all_btn = QPushButton("Select All Duplicates")
        self.select_all_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogApplyButton))
        self.select_all_btn.clicked.connect(self.select_all_duplicates)
        layout.addWidget(self.select_all_btn)

        info_label = QLabel("Note: Main files are automatically selected based on strategy. All other copies are pre-selected as duplicates.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet(f"color: {ModernStyle.FG_MEDIUM}; font-size: 9pt; padding: 5px;")
        layout.addWidget(info_label)

        stats_group = QGroupBox("Scan Statistics")
        stats_layout = QVBoxLayout(stats_group)

        self.stats_total_label = QLabel("Files: -")
        self.stats_dupes_label = QLabel("Duplicates: -")
        self.stats_space_label = QLabel("Space to free: -")
        self.stats_time_label = QLabel("Time: -")

        stats_layout.addWidget(self.stats_total_label)
        stats_layout.addWidget(self.stats_dupes_label)
        stats_layout.addWidget(self.stats_space_label)
        stats_layout.addWidget(self.stats_time_label)

        layout.addWidget(stats_group)

        self.groups_tree = QTreeWidget()
        self.groups_tree.setHeaderLabels(["Group", "Size", "Copies"])
        self.groups_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.groups_tree.setAlternatingRowColors(True)
        self.groups_tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.groups_tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.groups_tree.itemSelectionChanged.connect(self.on_group_selected)

        layout.addWidget(self.groups_tree)

        return panel

    def create_right_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(5)

        self.right_title = QLabel("Group Details")
        title_font = QFont()
        title_font.setBold(True)
        self.right_title.setFont(title_font)
        layout.addWidget(self.right_title)

        self.right_info = QLabel("")
        self.right_info.setWordWrap(True)
        layout.addWidget(self.right_info)

        action_layout = QHBoxLayout()

        self.move_btn = QPushButton("Move Selected")
        self.move_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ArrowRight))
        self.move_btn.setProperty("class", "warning")
        self.move_btn.setEnabled(False)
        self.move_btn.clicked.connect(lambda: self.process_duplicates("move"))

        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_TrashIcon))
        self.delete_btn.setProperty("class", "danger")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(lambda: self.process_duplicates("delete"))

        action_layout.addWidget(self.move_btn)
        action_layout.addWidget(self.delete_btn)

        layout.addLayout(action_layout)

        group_btn_layout = QHBoxLayout()

        set_main_btn = QPushButton("Set as Main")
        set_main_btn.clicked.connect(self.set_as_main)

        select_group_btn = QPushButton("Select All in Group")
        select_group_btn.clicked.connect(self.select_all_in_group)

        group_btn_layout.addWidget(set_main_btn)
        group_btn_layout.addWidget(select_group_btn)

        layout.addLayout(group_btn_layout)

        files_label = QLabel("Files:")
        files_font = QFont()
        files_font.setBold(True)
        files_label.setFont(files_font)
        layout.addWidget(files_label)

        self.files_tree = QTreeWidget()
        self.files_tree.setHeaderLabels(["", "File", "Size", "Date"])
        self.files_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.files_tree.setAlternatingRowColors(True)
        self.files_tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        layout.addWidget(self.files_tree)

        return panel

    def create_progress_panel(self):
        panel = QWidget()
        panel.setMaximumHeight(80)
        layout = QVBoxLayout(panel)
        layout.setSpacing(5)

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel("Progress:"))

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("")
        self.progress_label.setMinimumWidth(150)
        progress_layout.addWidget(self.progress_label)

        layout.addLayout(progress_layout)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        return panel

    def setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")
        select_scan_action = QAction("&Select Scan Folder...", self)
        select_scan_action.setShortcut(QKeySequence.StandardKey.Open)
        select_scan_action.triggered.connect(self.browse_scan_folder)
        file_menu.addAction(select_scan_action)

        select_dupes_action = QAction("Select &Duplicates Folder...", self)
        select_dupes_action.triggered.connect(self.browse_dupes_folder)
        file_menu.addAction(select_dupes_action)

        file_menu.addSeparator()
        start_scan_action = QAction("&Start Scan", self)
        start_scan_action.setShortcut(QKeySequence("Ctrl+R"))
        start_scan_action.triggered.connect(self.start_scan)
        file_menu.addAction(start_scan_action)

        reset_action = QAction("&Reset", self)
        reset_action.setShortcut(QKeySequence("Ctrl+Shift+R"))
        reset_action.triggered.connect(self.reset_all)
        file_menu.addAction(reset_action)

        edit_menu = menubar.addMenu("&Edit")
        select_all_action = QAction("Select &All Duplicates", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.select_all_duplicates)
        edit_menu.addAction(select_all_action)

        deselect_all_action = QAction("&Deselect All", self)
        deselect_all_action.setShortcut(QKeySequence("Ctrl+Shift+A"))
        deselect_all_action.triggered.connect(self.deselect_all)
        edit_menu.addAction(deselect_all_action)

        edit_menu.addSeparator()
        test_mode_action = QAction("&Test Mode", self)
        test_mode_action.setCheckable(True)
        test_mode_action.triggered.connect(lambda b: self.state.update({'dry_run': b}))
        edit_menu.addAction(test_mode_action)

        view_menu = menubar.addMenu("&View")
        stats_action = QAction("Show &Statistics", self)
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

        delete_action = QAction("&Delete Selected Files", self)
        delete_action.setShortcut(QKeySequence("Ctrl+D"))
        delete_action.triggered.connect(lambda: self.process_duplicates("delete"))
        tools_menu.addAction(delete_action)

        tools_menu.addSeparator()
        clean_action = QAction("&Clean Dupes Folder", self)
        clean_action.triggered.connect(self.clean_duplicates_folder)
        tools_menu.addAction(clean_action)

        tools_menu.addSeparator()
        open_folder_action = QAction("&Open Dupes Folder", self)
        open_folder_action.triggered.connect(self.open_dupes_folder)
        tools_menu.addAction(open_folder_action)

        help_menu = menubar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        docs_action = QAction("&Documentation", self)
        docs_action.triggered.connect(self.open_documentation)
        help_menu.addAction(docs_action)

        help_menu.addSeparator()
        report_action = QAction("&Report Issue", self)
        report_action.triggered.connect(self.report_issue)
        help_menu.addAction(report_action)

        license_action = QAction("&License", self)
        license_action.triggered.connect(self.show_license)
        help_menu.addAction(license_action)

    def browse_scan_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Scan Folder", self.state['root_path']
        )
        if folder:
            self.path_edit.setText(folder)
            self.state['root_path'] = folder

    def browse_dupes_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Duplicates Folder", self.state['dupes_folder']
        )
        if folder:
            self.dupes_folder_edit.setText(folder)
            self.state['dupes_folder'] = folder

    def browse_priority_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Priority Folder", self.state['priority_folder'] or self.state['root_path']
        )
        if folder:
            self.priority_edit.setText(folder)
            self.state['priority_folder'] = folder

    def on_strategy_changed(self, text):
        if text == "shortest path":
            self.state['strategy'] = "shortest"
        elif text == "longest path":
            self.state['strategy'] = "longest"
        elif text == "priority folder":
            self.state['strategy'] = "priority"
        else:
            self.state['strategy'] = text

    def start_scan(self):
        if self.state['is_scanning']:
            return

        if not os.path.exists(self.state['root_path']):
            QMessageBox.critical(self, "Error", "Scan folder does not exist!")
            return

        self.scan_btn.setEnabled(False)
        self.reset_btn.setEnabled(False)
        self.move_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.cancel_btn.setVisible(True)
        self.select_all_btn.setEnabled(False)

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
        self.right_info.setText("")

        self.progress_bar.setValue(0)
        self.status_label.setText("Scanning...")
        self.progress_label.setText("Finding files...")

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
            self.scan_worker.stop()
            self.scan_worker.wait()
            self.scan_worker = None

        self.state['is_scanning'] = False
        self.scan_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
        self.cancel_btn.setVisible(False)
        self.select_all_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Scan cancelled")
        self.progress_label.setText("")

    def on_scan_progress(self, current, total, message):
        if total > 0:
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
        self.progress_label.setText(message)

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

        if self.state['groups']:
            self.move_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)

        self.status_label.setText(f"Scan complete. Found {len(self.state['groups'])} duplicate groups.")
        self.progress_bar.setValue(self.progress_bar.maximum())

    def on_scan_error(self, error_msg):
        QMessageBox.critical(self, "Scan Error", f"An error occurred during scan:\n{error_msg}")
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
            f"Files: {self.state['total_files']} ({FileInfo._format_size(self.state['total_size'])})"
        )
        self.stats_dupes_label.setText(f"Duplicates: {self.state['duplicate_cnt']}")
        self.stats_space_label.setText(
            f"Space to free: {FileInfo._format_size(self.state['duplicate_sum'])}"
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
            self.right_info.setText("")
            return

        group = selected[0].data(0, Qt.ItemDataRole.UserRole)
        self.current_group = group

        self.right_title.setText(f"Group: {group.id}")
        self.right_info.setText(
            f"Size: {group.size_str}\n"
            f"Copies: {group.file_count}\n"
            f"Total: {FileInfo._format_size(group.size * group.file_count)}"
        )

        self.files_tree.clear()

        for file in group.files:
            item = QTreeWidgetItem()
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(0, Qt.CheckState.Checked if file.selected else Qt.CheckState.Unchecked)
            item.setText(1, file.name)
            item.setText(2, file.size_str)
            item.setText(3, file.date_str)
            item.setData(0, Qt.ItemDataRole.UserRole, file)

            if file.is_main:
                item.setIcon(1, self.style().standardIcon(self.style().StandardPixmap.SP_DialogApplyButton))

            self.files_tree.addTopLevelItem(item)

        self.files_tree.resizeColumnToContents(0)
        self.files_tree.resizeColumnToContents(2)
        self.files_tree.resizeColumnToContents(3)

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
        elif strategy == "priority" and self.state['priority_folder']:
            priority = self.state['priority_folder']
            for f in files:
                if priority in f.path:
                    return f
            return min(files, key=lambda f: f.mod_time)
        return min(files, key=lambda f: f.mod_time)

    def set_as_main(self):
        if not self.current_group:
            return

        selected = self.files_tree.selectedItems()
        if not selected:
            return

        file = selected[0].data(0, Qt.ItemDataRole.UserRole)

        for f in self.current_group.files:
            f.is_main = (f.path == file.path)
        self.current_group.main_file = file

        self.on_group_selected()

    def select_all_in_group(self):
        if not self.current_group:
            return

        for file in self.current_group.files:
            if file != self.current_group.main_file:
                file.selected = True

        self.on_group_selected()

    def select_all_duplicates(self):
        if not self.state['groups']:
            return

        selected_count = 0
        for group in self.state['groups']:
            for file in group.files:
                if file != group.main_file:
                    file.selected = True
                    selected_count += 1

        if self.current_group:
            self.on_group_selected()

        QMessageBox.information(
            self, "Success",
            f"Selected {selected_count} duplicate files across {len(self.state['groups'])} groups"
        )

    def deselect_all(self):
        if not self.state['groups']:
            return

        for group in self.state['groups']:
            for file in group.files:
                file.selected = False

        if self.current_group:
            self.on_group_selected()

        QMessageBox.information(self, "Success", "All files deselected")

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
                "No files selected for processing. Use 'Select All Dupes' button or manually select files."
            )
            return

        action_past = "moved" if action == "move" else "deleted"

        if action == "delete":
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"PERMANENTLY delete {total_selected} selected duplicates?\nThis cannot be undone!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        target_folder = None
        if not self.state['dry_run'] and action == "move":
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

        for group in self.state['groups']:
            main_file = group.main_file or self.select_main_file(group.files)

            for i, file in enumerate(group.files):
                if file.path == main_file.path or not file.selected:
                    continue

                if not self.state['dry_run']:
                    try:
                        if action == "move":
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

                        elif action == "delete":
                            os.remove(file.path)

                        processed += 1
                        saved += group.size

                    except (OSError, IOError) as e:
                        errors.append(f"{file.name}: {e}")

        result_msg = (
            f"Files {action_past}: {processed}\n"
            f"Space freed: {FileInfo._format_size(saved)}"
        )

        if errors:
            result_msg += "\n\nErrors:\n" + "\n".join(errors)

        if self.state['dry_run']:
            result_msg = f"TEST MODE - no files were actually {action_past}\n\n{result_msg}"

        QMessageBox.information(self, "Done", result_msg)

        self.reset_all()

    def clean_duplicates_folder(self):
        if self.state['dry_run']:
            QMessageBox.information(self, "Test Mode", "Test mode enabled - no files would be deleted")
            return

        folder = self.state['dupes_folder']
        if not os.path.exists(folder):
            QMessageBox.information(self, "Info", "Duplicates folder does not exist")
            return

        reply = QMessageBox.question(
            self, "Confirm Cleanup",
            f"PERMANENTLY delete ALL contents of:\n{folder}\n\nThis will remove all subfolders and files!\nThis cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        deleted = 0
        errors = []

        for root, dirs, files in os.walk(folder):
            if root == folder:
                continue

            for name in files:
                path = os.path.join(root, name)
                try:
                    os.remove(path)
                    deleted += 1
                    if deleted % 10 == 0:
                        self.status_label.setText(f"Cleaned: {deleted} items")
                except OSError as e:
                    errors.append(f"{name}: {e}")

            try:
                if os.path.exists(root):
                    os.rmdir(root)
            except OSError:
                pass

        result_msg = f"Items deleted: {deleted}"
        if errors:
            result_msg += "\n\nErrors:\n" + "\n".join(errors)

        QMessageBox.information(self, "Cleanup Complete", result_msg)
        self.status_label.setText("Duplicates folder cleaned")

    def open_dupes_folder(self):
        folder = self.state['dupes_folder']
        if not os.path.exists(folder):
            QMessageBox.information(
                self, "Info",
                "Duplicates folder does not exist yet. Please run a scan first."
            )
            return

        import subprocess
        import sys

        if sys.platform == 'win32':
            os.startfile(folder)
        elif sys.platform == 'darwin':
            subprocess.run(['open', folder])
        else:
            subprocess.run(['xdg-open', folder])

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
        self.search_edit.clear()

        self.groups_tree.clear()
        self.files_tree.clear()

        self.right_title.setText("Group Details")
        self.right_info.setText("")

        self.stats_total_label.setText("Files: -")
        self.stats_dupes_label.setText("Duplicates: -")
        self.stats_space_label.setText("Space to free: -")
        self.stats_time_label.setText("Time: -")

        self.progress_bar.setValue(0)
        self.progress_label.setText("")
        self.status_label.setText("Ready")

        self.move_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.scan_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
        self.cancel_btn.setVisible(False)
        self.select_all_btn.setEnabled(True)

    def show_statistics(self):
        if not self.state['groups']:
            QMessageBox.information(self, "Statistics", "No scan data available")
            return

        stats = (
            f"Total Files: {self.state['total_files']} "
            f"({FileInfo._format_size(self.state['total_size'])})\n"
            f"Duplicate Groups: {len(self.state['groups'])}\n"
            f"Duplicate Files: {self.state['duplicate_cnt']}\n"
            f"Space to Free: {FileInfo._format_size(self.state['duplicate_sum'])}\n"
            f"Scan Time: {self.state['scan_time']:.1f}s"
        )

        QMessageBox.information(self, "Detailed Statistics", stats)

    def show_about(self):

        QMessageBox.about(self, "About Smart Duplicate Cleaner", self.config.about_text)

    def open_documentation(self):
        import webbrowser
        webbrowser.open(self.config.doc_url)

    def report_issue(self):
        import webbrowser
        webbrowser.open(self.config.issue_url)

    def show_license(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("License")
        msg.setText(self.config.license_text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
