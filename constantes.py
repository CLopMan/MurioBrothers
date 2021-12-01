""" Módulo de constantes: datos iniciales, proporciones de la ventana, parámetros que no varían """
# tablero:
WIDTH = 256
HEIGHT = 256
X = 0
VELOCIDAD = 0

# ==ENEMIGOS==
sprite_goomba = (0, 0, 48, 16, 16)
sprite_koopa = (0, 0, 48, 16, 16)
ENEMIGOS_XY = ((72, 144, "", sprite_goomba),)
VELOCIDAD_ENEMIGOS = 0.5

# ==MARIO==
POSICION_INICIAL_M = [5, 208]
# Para los dos siguientes parámentros el valor 0 corresponde con andar y el 1 con correr
ACELERACION = (0.25, 0.5)
VELOCIDAD_LIMITE = (2.5, 5)
ROZAMIENTO = (0.125, 0.25)

# ==OBSTACULOS==
POSICION_BLOQUES = (
    (46, 176), (50, 176), (54, 176), (140, 176), (144, 176), (146, 110), (148, 110), (150, 110), (152, 110), (154, 110),
    (156, 110), (160, 110), (162, 176), (176, 176), (190, 176), (192, 176))
SPRITE_BLOQUE = (0, 32, 16, 16, 16)
POSICION_LISO = ([0, 0])
SPRITE_LISO = (0, 48, 16, 16, 16)
SPRITE_DIAMANTE = (0, 16, 32, 16, 16)
SPRITE_TUBERIA = (0, 0, 80, 26, 31)

# ==Generales==
GRAVEDAD = 0.6

# hitbox = (16, 16)
# hitbox_mario_grande = (16, 32)
