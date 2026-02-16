from core import __version__ as ver

class Config:
    app_name = "Smart Duplicate Cleaner"
    version = ver
    doc_url = "https://github.com/smartlegionlab/smart-duplicate-cleaner-python"
    issue_url = "https://github.com/smartlegionlab/smart-duplicate-cleaner-python/issues"
    about_text = f"""
            <h2>Smart Duplicate Cleaner v{ver}</h2>
            <p>A powerful GUI application for finding and managing duplicate files.</p>
            <p>Built with Python and PyQt6.</p>
            <p><br></p>
            <p>Author: Alexander Suvorov</p>
            <p>GitHub: @smartlegionlab</p>
            <p><br></p>
            <p>License: BSD 3-Clause</p>
            <p>© 2026 Smart Legion Lab</p>
            """
    license_text = """
            <h3>BSD 3-Clause License</h3>
            <p>Copyright (c) 2026, Alexander Suvorov<br>
            All rights reserved.</p>
            <p>Redistribution and use in source and binary forms, with or without<br>
            modification, are permitted provided that the following conditions are met:</p>
            <p>1. Redistributions of source code must retain the above copyright notice,<br>
               this list of conditions and the following disclaimer.</p>
            <p>2. Redistributions in binary form must reproduce the above copyright notice,<br>
               this list of conditions and the following disclaimer in the documentation<br>
               and/or other materials provided with the distribution.</p>
            <p>3. Neither the name of the copyright holder nor the names of its<br>
               contributors may be used to endorse or promote products derived from<br>
               this software without specific prior written permission.</p>
            <p>THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"<br>
            AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE<br>
            IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE<br>
            DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE<br>
            FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL<br>
            DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR<br>
            SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER<br>
            CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,<br>
            OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE<br>
            OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.</p>
            """
    shortcuts_text = """
            <h3>Keyboard Shortcuts</h3>
            <table>
            <tr><th>Action</th><th>Shortcut</th></tr>
            <tr><td>Select Scan Folder</td><td>Ctrl+Shift+O</td></tr>
            <tr><td>Select Duplicates Folder</td><td>Ctrl+Shift+D</td></tr>
            <tr><td>Start Scan</td><td>Ctrl+R</td></tr>
            <tr><td>Cancel Scan</td><td>Ctrl+Shift+C</td></tr>
            <tr><td>Reset</td><td>Ctrl+Shift+R</td></tr>
            <tr><td>Exit</td><td>Ctrl+Q</td></tr>
            <tr><td>Select All Duplicates</td><td>Ctrl+A</td></tr>
            <tr><td>Deselect All</td><td>Ctrl+Shift+A</td></tr>
            <tr><td>Test Mode</td><td>Ctrl+T</td></tr>
            <tr><td>Show Statistics</td><td>Ctrl+I</td></tr>
            <tr><td>Clear Search</td><td>Ctrl+L</td></tr>
            <tr><td>Move Selected Files</td><td>Ctrl+M</td></tr>
            <tr><td>Delete Selected Files</td><td>Ctrl+Shift+Delete</td></tr>
            <tr><td>Open Dupes Folder</td><td>Ctrl+Shift+F</td></tr>
            <tr><td>Keyboard Shortcuts</td><td>Ctrl+/</td></tr>
            <tr><td>About</td><td>Ctrl+H</td></tr>
            <tr><td>Documentation</td><td>F1</td></tr>
            <tr><td>Report Issue</td><td>Ctrl+Shift+I</td></tr>
            </table>
            """