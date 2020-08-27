import sys
import pygame
import time
from win32api import GetSystemMetrics
import random
import math


# Inicjalizacja modułów
pygame.init()
pygame.display.set_caption("Snake_Mańczak")
myfont = pygame.font.SysFont('Arial', 30)

# pygame.display.set_icon(pygame.image.load('Path_to_icon'))

# Ustaw rozmiar okna na kwadrat o boku równym połowie wysokości obecnego ekranu
window_size = window_width, window_height = int(
    GetSystemMetrics(1)/2), int(GetSystemMetrics(1)/2)

# Wymiary poszczególnego bloku
snake_block_dimensions = 20, 20

# Kolor węża
#     R   G   B
skin_colour = 0, 255, 0

# Utwórz nowe okno
screen = pygame.display.set_mode(window_size)


class snake_block:  # Klasa odpowiadająca za pojedyńczy segment węża
    def __init__(self, var_pos_x, var_pos_y):
        self.pos_x = var_pos_x
        self.pos_y = var_pos_y
        self.snake_block = pygame.Rect(
            self.pos_x, self.pos_y, snake_block_dimensions[0], snake_block_dimensions[1])

    def draw(self):  # Wyrysowuje dany segment na ekran
        pygame.draw.rect(screen, skin_colour, self.snake_block)

    def move(self, speed):  # Porusza dany segment o zadaną odległość oraz aktualizuje wartości jego pozycji
        self.snake_block = self.snake_block.move(speed[0], speed[1])
        self.pos_x = self.pos_x+speed[0]
        self.pos_y = self.pos_y+speed[1]
        # Teleportacja na krawędziach
        if self.snake_block.left < 0:  # lewo->prawo
            self.snake_block = pygame.Rect(
                window_width-(snake_block_dimensions[0]+1), self.snake_block.top, snake_block_dimensions[0], snake_block_dimensions[1])
            self.pos_x = window_width-(snake_block_dimensions[0]+1)
            self.pos_y = self.snake_block.top
        elif self.snake_block.right > window_width:  # prawo->lewo
            self.snake_block = pygame.Rect(
                0, self.snake_block.top, snake_block_dimensions[0], snake_block_dimensions[1])
            self.pos_x = 0
            self.pos_y = self.snake_block.top
        if self.snake_block.top < 0:  # góra->doł
            self.snake_block = pygame.Rect(
                self.snake_block.left, window_height-(snake_block_dimensions[1]+1), snake_block_dimensions[0], snake_block_dimensions[1])
            self.pos_x = self.snake_block.left
            self.pos_y = window_height-(snake_block_dimensions[1]+1)
        elif self.snake_block.bottom > window_height:  # dół->góra
            self.snake_block = pygame.Rect(
                self.snake_block.left, 0, snake_block_dimensions[0], snake_block_dimensions[1])
            self.pos_x = self.snake_block.left
            self.pos_y = 0

    def follow(self, var_pos_x, pos_y):  # Przenosi dany segment na zadane współrzędne
        self.pos_x = var_pos_x
        self.pos_y = pos_y
        self.snake_block = pygame.Rect(
            self.pos_x, self.pos_y, snake_block_dimensions[0], snake_block_dimensions[1])


wonsz = []


class Apple:  # Klasa odpowiadająca za jabka
    def __init__(self):
        # Losowanie pozycji x y w obrębie okna, z upewnieniem się, że będzie to wielokrotność skoku
        self.pos_x = (
            (random.randint(25, window_width-(snake_block_dimensions[0]+10)))//speed_multiplier)*speed_multiplier
        self.pos_y = (random.randint(
            25, window_height-(snake_block_dimensions[1]+10))//speed_multiplier)*speed_multiplier

        self.apple_block = pygame.Rect(
            self.pos_x, self.pos_y, snake_block_dimensions[0], snake_block_dimensions[1])

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.apple_block)


# Parametry gry
speed_multiplier = 20  # Musi zostać dodatnie,
speed = [speed_multiplier, 0]

game_over = False
# Utwórz pierwszy blok węża, oraz pierwsze jabłko
wonsz.append(snake_block(20, 20))
apple = Apple()


while not game_over:
    for event in pygame.event.get():  # Obsługa sterowania okienkiem oraz strzałek
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and speed[0] == 0:
                print("K_LEFT")
                speed = [-1*speed_multiplier, 0]

            if event.key == pygame.K_RIGHT and speed[0] == 0:
                print("K_RIGHT")
                speed = [speed_multiplier, 0]

            if event.key == pygame.K_UP and speed[1] == 0:
                print("K_UP")
                speed = [0, -1*speed_multiplier]

            if event.key == pygame.K_DOWN and speed[1] == 0:
                print("K_DOWN")
                speed = [0, speed_multiplier]

            if event.key == pygame.K_SPACE:
                print("K_SPACE")
    # Czyścimy ekran
    screen.fill((0, 0, 0))

    apple.draw()

    # Rysowanie i podążanie elementów za sobą
    for obj in reversed(range(len(wonsz))):

        wonsz[obj].draw()

        if obj != 0:
            wonsz[obj].follow(wonsz[obj-1].pos_x, wonsz[obj-1].pos_y)

    # Wykonaj ruch
    wonsz[0].move(speed)

    textsurface = myfont.render(
        'Wynik: '+str(len(wonsz)-1), False, (255, 255, 255))
    screen.blit(textsurface, (0, 0))

    pygame.display.flip()
    time.sleep(0.1)

    # Jeżeli jestesmy w obrebie jabka, usuwamy je, spawn nowe, i zwiekszamy węża
    if math.hypot(wonsz[0].pos_x-apple.pos_x, wonsz[0].pos_y-apple.pos_y) < (snake_block_dimensions[0]-2):
        del apple
        apple = Apple()
        wonsz.append(snake_block(wonsz[0].pos_x, wonsz[0].pos_y))
