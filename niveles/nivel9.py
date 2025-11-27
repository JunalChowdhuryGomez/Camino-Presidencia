import os
import pygame
import random
import sys
from config import *
from utils import *

class AutoPresidencial(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Imagen del auto, escalada. Si no existe el asset, crear fallback
        path = os.path.join("assets", "carro.png")
        if os.path.exists(path):
            self.image = cargar_imagen("carro.png", (s(120), s(60)), NEGRO)
        else:
            self.image = pygame.Surface((s(120), s(60)), pygame.SRCALPHA)
            self.image.fill(NEGRO)
            pygame.draw.rect(self.image, (50, 50, 50), (s(10), s(10), s(100), s(40)))  # Ventanas

        self.rect = self.image.get_rect()
        self.rect.x = sx(0.08)  # posicion inicial proporcional
        self.base_y = ALTO - s(100)
        self.rect.bottom = self.base_y

        # Física escalada
        self.velocidad_y = 0
        self.gravedad = 0.8 * ui_scale()
        self.fuerza_salto = int(-15 * ui_scale())
        self.saltando = False

    def saltar(self):
        if not self.saltando:
            self.velocidad_y = self.fuerza_salto
            self.saltando = True
            return True
        return False

    def update(self):
        # Física de Salto
        self.velocidad_y += self.gravedad
        self.rect.y += self.velocidad_y
        
        # Piso
        if self.rect.bottom >= self.base_y:
            self.rect.bottom = self.base_y
            self.velocidad_y = 0
            self.saltando = False

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, tipo, velocidad_scroll):
        super().__init__()
        self.tipo = tipo # 0: Miguelito (Chico), 1: Fiscal (Medio), 2: Patrulla (Grande)
        
        if tipo == 0: # Miguelito
            path = os.path.join("assets", "obs_miguelito.png")
            if os.path.exists(path):
                self.image = cargar_imagen("obs_miguelito.png", (s(40), s(40)), (200, 200, 200))
            else:
                self.image = pygame.Surface((s(40), s(40)), pygame.SRCALPHA)
                self.image.fill((200,200,200))
                pygame.draw.polygon(self.image, (150,150,150), [(0, s(40)), (s(20), 0), (s(40), s(40))])
            self.rect = self.image.get_rect()
            self.rect.bottom = ALTO - s(80) # Pegado al suelo
            
        elif tipo == 1: # Fiscal
            path = os.path.join("assets", "obs_fiscal.png")
            if os.path.exists(path):
                self.image = cargar_imagen("obs_fiscal.png", (s(50), s(90)), AZUL_POLICIA)
            else:
                self.image = pygame.Surface((s(50), s(90)), pygame.SRCALPHA)
                self.image.fill(AZUL_POLICIA)
            self.rect = self.image.get_rect()
            self.rect.bottom = ALTO - s(80)
            
        else: # Patrulla
            path = os.path.join("assets", "camionetapolicia.png")
            if os.path.exists(path):
                self.image = cargar_imagen("camionetapolicia.png", (s(100), s(60)), BLANCO)
            else:
                self.image = pygame.Surface((s(100), s(60)), pygame.SRCALPHA)
                self.image.fill(BLANCO)
                pygame.draw.rect(self.image, VERDE, (0, s(20), s(100), s(10)))  # Franja policial
            self.rect = self.image.get_rect()
            self.rect.bottom = ALTO - s(80)

        # Posición inicial y velocidad horizontal (escaladas)
        self.rect.x = ANCHO + random.randint(0, int(100 * ui_scale()))
        self.velocidad = velocidad_scroll * ui_scale()

    

    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            self.kill()

def ejecutar_nivel():
    snd_sirena = cargar_sonido("sirena_policia.wav")
    snd_choque = cargar_sonido("choque.wav")
    snd_salto = cargar_sonido("salto.wav")
    
    if snd_sirena: 
        snd_sirena.set_volume(0.4)
        snd_sirena.play(-1) # Loop fondo

    jugador = AutoPresidencial()
    obstaculos = pygame.sprite.Group()
    todos = pygame.sprite.Group()
    todos.add(jugador)
    
    distancia = 0
    meta_distancia = 1000  # Metros para llegar a la embajada
    velocidad_juego = 8 * ui_scale()  # Velocidad inicial escalada
    
    start_ticks = pygame.time.get_ticks()
    timer_spawn = 0
    
    fondo = cargar_imagen("carretera.jpg", (ANCHO, ALTO), (200, 180, 140)) # Color arena
    
    while True:
        # Aumentar dificultad progresiva
        distancia += 1 + (velocidad_juego / 20)
        
        # Cada 500 puntos de distancia, acelera
        if distancia % 500 < 5: 
            velocidad_juego += 0.01

        # Generar obstaculos
        timer_spawn += 1
        # Random spawn rate basado en velocidad (a más rápido, aparecen más seguido)
        spawn_threshold = max(int(30 * ui_scale()), 100 - int(velocidad_juego * 2))
        if timer_spawn > spawn_threshold:
            timer_spawn = 0
            tipo = random.choice([0, 0, 1, 2])  # Más probabilidad de miguelitos
            obs = Obstaculo(tipo, velocidad_juego)
            obstaculos.add(obs)
            todos.add(obs)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1: 
                    if snd_sirena: snd_sirena.stop()
                    return "GANASTE"
                
                if event.key == pygame.K_SPACE:
                    if jugador.saltar():
                        if snd_salto: snd_salto.play()

        # Update
        todos.update()
        
        # Colisiones
        if pygame.sprite.spritecollide(jugador, obstaculos, False):
            if snd_choque: snd_choque.play()
            if snd_sirena: snd_sirena.stop()
            pygame.time.wait(1000) # Pausa dramática
            return "PERDISTE"

        # Draw
        # Efecto Parallax simple (Fondo estático o moviéndose si tienes una imagen larga)
        PANTALLA.blit(fondo, (0,0))

        # Carretera
        pygame.draw.rect(PANTALLA, (50, 50, 50), (0, ALTO - s(80), ANCHO, s(80)))  # Pista
        pygame.draw.line(PANTALLA, (255, 255, 0), (0, ALTO - s(40)), (ANCHO, ALTO - s(40)), s(4))  # Linea amarilla

        todos.draw(PANTALLA)

        # UI
        mostrar_texto(PANTALLA, f"DISTANCIA A LA EMBAJADA: {int(meta_distancia - distancia)} m", s(20), s(20), s(20), ROJO)

        # Meta
        if distancia >= meta_distancia:
            if snd_sirena: snd_sirena.stop()
            return "GANASTE"

        pygame.display.flip()
        RELOJ.tick(FPS)