# Smart Duplicate Cleaner v0.5.0

**Smart Duplicate Cleaner** is a powerful GUI application for finding and managing duplicate files. Built with Python and PyQt6.

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

```bash
# Clone repository
git clone https://github.com/smartlegionlab/smart-duplicate-cleaner-python.git
cd smart-duplicate-cleaner-python

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## ✨ Features

### Core Functionality
- **Multi-threaded scanning** - Uses all CPU cores for maximum performance
- **Fast hashing** - Uses xxHash (5-10x faster than MD5) with MD5 fallback
- **Real-time progress** - Live updates with file count and current operation
- **Smart filtering** - Filter by size, extensions, and exclude specific folders

### Duplicate Management
- **7 selection strategies** for automatic main file selection:
  - Oldest / Newest files (by modification time)
  - Smallest / Largest size
  - Shortest / Longest path
  - Priority folder preference
- **Global selection** - Select all duplicates across all groups with one click
- **Batch processing** - Process all selected duplicates in a single operation
- **Dual action modes**:
  - **Move** - Safely relocate duplicates to organized folder structure
  - **Delete** - Permanently remove selected duplicates (with confirmation)
- **Organized storage** - Moved files are stored in dated subfolders
- **Folder maintenance** - Clean up duplicates folder with one click
- **Interactive UI** - Manually check/uncheck files in any group
- **Main file override** - Change which file to keep in each group
- **Test mode** - Preview actions without actually moving/deleting files

### Modern Interface
- **Three-panel layout**:
  - **Left panel**: Settings panel with all configuration options
  - **Center panel**: Searchable list of duplicate groups
  - **Right panel**: Detailed file view with checkboxes
- **Live search** - Filter groups by filename in real-time
- **Progress tracking** - Visual progress bar with detailed status
- **File information** - View full path, size, modification date, and hash
- **Classic menu bar** with keyboard shortcuts
- **Button bar** - Logically grouped buttons at the bottom
- **Dark theme** - Modern Bootstrap-like dark theme with color-coded buttons

## 📝 Usage Example

```bash
# Run the application
python main.py

# Basic workflow:
# 1. Select folder to scan
# 2. Choose duplicates folder
# 3. Set strategy (e.g., "oldest")
# 4. Click "Start Scan"
# 5. Click "Select All Dupes"
# 6. Click "Move Selected" or "Delete Selected"
```

## 📄 License

[BSD 3-Clause License](LICENSE)