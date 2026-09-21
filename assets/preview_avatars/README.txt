Preview avatars
===============

The menu loads GLB first, then OBJ. With textures, use a folder per rig:

  assets/preview_avatars/<Style>/<R15|R6> <Style>/<R15|R6> <Style>.obj
  + the .mtl and pngs next to that .obj

Example:

  Bacon/R6 Bacon/R6 Bacon.obj
  Bacon/R6 Bacon/R6 Bacon.mtl
  Bacon/R6 Bacon/*.png
  Bacon/R15 Bacon/R15 Bacon.obj
  Noob/R15 Noob/R15 Noob.obj

Styles: Noob, Bacon, Roblox, Builderman, Telamon, Slender, CNG, Troll, Headless, Template

Keep the file name EXACTLY:  R15 Noob.glb  /  R6 Roblox.glb
Do not rename objects inside the file (Head, Torso, ...). Those names travel
Studio -> OBJ -> Blender Outliner -> GLB nodes.

============================================================
STEP BY STEP: Studio OBJ -> Blender -> GLB -> this folder
============================================================

0. Names first (do this in Studio BEFORE export)
-----------------------------------------------
Put each character in its own Model and name the Model exactly:

  R15 Noob
  R6 Noob
  R15 Bacon
  R6 Bacon
  R15 Roblox
  R6 Roblox
  R15 Builderman
  R6 Builderman
  R15 Telamon
  R6 Telamon
  R15 Slender
  R6 Slender
  R15 CNG
  R6 CNG
  R15 Troll
  R6 Troll
  R15 Headless
  R6 Headless
  R15 Template
  R6 Template

Limb / accessory names (Head, Torso, Left Arm, ...) can stay as they are.
Do NOT join parts into one mesh in Studio.

1. Export OBJ from Roblox Studio
--------------------------------
For each Model:

  1. Click the Model in Explorer (the one named "R15 Noob", etc.).
  2. File -> Export Selection
     If you do not see that: File -> Export -> Wavefront (*.obj)
     Some Studio builds put it under File -> Advanced -> Export as Obj.
  3. Save into one folder, e.g.  C:\rbx_exports
  4. Use the Model name as the file name:  R15 Noob.obj
  5. If Studio asks about textures, export them too. Keep the .mtl and any
     .png/.jpg NEXT TO the .obj. Do not rename those either.

Repeat until you have all 20 (10 styles x R15 + R6).

2. Import that OBJ into Blender (one character at a time)
---------------------------------------------------------
  1. Open Blender. File -> New -> General.
  2. Select the default cube, light, and camera. Press X -> Delete.
  3. File -> Import -> Wavefront (.obj)
  4. Click the .obj (example: R15 Noob.obj).
  5. In the import panel on the RIGHT of the file window, set:

       Transform
         Forward Axis = -Z
         Up Axis      = Y

       Geometry
         Split by Object = ON
         Split by Groups = ON
         Validate Meshes = ON

  6. Click Import OBJ.

Check the Outliner (top-right). You should see separate objects:
Head, Torso, Left Arm, ...  Those are the Roblox names.

DO NOT:
  - Press Ctrl+J / Join
  - Rename anything in the Outliner
  - Rotate the character "to stand up" if they already look upright
  - Apply a Scale of 0

If they are lying on their side, undo and re-import with Up Axis = Z.
Do not hand-rotate unless the second import still looks wrong.

Optional cleanup (safe):
  - Select all (A), then Ctrl+A -> All Transforms
    This bakes location/rotation/scale without renaming.

3. Export GLB from Blender
--------------------------
  1. File -> Export -> glTF 2.0 (.glb/.gltf)
  2. Bottom-right export settings:

       Format = glTF Binary (.glb)

       Include
         Limit to Selected Objects = OFF
         (you want the whole character)

       Transform
         +Y Up = ON   (if your Blender version still shows this)

       Data -> Mesh
         UVs     = ON
         Normals = ON

       Data -> Material
         Materials = Export
         Images    = Automatic     (embeds PNG/JPEG in the GLB)
         Do NOT enable Draco mesh compression

       Data -> Animation
         Animation = OFF
         Skinning  = OFF   (skip for now)

  3. File name MUST match the original:
       R15 Noob.glb
       R6 Roblox.glb
       ...
  4. Click Export glTF 2.0.

One .glb is enough. You do not need the .obj / .mtl next to it after this.

4. Put the GLB in the matching folder
-------------------------------------
Copy each file here:

  Smashed\Smashed\assets\preview_avatars\<Style>\<file>

Examples:

  ...\preview_avatars\Noob\R15 Noob.glb
  ...\preview_avatars\Noob\R6 Noob.glb
  ...\preview_avatars\Bacon\R15 Bacon.glb
  ...\preview_avatars\Roblox\R6 Roblox.glb
  ...\preview_avatars\CNG\R15 CNG.glb

Or dump every GLB into one folder and run:

  py organize_objs.py "C:\rbx_exports"

That copies any file named "R15 Noob.glb" / "R6 Roblox.glb" into the
right style folder without renaming.

5. Load it in Smashed
---------------------
Rebuild (post-build copies assets into build\assets), then in Visuals:

  Rig   = R15 or R6
  Style = Noob / Bacon / ...

If the GLB is missing, the built-in noob dummy is shown instead.
A .glb in the slot is preferred over a leftover .obj.

============================================================
Mass convert in Blender (all OBJs at once)
============================================================
After Studio export, from a terminal:

  blender --background --python batch_blender_glb.py -- --input "C:\rbx_exports" --output "C:\Users\puref\source\repos\Smashed\Smashed\assets\preview_avatars"

That imports each OBJ with the settings above and writes:

  Noob/R15 Noob.glb
  Roblox/R6 Roblox.glb
  ...

Object names inside the file are kept. File names are kept.

============================================================
Name-loss checklist
============================================================
Names die if you:
  - Join meshes in Studio or Blender
  - Export OBJ as one object
  - Type a new name in the Blender export box (R15Noob.glb, noob.glb, ...)
  - Export glTF Separate (.gltf + .bin + textures) and then rename pieces

Names live if you:
  - Name the Studio Model  R15 Noob
  - Import OBJ with Split by Object / Split by Groups ON
  - Leave Outliner names alone
  - Export glTF Binary (.glb) with that same file name
