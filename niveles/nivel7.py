import pygame
import random
import sys
from config import *
from utils import *

class Objetivo(pygame.sprite.Sprite):
    def __init__(self, es_terna, spawn_pos):
        super().__init__()
        self.es_terna = es_terna
        self.estado = "SUBIENDO" # SUBIENDO, ESPERANDO, BAJANDO
        
        if self.es_terna:
            self.image = cargar_imagen("terna.png", (80, 120), (50, 50, 50))
            # Marca visual de fallback
            if "terna" not in self.image.get_at((0,0)): 
                 pygame.draw.rect(self.image, NEGRO, (20, 20, 40, 40)) # Capucha oscura
        else:
            self.image = cargar_imagen("protestante.png", (80, 120), (200, 200, 200))
             # Marca visual de fallback
            if "protestante" not in self.image.get_at((0,0)):
                 pygame.draw.rect(self.image, BLANCO, (10, 10, 60, 30)) # Cartel blanco

        self.rect = self.image.get_rect()
        # Posición base (escondido abajo)
        self.base_y = spawn_pos[1]
        self.rect.x = spawn_pos[0]
        self.rect.y = self.base_y
        
        self.altura_max = self.base_y - 130
        self.velocidad = 5
        self.timer_espera = 0
        self.tiempo_espera_max = random.randint(30, 60) # Frames que espera arriba

    def update(self):
        if self.estado == "SUBIENDO":
            self.rect.y -= self.velocidad
            if self.rect.y <= self.altura_max:
                self.rect.y = self.altura_max
                self.estado = "ESPERANDO"
                
        elif self.estado == "ESPERANDO":
            self.timer_espera += 1
            if self.timer_espera >= self.tiempo_espera_max:
                self.estado = "BAJANDO"
                
        elif self.estado == "BAJANDO":
            self.rect.y += self.velocidad
            if self.rect.y >= self.base_y:
                self.kill() # Se escondió de nuevo

def ejecutar_nivel():
    # Ocultar el cursor real y usar la mira
    pygame.mouse.set_visible(False)
    img_mira = cargar_imagen("mira.png", (40, 40), ROJO)
    mira_rect = img_mira.get_rect()
    
    # Sonidos
    snd_disparo = cargar_sonido("disparo_gas.wav")
    snd_acierto = cargar_sonido("grito_impacto.wav")
    snd_error_terna = cargar_sonido("radio_policia.wav")
    
    objetivos = pygame.sprite.Group()
    
    # Puntos de aparición (detrás de "barricadas" imaginarias en la parte baja)
    spawn_points = [(100, ALTO), (300, ALTO), (500, ALTO), (700, ALTO)]
    
    puntaje = 0
    meta_puntaje = 150 # Puntos necesarios para "pacificar"
    tiempo = 45
    start = pygame.time.get_ticks()
    
    timer_spawn = 0
    
    feedback_txt = ""
    feedback_timer = 0
    feedback_color = BLANCO

    while True:
        restante = tiempo - (pygame.time.get_ticks() - start) / 1000
        mira_pos = pygame.mouse.get_pos()
        mira_rect.center = mira_pos
        
        # Spawner
        timer_spawn += 1
        if timer_spawn > 30 and len(objetivos) < 3: # Máximo 3 en pantalla
            es_terna = random.random() < 0.3 # 30% chance de Terna
            pos = random.choice(spawn_points)
            # Verificar que no haya otro en esa posición exacta
            ocupado = any(o.rect.x == pos[0] for o in objetivos)
            if not ocupado:
                objetivos.add(Objetivo(es_terna, pos))
                timer_spawn = 0
                # Aumentar dificultad con el tiempo
                if restante < 20: timer_spawn = 15

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F1: 
                pygame.mouse.set_visible(True); return "GANASTE"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if snd_disparo: snd_disparo.play()
                # Chequear impacto
                # Usamos collidepoint con la posición del mouse
                impactos = [obj for obj in objetivos if obj.rect.collidepoint(mira_pos)]
                
                if impactos:
                    # Solo le damos al primero que esté al frente (por si se solapan)
                    obj = impactos[0]
                    if not obj.es_terna:
                        # Acierto a manifestante
                        puntaje += 10
                        feedback_txt = "+10 PACIFICACIÓN"; feedback_color = VERDE
                        if snd_acierto: snd_acierto.play()
                    else:
                        # Error: Terna
                        puntaje -= 30 # Castigo severo
                        feedback_txt = "¡CUIDADO! ¡ES TERNA! (-30)"; feedback_color = ROJO
                        if snd_error_terna: snd_error_terna.play()
                    
                    obj.kill() # Desaparece al ser golpeado
                    feedback_timer = 30
                else:
                    # Fallo al aire
                    puntaje -= 1
                    feedback_txt = "FALLO (-1)"; feedback_color = GRIS_CALLE
                    feedback_timer = 15

        # Update
        objetivos.update()
        if feedback_timer > 0: feedback_timer -= 1

        # DRAW
        PANTALLA.fill((30, 30, 50)) # Fondo oscuro base
        fondo = cargar_imagen("fondo_plaza_humo.png", (ANCHO, ALTO), (30,30,50))
        PANTALLA.blit(fondo, (0,0))
        
        # Dibujar objetivos (Detrás de la "niebla" del fondo si tuviera transparencia)
        objetivos.draw(PANTALLA)
        
        # Dibujar elementos del primer plano (barricadas para tapar el spawn)
        pygame.draw.rect(PANTALLA, (20, 20, 20), (0, ALTO - 50, ANCHO, 50))

        # Dibujar Mira (Siempre al final para estar encima de todo)
        PANTALLA.blit(img_mira, mira_rect)

        # UI
        pygame.draw.rect(PANTALLA, NEGRO, (0,0, ANCHO, 60))
        mostrar_texto(PANTALLA, f"Puntaje de Orden: {puntaje}/{meta_puntaje}", 30, 20, 20, NARANJA)
        mostrar_texto(PANTALLA, f"Tiempo: {int(restante)}", 30, ANCHO - 150, 20)
        
        if feedback_timer > 0:
            mostrar_texto(PANTALLA, feedback_txt, 25, mira_pos[0]+20, mira_pos[1]-20, feedback_color)

        # Condiciones
        if puntaje >= meta_puntaje:
            pygame.mouse.set_visible(True) # Restaurar cursor
            return "GANASTE"
        
        if restante <= 0:
            pygame.mouse.set_visible(True) # Restaurar cursor
            return "PERDISTE"
            
        pygame.display.flip()
        RELOJ.tick(FPS)