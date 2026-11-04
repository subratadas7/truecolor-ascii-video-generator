#!/usr/bin/env python3
"""Create RGB-coloured ASCII characters directly from the original video."""

import argparse
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CHARS = " .,:;irsXA253hMHGS#9B&@"
CELL_W, CELL_H = 9, 16


def load_font(size=13):
    for path in (
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
    ):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
    return ImageFont.load_default()


def render_rgb_ascii(frame_bgr, columns, font, contrast=1.15, brightness=1.05):
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    source = Image.fromarray(rgb)
    rows = max(1, round(columns * source.height / source.width * CELL_W / CELL_H))
    small = source.resize((columns, rows), Image.Resampling.LANCZOS)
    pixels = np.asarray(small, dtype=np.float32)

    luminance = (
        0.2126 * pixels[:, :, 0]
        + 0.7152 * pixels[:, :, 1]
        + 0.0722 * pixels[:, :, 2]
    )
    luminance = np.clip((luminance - 12.0) * contrast + 12.0, 0, 255)
    luminance = np.clip(luminance * brightness, 0, 255)

    canvas = Image.new("RGB", (columns * CELL_W, rows * CELL_H), (0, 0, 0))
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
            draw.text((x * CELL_W, y * CELL_H), char, font=font, fill=(r, g, b))

    return canvas


def convert(input_path, output_path, columns=120, fps=10.0,
            contrast=1.15, brightness=1.05):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            f"Can't find '{input_path}'. Put the video in this folder or pass its filename."
        )

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError("Could not open the input video.")

    source_fps = cap.get(cv2.CAP_PROP_FPS) or fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        cap.release()
        raise RuntimeError("Could not read input video dimensions.")

    rows = max(1, round(columns * height / width * CELL_W / CELL_H))
    output_size = (columns * CELL_W, rows * CELL_H)
    writer = cv2.VideoWriter(
        output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, output_size
    )
    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Could not create output MP4.")

    step = max(1, round(source_fps / fps))
    font = load_font()
    index = written = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if index % step == 0:
                image = render_rgb_ascii(frame, columns, font, contrast, brightness)
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
    print("\\nTrue-colour ASCII video created!")
    print("Output:", os.path.abspath(output_path))
    print(f"Frames: {written}; resolution: {output_size[0]}x{output_size[1]}")


def main():
    parser = argparse.ArgumentParser(
        description="Create RGB-coloured ASCII characters from the original video."
    )
    parser.add_argument("input", nargs="?", default="1.mp4")
    parser.add_argument("-o", "--output", default="truecolor_ascii_output.mp4")
    parser.add_argument("--width", type=int, default=120)
    parser.add_argument("--fps", type=float, default=10.0)
    parser.add_argument("--contrast", type=float, default=1.15)
    parser.add_argument("--brightness", type=float, default=1.05)
    args = parser.parse_args()

    if args.width < 30 or args.fps <= 0 or args.contrast <= 0 or args.brightness <= 0:
        parser.error("width must be >=30; fps, contrast and brightness must be positive")
    try:
        convert(args.input, args.output, args.width, args.fps,
                args.contrast, args.brightness)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
