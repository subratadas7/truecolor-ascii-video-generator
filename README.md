# Truecolor ASCII Video Generator 🎬✨

A high-performance Python tool that transforms any video into a vibrant, truecolor (24-bit RGB) ASCII art video. Instead of relying on ANSI terminal escape sequences or pre-rendered text files, it samples original RGB colors directly from the source video cells and dynamically renders anti-aliased monospace glyphs onto a crisp video canvas.

Supports **Windows**, **macOS**, and **Linux** out of the box.

---

## ✨ Features

- **True 24-bit RGB Color**: Each ASCII character preserves the exact sampled RGB color from the source video frame.
- **Cross-Platform Font Auto-Detection**: Automatically detects native monospace fonts:
  - **Windows**: `Consolas`, `Lucida Console`, `Courier New`
  - **macOS**: `Menlo`, `Courier New`
  - **Linux**: `DejaVu Sans Mono`, `Liberation Mono`
- **Accurate Luminance Mapping**: Maps grayscale brightness values to carefully chosen ASCII density glyphs (` .,:;irsXA253hMHGS#9B&@`).
- **Aspect-Ratio Preserving Grid**: Automatically calculates appropriate row heights based on font cell dimensions (`9x16`) so the aspect ratio is never distorted.
- **Contrast & Brightness Controls**: Fine-tune contrast and brightness multipliers to make characters pop against dark backgrounds.
- **Customizable Resolution & FPS**: Adjust column width and target frames-per-second to strike the right balance between conversion speed and visual fidelity.

---

## 📋 Prerequisites

- **Python 3.9 or higher**
  - **Windows Users**: When installing Python from [python.org](https://www.python.org/downloads/), check the box **"Add python.exe to PATH"** on the first installer screen.

---

## 🚀 Installation & Setup

### 🪟 Windows Setup

#### Option A: One-Click Auto Runner (`run_windows.bat` - Easiest)
Double-click **`run_windows.bat`**!
- It automatically detects Python, sets up `.venv`, installs requirements, and converts `1.mp4`.
- **Drag & Drop**: You can also drag and drop any video file directly onto `run_windows.bat` to convert it instantly without opening a terminal!

#### Option B: Using PowerShell (Manual)
```powershell
# 1. Clone the repository
git clone https://github.com/subratadas7/Truecolor-ascii-video-genarator.git
cd Truecolor-ascii-video-genarator

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate the virtual environment
.venv\Scripts\Activate.ps1

# Note: If PowerShell shows an execution policy error, run:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# and then re-run: .venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt
```

#### Option C: Using Command Prompt (CMD)
```cmd
:: 1. Clone the repository
git clone https://github.com/subratadas7/Truecolor-ascii-video-genarator.git
cd Truecolor-ascii-video-genarator

:: 2. Create a virtual environment
python -m venv .venv

:: 3. Activate the virtual environment
.venv\Scripts\activate.bat

:: 4. Install dependencies
pip install -r requirements.txt
```

---

### 🍎 macOS & 🐧 Linux Setup

```bash
# 1. Clone the repository
git clone https://github.com/subratadas7/Truecolor-ascii-video-genarator.git
cd Truecolor-ascii-video-genarator

# 2. Create a virtual environment
python3 -m venv .venv

# 3. Activate the virtual environment
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 💻 Usage

### Quick Start
Place an input video named `1.mp4` in the project directory, then run:

- **Windows:**
  ```cmd
  python export_truecolor_ascii_video.py
  ```
- **macOS / Linux:**
  ```bash
  python export_truecolor_ascii_video.py
  ```

The rendered ASCII video will be saved as `truecolor_ascii_output.mp4`.

---

### Custom Input and Output Paths

```bash
python export_truecolor_ascii_video.py my_video.mp4 -o my_output.mp4
```

> **Tip for Windows**: If your video path contains spaces, wrap it in double quotes:
> ```powershell
> python export_truecolor_ascii_video.py "C:\Users\YourName\Videos\input video.mp4" -o "output.mp4"
> ```

---

### Advanced Examples

- **High-detail wide rendering:**
  ```bash
  python export_truecolor_ascii_video.py 1.mp4 --width 160 --contrast 1.25 --brightness 1.15
  ```

- **Smoother motion (higher FPS):**
  ```bash
  python export_truecolor_ascii_video.py 1.mp4 --fps 24.0
  ```

- **Compact / quick preview:**
  ```bash
  python export_truecolor_ascii_video.py 1.mp4 --width 80 --fps 10.0
  ```

---

## ⚙️ CLI Options & Arguments

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input` | `str` | `1.mp4` | Path to the source input video file. |
| `-o`, `--output` | `str` | `truecolor_ascii_output.mp4` | Destination path for the converted MP4 video. |
| `--width` | `int` | `120` | Number of ASCII character columns across the frame (min: `30`). |
| `--fps` | `float` | `10.0` | Output video framerate in frames per second. |
| `--contrast` | `float` | `1.15` | Contrast enhancement factor applied to luminance values. |
| `--brightness` | `float` | `1.05` | Brightness multiplier for glyph colors and thresholding. |

---

## 🔍 How It Works

1. **Frame Extraction**: Reads frames from the source video using OpenCV.
2. **Downsampling & Resizing**: Resizes each frame to `columns x rows`, scaling rows based on the font cell aspect ratio (`9x16`).
3. **Luminance Calculation**: Computes ITU-R BT.709 perceived luminance for each cell:
   $$\text{Luminance} = 0.2126R + 0.7152G + 0.0722B$$
4. **Glyph Selection**: Maps computed luminance to an ASCII character density scale (`CHARS = " .,:;irsXA253hMHGS#9B&@"`).
5. **Truecolor Rendering**: Draws each character onto a black canvas using Pillow with its original RGB color using the system's native monospace font.
6. **Video Encoding**: Encodes the rendered frames into an MP4 video stream using OpenCV's `VideoWriter`.

---

## 🛠️ Windows Troubleshooting

- **`'python' is not recognized as an internal or external command`**:
  Make sure you checked "Add python.exe to PATH" when installing Python. You can also re-run the Python installer and choose **Modify** to check the box.
- **PowerShell Script Execution Error (`PSSecurityException`)**:
  Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in your PowerShell window and try activating the `.venv` again.
- **Missing Codec Warning**:
  OpenCV uses the standard `mp4v` codec which is natively supported on Windows Media Player, Movies & TV, VLC, and modern browsers.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
