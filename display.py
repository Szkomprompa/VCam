import pygame
import numpy as np
from pygame.locals import *
from wireframe import *


class Display:

    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Wirtualna kamera")
        self.cubes = []
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.camera_rotation = np.array([0.0, 0.0, 0.0])
        self.camera_position = np.array([0, 0, 0, 1])
        self.theta = 10

    def add_cubes(self):
        cube = Wireframe()
        cube.read_cube_from_file("data/cube.txt")
        cube2 = Wireframe()
        cube2.read_cube_from_file("data/cube2.txt")
        cube3 = Wireframe()
        cube3.read_cube_from_file("data/cube3.txt")
        cube4 = Wireframe()
        cube4.read_cube_from_file("data/cube4.txt")
        self.cubes = [cube, cube2, cube3, cube4]

    def perspective_projection(self, vertex):
        dir_vector = np.array(vertex[:3]) - self.camera_position[:3]
        rotated_matrix = np.dot(rotation_matrix(self.camera_rotation), dir_vector)
        x, y, z = rotated_matrix[:3]

        if z > 0:
            x_proj = int(x * 1 / z * self.SCREEN_WIDTH / 2 + self.SCREEN_WIDTH / 2)
            y_proj = int(y * 1 / z * self.SCREEN_HEIGHT / 2 + self.SCREEN_HEIGHT / 2)
            return x_proj, y_proj
        else:
            return None

    def draw_frame(self):
        self.screen.fill(self.WHITE)

        for c in self.cubes:
            for edge in c.edges:
                start_vertex = self.perspective_projection(c.nodes[edge[0]])
                stop_vertex = self.perspective_projection(c.nodes[edge[1]])
                if start_vertex is not None and stop_vertex is not None:
                    pygame.draw.aaline(self.screen, self.BLACK, start_vertex, stop_vertex)

        pygame.display.flip()

    def run(self):

        running = True
        while running:
            self.screen.fill(self.WHITE)
            camera_position = self.camera_position
            camera_rotation = self.camera_rotation
            theta = self.theta

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        camera_position[0] -= 10
                    if event.key == K_RIGHT:
                        camera_position[0] += 10
                    if event.key == K_UP:
                        camera_position[2] += 10
                    if event.key == K_DOWN:
                        camera_position[2] -= 10
                    if event.key == K_EQUALS:
                        camera_position[1] -= 10
                    if event.key == K_MINUS:
                        camera_position[1] += 10
                    if event.key == K_w:
                        camera_rotation[2] += np.radians(theta)
                    if event.key == K_s:
                        camera_rotation[2] -= np.radians(theta)
                    if event.key == K_a:
                        camera_rotation[1] += np.radians(theta)
                    if event.key == K_d:
                        camera_rotation[1] -= np.radians(theta)
                    if event.key == K_q:
                        camera_rotation[0] += np.radians(theta)
                    if event.key == K_e:
                        camera_rotation[0] -= np.radians(theta)

                    self.draw_frame()

        pygame.quit()
