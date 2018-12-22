# ase2spine
Script to export a aseprite file as set of png files and a json, to import to Spine.

## Usage
1. Create a source ase file by aseprite.
2. Tag the single frame to export.
3. Run,
```
python ase2spine.py <source ase file> <aseprite tag> <dist dir>
```
4. Import a json in the <dist dir> to Spine.

## Example
```bash
cd ase2spine
mkdir tmp
python ase2spine.py tests/data/4x4.ase Tag tmp
```

## Tested Version
Tested only on Ubuntu.
* aseprite v1.2.9
* Spine 3.7.77 beta