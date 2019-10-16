from dataclasses import dataclass


@dataclass
class SliceParams:
    offset: int = 0
    limit: int = 128
