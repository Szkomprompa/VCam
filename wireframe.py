import numpy as np


def translate_matrix(dx=0, dy=0, dz=0):
    """ Return matrix for translation along vector (dx, dy, dz). """

    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [dx, dy, dz, 1]])


def scale_matrix(sx=0, sy=0, sz=0):
    """ Return matrix for scaling equally along all axes centred on the point (cx,cy,cz). """

    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])


def rotate_x_matrix(radians):
    """ Return matrix for rotating about the x-axis by 'radians' radians """

    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[1, 0, 0, 0],
                     [0, c, -s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]])


def rotate_y_matrix(radians):
    """ Return matrix for rotating about the y-axis by 'radians' radians """

    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]])


def rotate_z_matrix(radians):
    """ Return matrix for rotating about the z-axis by 'radians' radians """

    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, -s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


# Funkcje do tworzenia macierzy rotacji
def rotate_up(theta):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta), -np.sin(theta), 0],
        [0, np.sin(theta), np.cos(theta), 0],
        [0, 0, 0, 1]
    ])


def rotate_down(theta):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta), np.sin(theta), 0],
        [0, -np.sin(theta), np.cos(theta), 0],
        [0, 0, 0, 1]
    ])


def rotate_right(theta):
    return np.array([
        [np.cos(theta), 0, np.sin(theta), 0],
        [0, 1, 0, 0],
        [-np.sin(theta), 0, np.cos(theta), 0],
        [0, 0, 0, 1]
    ])


def rotate_left(theta):
    return np.array([
        [np.cos(theta), 0, -np.sin(theta), 0],
        [0, 1, 0, 0],
        [np.sin(theta), 0, np.cos(theta), 0],
        [0, 0, 0, 1]
    ])


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
        print("\n --- Nodes --- ")
        for i, (x, y, z, _) in enumerate(self.nodes):
            print("   %d: (%d, %d, %d)" % (i, x, y, z))

    def output_edges(self):
        print("\n --- Edges --- ")
        for i, (node1, node2) in enumerate(self.edges):
            print("   %d: %d -> %d" % (i, node1, node2))

    def transform(self, matrix):
        """ Apply a transformation defined by a given matrix. """
        self.nodes = np.dot(self.nodes, matrix)

    def scale(self, centre_x, centre_y, scale):
        """ Scale the wireframe from the centre of the screen. """
        scale_matrix_func = scale_matrix(scale, scale, scale)
        self.transform(scale_matrix_func)

    def add_all_cube_edges(self):
        self.add_edges([(n, n + 4) for n in range(0, 4)])
        self.add_edges([(n, n + 1) for n in range(0, 8, 2)])
        self.add_edges([(n, n + 2) for n in (0, 1, 4, 5)])

    def output_all(self):
        self.output_nodes()
        self.output_edges()

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
