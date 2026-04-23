# Smart File Duplicate Manager <sup>v1.2.3</sup>

**Smart File Duplicate Manager** is an app for finding and managing duplicate files. It's written on Python using PyQt6.

---

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/smartlegionlab/smart-file-duplicate-manager)](https://github.com/smartlegionlab/smart-file-duplicate-manager/)
![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-file-duplicate-manager)
[![GitHub](https://img.shields.io/github/license/smartlegionlab/smart-file-duplicate-manager)](https://github.com/smartlegionlab/smart-file-duplicate-manager/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-file-duplicate-manager?style=social)](https://github.com/smartlegionlab/smart-file-duplicate-manager/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-file-duplicate-manager?style=social)](https://github.com/smartlegionlab/smart-file-duplicate-manager/network/members)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)

---

## ⚠️ Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks.

**Full legal disclaimer:** See [DISCLAIMER.md](https://github.com/smartlegionlab/smart-file-duplicate-manager/blob/master/DISCLAIMER.md)

---

## Features

### Duplicate Search
- Scan the selected folder and all subfolders
- Compare files by size, then by hash (xxHash, or MD5 if none)
- Multi-threaded scanning (uses all available processor cores)
- Filters by file size and extension

### Duplicate Management
- Automatically determines the primary file in each group based on the following strategy:
- Oldest / Newest
- Smallest / Largest
- Shortest / Longest Path
- All other files in the group are automatically marked as duplicates
- Manually select files in each group (checkboxes)
- Ability to change the primary file in a group
- Globally select all duplicates / deselect all

### File Actions
- **Move** — duplicates are moved to the destination folder in a subfolder with the date and time. A JSON log with all information about the moved files is saved in the folder.
- **Test Mode** — simulates actions without actually moving

### Restore
- View all previously moved files from JSON logs
- Selective file restore to their original folders
- Automatic log update and deletion of empty folders

### Interface
- Three main panels:
- Left — scan settings
- Center — list of duplicate groups with statistics
- Right — group details and file list with checkboxes
- Search by file name
- Progress bar and status bar
- Confirmation of all important actions
- Hotkeys for basic operations
- Dark theme

## Installation and Run

```bash
# Cloning the repository
git clone https://github.com/smartlegionlab/smart-file-duplicate-manager.git
cd smart-file-duplicate-manager

python -m venv venv
source venv/bin/activate

# Installing dependencies
pip install -r requirements.txt

# Running
python app.py
```

## System Requirements
- Python 3.8 or higher
- Windows / Linux / macOS

## Dependencies
- PyQt6 — GUI
- xxhash — fast hashing (optional)

## Usage

1. In the left panel, specify the scan folder and the duplicates folder.
2. If necessary, adjust filters and select a strategy.
3. Click "Start Scan."
4. After scanning is complete, select the desired files (or use "Select All").
5. To restore previously moved files, use the "Tools" → "Restore Files" menu.

---

### Desktop Integration (Linux)

**Creating Application Shortcuts:**

The application allows you to create desktop entries directly from the menu:

1. **Go to File → Create Desktop Entry**
2. **Choose locations:**
   - ✓ Application Menu (`~/.local/share/applications/`) - adds to system app menu
   - □ Desktop (`~/Desktop/`) - creates shortcut on desktop
3. **Click "Create Entry"**

**What happens:**
- Creates `.desktop` file(s) with proper configuration
- Sets executable permissions automatically
- Uses application icon if available

**After creation:**
- **Application Menu**: Log out and back in (or restart desktop) for entry to appear
- **Desktop shortcut**: May show "Unsecured Application Launcher" warning
  - Right-click on shortcut → "Allow Launching" or "Trust"
  - This is a one-time security confirmation

**Note:** This feature is only available on Linux systems with desktop environments that support `.desktop` files (GNOME, KDE, XFCE, etc.).

---

## Hotkeys

| Action                   | Keys         |
|--------------------------|--------------|
| Select Scan Folder       | Ctrl+Shift+O |
| Select Duplicates Folder | Ctrl+Shift+D |
| Start scan               | Ctrl+R       |
| Cancel scan              | Ctrl+Shift+C |
| Reset                    | Ctrl+X       |
| Exit                     | Ctrl+Q       |
| Select all duplicates    | Ctrl+A       |
| Deselect all             | Ctrl+Shift+A |
| Test mode                | Ctrl+T       |
| Show statistics          | Ctrl+I       |
| Clear search             | Ctrl+L       |
| Move selected files      | Ctrl+M       |
| Restore files            | Ctrl+Shift+R |
| Open duplicates folder   | Ctrl+Shift+F |
| Keyboard Shortcuts       | Ctrl+/       |
| About                    | Ctrl+H       |
| Documentation            | F1           |
| Report Issue             | Ctrl+Shift+I |
| License                  | Ctrl+Alt+L   |

---

## 👤 Author

**Alexander Suvorov**
- GitHub: [@smartlegionlab](https://github.com/smartlegionlab)

If you find this tool useful, please consider giving it a star on GitHub!

---

## License

BSD 3-Clause License. See the [LICENSE](LICENSE) file for more details.

---

*Made with ❤️ for the open-source community*

---

## 🖼️ Screenshot

![Smart File Duplicate Manager](https://github.com/smartlegionlab/smart-file-duplicate-manager/blob/master/data/images/smart-file-duplicate-manager.png)