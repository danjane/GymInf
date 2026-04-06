from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Desk:
    desk_id: str
    x: float
    y: float
    facing: str = "front"
    group: Optional[str] = None
    row: Optional[int] = None
    seat_index: Optional[int] = None
    enabled: bool = True


@dataclass(frozen=True)
class Layout:
    name: str
    desks: List[Desk]


@dataclass(frozen=True)
class SeatingAssignment:
    desk_id: str
    student: str


@dataclass(frozen=True)
class SeatingPlan:
    course: str
    date: str
    layout_name: str
    assignments: Dict[str, str]
    desk_facings: Dict[str, str] = field(default_factory=dict)
