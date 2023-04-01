"""
Generate a test file with dummy bytes and optional bloat to simulate malware.

Author: Zack Hankin <zth440@uowmail.edu.au>
"""
# !/bin/python3.11
from __future__ import annotations

import os
import random
import string
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Generator

import click
from loguru import logger


def repeat_function(
    func: Callable[..., Any],
    *args: Any,
    repeats: int = 1_000,
    **kwargs: Any,
) -> Generator:
    """
    Run a function n times with given argument and keyword arguments.

    Args:
        func (Callable[[...], ...]): Function to run.
        *args (Any): Positional arguments for the function.
        repeats (int): Number of times to repeat the function call.
        **kwargs (Any): Keyword arguments for the function.

    Returns:
        Generator: With for the function to be called n number of times.

    Yields:
        Any: Result from the function call.
    """
    for _ in range(repeats):
        yield func(*args, **kwargs)


def random_bytes(length: int = 1000) -> bytes:
    """
    Generate random bytes in hex format.

    Args:
        length (int): Length of random hex digits.

    Returns:
        bytes: A byte string of hex digits of a given length.
    """
    program = "".join(
        repeat_function(
            random.choice,
            string.hexdigits,
            repeats=length,
        )
    )
    return b"".fromhex(program)


def write_file(
    path: Path,
    program_start: int = 100_000,
    bloat: int = 100_000,
    program_end: int = 0,
) -> None:
    """
    Writes the hex code for a test file.

    Args:
        path (Path): A file path for the file.
        program_start (int): Length of the "program" code at start of file.
        bloat (int): Length of bloat or no operation bytes '\x00' in the file.
        program_end (int): Length of the "program" code at end of file.

    Returns:
        None
    """
    with open(path, "wb") as f:
        program: bytes = b""
        if program_start:
            program += random_bytes(program_start)
        if bloat:
            program += b"\x00" * bloat
        if program_end:
            program += random_bytes(program_end)
        f.write(program)


@click.command()
@click.option(
    "-f",
    "--filepath",
    type=click.Path(path_type=Path),
    default=Path("./testing/file.out"),
    help="Filepath to save the file. Default = './testing/file.out'",
)
@click.option(
    "-s",
    "--start",
    default=1_000,
    help="Number of hex digits in the simulated program at the start of file.",
)
@click.option(
    "-b",
    "--bloat",
    default=1_000,
    help=(  # fmt: off
        "Number of bloat hex digits or '\x00' (which would be 2) in the file."
    ),  # fmt: on
)
@click.option(
    "-e",
    "--end",
    default=0,
    help="Number of hex digits in the simulated program at the end of file.",
)
def main(filepath: Path, start: int = 1_000, bloat: int = 1_000, end: int = 0):
    """
    Write a file with random bits as the 'program' and optional bloat.
    """
    logger.info(f"Creating file: {filepath.resolve()}")
    write_file(filepath, start, bloat, end)
    size_str: str
    if (size := os.stat(filepath).st_size) < 1_000:
        size_str = f"{size:,.2f} B"
    elif size < (1_000 * 1024):
        size_str = f"{size / 1024:,.2f} KB"
    elif size < (1_000 * 1024**2):
        size_str = f"{size / 1024 ** 2:,.2f} MB"
    else:
        size_str = f"{size / 1024 ** 3:,.2f} GB"
    logger.info(f"File created of size: {size_str}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
