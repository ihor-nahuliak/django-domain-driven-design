import dataclasses
from typing import Optional


@dataclasses.dataclass
class SlicingParams:
    offset: Optional[int] = 0
    limit: Optional[int] = None
