import typing
import dataclasses


@dataclasses.dataclass
class ScopingParams:
    attrs: typing.Tuple[str]
