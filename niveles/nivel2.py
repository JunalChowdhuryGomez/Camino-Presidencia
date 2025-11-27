import pygame
import random
import math
import sys
from config import *
from utils import *

class Promesa(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo # 0, 1, 2
        colores = [DORADO, ROJO, NEGRO]
        imgs = ["icon_dinero.png", "icon_comida.png", "icon_bala.png"]
        self.image = cargar_imagen(imgs[tipo], (60, 60), colores[tipo])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, ANCHO - 100)
        self.rect.y = -50
        self.velocidad = 5

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

    while True:
        restante = tiempo - (pygame.time.get_ticks() - start) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1: 
                    if musica: musica.stop()
                    return "GANASTE"
                
                if event.key in mapa_teclas:
                    tipo = mapa_teclas[event.key]
                    hit = False
                    for p in promesas:
                        if p.tipo == tipo and p.rect.y > ALTO//2:
                            p.kill(); hit = True; euforia += 5
                            break
                    if not hit: euforia -= 5

        promesas.update()
        if random.random() < 0.03:
            promesas.add(Promesa(random.randint(0,2)))
        
        # Verificar caídas
        for p in promesas:
            if p.rect.top >= ALTO:
                p.kill(); euforia -= 10

        fondo = cargar_imagen("fondo_mitin.png", (ANCHO, ALTO), (20,0,50))
        PANTALLA.blit(fondo, (0,0))
        promesas.draw(PANTALLA)
        
        # Barra UI
        pygame.draw.rect(PANTALLA, GRIS_CALLE, (ANCHO//2-150, 50, 300, 30))
        pygame.draw.rect(PANTALLA, VERDE if euforia > 50 else ROJO, (ANCHO//2-150, 50, 3 * euforia, 30))
        mostrar_texto(PANTALLA, f"Euforia: {euforia}%", 30, ANCHO//2-60, 55, BLANCO)
        
        # Guía
        mostrar_texto(PANTALLA, "← PLATA  |  ↓ COMIDA  |  MANO DURA →", 30, 150, ALTO-50)

        if euforia <= 0: 
            if musica: musica.stop()
            return "PERDISTE"
        if restante <= 0:
            if musica: musica.stop()
            return "GANASTE"

        pygame.display.flip()
        RELOJ.tick(FPS)