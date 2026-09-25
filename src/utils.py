
# A cross platform , dev friendly path resolver respecting absurd run files

import os
import sys
from pathlib import Path

def resourcePath(resourceName:str) -> str:
    BASE_DIR = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).resolve().parent.parent
    resource = BASE_DIR / "assets" / resourceName
    return str(resource)


def dataPath(filename: str) -> str:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
        app_dir = base / "FaceRecon"

    elif sys.platform == "darwin":
        app_dir = Path.home() / "Library" / "Application Support" / "FaceRecon"

    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
        app_dir = base / "FaceRecon"

    app_dir.mkdir(parents=True, exist_ok=True)

    return str(app_dir / filename)

def modelPath(resourceName:str) -> str:
    BASE_DIR = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).resolve().parent.parent
    resource = BASE_DIR / "model" / resourceName
    return str(resource)
