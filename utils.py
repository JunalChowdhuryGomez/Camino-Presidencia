import pygame
import os
import sys
from config import *

# Función para cargar imágenes de forma segura
def cargar_imagen(nombre, tamaño, color_fallback):
    # Asume que 'assets' está en la carpeta raíz
    ruta = os.path.join("assets", nombre)
    try:
        img = pygame.image.load(ruta).convert_alpha()
        img = pygame.transform.scale(img, tamaño)
        return img
    except FileNotFoundError:
        # Crea un cuadrado de color si no existe la imagen
        surf = pygame.Surface(tamaño)
        surf.fill(color_fallback)
        return surf

# Función para cargar sonidos
def cargar_sonido(nombre):
    ruta = os.path.join("assets", nombre)
    try:
        return pygame.mixer.Sound(ruta)
    except FileNotFoundError:
        return None

# Función para mostrar texto rápido
def mostrar_texto(pantalla, texto, tamaño, x, y, color=BLANCO):
    fuente = pygame.font.Font(None, tamaño)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect()
    rect.topleft = (x, y)
    pantalla.blit(superficie, rect)

# Pantalla de Introducción genérica para todos los niveles
def pantalla_intro(nivel, titulo, descripcion):
    intro = True
    fondo = cargar_imagen(f"intro_n{nivel}.png", (ANCHO, ALTO), NEGRO)
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                if event.key == pygame.K_F1: 
                    return "SKIP"

        PANTALLA.blit(fondo, (0,0))
        
        # Sombra del texto para que se lea mejor
        mostrar_texto(PANTALLA, titulo, 60, 52, ALTO//2 - 48, NEGRO) 
        mostrar_texto(PANTALLA, titulo, 60, 50, ALTO//2 - 50, NARANJA)
        
        mostrar_texto(PANTALLA, descripcion, 30, 50, ALTO//2 + 20)
        mostrar_texto(PANTALLA, "[ESPACIO] Jugar  -  [F1] Saltar Nivel", 25, 50, ALTO - 50, DORADO)
        
        pygame.display.flip()
        RELOJ.tick(15)
    return "JUGAR"