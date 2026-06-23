## 📥 Installation

The recommended way to install `pypineofetch` is via **pipx**, as it isolates the application and its dependencies from your global system packages.

### 🐧 Linux (Ubuntu, Mint, Debian, etc.)

sudo apt install pipx
pipx ensurepath
# Restart your terminal, then run:
pipx install pypineofetch

###🐧 Linux (Arch Linux)

sudo pacman -S python-pipx
pipx ensurepath
# Restart your terminal. If "pyfetch: command not found" occurs, run:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
# Then run:
pipx install pypineofetch

🪟 Windows

Open PowerShell as Administrator and run:
python -m pip install --user pipx
pipx ensurepath
# Restart your terminal, then run:
pipx install pypineofetch


🍏 macOS
brew install pipx
pipx ensurepath
pipx install pypineofetch

🐍 Standard Pip (Inside a virtual environment)
pip install pypineofetch
or
pip3 install pypineofetch
for update - pip install --upgrade pypineofetch

🚀 Usage

Once installed, simply run the following command in your terminal:
pyfetch
pyfetch macos - run pyfetch with macos
pyfetch windows - run pyfetch with windows

for update - pipx upgrade pypineofetch
or reinstall
pipx uninstall pyfetch
pipx reinstall pypineofetch

if doesn't work, let me know
my discord: dizort21
(or googling)
