# Desktop builds

The same PyQt5 source builds on Windows and macOS. Each package includes `ffmpeg` and `ffprobe`; users do not need Python or FFmpeg installed.

## Local build

Install Python 3.11, FFmpeg and FFprobe for the current platform, then run:

```text
python -m venv .venv
python -m pip install -r requirements-build.txt
python build.py
```

Use the virtual environment's `python` for the last two commands. If the FFmpeg programs are not on `PATH`, set `FFMPEG_BIN_DIR` to the folder containing both programs. The output is `dist/AB-Video-Processor` on Windows and `dist/AB-Video-Processor.app` on macOS.

## Automated builds

Run **Build desktop packages** from GitHub Actions or push a `v*` tag. The workflow produces a Windows ZIP and macOS DMGs for Apple Silicon and Intel. A macOS build must run on macOS. The DMGs are unsigned; public distribution requires Apple code signing and notarization with the publisher's credentials.

FFmpeg is distributed under its own license. Review the license of the selected FFmpeg build before publishing packages, and include its required license and source notices.
