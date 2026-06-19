import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 
import os
import sys
import re
import platform
import psutil
import getpass
import socket
import subprocess
from cpuinfo import get_cpu_info
from pynvml import (
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetName,
    nvmlInit,
    nvmlShutdown,
)                                   #imports

# colors for ascii arts
CYAN = "\033[36m"
YELLOW = "\033[33m"
GRAY = "\033[2m"
RED = "\033[31m"                            
MAGENTA = "\033[35m"
BLUE = "\033[34m"
ORANGE = "\033[38;5;208m"
GREEN = "\033[32m"
RESET = "\033[0m"

# OS ASCII arts 
LOGOS = {
    "Linux": fr"""         
{GRAY}            a8888b.{RESET}
{GRAY}           d888888b.{RESET}
{GRAY}           8P"YP"Y88{RESET}
{GRAY}           8{RESET}|o||o|{GRAY}88{RESET}
{GRAY}           8{RESET}{YELLOW}'    .{RESET}{GRAY}88{RESET}
{GRAY}           8{RESET}{YELLOW}`._.' {RESET}{GRAY}Y8.{RESET}
{GRAY}          d/      `8b.{RESET}
{GRAY}         dP{RESET}   .    {GRAY}Y8b.{RESET}
{GRAY}        d8:{RESET}'  "  `::{GRAY}88b{RESET}
{GRAY}       d8{RESET}"         '{GRAY}Y88b{RESET}
{GRAY}      :8P{RESET}    '      :{GRAY}888{RESET}
{GRAY}       8a{RESET}.   :     _{GRAY}a88P{RESET}
{YELLOW}     ._/"Y{RESET}aa_:   .{YELLOW}./\/\/\{RESET}
{YELLOW}     \    Y{RESET}P"    `{YELLOW}|      '{RESET}
{YELLOW}     /     \{RESET}.___.d{YELLOW}|    .'{RESET}
{YELLOW}     `--..__){RESET}{GRAY}8888P{RESET}{YELLOW}`._.' {RESET}
  """,
    "Windows": fr"""
{GREEN}                    ....,,:;+ccllll{RESET}
{RED}      ...,,+:;{RESET}  {GREEN}cllllllllllllllllll{RESET}
{RED},cclllllllllll{RESET}  {GREEN}lllllllllllllllllll{RESET}
{RED}llllllllllllll{RESET}  {GREEN}lllllllllllllllllll{RESET}
{RED}llllllllllllll{RESET}  {GREEN}lllllllllllllllllll{RESET}
{RED}llllllllllllll{RESET}  {GREEN}lllllllllllllllllll{RESET}
{RED}llllllllllllll{RESET}  {GREEN}lllllllllllllllllll{RESET}
{RED}llllllllllllll{RESET}  {GREEN}lllllllllllllllllll{RESET}

{BLUE}llllllllllllll{RESET}  {YELLOW}lllllllllllllllllll{RESET}
{BLUE}llllllllllllll{RESET}  {YELLOW}lllllllllllllllllll{RESET}
{BLUE}llllllllllllll{RESET}  {YELLOW}lllllllllllllllllll{RESET}
{BLUE}llllllllllllll{RESET}  {YELLOW}lllllllllllllllllll{RESET}
{BLUE}llllllllllllll{RESET}  {YELLOW}lllllllllllllllllll{RESET}
{BLUE}`'ccllllllllll{RESET}  {YELLOW}lllllllllllllllllll{RESET}
{BLUE}       `' \\*::{RESET}{YELLOW}  :ccllllllllllllllll{RESET}
{YELLOW}                       ````''*::cll{RESET}
{YELLOW}                                 ``⠀{RESET}
""",
    "Darwin": fr"""
{GREEN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀{RESET}⠀
{GREEN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⡿⠀⠀⠀⠀⠀{RESET}⠀
{GREEN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⠟⠁⠀⠀⠀⠀⠀{RESET}⠀
{GREEN}⠀⠀⠀⢀⣠⣤⣤⣤⣀⣀⠈⠋⠉⣁⣠⣤⣤⣤⣀⡀⠀{RESET}⠀
{YELLOW}⠀⢠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀{RESET}
{YELLOW}⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀{RESET}
{ORANGE}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀{RESET}⠀
{ORANGE}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀{RESET}⠀
{RED}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀{RESET}
{RED}⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀{RESET}
{MAGENTA}⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁{RESET}
{MAGENTA}⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀{RESET}
{BLUE}⠀⠀⠀⠈⠙⢿⣿⣿⣿⠿⠟⠛⠻⠿⣿⣿⣿⡿⠋⠀⠀⠀{RESET}
""",  
    "Unknown": """
UNKNOWN OPERATING SYSTEM
""",
}

current_os = "Unknown"
info_lines = []

def get_motherboard_info(target_os):            #getting motherboard (host)
    if target_os == "Linux":
        try:
            with open("/sys/devices/virtual/dmi/id/board_vendor", "r") as f:
                vendor = f.read().strip()
            with open("/sys/devices/virtual/dmi/id/board_name", "r") as f:
                model = f.read().strip()
            return f"{vendor} {model}"
        except (FileNotFoundError, PermissionError):
            return "Unknown Linux Board"

    elif target_os == "Windows":
        try:
            output = subprocess.check_output(
                "wmic baseboard get manufacturer,product", shell=True
            )
            lines = output.decode("cp866").strip().split("\n")
            if len(lines) > 1:
                info = lines[1].strip().split()
                return " ".join(info)
            return "Unknown Windows Board"
        except Exception:
            return "Unknown Windows Board"

    elif target_os == "Darwin":
        try:
            output = subprocess.check_output(
                ["sysctl", "-n", "hw.model"]
            ).decode("utf-8")
            return output.strip()
        except Exception:
            return "Apple Device"

    return "Unsupported OS"


def get_resolution(target_os):   #getting resolution of all monitors
    try:
        if target_os == "Linux":
            output = subprocess.check_output("xrandr", shell=True).decode(
                "utf-8"
            )
            resolutions = []
            for line in output.splitlines():
                if "*" in line:
                    res = line.strip().split()[0]
                    if res not in resolutions:
                        resolutions.append(res)
            if resolutions:
                return ", ".join(resolutions)
            return "Unknown"

        elif target_os == "Windows":
            cmd = "Get-CimInstance Win32_VideoController | Select-Object CurrentHorizontalResolution, CurrentVerticalResolution | Format-Table -HideTableHeaders"
            output = subprocess.check_output(
                ["powershell", "-Command", cmd], shell=True
            ).decode("utf-8")
            resolutions = []
            for line in output.splitlines():
                parts = line.strip().split()
                if len(parts) == 2:
                    res = f"{parts[0]}x{parts[1]}"
                    if res not in resolutions:
                        resolutions.append(res)
            if resolutions:
                return ", ".join(resolutions)
            return "Unknown"

        elif target_os == "Darwin":
            cmd = "system_profiler SPDisplaysDataType | grep Resolution"
            output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            resolutions = []
            for line in output.splitlines():
                if ":" in line:
                    res = line.split(":")[1].strip()
                    if res not in resolutions:
                        resolutions.append(res)
            if resolutions:
                return ", ".join(resolutions)
            return "Unknown"

        return "Unknown"
    except Exception:
        return "Unknown"


def get_de(target_os):   #getting de
    if target_os == "Linux":
        de = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")
        if "Cinnamon" in de:
            try:
                ver = (
                    subprocess.check_output(["cinnamon", "--version"])
                    .decode()
                    .strip()
                )
                return ver
            except Exception:
                pass
        return de
    elif target_os == "Windows":
        return "Explorer"
    elif target_os == "Darwin":
        return "Aqua"
    return "Unknown"


def get_gsettings_value(schema, key):
    try:
        res = subprocess.check_output(["gsettings", "get", schema, key])
        return res.decode("utf-8").strip().strip("'\"")
    except Exception:
        return None

    
def get_kernel():
    kernel = platform.release()
    info_lines.append(f"Kernel: {kernel}")


def cpu_get():
    try:
        cpu_brand = get_cpu_info().get("brand_raw", "Unknown CPU")
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            current_ghz = round(cpu_freq.current / 1000, 2)
            max_ghz = (
                round(cpu_freq.max / 1000, 2)
                if cpu_freq.max and cpu_freq.max > 0
                else current_ghz
            )
            freq_info = f"{current_ghz} / {max_ghz} GHz"
        else:
            freq_info = "Unknown Freq"
        info_lines.append(f"CPU: {cpu_brand} | {freq_info}")
    except Exception:
        info_lines.append("CPU: Unknown")


def gpu_get(target_os):   #GPU
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        gpu_name_raw = nvmlDeviceGetName(handle)
        gpu_name = (
            gpu_name_raw.decode("utf-8")
            if isinstance(gpu_name_raw, bytes)
            else gpu_name_raw
        )
        mem_info = nvmlDeviceGetMemoryInfo(handle)
        total_gb = round(mem_info.total / (1024**2))
        used_gb = round(mem_info.used / (1024**2))
        info_lines.append(f"GPU: {gpu_name} | {used_gb} / {total_gb} MB")
        nvmlShutdown()
    except Exception:
        if target_os == "Darwin":
            info_lines.append("GPU: Apple Integrated Graphics")
        else:
            info_lines.append("GPU: Drivers not found or non-NVIDIA card")


def get_ram():         #ram (1024**2 = megabyte 1024**3 = gigabyte)
    ram = psutil.virtual_memory()
    info_lines.append(
        f"Memory: {ram.used // (1024**2)} / {ram.total // (1024**2)} MB"
    )


def get_disk(target_os):
    try:
        path = "C:\\" if target_os == "Windows" else "/"
        disk = psutil.disk_usage(path)
        
        used_gb = disk.used // (1024**3)
        total_gb = disk.total // (1024**3)
        
        info_lines.append(f"Disk ({path}): {used_gb} / {total_gb} GB")
    except Exception:
        info_lines.append("Disk: Unknown")

def get_name():            #pc name and user name
    try:
        namepc = socket.gethostname()
        login_name = getpass.getuser()
        info_lines.append(f"Name: {login_name}@{namepc}")
    except Exception as e:
        info_lines.append(f"error{e}")

def get_shell(target_os):  #shell 
    try:
        if target_os == "Windows":
            parent_name = psutil.Process(os.getppid()).name()
            shell_name = parent_name.replace(".exe", "").lower()
            
            if "python" in shell_name or "code" in shell_name:
                return "powershell"
            return shell_name
        else:
            shell_path = os.environ.get("SHELL")
            if shell_path:
                return shell_path.split("/")[-1]
            
            parent_name = psutil.Process(os.getppid()).name()
            return parent_name.split("/")[-1]
    except Exception:
        return "Unknown"


def wmthemeicons(target_os):        
    if target_os == "Linux":
        wm_theme = get_gsettings_value(
            "org.cinnamon.desktop.wm.preferences", "theme"        #only for linux wmtheme icons and theme
        )
        theme = get_gsettings_value("org.cinnamon.desktop.interface", "gtk-theme")
        icons = get_gsettings_value("org.cinnamon.desktop.interface", "icon-theme")
        if wm_theme:
            info_lines.append(f"WM: {wm_theme}")
        if theme:
            info_lines.append(f"Theme: {theme}")
        if icons:
            info_lines.append(f"Icons: {icons}")


def visible_len(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m|\033\[[0-9;]*m')
    return len(ansi_escape.sub('', text))

def main():
    global current_os, info_lines
    
    current_os = platform.system()


    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "windows":
            current_os = "Windows"
        elif arg == "linux":
            current_os = "Linux"                      #os select (pyfetch macos/windows/linux)
        elif arg in ["mac", "macos", "darwin"]:
            current_os = "Darwin"

    info_lines = []

    if current_os == "Linux":    #OS print
        try:
            os_info = platform.freedesktop_os_release()
            info_lines.append(f"OS: {os_info['PRETTY_NAME']} | {platform.machine()}")
        except AttributeError:
            info_lines.append(f"OS: {platform.system()} {platform.release()} | {platform.machine()}")
    elif current_os == "Windows":
        info_lines.append(f"OS: Windows {platform.release()} | {platform.machine()}")
    elif current_os == "Darwin":
        mac_ver = platform.mac_ver()[0]
        info_lines.append(f"OS: macOS {mac_ver} | {platform.machine()}")
    
    get_kernel()
    get_name()
    info_lines.append(f"Host: {get_motherboard_info(current_os)}") 
    cpu_get() 
    gpu_get(current_os) 
    get_ram()
    get_disk(current_os)
    info_lines.append(f"Resolution: {get_resolution(current_os)}") 
    info_lines.append(f"DE: {get_de(current_os)}") 
    info_lines.append(f"Shell: {get_shell(current_os)}")
    wmthemeicons(current_os)
    info_lines.append(f"Python version: {platform.python_version()}") 

    logo_raw = LOGOS.get(current_os, LOGOS["Unknown"])
    logo_lines = logo_raw.strip('\n').splitlines()

    max_logo_width = max(visible_len(line) for line in logo_lines) if logo_lines else 0
    max_lines = max(len(logo_lines), len(info_lines))

    print("")  
    for i in range(max_lines):
        logo_part = logo_lines[i] if i < len(logo_lines) else ""
        
        padding = max_logo_width - visible_len(logo_part)
        logo_part_padded = logo_part + (" " * padding)

        info_part = info_lines[i] if i < len(info_lines) else ""

        print(f"  {logo_part_padded}   {info_part}")
    print("")

if __name__ == "__main__":
    main()
