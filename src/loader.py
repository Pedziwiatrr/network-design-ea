import xml.etree.ElementTree as ET
from models import Network, Node, Link, Demand

class SNDlibLoader:
    @staticmethod
    def load(file_path: str) -> Network:
        network = Network()
        tree = ET.parse(file_path)
        root = tree.getroot()

        node_pattern = re.compile(r'(\S+)\s*\(\s*([\d\.]+)\s+([\d\.]+)\s*\)')
        link_pattern = re.compile(r'(\S+)\s*\(\s*(\S+)\s+(\S+)\s*\)')
        demand_pattern = re.compile(r'(\S+)\s*\(\s*(\S+)\s+(\S+)\s*\)\s+\d+\s+([\d\.]+)')
        path_pattern = re.compile(r'(P_\d+)\s*\((.*)\)')

        with open(file_path, 'r') as fh:
            for line in fh:
                line = line.strip()
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
                        current_demand_id = node_pattern
                    continue
                elif line == '(':
                    continue

                #TODO: parse data from specific sections
                #if current_section == 'NODES':
