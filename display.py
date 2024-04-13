import pygame
import numpy as np
from pygame.locals import *
from wireframe import *


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
        self.zoom_factor = 1.0
        self.max_zoom = 5.0

    def add_cubes(self):
        cube = Wireframe()
        cube.read_cube_from_file("data/cube.txt")
        cube.set_color((255, 0, 0))
        cube2 = Wireframe()
        cube2.read_cube_from_file("data/cube2.txt")
        cube2.set_color((0, 255, 0))
        cube3 = Wireframe()
        cube3.read_cube_from_file("data/cube3.txt")
        cube3.set_color((0, 0, 255))
        cube4 = Wireframe()
        cube4.read_cube_from_file("data/cube4.txt")
        cube4.set_color((255, 255, 0))
        self.cubes = [cube, cube2, cube3, cube4]

    def move_camera_forward(self):
        local_forward = np.array([0, 0, 1])
        rotated_forward = np.dot(rotation_matrix(self.camera_rotation), -local_forward)
        rotated_forward[2] = -rotated_forward[2]
        self.camera_position[:3] = (self.camera_position[:3] + rotated_forward * 10).astype(int)

    def move_camera_backward(self):
        local_backward = np.array([0, 0, -1])
        rotated_backward = np.dot(rotation_matrix(self.camera_rotation), -local_backward)
        rotated_backward[2] = -rotated_backward[2]
        self.camera_position[:3] = (self.camera_position[:3] + rotated_backward * 10).astype(int)

    def move_camera_left(self):
        local_left = np.array([1, 0, 0])
        rotated_left = np.dot(rotation_matrix(self.camera_rotation), local_left)
        rotated_left[0] = -rotated_left[0]
        self.camera_position[:3] = (self.camera_position[:3] + rotated_left * 10).astype(int)

    def move_camera_right(self):
        local_right = np.array([-1, 0, 0])
        rotated_right = np.dot(rotation_matrix(self.camera_rotation), local_right)
        rotated_right[0] = -rotated_right[0]
        self.camera_position[:3] = (self.camera_position[:3] + rotated_right * 10).astype(int)

    def move_camera_up(self):
        local_up = np.array([0, 1, 0])
        rotated_up = np.dot(rotation_matrix(self.camera_rotation), local_up)
        rotated_up[1] = -rotated_up[1]
        self.camera_position[:3] = (self.camera_position[:3] + rotated_up * 10).astype(int)

    def move_camera_down(self):
        local_down = np.array([0, -1, 0])
        rotated_down = np.dot(rotation_matrix(self.camera_rotation), local_down)
        rotated_down[1] = -rotated_down[1]
        self.camera_position[:3] = (self.camera_position[:3] + rotated_down * 10).astype(int)

    def perspective_projection(self, vertex):
        dir_vector = np.array(vertex[:3]) - self.camera_position[:3]
        rotated_matrix = np.dot(rotation_matrix(self.camera_rotation), dir_vector)
        x, y, z = rotated_matrix[:3]

        if z > 0:
            x_proj = int(x * 1 / z * self.SCREEN_WIDTH / 2 * self.zoom_factor + self.SCREEN_WIDTH / 2)
            y_proj = int(y * 1 / z * self.SCREEN_HEIGHT / 2 * self.zoom_factor + self.SCREEN_HEIGHT / 2)
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
                    pygame.draw.aaline(self.screen, c.color, start_vertex, stop_vertex)

        pygame.display.flip()

    def run(self):

        running = True
        while running:
            self.screen.fill(self.WHITE)
            camera_rotation = self.camera_rotation
            theta = self.theta

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.move_camera_left()
                    if event.key == K_RIGHT:
                        self.move_camera_right()
                    if event.key == K_UP:
                        self.move_camera_forward()
                    if event.key == K_DOWN:
                        self.move_camera_backward()
                    if event.key == K_EQUALS:
                        self.move_camera_up()
                    if event.key == K_MINUS:
                        self.move_camera_down()
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
                    if event.key == K_PAGEUP:
                        self.zoom_factor = min(self.zoom_factor + 0.1, self.max_zoom)
                    if event.key == K_PAGEDOWN:
                        self.zoom_factor = max(self.zoom_factor - 0.1, 0.1)

                    print(self.camera_rotation)
                    self.draw_frame()

        pygame.quit()
