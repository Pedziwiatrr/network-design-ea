import re
from .models import Network, Node, Link, Demand

class SNDlibLoader:
    @staticmethod
    def load(file_path: str) -> Network:
        """
        Function to parse data from .txt in SNDlib native format
        """
        network = Network()
        current_section = None
        current_demand_id = None

        # Regex definitions
        node_pattern = re.compile(r'(\S+)\s*\(\s*([\d\.]+)\s+([\d\.]+)\s*\)')
        link_pattern = re.compile(r'(\S+)\s*\(\s*(\S+)\s+(\S+)\s*\)')
        demand_pattern = re.compile(r'(\S+)\s*\(\s*(\S+)\s+(\S+)\s*\)\s+\d+\s+([\d\.]+)')
        path_pattern = re.compile(r'(P_\d+)\s*\((.*)\)')

        with open(file_path, 'r') as fh:
            for line in fh:
                line = line.strip()

                # Section loading
                if not line or line.startswith('#'):
                    continue
                if line.startswith('NODES'):
                    current_section = 'NODES'
                    continue
                elif line.startswith('LINKS'):
                    current_section = 'LINKS'
                    continue
                elif line.startswith('DEMANDS'):
                    current_section = 'DEMANDS'
                    continue
                elif line.startswith('ADMISSIBLE_PATHS'):
                    current_section = 'PATHS'
                    continue
                elif line == ')':
                    if current_section == 'PATHS' and current_demand_id:
                        current_demand_id = None
                    continue
                elif line == '(':
                    continue

                # Parsing data depending on section
                if current_section == 'NODES':
                    match = node_pattern.search(line)
                    if match:
                        node_id = match.group(1)
                        x = float(match.group(2))
                        y = float(match.group(3))
                        network.add_node(Node(id=node_id, x=x, y = y))
                elif current_section == 'LINKS':
                    match = link_pattern.search(line)
                    if match:
                        link_id = match.group(1)
                        src = match.group(2)
                        trg = match.group(3)
                        parts = line.split()
                        cost = float(parts[8])
                        network.add_link(Link(id=link_id, source=src, target=trg, cost=cost))
                elif current_section == 'DEMANDS':
                    match = demand_pattern.search(line)
                    if match:
                        demand_id = match.group(1)
                        src = match.group(2)
                        trg = match.group(3)
                        val = float(match.group(4))
                        network.add_demand(Demand(id=demand_id, source=src, target=trg, value=val))
                elif current_section == 'PATHS':
                    if line.startswith('Demand_'):
                        parts = line.split()
                        current_demand_id = parts[0]
                    elif line.startswith('P_') and current_demand_id:
                        match = path_pattern.search(line)
                        if match:
                            links_str = match.group(2)
                            links_list = links_str.strip().split()
                            if current_demand_id in network.demands:
                                network.demands[current_demand_id].admissable_paths.append(links_list)

        return network