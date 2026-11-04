#!/usr/bin/env python3
"""Create RGB-coloured ASCII characters directly from the original video.

Compatible with macOS, Windows, and Linux.
"""

import argparse
import os
import platform
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CHARS = " .,:;irsXA253hMHGS#9B&@"


def load_font(size=13):
    """Load native monospace font depending on the operating system."""
    system = platform.system()
    candidates = []

    if system == "Darwin":  # macOS
        candidates = [
            "/System/Library/Fonts/Menlo.ttc",
            "/System/Library/Fonts/SFNSMono.ttf",
            "/System/Library/Fonts/Supplemental/Courier New.ttf",
            "/Library/Fonts/Courier New.ttf",
            "Menlo.ttc",
            "Courier New.ttf",
        ]
    elif system == "Windows":  # Windows
        windir = os.environ.get("WINDIR") or os.environ.get("SystemRoot") or r"C:\Windows"
        candidates = [
            os.path.join(windir, "Fonts", "consola.ttf"),
            os.path.join(windir, "Fonts", "lucon.ttf"),
            os.path.join(windir, "Fonts", "cour.ttf"),
            "consola.ttf",
            "cour.ttf",
            "Courier New.ttf",
        ]
    else:  # Linux / Unix
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "DejaVuSansMono.ttf",
        ]

    # Universal fallbacks
    candidates.extend(["Courier New.ttf", "DejaVuSansMono.ttf"])

    for font_path in candidates:
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            continue

    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def get_cell_size(font):
    """Calculate character cell width and height dynamically based on the loaded font."""
    try:
        w = int(round(font.getlength("M")))
        ascent, descent = font.getmetrics()
        h = ascent + descent
        return max(w, 6), max(h, 10)
    except Exception:
        return 9, 16


def render_rgb_ascii(frame_bgr, columns, font, cell_w, cell_h,
                     contrast=1.15, brightness=1.05):
    """Render a single frame as a truecolor ASCII art image."""
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    source = Image.fromarray(rgb)
    rows = max(1, round(columns * source.height / source.width * cell_w / cell_h))
    small = source.resize((columns, rows), Image.Resampling.LANCZOS)
    pixels = np.asarray(small, dtype=np.float32)

    luminance = (
        0.2126 * pixels[:, :, 0]
        + 0.7152 * pixels[:, :, 1]
        + 0.0722 * pixels[:, :, 2]
    )
    luminance = np.clip((luminance - 12.0) * contrast + 12.0, 0, 255)
    luminance = np.clip(luminance * brightness, 0, 255)

    canvas = Image.new("RGB", (columns * cell_w, rows * cell_h), (0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    for y in range(rows):
        for x in range(columns):
            lum = float(luminance[y, x])
            if lum < 16:
                continue
            char_index = min(len(CHARS) - 1, int(lum / 255 * (len(CHARS) - 1)))
            char = CHARS[char_index]

            # Preserve the sampled RGB hue for each individual glyph.
            color = pixels[y, x]
            factor = min(1.35, brightness)
            r, g, b = [int(np.clip(channel * factor, 0, 255)) for channel in color]
            draw.text((x * cell_w, y * cell_h), char, font=font, fill=(r, g, b))

    return canvas


def convert(input_path, output_path, columns=120, fps=10.0,
            contrast=1.15, brightness=1.05):
    """Convert input video to truecolor ASCII video."""
    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            f"Can't find '{input_path}'. Put the video in this folder or pass its filename."
        )

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open the input video: '{input_path}'.")

    source_fps = cap.get(cv2.CAP_PROP_FPS) or fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        cap.release()
        raise RuntimeError("Could not read input video dimensions.")

    font = load_font()
    cell_w, cell_h = get_cell_size(font)
    rows = max(1, round(columns * height / width * cell_w / cell_h))
    output_size = (columns * cell_w, rows * cell_h)

    # Ensure parent directory exists (especially helpful on Windows)
    parent_dir = os.path.dirname(os.path.abspath(output_path))
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    # Cross-platform codec fallbacks (avc1 for QuickTime/macOS/Windows, mp4v, etc.)
    writer = None
    for fourcc_code in ("avc1", "mp4v", "H264", "XVID"):
        try:
            candidate = cv2.VideoWriter(
                output_path, cv2.VideoWriter_fourcc(*fourcc_code), fps, output_size
            )
            if candidate.isOpened():
                writer = candidate
                break
        except Exception:
            continue

    if writer is None or not writer.isOpened():
        cap.release()
        raise RuntimeError(
            f"Could not create output video at '{output_path}'. "
            "Ensure the destination folder is writable and OpenCV video codec is available."
        )

    step = max(1, round(source_fps / fps))
    index = written = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if index % step == 0:
                image = render_rgb_ascii(
                    frame, columns, font, cell_w, cell_h, contrast, brightness
                )
                bgr = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
                writer.write(bgr)
                written += 1
                if written % 25 == 0:
                    print(f"Rendering true-colour frames: {written}", flush=True)
            index += 1
    finally:
        cap.release()
        writer.release()

    if not written:
        raise RuntimeError("No frames were converted.")
    print("\nTrue-colour ASCII video created successfully!")
    print("Output:", os.path.abspath(output_path))
    print(f"Frames: {written}; resolution: {output_size[0]}x{output_size[1]}; cell size: {cell_w}x{cell_h}")


def main():
    parser = argparse.ArgumentParser(
        description="Create RGB-coloured ASCII characters from the original video (macOS & Windows)."
    )
    parser.add_argument("input", nargs="?", default="1.mp4",
                        help="Input video file path (default: 1.mp4)")
    parser.add_argument("-o", "--output", default="truecolor_ascii_output.mp4",
                        help="Output video file path (default: truecolor_ascii_output.mp4)")
    parser.add_argument("--width", type=int, default=120,
                        help="Number of ASCII character columns (default: 120)")
    parser.add_argument("--fps", type=float, default=10.0,
                        help="Target frame rate (default: 10.0)")
    parser.add_argument("--contrast", type=float, default=1.15,
                        help="Contrast factor (default: 1.15)")
    parser.add_argument("--brightness", type=float, default=1.05,
                        help="Brightness factor (default: 1.05)")
    args = parser.parse_args()

    if args.width < 30 or args.fps <= 0 or args.contrast <= 0 or args.brightness <= 0:
        parser.error("width must be >= 30; fps, contrast and brightness must be positive")
    try:
        convert(args.input, args.output, args.width, args.fps,
                args.contrast, args.brightness)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
