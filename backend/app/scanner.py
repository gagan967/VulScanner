import subprocess
import datetime
import platform
import json
import os
import shutil

def scan_installed_software():
    system = platform.system()
    
    if system == "Windows":
        return scan_windows()
    elif system == "Linux":
        return scan_linux()
    else:
        return []

def scan_windows():
    # PowerShell command to get installed software from Registry calls or Get-Package
    # Using a simple Get-ItemProperty approach for common registry paths
    ps_script = """
    $paths = @(
        'HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*',
        'HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*'
    )
    $software = Get-ItemProperty -Path $paths -ErrorAction SilentlyContinue | 
                Select-Object DisplayName, DisplayVersion | 
                Where-Object { $_.DisplayName -ne $null }
    
    $software | ConvertTo-Json
    """
    
    ps_executable = "powershell"
    # Try to find powershell if default fails (common in some envs)
    import shutil
    if not shutil.which("powershell"):
        # Common paths
        paths = [
            r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
        ]
        for p in paths:
            if os.path.exists(p):
                ps_executable = p
                break
    
    try:
        result = subprocess.run(
            [ps_executable, "-Command", ps_script],
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            return []

        software_list = []
        # Powershell JSON output might be a single object or list
        try:
            data = json.loads(result.stdout)
            if isinstance(data, dict):
                data = [data]
        except json.JSONDecodeError:
            return []

        for item in data:
            name = item.get("DisplayName")
            version = item.get("DisplayVersion", "Unknown")
            if name:
                software_list.append({
                    "name": name,
                    "version": version,
                    "published_date": datetime.date.today()
                })
        return software_list

    except Exception as e:
        print(f"Error scanning Windows: {e}")
        return []

def scan_linux():
    try:
        result = subprocess.run(
            ["dpkg-query", "-W", "-f=${Package} ${Version}\n"],
            capture_output=True,
            text=True
        )

        software_list = []
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                version = parts[1]
                software_list.append({
                    "name": name,
                    "version": version,
                    "published_date": datetime.date.today()
                })
        return software_list
    except FileNotFoundError:
        return []

