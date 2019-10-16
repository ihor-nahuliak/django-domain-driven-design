from dataclasses import dataclass
from typing import Tuple


@dataclass
class OrderParams:
    by: Tuple[str] = ('id',)
