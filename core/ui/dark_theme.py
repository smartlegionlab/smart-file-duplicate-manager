from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor


class ModernStyle:
    PRIMARY = "#0d6efd"
    SECONDARY = "#6c757d"
    SUCCESS = "#198754"
    DANGER = "#dc3545"
    WARNING = "#ffc107"

    BG_DARK = "#1a1a1a"
    BG_MEDIUM = "#2d2d2d"
    BG_LIGHT = "#3d3d3d"
    FG_LIGHT = "#e0e0e0"
    FG_MEDIUM = "#b0b0b0"
    FG_DARK = "#808080"
    BORDER = "#4a4a4a"
    SELECTION = "#0d6efd"
    HOVER = "#4a4a4a"

    FONT_FAMILY = "Segoe UI, Arial, sans-serif"
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_TITLE = 14

    @classmethod
    def apply(cls, app):
        font = QFont(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL)
        app.setFont(font)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(cls.BG_DARK))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(cls.FG_LIGHT))
        palette.setColor(QPalette.ColorRole.Base, QColor(cls.BG_MEDIUM))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(cls.BG_LIGHT))
        palette.setColor(QPalette.ColorRole.Text, QColor(cls.FG_LIGHT))
        palette.setColor(QPalette.ColorRole.Button, QColor(cls.BG_LIGHT))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(cls.FG_LIGHT))
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(cls.SELECTION))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(cls.FG_LIGHT))
        app.setPalette(palette)

        app.setStyleSheet(f"""
            QMainWindow {{ background-color: {cls.BG_DARK}; }}
            QWidget {{ background-color: transparent; color: {cls.FG_LIGHT}; }}
            QPushButton {{
                background-color: {cls.BG_LIGHT};
                border: 1px solid {cls.BORDER};
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background-color: {cls.HOVER}; border-color: {cls.PRIMARY}; }}
            QPushButton:pressed {{ background-color: {cls.PRIMARY}; }}
            QPushButton:disabled {{ background-color: {cls.BG_MEDIUM}; color: {cls.FG_DARK}; }}
            QPushButton[class="primary"] {{ background-color: {cls.PRIMARY}; color: white; }}
            QPushButton[class="danger"] {{ background-color: {cls.DANGER}; color: white; }}
            QPushButton[class="warning"] {{ background-color: {cls.WARNING}; color: black; }}
            QLineEdit, QComboBox {{
                background-color: {cls.BG_MEDIUM};
                border: 1px solid {cls.BORDER};
                border-radius: 4px;
                padding: 5px;
            }}
            QCheckBox::indicator {{
                width: 18px; height: 18px;
                border: 1px solid {cls.BORDER};
                border-radius: 3px;
                background-color: {cls.BG_MEDIUM};
            }}
            QCheckBox::indicator:checked {{
                background-color: {cls.PRIMARY};
                border-color: {cls.PRIMARY};
            }}
            QTreeWidget {{
                background-color: {cls.BG_MEDIUM};
                border: 1px solid {cls.BORDER};
                border-radius: 4px;
                outline: none;
            }}
            QTreeWidget::item {{ padding: 5px; border-bottom: 1px solid {cls.BORDER}; }}
            QTreeWidget::item:selected {{ background-color: {cls.SELECTION}; }}
            QTreeWidget::item:hover {{ background-color: {cls.HOVER}; }}
            QHeaderView::section {{
                background-color: {cls.BG_LIGHT};
                padding: 5px;
                border: none;
                font-weight: bold;
            }}
            QProgressBar {{
                border: 1px solid {cls.BORDER};
                border-radius: 4px;
                text-align: center;
                background-color: {cls.BG_MEDIUM};
            }}
            QProgressBar::chunk {{ background-color: {cls.PRIMARY}; border-radius: 3px; }}
            QGroupBox {{
                border: 1px solid {cls.BORDER};
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 5px; }}
            QMenuBar {{ background-color: {cls.BG_DARK}; border-bottom: 1px solid {cls.BORDER}; }}
            QMenuBar::item {{ padding: 5px 10px; border-radius: 4px; }}
            QMenuBar::item:selected {{ background-color: {cls.HOVER}; }}
            QMenu {{ background-color: {cls.BG_MEDIUM}; border: 1px solid {cls.BORDER}; }}
            QMenu::item {{ padding: 5px 20px; }}
            QMenu::item:selected {{ background-color: {cls.SELECTION}; }}
            QStatusBar {{ background-color: {cls.BG_DARK}; border-top: 1px solid {cls.BORDER}; }}
            QScrollBar:vertical {{
                border: none; background-color: {cls.BG_DARK}; width: 10px; border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {cls.BG_LIGHT}; border-radius: 5px; min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{ background-color: {cls.HOVER}; }}
            QSplitter::handle {{ background-color: {cls.BORDER}; width: 1px; }}
            QSplitter::handle:hover {{ background-color: {cls.PRIMARY}; }}
        """)
