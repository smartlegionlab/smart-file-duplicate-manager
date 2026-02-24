# Smart File Duplicate Manager <sup>v1.2.0</sup>

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/smartlegionlab/smart-file-duplicate-manager)](https://github.com/smartlegionlab/smart-file-duplicate-manager/)
![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-file-duplicate-manager)
[![GitHub](https://img.shields.io/github/license/smartlegionlab/smart-file-duplicate-manager)](https://github.com/smartlegionlab/smart-file-duplicate-manager/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-file-duplicate-manager?style=social)](https://github.com/smartlegionlab/smart-file-duplicate-manager/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-file-duplicate-manager?style=social)](https://github.com/smartlegionlab/smart-file-duplicate-manager/network/members)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)

**Smart File Duplicate Manager** is an app for finding and managing duplicate files. It's written on Python using PyQt6.

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

## ⚠️ DISCLAIMER

### COMPLETE AND UNCONDITIONAL WAIVER OF LIABILITY

**BY USING, DOWNLOADING, INSTALLING, COMPILING, OR OTHERWISE INTERACTING WITH THIS SOFTWARE (THE "SOFTWARE"), YOU (THE "USER") EXPRESSLY AND IRREVOCABLY AGREE TO THE FOLLOWING TERMS:**

#### 1. ABSOLUTE WAIVER OF LIABILITY

THE AUTHOR, COPYRIGHT HOLDER, AND CONTRIBUTORS (COLLECTIVELY, THE "AUTHOR") SHALL NOT BE HELD LIABLE UNDER ANY CIRCUMSTANCES, WHETHER IN CONTRACT, TORT (INCLUDING NEGLIGENCE), STRICT LIABILITY, OR ANY OTHER LEGAL OR EQUITABLE THEORY, FOR ANY:

- DIRECT, INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR EXEMPLARY DAMAGES
- LOSS OF PROFITS, REVENUE, OR DATA
- LOSS OF BUSINESS OPPORTUNITY OR GOODWILL
- SYSTEM FAILURE OR MALFUNCTION
- CORRUPTION OR LOSS OF FILES OR DATA
- UNAUTHORIZED ACCESS TO OR DELETION OF FILES
- HARDWARE DAMAGE OR FAILURE
- ANY OTHER DAMAGES OR LOSSES WHATSOEVER

**THIS WAIVER APPLIES EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.**

#### 2. UNCONDITIONAL ACCEPTANCE OF RISK

THE USER ACKNOWLEDGES AND ACCEPTS THAT:

- THE SOFTWARE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT ANY WARRANTIES WHATSOEVER
- THE USER ASSUMES ALL RISKS ASSOCIATED WITH THE USE OF THIS SOFTWARE
- THE USER IS SOLELY RESPONSIBLE FOR BACKING UP ALL DATA BEFORE USING THE SOFTWARE
- THE USER IS SOLELY RESPONSIBLE FOR VERIFYING ALL ACTIONS PERFORMED BY THE SOFTWARE
- THE USER BEARS FULL RESPONSIBILITY FOR ANY CONSEQUENCES ARISING FROM THE USE OF THIS SOFTWARE

#### 3. NO WARRANTIES

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THE AUTHOR EXPRESSLY DISCLAIMS ALL WARRANTIES, WHETHER EXPRESS, IMPLIED, STATUTORY, OR OTHERWISE, INCLUDING BUT NOT LIMITED TO:

- WARRANTIES OF MERCHANTABILITY
- WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE
- WARRANTIES OF TITLE OR NON-INFRINGEMENT
- WARRANTIES OF ACCURACY, RELIABILITY, OR COMPLETENESS
- WARRANTIES OF UNINTERRUPTED OR ERROR-FREE OPERATION

---

## 🚧 DEVELOPMENT STATUS

### ALPHA SOFTWARE NOTICE

**THIS SOFTWARE IS IN ACTIVE DEVELOPMENT AND IS PROVIDED "AS IS" WITHOUT ANY WARRANTIES WHATSOEVER.**

#### 1. DEVELOPMENT STAGE

THE USER ACKNOWLEDGES AND ACCEPTS THAT:

- THIS SOFTWARE IS CURRENTLY IN **ALPHA DEVELOPMENT STAGE**
- THE SOFTWARE IS NOT YET FEATURE-COMPLETE OR STABLE
- THE SOFTWARE IS SUBJECT TO SIGNIFICANT CHANGES WITHOUT NOTICE
- THE SOFTWARE MAY CONTAIN BUGS, ERRORS, OR DEFICIENCIES
- THE SOFTWARE MAY NOT FUNCTION AS INTENDED OR DOCUMENTED
- THE SOFTWARE MAY NOT BE SUITABLE FOR PRODUCTION USE

#### 2. UNPREDICTABLE BEHAVIOR

THE USER UNDERSTANDS THAT THE SOFTWARE MAY EXHIBIT UNPREDICTABLE BEHAVIOR INCLUDING BUT NOT LIMITED TO:

- CRASHES OR FREEZES DURING OPERATION
- INCORRECT IDENTIFICATION OF DUPLICATE FILES
- FAILURE TO DETECT ACTUAL DUPLICATES
- ACCIDENTAL SELECTION OF INCORRECT FILES
- UNINTENDED MOVEMENT OR DELETION OF FILES
- DATA CORRUPTION OR LOSS
- PERFORMANCE DEGRADATION OR HANGS
- INCOMPATIBILITY WITH CERTAIN SYSTEMS OR CONFIGURATIONS
- INCORRECT FILE HASH COMPUTATION
- FAILURE TO PROPERLY HANDLE LARGE NUMBERS OF FILES

#### 3. RECOMMENDATIONS

THE USER IS STRONGLY ADVISED TO:

- USE THE SOFTWARE ONLY FOR TESTING AND EVALUATION PURPOSES
- NEVER USE THE SOFTWARE WITH CRITICAL OR IRREPLACEABLE DATA
- ALWAYS MAINTAIN COMPLETE AND VERIFIED BACKUPS
- TEST THE SOFTWARE THOROUGHLY IN A SAFE ENVIRONMENT FIRST
- VERIFY ALL ACTIONS AND SELECTIONS BEFORE EXECUTING THEM
- REPORT ANY ISSUES OR UNEXPECTED BEHAVIOR TO THE AUTHOR
- READ THE DOCUMENTATION CAREFULLY BEFORE USE

---

*Made with ❤️ for the open-source community*

**LAST UPDATED: 2026**

---

## 🖼️ Screenshot

![Smart File Duplicate Manager](https://github.com/smartlegionlab/smart-file-duplicate-manager/blob/master/data/images/smart-file-duplicate-manager.png)