"""Batch: Studio OBJ -> Blender -> GLB into preview_avatars folders.

Keeps file names (R15 Noob.obj -> Noob/R15 Noob.glb)
and object names (Head, Torso, ...) as glTF nodes.

Usage:
  blender --background --python batch_blender_glb.py -- --input "C:\\rbx_exports" --output "C:\\Users\\puref\\source\\repos\\Smashed\\Smashed\\assets\\preview_avatars"
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
                return dest_dir / f"{rig} {known}.glb"
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


def export_glb(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    kwargs = {
        "filepath": str(path),
        "export_format": "GLB",
        "use_selection": False,
        "export_texcoords": True,
        "export_normals": True,
        "export_materials": "EXPORT",
        "export_cameras": False,
        "export_extras": True,
        "export_apply": True,
        "export_animations": False,
        "export_skins": False,
        "export_yup": True,
        "export_image_format": "AUTO",
        "export_draco_mesh_compression_enable": False,
    }
    op = bpy.ops.export_scene.gltf
    rna = op.get_rna_type() if hasattr(op, "get_rna_type") else None
    if rna is not None:
        allowed = {p.identifier for p in rna.properties}
        kwargs = {k: v for k, v in kwargs.items() if k in allowed}
    op(**kwargs)


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
        export_glb(dest)
        print(f"{path.name} -> {dest}")


if __name__ == "__main__":
    main()
