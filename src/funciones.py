import pygame
from random import randint
from settings import *


def salir_juego() -> None:
    """Ejecuta las funciones pygame.quit() y exit() para detener la ejecucion y cerrar la ventana.
    """
    pygame.quit()
    exit()


def crear_personaje(imagen: pygame.image = None, pos_x: int = 0, pos_y: int = 0, ancho: int = 50, alto: int = 50) -> dict:
    """Crea una entidad. Recibe una imagen, la posicion de la entidad y el tamanio. Retorna un diccionario con la imagen y el rectangulo de la entidad.

    Args:
        imagen (pygame.image, optional): Imagen que se aplicara a la entidad dentro del juego. Se escalara segun el tamanio recibido. Defaults to None. 
        pos_x (int, optional): Posicion en X que se asignara a la entidad dentro del juego. Defaults to 0.
        pos_y (int, optional): Posicion en Y que se asignara a la entidad dentro del juego. Defaults to 0.
        ancho (int, optional): Ancho al que se escalara la imagen recibida. Defaults to 50.
        alto (int, optional): Alto al que se escalara la imagen recibida. Defaults to 50.

    Returns:
        dict: Diccionario con la imagen y el rectangulo de la entidad.
    """

    # A la posicion se le resta la mitad del tamanio de la imagen para obtener el centro (para mas facil posicionamiento).
    pos_x -= ancho // 2
    pos_y -= alto // 2

    rect = pygame.Rect(pos_x, pos_y, ancho, alto)

    if imagen:
        imagen = pygame.transform.scale(imagen, (ancho, alto))

    personaje = {
        "rect": rect,
        "imagen": imagen,
    }

    return personaje


def caragar_lista_enemigos(lista: list, cantidad: int, imagen: pygame.image = None) -> None:
    """Carga una lista recibida con enemigos.

    Args:
        lista (list): Lista en la que se cargaran los enemigos
        cantidad (int): Cantidad de enemigos a cargar
        imagen (pygame.image, optional): Imagen que se aplicara a los enemigos. Defaults to None.
    """
    for _ in range(cantidad):
        lista.append(crear_personaje(imagen,
                                     randint(0, SCREEN_WIDTH - ABEJA_WIDTH),
                                     randint(- SCREEN_HEIGHT,
                                             0 - ABEJA_HEIGHT),
                                     ABEJA_WIDTH,
                                     ABEJA_HEIGHT))


def crear_proyectil(pos_x: int, pos_y: int, ancho: int, alto: int, velocidad: int) -> dict:
    """Crea un proyectil con el metodo Rect con el tamanio recibido y en al posicion recibida. Retorna un diccionario con el proyectil y su velocidad.

    Args:
        pos_x (int): Posicion en X del proyectil.
        pos_y (int): Posicion en Y del proyectil.
        ancho (int, optional): Ancho del proyectil.
        alto (int, optional): Alto del proyectil..
        velocidad (int, optional): Velocidad a la que sera movido el proyectil.

    Returns:
        dict: Diccionario con el rectangulo y la velocidad del proyectil.
    """
    rect = pygame.Rect(pos_x, pos_y, ancho, alto)

    proyectil = {
        "rect": rect,
        "velocidad": velocidad,
    }

    return proyectil


def mover_proyectil(proyectil: dict) -> None:
    """Recibe un proyectil por parametros y lo mueve.

    Args:
        proyectil (dict): Proyectil con clave rect y velocidad. Su posicion sera actualizada segun su clave velocidad.
    """
    proyectil["rect"].y -= proyectil["velocidad"]


def mostrar_texto(superficie: pygame.surface, texto: str, fuente: pygame.font, posicion: tuple[int, int], color: tuple[int, int, int], color_fondo: tuple[int, int, int] = None) -> None:
    """Muestra un texto en la posicion recibida sobre la superficie recibida. El texto tendra la fuente, color y color de fondo recibidos por parametros. 

    Args:
        superficie (pygame.surface): Es la superficie sobre la que se bliteara el texto.
        texto (str): Texto a mostrar.
        fuente (pygame.font): Fuente que tendra el texto.
        posicion (tuple[int, int]): Posicion en la que se bliteara el texto.
        color (tuple[int, int, int]): Color que tendra el texto en pantalla.
        color_fondo (tuple[int, int, int], optional): Color de fondo opcional que tendra el texto. Defaults to None.
    """
    sup_texto = fuente.render(texto, True, color, color_fondo)
    rect_texto = sup_texto.get_rect()
    rect_texto.center = posicion
    superficie.blit(sup_texto, rect_texto)
    pygame.display.flip()


def get_path_actual(nombre_archivo: str) -> str:
    """Usa el metodo path.dirname para hallar y retornar el path del directorio actual.

    Args:
        nombre_archivo (str): nombre del archivo deseado que sera adjunto al path para completarlo.

    Returns:
        str: Path completo del archivo cuyo nombre fue recibido por parametros.
    """
    import os
    directorio_actual = os.path.dirname(__file__)
    return os.path.join(directorio_actual, nombre_archivo)
