# Stable ASCII Video

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)]()

A high-performance Python tool that transforms any video into a vibrant, truecolor (24-bit RGB) ASCII art video. Instead of relying on ANSI terminal escape sequences or pre-rendered text files, it samples original RGB colors directly from the source video cells and dynamically renders anti-aliased monospace glyphs onto a crisp video canvas.

Supports **Windows**, **macOS**, and **Linux** out of the box.

---

## ✨ Features

- **True 24-bit RGB Color**: Each ASCII character preserves the exact sampled RGB color from the source video frame.
- **Cross-Platform Monospace Font Auto-Detection**:
  - **Windows**: `Consolas`, `Lucida Console`, `Courier New`
  - **macOS**: `Menlo`, `SF Mono`, `Courier New`
  - **Linux**: `DejaVu Sans Mono`, `Liberation Mono`
- **Dynamic Cell Metrics**: Automatically calculates glyph dimensions (`get_cell_size`) based on the active font to avoid distortion, stretching, or clipping on all platforms.
- **Optimized Video Codecs**: Uses `avc1` (H.264) with `mp4v` fallbacks, making output videos instantly playable in **Apple QuickTime Player**, **macOS Finder Quick Look (Spacebar preview)**, and **Windows Media Player / Movies & TV**.
- **Aspect-Ratio Preserving Grid**: Scales row counts to match character dimensions so the aspect ratio is never warped.
- **Contrast & Brightness Controls**: Fine-tune contrast and brightness multipliers to make characters pop against dark backgrounds.
- **1-Click Auto Runners**: Includes `run_windows.bat` for Windows and `run_mac.sh` for macOS/Linux.

---

## 🪟 Windows: Step-by-Step Guide

Follow these steps on Windows:

### Step 1: Install Python
1. Download Python (version 3.9 or newer) from [python.org](https://www.python.org/downloads/).
2. **IMPORTANT**: On the first installer screen, make sure to check the box:
   > ☑️ **"Add python.exe to PATH"**
3. Complete the setup.

### Step 2: Download the Project
Open PowerShell or Command Prompt, and run:
```cmd
git clone https://github.com/subratadas7/Truecolor-ascii-video-genarator.git
cd Truecolor-ascii-video-genarator
```
*(Or click **Code -> Download ZIP** on GitHub and extract the folder).*

### Step 3: Add Your Video
Place the video you want to convert into this folder and name it **`1.mp4`** (or keep its original name).

### Step 4: Run the Converter

#### 🟢 Method A: 1-Click Auto Run (Easiest)
- Simply double-click **`run_windows.bat`**.
- It will automatically set up the virtual environment, install requirements, and convert `1.mp4`.
- **Drag & Drop**: You can also drag-and-drop any video file directly on top of `run_windows.bat` to convert it immediately.

#### 🔵 Method B: Using PowerShell (Manual)
```powershell
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
.venv\Scripts\Activate.ps1

# (If you get an execution policy error, run:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# and then re-run .venv\Scripts\Activate.ps1)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run generator
python export_truecolor_ascii_video.py
```

#### 🟡 Method C: Using Command Prompt (CMD)
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python export_truecolor_ascii_video.py
```

### Step 5: Check Your Output
Your converted video will be saved as **`truecolor_ascii_output.mp4`** in the same folder. You can open and play it with Windows Media Player, Movies & TV, or VLC.

---

## 🍎 macOS: Step-by-Step Guide

Follow these steps on a Mac:

### Step 1: Verify Python Installation
Open **Terminal** (`Cmd + Space` -> type `Terminal`) and check Python:
```bash
python3 --version
```
*(If Python is not installed, install it via [python.org](https://www.python.org/downloads/) or via Homebrew: `brew install python`).*

### Step 2: Clone the Project
In Terminal, run:
```bash
git clone https://github.com/subratadas7/Truecolor-ascii-video-genarator.git
cd Truecolor-ascii-video-genarator
```

### Step 3: Add Your Video
Place your source video into this folder as **`1.mp4`**.

### Step 4: Run the Converter

#### 🟢 Method A: 1-Click Auto Run (Easiest)
Make `run_mac.sh` executable and run it:
```bash
chmod +x run_mac.sh
./run_mac.sh
```
*(This automatically creates `.venv`, installs requirements, and renders `1.mp4`).*

#### 🔵 Method B: Manual Terminal Commands
```bash
# 1. Create virtual environment
python3 -m venv .venv

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the script
python export_truecolor_ascii_video.py
```

### Step 5: Check Your Output
The output file is **`truecolor_ascii_output.mp4`**.
- On Mac, you can select it in Finder and press **Spacebar (Quick Look)** to preview it instantly, or double-click to open in **QuickTime Player**.

---

## 🧑‍💻 Running in VS Code (Visual Studio Code)

This project has built-in **`.vscode`** configuration for both Windows and macOS:

1. **Open the folder in VS Code**:
   - Go to `File > Open Folder...` and select `Truecolor-ascii-video-genarator`.
2. **Install the Python Extension**:
   - Install the official **Python** extension (`ms-python.python`) if not already installed.
3. **Select the Python Interpreter**:
   - Press `Ctrl + Shift + P` (Windows) or `Cmd + Shift + P` (macOS).
   - Type and select **`Python: Select Interpreter`**.
   - Choose the one pointing to `./.venv`.
4. **Run the Project**:
   - **▷ Play Button**: Open `export_truecolor_ascii_video.py` and click the **Run Python File (Play icon)** in the top-right corner.
   - **F5 / Run & Debug**: Press `F5` to run with debugging. You can select either:
     - `Python: Convert Default (1.mp4)`
     - `Python: Convert High Quality (160 cols, 15 FPS)`
   - **Integrated Terminal**: Open the terminal (`` Ctrl + ` `` or `` Cmd + ` ``) and run:
     ```bash
     python export_truecolor_ascii_video.py
     ```

---

## 💻 CLI Options & Custom Settings

You can customize the resolution, speed, and look using command-line arguments on either Mac or Windows:

```bash
python export_truecolor_ascii_video.py [input_video] [options]
```

### Examples:
- **Custom input/output names:**
  ```bash
  python export_truecolor_ascii_video.py my_video.mp4 -o custom_output.mp4
  ```
- **High-detail rendering (wider terminal):**
  ```bash
  python export_truecolor_ascii_video.py 1.mp4 --width 160 --contrast 1.25 --brightness 1.15
  ```
- **Smoother framerate:**
  ```bash
  python export_truecolor_ascii_video.py 1.mp4 --fps 24.0
  ```
- **Compact preview:**
  ```bash
  python export_truecolor_ascii_video.py 1.mp4 --width 80 --fps 10.0
  ```

### Arguments Reference Table:

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input` | `str` | `1.mp4` | Path to the source input video file. |
| `-o`, `--output` | `str` | `truecolor_ascii_output.mp4` | Destination path for the converted MP4 video. |
| `--width` | `int` | `120` | Number of ASCII character columns across the frame (min: `30`). |
| `--fps` | `float` | `10.0` | Output video framerate in frames per second. |
| `--contrast` | `float` | `1.15` | Contrast factor for character luminance. |
| `--brightness` | `float` | `1.05` | Brightness multiplier for character color. |

---

## 🔍 How It Works

1. **Frame Extraction**: Decodes video frames via OpenCV.
2. **Monospace Font & Cell Detection**: Loads native fonts (`Menlo` on macOS, `Consolas` on Windows) and computes character cell width and height.
3. **Resizing & Aspect Calculation**: Resizes the image to `columns x rows` accounting for font aspect ratio.
4. **Luminance & Color Mapping**: Computes ITU-R BT.709 perceived luminance ($0.2126R + 0.7152G + 0.0722B$) and assigns ASCII glyphs (` .,:;irsXA253hMHGS#9B&@`).
5. **Color Drawing**: Draws every character with its sampled 24-bit RGB color onto an image canvas.
6. **Encoding**: Saves to an MP4 video using native `avc1` / `mp4v` codec.

---

## 🛠️ Troubleshooting

### Windows:
- **`'python' is not recognized as an internal or external command`**:
  Re-run the Python installer, choose **Modify**, and make sure **"Add python.exe to PATH"** is checked.
- **PowerShell Script Execution Error (`PSSecurityException`)**:
  Run:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
  Then re-run `.venv\Scripts\Activate.ps1`.
- **Path with Spaces**:
  Always enclose paths in double quotes: `python export_truecolor_ascii_video.py "C:\My Videos\input.mp4"`.

### macOS:
- **`zsh: permission denied: ./run_mac.sh`**:
  Run `chmod +x run_mac.sh` once in Terminal to make it executable.
- **`command not found: python3`**:
  Install Xcode command line tools with `xcode-select --install` or download Python from [python.org](https://www.python.org/).

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
