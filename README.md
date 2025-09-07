# Pepperoni Pages

## usage:

First: CD into the /source folder containing peppages.py.

Processing a single file: ```python peppages.py -s page.p2f```
Pepperoni Pages automatically switches to the pages directory, so no need to do that.
it also means that all file paths must be relative to the pages directory.

Processing an entire folder: ``` python peppages.py -b ./```

## Setup:

Extract the latest release into whatever folder you please, then put any pages/templates you want to generate into their respective folders.

### Requirements:
**Python 3.13 or greater.**

**Markdown**

(requirements.txt coming soon)

## Documentation:

[Writing Pages](docs/p2f.md)

[Writing Templates](docs/templates.md)

[More usage](docs/usage.md)

Examples may be found in [examples.](examples)

## Planned features:

Metadata templates; Acts like page templates, but has site metadata inside instead. A default can be set per page template.

Last updated variables; This allows you to put a tag anywhere which the site generator replaces with the date and/or time of the last update to the page.
