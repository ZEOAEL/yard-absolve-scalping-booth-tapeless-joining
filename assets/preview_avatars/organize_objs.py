"""Sort exported avatars into style / rig folders without renaming.

Usage:
  py organize_objs.py "C:\\path\\to\\export\\folder"

Looks for files named:
  R15 Noob.obj
  R6 Bacon.obj
  ...plus .mtl and textures sitting next to them.

Copies them into:
  <this>/Noob/R15 Noob/R15 Noob.obj
  <this>/Bacon/R6 Bacon/R6 Bacon.obj
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

STYLES = [
    "Noob",
    "Bacon",
    "Roblox",
    "Builderman",
    "Telamon",
    "Slender",
    "CNG",
    "Troll",
    "Headless",
    "Template",
]

ROOT = Path(__file__).resolve().parent
MODEL_EXTS = {".glb", ".gltf", ".obj"}
SIDECAR_EXTS = {".bin", ".mtl", ".png", ".jpg", ".jpeg"}
EXTS = MODEL_EXTS | SIDECAR_EXTS


def match_style(stem: str) -> tuple[str, str] | None:
    name = stem.strip()
    for rig in ("R15", "R6"):
        prefix = f"{rig} "
        if not name.lower().startswith(prefix.lower()):
            continue
        style = name[len(prefix) :].strip()
        for known in STYLES:
            if style.lower() == known.lower():
                return rig, known
    return None


def copy_file(src: Path, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"{src.name} -> {dest.relative_to(ROOT)}")
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: py organize_objs.py <export_folder>")
        return 1
    src = Path(sys.argv[1])
    if not src.is_dir():
        print(f"Not a folder: {src}")
        return 1

    copied = 0
    seen_dirs: set[Path] = set()

    for path in src.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in MODEL_EXTS:
            continue
        hit = match_style(path.stem)
        if not hit:
            continue
        rig, style = hit
        dest_dir = ROOT / style / f"{rig} {style}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{rig} {style}{path.suffix.lower()}"
        copy_file(path, dest)
        copied += 1

        folder_key = path.parent.resolve()
        if folder_key in seen_dirs:
            continue
        seen_dirs.add(folder_key)

        for extra in path.parent.iterdir():
            if not extra.is_file() or extra == path:
                continue
            ext = extra.suffix.lower()
            if ext not in SIDECAR_EXTS:
                continue
            extra_hit = match_style(extra.stem)
            if extra_hit and extra_hit != hit:
                continue
            if extra_hit == hit:
                out_name = f"{rig} {style}{ext}"
            else:
                out_name = extra.name
            copy_file(extra, dest_dir / out_name)
            copied += 1

    if copied == 0:
        print("No matching files. Name them like: R15 Noob.obj / R6 Bacon.obj")
        return 1
    print(f"Copied {copied} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
