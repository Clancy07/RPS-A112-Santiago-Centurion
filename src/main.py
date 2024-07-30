import pygame
from pygame import time, display, event
from pygame.locals import *
from settings import *
from uploads import *
from funciones import *
from random import randint
from funciones_colisiones import *


def wait_user(tecla: int):
    continuar = True
    while continuar:
        for e in event.get():

            # Evento el usuario cierra la ventana.
            if e.type == QUIT:
                salir_juego()

            if e.type == KEYDOWN:
                if e.key == tecla:
                    continuar = False


def wait_user_click(button_rect: pygame.Rect):
    continuar = True
    while continuar:
        for e in event.get():
            # Evento el usuario cierra la ventana.
            if e.type == QUIT:
                salir_juego()

            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if punto_en_rectangulo(e.pos, button_rect):
                        continuar = False


pygame.init
pygame.mixer.init()

clock = pygame.time.Clock()
rect_boton_start = imagen_boton_start.get_rect()
rect_boton_start.center = BOTON_START_POS

screen = display.set_mode(SCREEN_SIZE)
display.set_caption("Galaga BERRETA")
pygame.mixer.music.load("./src/assets/musica.mp3")
playing_music = True
sonido_explosion.set_volume(10)
sonido_golpe.set_volume(0.4)
sonido_disparo.set_volume(0.15)
pygame.mixer.music.set_volume(2)

TIMERESCUDO = pygame.USEREVENT + 1


while True:

    screen.blit(imagen_menu, ORIGEN)

    player = crear_personaje(imagen=imagen_player,
                             pos_x=PLAYER_SPAWN_POINT_X,
                             pos_y=PLAYER_SPAWN_POINT_Y,
                             ancho=PLAYER_WIDTH,
                             alto=PLAYER_HEIGHT)

    abejas = []
    caragar_lista_enemigos(abejas, 25, imagen_abeja)

    screen.blit(imagen_boton_start, rect_boton_start)
    pygame.display.flip()
    wait_user_click(rect_boton_start)

    pygame.mixer.music.play(-1)

    move_left = False
    move_right = False

    proyectiles = []
    escudos = []
    score = 0
    max_score = 0
    timer_explosion = 0
    vidas = 3
    running = True

    pygame.time.set_timer(TIMERESCUDO, 10000)

    while running:
        clock.tick(FPS)
        mostrar_texto(screen, f"VIDAS: {vidas}", fuente,
                      (50, 20), WHITE)

        # Eventos ======================================================================================
        for evento in pygame.event.get():

            # Cerrar ventana.
            if evento.type == QUIT:
                salir_juego()

            # Presionar teclas.
            if evento.type == KEYDOWN:

                if evento.key == K_LEFT:
                    move_left = True
                    move_right = False

                if evento.key == K_RIGHT:
                    move_right = True
                    move_left = False

                if evento.key == K_z:
                    sonido_disparo.play()
                    nuevo_proyectil = crear_proyectil(
                        player["rect"].centerx, player["rect"].top, PROYECTIL_WIDTH, PROYECTIL_HEIGHT, VELOCIDAD_PROYECTIL)
                    proyectiles.append(nuevo_proyectil)

                # Pausa.
                if evento.key == K_p:
                    # Se pausa la musica (si ya estaba pausada, seguira en el mismo estado).
                    pygame.mixer.music.pause()
                    mostrar_texto(screen, "PAUSA", fuente,
                                  SCREEN_CENTER, MAGENTA)
                    wait_user(K_p)
                    # Si la musica no estaba pausada, se despausa cuando se reanuda el juego.
                    if playing_music:
                        pygame.mixer.music.unpause()

            # Timer escudo.
            if evento.type == TIMERESCUDO:
                escudo = crear_personaje(imagen_escudo,
                                         randint(0, SCREEN_WIDTH -
                                                 ESCUDO_WIDTH),
                                         randint(- SCREEN_HEIGHT,
                                                 0 - ESCUDO_HIGHT),
                                         ESCUDO_WIDTH, ESCUDO_HIGHT)
                escudos.append(escudo)

            # Soltar teclas.
            if evento.type == KEYUP:
                if evento.key == K_LEFT:
                    move_left = False
                if evento.key == K_RIGHT:
                    move_right = False
        # ==============================================================================================

        # Movimientos ==================================================================================
        if move_left and player["rect"].left > 0:
            player["rect"].left -= PLAYER_SPEED
        if move_right and player["rect"].right < SCREEN_WIDTH:
            player["rect"].right += PLAYER_SPEED

        # Mover los proyectiles
        for proyectil in proyectiles:
            mover_proyectil(proyectil)
            # Eliminar proyectiles fuera de la pantalla
            if proyectil["rect"].bottom < 0:
                proyectiles.remove(proyectil)

        for abeja in abejas:
            abeja["rect"].move_ip(0, VELOCIDAD_ABEJA)
            if abeja["rect"].top > SCREEN_HEIGHT:
                abeja["rect"].bottom = 0

        for escudo in escudos:
            escudo["rect"].move_ip(0, VELOCIDAD_ESCUDO)

            if escudo['rect'].top > SCREEN_HEIGHT:
                escudos.remove(escudo)

        # ==============================================================================================
        mostrar_texto(screen, f"VIDAS: {vidas}", fuente,
                      (50, 20), WHITE)
        
        # Verificar colisiones =========================================================================
        # Colision enemigo-jugador.
        for abeja in abejas.copy():
            if detectar_colision(player["rect"], abeja["rect"]):
                sonido_explosion.play()
                vidas -= 1
                abejas.remove(abeja)
                player["imagen"] = imagen_explosion
                timer_explosion = pygame.time.get_ticks()

                if vidas == 0:
                    running = False

            # Colision proyectil-enemigo.
            for proyectil in proyectiles.copy():
                if detectar_colision(proyectil["rect"], abeja["rect"]):
                    sonido_golpe.play()
                    score += 1
                    abejas.remove(abeja)
                    proyectiles.remove(proyectil)

        # La imagen de la explosion dura 1 segundo.
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - timer_explosion >= 1000:
            player["imagen"] = imagen_player

        # Colision escudo-jugador.
        for escudo in escudos.copy():
            if detectar_colision(player["rect"], escudo["rect"]):
                sonido_escudo.play()
                vidas += 1
                escudos.remove(escudo)

        # ==============================================================================================
        if len(abejas) == 0:
            caragar_lista_enemigos(abejas, 25, imagen_abeja)

        # Actualizacion de pantalla ====================================================================
        screen.blit(imagen_fondo, ORIGEN)

        for abeja in abejas:
            screen.blit(abeja["imagen"], abeja["rect"])

        screen.blit(player["imagen"], player["rect"])

        for proyectil in proyectiles:
            pygame.draw.rect(screen, RED, proyectil["rect"])

        for escudo in escudos:
            screen.blit(escudo["imagen"], escudo["rect"])

        pygame.display.flip()
        # ==============================================================================================

    # Pantalla game over.

    if score > max_score:
        max_score = score
    pygame.mixer.music.stop()
    sonido_game_over.play()
    screen.fill(BLACK)
    mostrar_texto(screen, f'Last score: {score}',
                  fuente, ULTIMO_SCORE_POS, CYAN)
    mostrar_texto(
        screen, f'Max score: {max_score}', fuente, MAX_SCORE_POS, CYAN)
    mostrar_texto(screen, "GAME OVER", fuente, SCREEN_CENTER, BLUE)
    mostrar_texto(screen, "Pulsa SPACE para comenzar",
                  fuente, MESSAGE_START_POS, RED)
    wait_user(K_SPACE)

    with open(get_path_actual("scores.csv"), 'w', encoding='utf-8') as archivo:
        archivo.write('scores,')
        archivo.write('max scores')
        archivo.write('\n')
        archivo.write(str(f'{score},'))
        archivo.write(str(max_score))
