# ttt2 release prep script

This script updates the following files in the ttt2 codebase to prepare for a release:

- `CHANGELOG.md` (idempotent)
- `gamemodes/terrortown/gamemode/shared/sh_init.lua` (idempotent)
- `gamemodes/terrortown/gamemode/client/cl_changes.lua` (**not** idempotent)

## Usage

Before running this make sure you have all needed requirements installed:

```shell
pip install -r requirements.txt
```

```shell
usage: releaseprep.py [-h] [--ttt2repo TTT2REPO] version

Prepare TTT2 files for a release.

positional arguments:
  version              The new version string. e.g. '0.13.1b'.

options:
  -h, --help           show this help message and exit
  --ttt2repo TTT2REPO  Base path to the ttt2 repo.
```
