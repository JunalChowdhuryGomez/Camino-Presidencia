import pygame
import random
import math
import sys
from config import *
from utils import *

class Promesa(pygame.sprite.Sprite):
    def __init__(self, tipo, tamaño):
        super().__init__()
        self.tipo = tipo # 0, 1, 2
        colores = [DORADO, ROJO, NEGRO]
        imgs = ["soles.png", "comida.png", "bala.png"]
        self.image = cargar_imagen(imgs[tipo], (tamaño, tamaño), colores[tipo])
        self.rect = self.image.get_rect()
        # Posición X se asignará desde el nivel (columnas calculadas dinámicamente)
        self.rect.centerx = 0
        # Empiezan desde arriba
        self.rect.y = -tamaño
        # Velocidad basada en tamaño/pantalla para consistencia en distintas resoluciones
        self.velocidad = max(3, tamaño // 12)

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO: self.kill()

def ejecutar_nivel():
    musica = cargar_sonido("cumbia_fondo.mp3")
    if musica: musica.play(-1)
    
    promesas = pygame.sprite.Group()
    euforia = 50
    tiempo = 45
    start = pygame.time.get_ticks()
    mapa_teclas = {pygame.K_LEFT: 0, pygame.K_DOWN: 1, pygame.K_RIGHT: 2}

    # Ajustes escalables según resolución
    promesa_tamaño = max(40, int(ANCHO * 0.06))
    spacing = int(ANCHO * 0.12)
    columnas = [ANCHO//2 - spacing, ANCHO//2, ANCHO//2 + spacing]

    # Prev keys para detectar pulsaciones nuevas (debounce simple)
    prev_keys = pygame.key.get_pressed()

    while True:
        restante = tiempo - (pygame.time.get_ticks() - start) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    if musica: musica.stop()
                    return "GANASTE"

        promesas.update()
        if random.random() < 0.03:
            p = Promesa(random.randint(0,2), promesa_tamaño)
            # asignar columna X según tipo
            p.rect.centerx = columnas[p.tipo]
            promesas.add(p)

        # Detección de teclas más fiable: detectar pulsaciones nuevas entre frames
        keys = pygame.key.get_pressed()
        # Zona de golpe proporcional
        HIT_TOP = ALTO - int(ALTO * 0.25)
        HIT_BOTTOM = ALTO - int(ALTO * 0.08)

        # Para cada tecla mapeada, si fue pulsada en este frame (y no en prev), procesar
        for key, tipo in mapa_teclas.items():
            if keys[key] and not prev_keys[key]:
                hit = False
                # Priorizar la promesa más baja (más cercana a la zona)
                candidatos = sorted([p for p in promesas if p.tipo == tipo], key=lambda x: x.rect.centery, reverse=True)
                for p in candidatos:
                    cy = p.rect.centery
                    if HIT_TOP <= cy <= HIT_BOTTOM:
                        p.kill()
                        hit = True
                        euforia += 5
                        break
                if not hit:
                    euforia -= 5
        prev_keys = keys
        
        # Verificar caídas
        for p in promesas:
            if p.rect.top >= ALTO:
                p.kill(); euforia -= 10

        fondo = cargar_imagen("miting.jpg", (ANCHO, ALTO), (20,0,50))
        PANTALLA.blit(fondo, (0,0))
        promesas.draw(PANTALLA)
        # Dibujar las dianas/targets donde caen las promesas (para guiar al jugador)
        for i, cx in enumerate(columnas):
            pygame.draw.rect(PANTALLA, GRIS_CALLE, (cx - promesa_tamaño//2, ALTO - 100, promesa_tamaño, 10))
        # Etiquetas de control sobre cada columna
        labels = ["← PLATA", "↓ COMIDA", "→ MANO DURA"]
        for i, cx in enumerate(columnas):
            mostrar_texto(PANTALLA, labels[i], 22, cx - promesa_tamaño//2, ALTO - 140, BLANCO)

        # Instrucciones generales
        mostrar_texto(PANTALLA, "Presiona ←  ·  ↓  ·  → para golpear las promesas en su carril", 22, ANCHO//2 - 320, 100, DORADO)
        
        # Barra UI
        pygame.draw.rect(PANTALLA, GRIS_CALLE, (ANCHO//2-150, 50, 300, 30))
        pygame.draw.rect(PANTALLA, VERDE if euforia > 50 else ROJO, (ANCHO//2-150, 50, 3 * euforia, 30))
        mostrar_texto(PANTALLA, f"Euforia: {euforia}%", 30, ANCHO//2-60, 55, BLANCO)
        
        # Guía (usar flechas Unicode en lugar de emojis para mejor compatibilidad en Linux/pygame)
        mostrar_texto(PANTALLA, " ← PLATA  |  ↓ COMIDA  |  MANO DURA →", 30, 150, ALTO-50)

        if euforia <= 0: 
            if musica: musica.stop()
            return "PERDISTE"
        if restante <= 0:
            if musica: musica.stop()
            return "GANASTE"

        pygame.display.flip()
        RELOJ.tick(FPS)