# True-colour ASCII exporter

This version samples original RGB color from every source-video cell and draws
each ASCII character in that sampled color. It does not rely on ANSI color codes
or pre-existing ASCII text files.

## macOS

The default input filename is `1.mp4`.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python export_truecolor_ascii_video.py
```

Output: `truecolor_ascii_output.mp4`

For a differently named video:

```bash
python export_truecolor_ascii_video.py my_video.mp4
```

For more detail and a slightly brighter result:

```bash
python export_truecolor_ascii_video.py 1.mp4 --width 140 --contrast 1.2 --brightness 1.1
```
