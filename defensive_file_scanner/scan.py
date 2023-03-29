#!/bin/python3.11
from __future__ import annotations

from collections import Counter
from pathlib import Path
from pathlib import PurePath

import click
from icecream import ic
from loguru import logger


@click.command()
@click.argument(
    "file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=False,
)
def main(file: Path):
    malware = Malware(file)


class Malware:
    def __init__(self, file: PurePath):
        self.file: PurePath = file
        self.counter = Counter()
        logger.info(f'Initiating Scan of file: {file}')
        logger.debug(repr(self))
        self.test_whole_file()
        ic(self.most_common)
        ic(self.total_bits)
        ic(self.ratio)

    def __str__(self):
        return f"file='{self.file}'"

    def __repr__(self):
        return f'{type(self).__name__}({str(self)})'

    def test_whole_file(self) -> tuple[bytes, int]:
        with open(self.file, 'rb', buffering=1024) as f:
            # todo: add tqdm loading bar.
            while True:
                if not (line := f.read(100)):
                    break
                self.counter.update(line)
        logger.success(f'Most common bit: {self.counter.most_common(1)[0]}')
        return self.counter.most_common(1)[0]

    @property
    def most_common(self):
        if self.counter:
            return self.counter.most_common(1)[0]
        return self.test_whole_file()

    @property
    def total_bits(self):
        return self.counter.total()

    @property
    def ratio(self):
        return self.most_common[1] / self.total_bits

    @property
    def file_hash(self) -> str:
        ...

    def sum_of_bit(self) -> int:
        ...


if __name__ == "__main__":
    raise SystemExit(main())
