import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from collections import defaultdict

class DigitalCircuit:
    def __init__(self):
        # Initialize component delay values
        self.delays = {
            'ADD': 1.0,
            'MUL': 1.0,
            'REG': 0.2,
            'MUX': 1.0,
            'INPUT': 0.0,
            'OUTPUT': 0.0
        }
        # Create directed graph using NetworkX
        self.graph = nx.DiGraph()
        self.node_types = {}

    def parse_circuit(self, filename: str) -> Dict:
        """
        Parse circuit description from file and create graph representation
        """
        try:
            with open(filename, 'r') as file:
                circuit_name = None
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        if not circuit_name and "Circuit name" in line:
                            circuit_name = line.split(':')[1].strip()
                        continue

                    parts = line.split()
                    node_type = parts[0]
                    node_id = parts[1]
                    input_nodes = parts[2:] if len(parts) > 2 else []

                    # Add node to graph
                    self.graph.add_node(node_id)
                    self.node_types[node_id] = node_type

                    # Add edges from input nodes
                    for input_node in input_nodes:
                        self.graph.add_edge(input_node, node_id)

            return {'name': circuit_name, 'graph': self.graph}

        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            return None
        except Exception as e:
            print(f"Error parsing circuit file: {str(e)}")
            return None

    def identify_node_type(self, node_id: str) -> str:
        """
        Determine the type of a node in the circuit
        """
        return self.node_types.get(node_id, "UNKNOWN")

    def calculate_path_delay(self, path: List[str]) -> float:
        """
        Calculate total delay along a given path
        """
        total_delay = 0.0
        for node in path:
            node_type = self.identify_node_type(node)
            total_delay += self.delays.get(node_type, 0.0)
        return total_delay

    def find_critical_path(self) -> Tuple[List[str], float]:
        """
        Find the critical path using topological sort and dynamic programming
        """
        # Get topological sort of the graph
        try:
            topo_sort = list(nx.topological_sort(self.graph))
        except nx.NetworkXUnfeasible:
            print("Error: Circuit contains cycles")
            return [], 0.0

        # Initialize distances and predecessors
        distances = {node: float('-inf') for node in self.graph.nodes()}
        predecessors = {node: None for node in self.graph.nodes()}

        # Set distance for input nodes
        for node in self.graph.nodes():
            if self.identify_node_type(node) == 'INPUT':
                distances[node] = 0

        # Calculate longest path
        for node in topo_sort:
            node_delay = self.delays.get(self.identify_node_type(node), 0.0)
            for successor in self.graph.successors(node):
                new_distance = distances[node] + node_delay
                if new_distance > distances[successor]:
                    distances[successor] = new_distance
                    predecessors[successor] = node

        # Find end node with maximum distance
        end_node = max(
            (node for node in self.graph.nodes()
             if self.identify_node_type(node) == 'OUTPUT'),
            key=lambda x: distances[x]
        )

        # Reconstruct critical path
        critical_path = []
        current = end_node
        while current is not None:
            critical_path.append(current)
            current = predecessors[current]
        critical_path.reverse()

        return critical_path, distances[end_node]

    def visualize_circuit(self, critical_path: List[str]):
        """
        Visualize the circuit and highlight the critical path
        """
        pos = nx.spring_layout(self.graph)
        plt.figure(figsize=(12, 8))

        # Draw regular edges
        nx.draw_networkx_edges(self.graph, pos, edge_color='gray')

        # Draw critical path edges
        critical_edges = list(zip(critical_path[:-1], critical_path[1:]))
        nx.draw_networkx_edges(self.graph, pos, edgelist=critical_edges,
                             edge_color='red', width=2)

        # Draw nodes
        node_colors = ['red' if node in critical_path else 'lightblue'
                      for node in self.graph.nodes()]
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors)
        nx.draw_networkx_labels(self.graph, pos)

        plt.title("Circuit Diagram with Critical Path Highlighted")
        plt.axis('off')
        plt.show()

def main():
    circuit = DigitalCircuit()
    cir_names = ["cir1.txt", "4-bit CLA.txt", "FIR Filter.txt", "6-Bit Binary Adder.txt", "Sequence Detector.txt"]

    for cur_circuit in cir_names:
        try:
            print(f"\nAnalyzing circuit: {cur_circuit}")
            circuit_info = circuit.parse_circuit(cur_circuit)

            if circuit_info:
                critical_path, total_delay = circuit.find_critical_path()

                # Print results
                print(f"Critical Path: {' -> '.join(critical_path)}")
                print("Path Components:")
                for node in critical_path:
                    node_type = circuit.identify_node_type(node)
                    if node_type in circuit.delays:
                        print(f"- {node_type} ({node}): {circuit.delays[node_type]:.1f} tu")
                print(f"Total Delay: {total_delay:.2f} time units")

                # Visualize circuit
                circuit.visualize_circuit(critical_path)

        except Exception as e:
            print(f"Error processing circuit {cur_circuit}: {str(e)}")

if __name__ == "__main__":
    main()
