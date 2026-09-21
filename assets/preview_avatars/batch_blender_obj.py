"""Batch import/export OBJ in Blender without renaming files or objects.

Usage (from a terminal):
  blender --background --python batch_blender_obj.py -- --input "C:\\exports" --output "C:\\Users\\puref\\source\\repos\\Smashed\\Smashed\\assets\\preview_avatars"

Keeps:
  - File names (R15 Noob.obj stays R15 Noob.obj)
  - Object names inside the OBJ (`o Head`, `o Torso`, ...)
"""

from __future__ import annotations

import sys
from pathlib import Path

import bpy

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


def parse_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1 :]
    else:
        argv = []
    inp = None
    out = None
    i = 0
    while i < len(argv):
        if argv[i] == "--input" and i + 1 < len(argv):
            inp = Path(argv[i + 1])
            i += 2
            continue
        if argv[i] == "--output" and i + 1 < len(argv):
            out = Path(argv[i + 1])
            i += 2
            continue
        i += 1
    if inp is None or out is None:
        raise SystemExit("Need --input <folder> --output <preview_avatars folder>")
    return inp, out


def match_dest(stem: str, out_root: Path) -> Path | None:
    for rig in ("R15", "R6"):
        prefix = f"{rig} "
        if not stem.lower().startswith(prefix.lower()):
            continue
        style = stem[len(prefix) :].strip()
        for known in STYLES:
            if style.lower() == known.lower():
                dest_dir = out_root / known / f"{rig} {known}"
                dest_dir.mkdir(parents=True, exist_ok=True)
                return dest_dir / f"{rig} {known}.obj"
    return None


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_obj(path: Path):
    if hasattr(bpy.ops.wm, "obj_import"):
        bpy.ops.wm.obj_import(
            filepath=str(path),
            forward_axis="NEGATIVE_Z",
            up_axis="Y",
        )
        return
    bpy.ops.import_scene.obj(
        filepath=str(path),
        use_split_objects=True,
        use_split_groups=True,
        use_image_search=True,
        axis_forward="-Z",
        axis_up="Y",
    )


def export_obj(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(bpy.ops.wm, "obj_export"):
        bpy.ops.wm.obj_export(
            filepath=str(path),
            export_selected_objects=False,
            export_uv=True,
            export_normals=True,
            export_materials=True,
            export_triangulated_mesh=False,
            forward_axis="NEGATIVE_Z",
            up_axis="Y",
        )
        return
    bpy.ops.export_scene.obj(
        filepath=str(path),
        use_selection=False,
        use_materials=True,
        use_triangles=False,
        use_blen_objects=True,
        group_by_object=True,
        group_by_group=True,
        keep_vertex_order=True,
        axis_forward="-Z",
        axis_up="Y",
    )


def main():
    src, dest_root = parse_args()
    files = [p for p in src.rglob("*.obj") if p.is_file()]
    if not files:
        raise SystemExit(f"No OBJ files in {src}")
    for path in files:
        dest = match_dest(path.stem, dest_root)
        if dest is None:
            print("skip (name must be like 'R15 Noob'):", path.name)
            continue
        reset_scene()
        import_obj(path)
        export_obj(dest)
        print(f"{path.name} -> {dest}")


if __name__ == "__main__":
    main()
