import dataclass

@dataclass
class Node:
    id: str
    x: float = 0.0
    y: float = 0.0

@dataclass
class Link:
    id: str
    source: str
    target: str
    cost: float = 0.0
    capacity: float = 0.0

@dataclass
class Demand:
    id: str
    source: str
    target: str


