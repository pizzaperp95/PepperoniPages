# Usage:

Usage of Pepperoni Pages is quite simple.

Examples:

Processing a single file: ```python peppages.py -s page.p2f```
Pepperoni Pages automatically switches to the pages directory, so no need to do that.
it also means that all file paths must be relative to the pages directory.

Processing an entire folder: ``` python peppages.py -b ./```

Argument 1 is the processing type. (batch, single)

Argument 2 is the file path.

## Arguments:

| Argument     | Function                                    |
| ------------ | ------------------------------------------- |
| -b / -batch  | Makes the generator do a batch generation.  |
| -s / -single | Makes the generator do a single generation. |
