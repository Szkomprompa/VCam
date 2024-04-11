import pygame
from pygame.locals import *

from wireframe import *


def get_camera_orientation(camera_rotation):
    # Sprawdź wartości w macierzy obrotu kamery
    x_axis = camera_rotation[:3, 0]
    y_axis = camera_rotation[:3, 1]
    z_axis = camera_rotation[:3, 2]

    # Określ orientację kamery na podstawie kierunku osi X i Y
    if np.allclose(y_axis, [0, 1, 0]):  # Kamera skierowana na północ
        return 'north'
    elif np.allclose(x_axis, [1, 0, 0]):  # Kamera skierowana na wschód
        return 'east'
    elif np.allclose(y_axis, [0, -1, 0]):  # Kamera skierowana na południe
        return 'south'
    elif np.allclose(x_axis, [-1, 0, 0]):  # Kamera skierowana na zachód
        return 'west'
    else:
        return 'unknown'


# Inicjalizacja Pygame
def display():
    # Inicjalizacja Pygame
    pygame.init()

    # Ustawienia ekranu
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Wirtualna kamera")

    # Kolory
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    cubes = []
    # Inicjalizacja obiektu Wireframe
    cube = Wireframe()
    cube.read_cube_from_file("data/cube.txt")
    cube2 = Wireframe()
    cube2.read_cube_from_file("data/cube2.txt")
    cube3 = Wireframe()
    cube3.read_cube_from_file("data/cube3.txt")
    cube4 = Wireframe()
    cube4.read_cube_from_file("data/cube4.txt")
    cubes = [cube, cube2, cube3, cube4]

    # Parametry kamery
    fov = 45  # Kąt widzenia (field of view) w stopniach
    aspect_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
    near = 1  # Odległość do bliskiej płaszczyzny od obserwatora
    far = 1000  # Odległość do dalekiej płaszczyzny od obserwatora

    camera_rotation = np.eye(4)
    camera_position = np.array([0, 0, 0, 1])
    theta = 0.1

    # Funkcja rzutowania perspektywicznego
    def perspective_projection(vertex, rotation):
        vertex_homogeneous = np.append(vertex[:3], 1)  # Dodanie współrzędnej jednorodnej
        transformed_vertex = np.dot(camera_rotation, vertex_homogeneous)  # Zastosowanie macierzy obrotu kamery
        x, y, z, _ = transformed_vertex
        if z <= -fov:
            return None
        x_proj = (fov / (fov + z)) * x
        y_proj = (fov / (fov + z)) * y
        x_proj += SCREEN_WIDTH / 2
        y_proj += SCREEN_HEIGHT / 2
        return np.array([x_proj, y_proj, z])

    # Główna pętla programu
    running = True
    while running:
        screen.fill(WHITE)

        # Rysowanie krawędzi
        for cube in cubes:
            for edge in cube.edges:
                start_node = cube.nodes[edge[0]]
                stop_node = cube.nodes[edge[1]]
                start_vertex = perspective_projection(start_node - camera_position, camera_rotation)
                stop_vertex = perspective_projection(stop_node - camera_position, camera_rotation)
                # Rysowanie krawędzi tylko wtedy, gdy punkty znajdują się przed ekranem
                if start_vertex is not None and stop_vertex is not None:
                    pygame.draw.aaline(screen, BLACK, (start_vertex[0], start_vertex[1]),
                                       (stop_vertex[0], stop_vertex[1]))

        # Wyświetlanie obiektu na ekranie
        pygame.display.flip()

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                # Obsługa klawiszy
                if event.key == K_LEFT:
                    camera_position[0] -= 10
                elif event.key == K_RIGHT:
                    camera_position[0] += 10
                elif event.key == K_UP:
                    camera_position[2] += 10
                elif event.key == K_DOWN:
                    camera_position[2] -= 10
                if event.key == K_EQUALS:
                    camera_position[1] -= 10
                elif event.key == K_MINUS:
                    camera_position[1] += 10
                if event.key == K_w:
                    camera_rotation = np.dot(rotate_down(theta), camera_rotation)
                    print(camera_rotation)
                elif event.key == K_s:
                    camera_rotation = np.dot(rotate_up(theta), camera_rotation)
                    print(camera_rotation)
                elif event.key == K_a:
                    camera_rotation = np.dot(rotate_right(theta), camera_rotation)
                    print(camera_rotation)
                elif event.key == K_d:
                    camera_rotation = np.dot(rotate_left(theta), camera_rotation)
                    print(camera_rotation)

    # Zakończenie Pygame
    pygame.quit()


if __name__ == "__main__":
    display()
