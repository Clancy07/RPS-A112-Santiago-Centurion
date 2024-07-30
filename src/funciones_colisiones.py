def punto_en_rectangulo(punto, rect):
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom


def detectar_colision(rec_1, rec_2) -> bool:
    # Revisa si algun punto de rec_1 esta dentro de rec_2
    if (punto_en_rectangulo(rec_1.topleft, rec_2) or
        punto_en_rectangulo(rec_1.topright, rec_2) or
        punto_en_rectangulo(rec_1.bottomright, rec_2) or
            punto_en_rectangulo(rec_1.bottomleft, rec_2)):
        return True

    # Revisa si algun punto de rec_2 esta dentro de rec_1
    if (punto_en_rectangulo(rec_2.topleft, rec_1) or
        punto_en_rectangulo(rec_2.topright, rec_1) or
        punto_en_rectangulo(rec_2.bottomright, rec_1) or
            punto_en_rectangulo(rec_2.bottomleft, rec_1)):
        return True

    # Si no encontro ninguna colision, devuelve False
    return False