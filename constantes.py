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
ACELERACION = (0.3, 0.6)
VELOCIDAD_LIMITE = (3, 6)
ROZAMIENTO = (0.075, 0.15)


# ==OBSTACULOS==
POSICION_BLOQUES = ((184, 184), (284, 200), (384, 160))
SPRITE_BLOQUE = (0, 32, 16, 16, 16)
SPRITE_LISO= (0, 48, 16, 16, 16)
SPRITE_DIAMANTE = (0, 16, 32, 16, 16)
SPRITE_TUBERIA = (0, 0, 80, 26, 31)

# ==Generales==
GRAVEDAD = 0.6


# hitbox = (16, 16)
# hitbox_mario_grande = (16, 32)
