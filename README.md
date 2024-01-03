# Spritesheet Generator

Generate spritesheets by single images inside subfolders.

## Base Usage
```bash
$ python spritesheet.py <input directory>
```

### Example:
Considering the following folder structure:
```bash
\---swordsman
    +---idle
    |       Swordsman_steady_00.png
    |       Swordsman_steady_01.png
    |       ...
    +---jump
    |       Swordsman_jump_000.png
    |       Swordsman_jump_001.png
    |       ...
    \---walk
            Swordsman_walk_00.png
            Swordsman_walk_01.png
            ...
```

The base command will generate the following:
```bash
$ python spritesheet.py swordsman

\---swordsman
    ...
    \---output
            swordsman-idle.png
            swordsman-jump.png
            swordsman-walk.png
```

## Advanced Usage
- `imagesPerRow`: How many images (or sprites) it will join per row. 
  - Default: `5`

  Example: <br />
  ```bash
  # Generate spritesheets with 10 sprites per row
  $ python spritesheet.py --imagesPerRow 10 swordsman
  # or
  $ python spritesheet.py -i 10 swordsman
  ```
- `only`: Only generate spritesheets for specific subfolders. Comma separated.
  - Default: `None` (will generate spritesheets for all subfolders)

  Example: <br />
  ```bash
  # Only generate idle and walk spritesheets
  $ python spritesheet.py --only idle,walk swordsman
  # or
  $ python spritesheet.py -o idle,walk swordsman
  ```
- `generateFullSpritesheet`: Generate a full spritesheet with all previously generated spritesheets in a single file
  - Default: `False`

  Example: <br />
  ```bash
  # Generate full spritesheet
  $ python spritesheet.py --generateFullSpritesheet swordsman
  # or
  $ python spritesheet.py -g swordsman
  ```