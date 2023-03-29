#!/bin/python3.11
from __future__ import annotations

import click

from .create_file import main as create
from .scan import main as scan


@click.group(commands={"create": create})
def main():
    ...


main.add_command(scan)

if __name__ == "__main__":
    raise SystemExit(main())
