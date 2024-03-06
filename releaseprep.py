#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime
from markdown import markdown
from jinja2 import Environment, FileSystemLoader

changelog = "CHANGELOG.md"
shinit = "gamemodes/terrortown/gamemode/shared/sh_init.lua"
clchanges = "gamemodes/terrortown/gamemode/client/cl_changes.lua"


def main():
    parser = ArgumentParser(description="Prepare TTT2 files for a release.")
    parser.add_argument(
        "--ttt2repo",
        default="",
        help="Base path to the ttt2 repo.",
        type=Path,
    )
    parser.add_argument(
        "version",
        help="The new version string. e.g. '0.13.1b'.",
    )
    args = parser.parse_args()
    args.version = args.version.replace("v", "")

    updateShInit(args.ttt2repo.joinpath(shinit), args.version)
    updateChangelog(args.ttt2repo.joinpath(changelog), args.version)
    updateClChanges(
        args.ttt2repo.joinpath(changelog),
        args.ttt2repo.joinpath(clchanges),
        args.version,
    )


def updateChangelog(changelogpath, version):
    with open(changelogpath, "r") as f:
        lines = []
        for line in f:
            if "## Unreleased" in line:
                lines += line
                lines += "\n"
                lines += (
                    "## [v"
                    + version
                    + "](https://github.com/TTT-2/TTT2/tree/"
                    + version
                    + ") ("
                    + datetime.now().strftime("%Y-%m-%d")
                    + ")\n"
                )
            elif "## [v" + version in line:
                # Idempotency: Remove version line (by not adding) and the empty line before
                lines.pop()
            else:
                lines += line

    with open(changelogpath, "w") as f:
        f.writelines(lines)


def updateShInit(path: Path, version: str):
    with open(path, "r") as f:
        lines = ""
        for line in f:
            if "GM.Version" in line:
                lines += 'GM.Version = "' + version + '"\n'
            else:
                lines += line

    with open(path, "w") as f:
        f.writelines(lines)


def updateClChanges(changelogpath, clchangespath, version):
    with open(changelogpath, "r") as f:
        copy = False
        lines = ""
        for line in f:
            if "## [v" + version in line:
                copy = True
                continue
            elif "## [v" in line:
                break
            elif copy:
                lines += line

    html = markdown(lines, tab_length=2)
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("cl_changes.j2")
    rendered = template.render(
        version=version,
        html=html,
        year=datetime.now().strftime("%Y"),
        month=datetime.now().strftime("%m"),
        day=datetime.now().strftime("%d"),
    )

    with open(clchangespath, "r") as f:
        lines = ""
        for line in f:
            if "--#endofchanges" in line:
                lines += rendered
                lines += "\n\n"
                lines += line
            else:
                lines += line

    with open(clchangespath, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    main()
