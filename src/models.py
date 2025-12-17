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
    value: float
    allowed_paths: List[List[str]] = field(default_factory=list)

@dataclass
class Network:
    nodes:

@dataclass
class Network:
    nodes: dict[str, Node] = field(default_factory=dict)
    links: dict[str, Link] = field(default_factory=dict)
    demands: dict[str, Demand] = field(default_factory=dict)

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def add_link(self, link: Link):
        self.links[link.id] = link

    def add_demand(self, demand: Demand):
        self.demands[demand.id] = demand