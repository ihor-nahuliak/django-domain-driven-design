import dataclasses


@dataclasses.dataclass
class SlicingParams:
    offset: int = 0
    limit: int = 128
