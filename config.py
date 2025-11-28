import pygame

# Dimensiones
ANCHO = 1200
ALTO = 750
FPS = 60

# Colores (Paleta Peruana)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
NARANJA = (255, 140, 0)      # Fuerza Popular / Gaseosa
ROJO = (220, 20, 60)         # Izquierda / Sangre / Error
VERDE = (34, 139, 34)        # Esperanza / Votante / Dólares
AZUL_POLICIA = (0, 0, 150)
GRIS_CALLE = (100, 100, 100)
DORADO = (255, 215, 0)       # Coima

# Configuración Pygame
pygame.init()
pygame.mixer.init()
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Camino a la Presidencia")
RELOJ = pygame.time.Clock()