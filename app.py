import sys

from PyQt6.QtWidgets import QApplication
from core.ui.dark_theme import ModernStyle
from core.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Smart Duplicate Cleaner")
    app.setOrganizationName("Smart Legion Lab")

    ModernStyle.apply(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
