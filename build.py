"""Build the same desktop application for the current operating system."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BIN_DIR = Path(os.environ.get("FFMPEG_BIN_DIR", "")) if os.environ.get("FFMPEG_BIN_DIR") else None


def find_tool(name):
    filename = name + (".exe" if sys.platform == "win32" else "")
    candidate = BIN_DIR / filename if BIN_DIR else None
    if candidate and candidate.is_file():
        return candidate
    found = shutil.which(filename)
    if found:
        return Path(found)
    raise SystemExit(f"Missing {filename}; install FFmpeg or set FFMPEG_BIN_DIR")


def main():
    if sys.platform not in ("win32", "darwin"):
        raise SystemExit("Desktop packages are built on Windows or macOS")
    separator = os.pathsep
    command = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
        "--windowed", "--onedir", "--name", "AB-Video-Processor",
        "--distpath", str(ROOT / "dist"),
        "--workpath", str(ROOT / "build"),
        "--specpath", str(ROOT / "build"),
    ]
    for name in ("ffmpeg", "ffprobe"):
        command.extend(["--add-binary", f"{find_tool(name)}{separator}bin"])
    command.extend(["--add-data", f"{ROOT / 'LICENSE'}{separator}licenses"])
    command.extend(["--add-data", f"{ROOT / 'THIRD_PARTY_NOTICES.md'}{separator}licenses"])
    ffmpeg_license = find_tool("ffmpeg").parent.parent / "LICENSE"
    if ffmpeg_license.is_file():
        command.extend(["--add-data", f"{ffmpeg_license}{separator}licenses/ffmpeg"])
    icon = ROOT / "assets" / "logo.ico"
    if sys.platform == "win32" and icon.is_file():
        command.extend(["--icon", str(icon)])
    command.append(str(ROOT / "src" / "main.py"))
    subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
