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
            <tr><td>Disclaimer</td><td style="color: #467fd4">Ctrl+D</td></tr>
            </table>
            """
    disclaimer_text = """LEGAL DISCLAIMER

COMPLETE AND ABSOLUTE RELEASE FROM ALL LIABILITY

SOFTWARE PROVIDED "AS IS" WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT.

The copyright holder, contributors, and any associated parties EXPLICITLY DISCLAIM AND DENY ALL RESPONSIBILITY AND LIABILITY for:

1. ANY AND ALL DATA LOSS: Complete or partial loss of any data, files, configuration, or information whatsoever
2. ANY AND ALL SECURITY INCIDENTS: Unauthorized access, breaches, compromises, theft, or exposure of any sensitive information
3. ANY AND ALL FINANCIAL LOSSES: Direct, indirect, incidental, special, consequential, or punitive damages of any kind
4. ANY AND ALL OPERATIONAL DISRUPTIONS: Service interruptions, system failures, authentication issues, or denial of service
5. ANY AND ALL IMPLEMENTATION ISSUES: Bugs, errors, vulnerabilities, misconfigurations, incorrect usage, or compatibility problems
6. ANY AND ALL LEGAL OR REGULATORY CONSEQUENCES: Violations of laws, regulations, compliance requirements, or third-party terms of service
7. ANY AND ALL PERSONAL OR BUSINESS DAMAGES: Reputational harm, business interruption, loss of revenue, lost profits, or any other damages
8. ANY AND ALL THIRD-PARTY CLAIMS: Claims made by any other parties affected by software usage
9. ANY AND ALL SYSTEM DAMAGES: Hardware damage, software corruption, operating system instability, or data corruption

USER ACCEPTS FULL AND UNCONDITIONAL RESPONSIBILITY

By installing, accessing, cloning, forking, or using this software in any manner, you irrevocably agree that:

- You assume ALL risks associated with software usage
- You bear SOLE responsibility for your data, credentials, and system security
- You accept COMPLETE responsibility for all testing and validation before production use
- You are EXCLUSIVELY liable for compliance with all applicable laws and regulations
- You accept TOTAL responsibility for any and all consequences of usage
- You PERMANENTLY AND IRREVOCABLY waive, release, and discharge all claims against the copyright holder, contributors, distributors, and any associated entities

NO WARRANTY OF ANY KIND

This software comes with ABSOLUTELY NO GUARANTEES regarding:
- Security effectiveness or cryptographic strength
- Reliability, availability, or uptime
- Fitness for any particular purpose or use case
- Accuracy, correctness, or completeness
- Freedom from defects, vulnerabilities, or backdoors
- Compatibility with any specific hardware, software, or environment

NOT A PROFESSIONAL OR CERTIFIED SOLUTION

This software is provided for educational and experimental purposes. It is not:
- Professional advice or consultation of any kind
- A certified, audited, or validated product
- A guaranteed security solution
- Enterprise-grade or production-ready software
- Endorsed by any authority, organization, or standards body

FINAL AND BINDING AGREEMENT

Usage of this software constitutes your FULL AND UNCONDITIONAL ACCEPTANCE of this disclaimer. If you do not accept ALL terms and conditions, DO NOT USE, CLONE, FORK, OR DOWNLOAD THIS SOFTWARE.

BY PROCEEDING, YOU ACKNOWLEDGE THAT YOU HAVE READ THIS DISCLAIMER IN ITS ENTIRETY, UNDERSTAND ITS TERMS COMPLETELY, AND ACCEPT THEM WITHOUT RESERVATION OR EXCEPTION.
    
    """