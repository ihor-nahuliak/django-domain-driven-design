import typing
import dataclasses


@dataclasses.dataclass
class SortingParams:
    by: typing.Tuple[str, ...]
