import numpy as np


def rotation_matrix(rotation):
    rotation_z, rotation_y, rotation_x = rotation
    return np.array([
        [np.cos(rotation_z) * np.cos(rotation_y),
         np.cos(rotation_z) * np.sin(rotation_y) * np.sin(rotation_x) - np.sin(rotation_z) * np.cos(rotation_x),
         np.cos(rotation_z) * np.sin(rotation_y) * np.cos(rotation_x) + np.sin(rotation_z) * np.sin(rotation_x)],
        [np.sin(rotation_z) * np.cos(rotation_y),
         np.sin(rotation_z) * np.sin(rotation_y) * np.sin(rotation_x) + np.cos(rotation_z) * np.cos(rotation_x),
         np.sin(rotation_z) * np.sin(rotation_y) * np.cos(rotation_x) - np.cos(rotation_z) * np.sin(rotation_x)],
        [-np.sin(rotation_y), np.cos(rotation_y) * np.sin(rotation_x), np.cos(rotation_y) * np.cos(rotation_x)]])


class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []

    def add_nodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def add_edges(self, edge_list):
        self.edges += edge_list

    def output_nodes(self):
        print(" --- Nodes --- ")
        for i, (x, y, z, _) in enumerate(self.nodes):
            print("   %d: (%d, %d, %d)" % (i, x, y, z))

    def output_edges(self):
        print(" --- Edges --- ")
        for i, (node1, node2) in enumerate(self.edges):
            print("   %d: %d -> %d" % (i, node1, node2))

    def output_all(self):
        self.output_nodes()
        self.output_edges()

    def add_all_cube_edges(self):
        self.add_edges([(n, n + 4) for n in range(0, 4)])
        self.add_edges([(n, n + 1) for n in range(0, 8, 2)])
        self.add_edges([(n, n + 2) for n in (0, 1, 4, 5)])

    def read_cube_from_file(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            num_nodes = len(lines)
            if num_nodes != 8:
                print("Error: Cube must have 8 nodes")
                return
            for line in lines:
                if len(line.split()) != 3:
                    print("Error: Node coordinates must be 3D")
                    return
                self.add_nodes(np.array([list(map(int, line.split()))]))
            self.add_all_cube_edges()
