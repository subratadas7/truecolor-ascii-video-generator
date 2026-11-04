# Truecolor ASCII Video Generator 🎬✨

A high-performance Python tool that transforms any video into a vibrant, truecolor (24-bit RGB) ASCII art video. Instead of relying on ANSI terminal escape sequences or pre-rendered text files, it samples original RGB colors directly from the source video cells and dynamically renders anti-aliased monospace glyphs onto a crisp video canvas.

---

## ✨ Features

- **True 24-bit RGB Color**: Each ASCII character preserves the exact sampled RGB color from the source video frame.
- **Accurate Luminance Mapping**: Maps grayscale brightness values to carefully chosen ASCII density glyphs (` .,:;irsXA253hMHGS#9B&@`).
- **Aspect-Ratio Preserving Grid**: Automatically calculates appropriate row heights based on font cell dimensions (`9x16`) so the aspect ratio is never distorted.
- **Contrast & Brightness Controls**: Fine-tune contrast and brightness multipliers to make characters pop against dark backgrounds.
- **Customizable Resolution & FPS**: Adjust column width and target frames-per-second to strike the right balance between file size, conversion speed, and visual fidelity.

---

## 📋 Requirements

- Python 3.9+
- Dependencies listed in `requirements.txt`:
  - `opencv-python`
  - `numpy`
  - `Pillow`

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/subratadas7/Truecolor-ascii-video-genarator.git
   cd Truecolor-ascii-video-genarator
   ```

2. **Create and activate a virtual environment:**
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows:**
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

### Quick Start
Place an input video named `1.mp4` in the project directory, then run:

```bash
python export_truecolor_ascii_video.py
```

The rendered ASCII video will be saved as `truecolor_ascii_output.mp4`.

---

### Custom Input and Output Paths

```bash
python export_truecolor_ascii_video.py input_video.mp4 -o output_ascii.mp4
```

---

### Advanced Examples

- **High-detail wide rendering:**
  ```bash
  python export_truecolor_ascii_video.py input.mp4 --width 160 --contrast 1.25 --brightness 1.15
  ```

- **Smoother motion (higher FPS):**
  ```bash
  python export_truecolor_ascii_video.py input.mp4 --fps 24.0
  ```

- **Compact / low-resolution preview:**
  ```bash
  python export_truecolor_ascii_video.py input.mp4 --width 80 --fps 10.0
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
2. **Downsampling & Resizing**: Resizes each frame to `columns x rows`, where rows are scaled to match the font cell aspect ratio (`9x16`).
3. **Luminance Calculation**: Computes ITU-R BT.709 perceived luminance for each cell:
   $$\text{Luminance} = 0.2126R + 0.7152G + 0.0722B$$
4. **Glyph Selection**: Maps computed luminance to an ASCII character density scale (`CHARS = " .,:;irsXA253hMHGS#9B&@"`).
5. **Truecolor Rendering**: Draws each character onto a black canvas using Pillow with its original RGB color.
6. **Video Encoding**: Writes the rendered frames into an MP4 video stream using OpenCV's `VideoWriter`.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
