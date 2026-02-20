# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from core import __version__ as ver

class Config:
    app_name = "Smart File Duplicate Manager"
    version = ver
    doc_url = "https://github.com/smartlegionlab/smart-file-duplicate-manager"
    issue_url = "https://github.com/smartlegionlab/smart-file-duplicate-manager/issues"
    about_text = f"""
    <div style='font-family: sans-serif;'>

        <p>A powerful GUI application for finding and managing duplicate files.<br>
        Built with Python and PyQt6.</p>

        <p><b style="color: #2a82da;">Features:</b></p>
        <ul>
            <li>Multi-threaded scanning</li>
            <li>Fast hashing with xxHash (MD5 fallback)</li>
            <li>6 selection strategies</li>
            <li>Move or delete duplicates</li>
            <li>JSON logs for moved files</li>
            <li>File restoration from logs</li>
            <li>Dark theme</li>
            <li>Keyboard shortcuts</li>
        </ul>

        <p><b style="color: #2a82da;">Author:</b> <a style="color: #467fd4" href='https://github.com/smartlegionlab'>Alexander Suvorov</a><br>

        <p><b style="color: #2a82da;">License:</b> BSD 3-Clause<br>
        Copyright (c) 2026 Smart Legion Lab</p>

        <p><i>This software is provided "AS IS" without any warranties.</i></p>
    </div>
    """
    license_text = """BSD 3-Clause License

        Copyright (c) 2026, Alexander Suvorov
    
        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions are met:
    
        1. Redistributions of source code must retain the above copyright notice, this
           list of conditions and the following disclaimer.
    
        2. Redistributions in binary form must reproduce the above copyright notice,
           this list of conditions and the following disclaimer in the documentation
           and/or other materials provided with the distribution.
    
        3. Neither the name of the copyright holder nor the names of its
           contributors may be used to endorse or promote products derived from
           this software without specific prior written permission.
    
        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
        AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
        IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
        FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
        DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
        SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
        CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
        OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
        OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""
    shortcuts_text = """
            <h3 style="color: #2a82da;">Keyboard Shortcuts</h3>
            <hr>
            <table>
            <tr><th>Action</th><th>Shortcut</th></tr>
            <tr><td>Select Scan Folder</td><td style="color: #467fd4">Ctrl+Shift+O</td></tr>
            <tr><td>Select Duplicates Folder</td><td style="color: #467fd4">Ctrl+Shift+D</td></tr>
            <tr><td>Start Scan</td><td style="color: #467fd4">Ctrl+R</td></tr>
            <tr><td>Cancel Scan</td><td style="color: #467fd4">Ctrl+Shift+C</td></tr>
            <tr><td>Reset</td><td style="color: #467fd4">Ctrl+X</td></tr>
            <tr><td>Exit</td><td style="color: #467fd4">Ctrl+Q</td></tr>
            <tr><td>Select All Duplicates</td><td style="color: #467fd4">Ctrl+A</td></tr>
            <tr><td>Deselect All</td><td style="color: #467fd4">Ctrl+Shift+A</td></tr>
            <tr><td>Test Mode</td><td style="color: #467fd4">Ctrl+T</td></tr>
            <tr><td>Show Statistics</td><td style="color: #467fd4">Ctrl+I</td></tr>
            <tr><td>Clear Search</td><td style="color: #467fd4">Ctrl+L</td></tr>
            <tr><td>Move Selected Files</td><td style="color: #467fd4">Ctrl+M</td></tr>
            <tr><td>Restore Files</td><td style="color: #467fd4">Ctrl+Shift+R</td></tr>
            <tr><td>Open Dupes Folder</td><td style="color: #467fd4">Ctrl+Shift+F</td></tr>
            <tr><td>Keyboard Shortcuts</td><td style="color: #467fd4">Ctrl+/</td></tr>
            <tr><td>About</td><td style="color: #467fd4">Ctrl+H</td></tr>
            <tr><td>Documentation</td><td style="color: #467fd4">F1</td></tr>
            <tr><td>Report Issue</td><td style="color: #467fd4">Ctrl+Shift+I</td></tr>
            <tr><td>License</td><td style="color: #467fd4">Ctrl+Alt+L</td></tr>
            </table>
            """
