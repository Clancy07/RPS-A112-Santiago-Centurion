import pygame
from settings import *

pygame.mixer.init()
pygame.font.init()

# Imagenes.
imagen_player = pygame.image.load("./src/assets/nave.png")

imagen_player = pygame.transform.scale(
    imagen_player, (PLAYER_WIDTH, PLAYER_HEIGHT))

imagen_fondo = pygame.transform.scale(pygame.image.load(
    "./src/assets/fondo.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

imagen_menu = pygame.image.load("./src/assets/menu.png")

imagen_abeja = pygame.image.load("./src/assets/abeja.png")

imagen_explosion = pygame.image.load("./src/assets/explosion.png")

imagen_escudo = pygame.image.load("./src/assets/escudo.png")


imagen_explosion = pygame.transform.scale(
    imagen_explosion, (PLAYER_WIDTH, PLAYER_HEIGHT))

imagen_boton_start = pygame.transform.scale(
    pygame.image.load("./src/assets/boton_start.png"), BOTON_START_SIZE)


# Audio.
sonido_explosion = pygame.mixer.Sound("./src/assets/explosion.mp3")
sonido_game_over = pygame.mixer.Sound("./src/assets/game_over.mp3")
sonido_golpe = pygame.mixer.Sound("./src/assets/golpe.mp3")
sonido_disparo = pygame.mixer.Sound("./src/assets/disparo.mp3")
sonido_escudo = pygame.mixer.Sound("./src/assets/escudo.mp3")


# Fuente.
fuente = pygame.font.SysFont(None, 24)
