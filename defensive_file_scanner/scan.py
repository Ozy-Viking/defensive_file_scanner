#!/bin/python3.11
from __future__ import annotations

from collections import Counter
from pathlib import Path
from pathlib import PurePath

import click
from loguru import logger


@click.command()
@click.argument(
    "file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=False,
)
def main(file: Path):
    malware = Malware(file)
    logger.info(malware)


class Malware:
    """
    Malware Object
    """

    def __init__(self, file: PurePath | str):
        """
        Initialise a suspected Malware Object.

        Args:
            file (PurePath | str): Path of the file to scan.
        """
        self.file: PurePath = Path(file)
        self.counter: Counter = Counter()
        logger.info(f"Initiating Scan of file: {file}")
        logger.debug(repr(self))

    def __str__(self):
        return f"file='{self.file}'"

    def __repr__(self):
        return f"{type(self).__name__}({str(self)})"

    def test_whole_file(self) -> list[tuple[str, int]]:
        """
        Scans the whole file and counts the hexbits.

        Returns:
            The count of the hex in the byte code ordered from most
            to least common.

        Todo:
            - [ ] Add tqdm loading bar.
        """
        with open(self.file, "rb", buffering=1024) as f:
            while True:
                if not (line := f.read(100)):
                    break
                self.counter.update(line)
        logger.success(f"Most common bit: {self.counter.most_common(1)[0]}")
        return self.counter.most_common()

    @property
    def most_common(self) -> tuple[str, int]:
        """
        The most come hex bit and frequency.
        """
        if self.counter:
            return self.counter.most_common(1)[0]
        return self.test_whole_file()[0]

    @property
    def total_bits(self) -> int:
        """
        The total number if hex bits.
        """
        return self.counter.total()

    @property
    def ratio(self):
        """
        Ratio between most common count and total count.
        """
        return self.most_common[1] / self.total_bits

    @property
    def file_hash(self) -> str:
        raise NotImplementedError

    def sum_of_bit(self) -> int:
        raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
