import pygame
import random
import sys
from config import *
from utils import *
import math

class Region(pygame.sprite.Sprite):
    def __init__(self, nombre, x, y, ancho, alto):
        super().__init__()
        self.nombre = nombre
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.votos = 50.0  # Empieza en 50% (Empate técnico)
        self.color = GRIS_CALLE
        
        # El rival ataca con distinta fuerza según la región
        # En la Sierra el rival (Lápiz) es más fuerte
        if nombre == "SIERRA": self.fuerza_rival = 0.15
        elif nombre == "SELVA": self.fuerza_rival = 0.10
        else: self.fuerza_rival = 0.05 # COSTA

    def update(self):
        # El rival siempre está haciendo campaña (bajan tus votos)
        self.votos -= self.fuerza_rival
        
        # Límites (0% a 100%)
        if self.votos < 0: self.votos = 0
        if self.votos > 100: self.votos = 100
        
        # Cambiar color según quién va ganando
        if self.votos > 50:
            # Se pone Naranja (Tu partido)
            intensidad = min(255, int(self.votos * 2.5))
            self.color = (255, 140, 0) # Naranja puro
        else:
            # Se pone Rojo (El rival)
            intensidad = min(255, int((100 - self.votos) * 2.5))
            self.color = (220, 20, 60) # Rojo

    def recibir_taper(self):
        # Al recibir taper, suben los votos drásticamente
        self.votos += 15
        if self.votos > 100: self.votos = 100

    def dibujar(self, pantalla):
        # Dibujar el recuadro de la región
        pygame.draw.rect(pantalla, self.color, self.rect, border_radius=15)
        pygame.draw.rect(pantalla, BLANCO, self.rect, 3, border_radius=15)
        
        # Texto de estado
        mostrar_texto(pantalla, self.nombre, s(24), self.rect.x + s(12), self.rect.y + s(12), BLANCO)
        mostrar_texto(pantalla, f"{int(self.votos)}%", s(36), self.rect.centerx - s(20), self.rect.centery - s(10), BLANCO)

class TaperVolador(pygame.sprite.Sprite):
    def __init__(self, target_pos):
        super().__init__()
        tamaño = s(40)
        self.image = cargar_imagen("taper.png", (tamaño, tamaño), NARANJA)
        self.rect = self.image.get_rect()
        # Sale desde abajo (Lima/Capital)
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO

        self.target = target_pos
        self.velocidad = 15

    def update(self):
        # Moverse hacia el objetivo
        dx = self.target[0] - self.rect.centerx
        dy = self.target[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        
        if dist < 10:
            self.kill() # Llegó
        else:
            self.rect.x += (dx / dist) * self.velocidad
            self.rect.y += (dy / dist) * self.velocidad

def ejecutar_nivel():
    # Sonidos
    snd_camion = cargar_sonido("taper.mp3")
    snd_moneda = cargar_sonido("punto.mp3")
    
    # Definir Regiones (Simulando un mapa)
    # Costa (Izquierda), Sierra (Centro), Selva (Derecha)
    # Posiciones escalables basadas en proporciones (basado en 800x600 referencia)
    regiones = [
        Region("COSTA", sx(0.0625), sy(0.1667), sx(0.25), sy(0.5)),
        Region("SIERRA", sx(0.35), sy(0.1667), sx(0.25), sy(0.5)),
        Region("SELVA", sx(0.6375), sy(0.1667), sx(0.25), sy(0.5))
    ]
    
    tapers_group = pygame.sprite.Group()
    
    presupuesto = 1000 # Millones de soles
    costo_taper = 50
    tiempo = 30 # Segundos para cerrar mesas
    start = pygame.time.get_ticks()
    
    mensaje = "¡Reparte tapers antes de que gane el Lápiz!"

    while True:
        restante = tiempo - (pygame.time.get_ticks() - start) / 1000
        
        # Calcular promedio nacional
        promedio_votos = sum([r.votos for r in regiones]) / 3
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F1: return "GANASTE"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Verificar clic en región
                for reg in regiones:
                    if reg.rect.collidepoint(pos):
                        if presupuesto >= costo_taper:
                            presupuesto -= costo_taper
                            reg.recibir_taper()
                            tapers_group.add(TaperVolador(reg.rect.center))
                            if snd_camion: snd_camion.play()
                        else:
                            mensaje = "¡No hay plata! (Pide a Odebrecht)"
                            if snd_moneda: snd_moneda.play() # Sonido error

        # Updates
        for reg in regiones: reg.update()
        tapers_group.update()
        
        # Regenerar presupuesto (Lavado de activos pasivo)
        if random.random() < 0.05: 
            presupuesto += 5
        
        # Dibujar
        PANTALLA.fill((40, 40, 40)) # Fondo oscuro mapa
        
        # Dibujar regiones
        for reg in regiones: reg.dibujar(PANTALLA)
        tapers_group.draw(PANTALLA)

        # UI Superior
        pygame.draw.rect(PANTALLA, NEGRO, (0, 0, ANCHO, s(80)))
        mostrar_texto(PANTALLA, f"Presupuesto: S/. {presupuesto} M", s(20), s(20), s(12), VERDE)
        mostrar_texto(PANTALLA, f"Tiempo: {int(restante)}s", s(20), ANCHO - s(150), s(12), BLANCO)

        # Barra Promedio Nacional
        mostrar_texto(PANTALLA, "PROMEDIO NACIONAL:", s(18), sx(0.375), s(10))
        barra_x = sx(0.375)
        barra_y = s(35)
        barra_w = sx(0.25)
        barra_h = s(20)
        pygame.draw.rect(PANTALLA, ROJO, (barra_x, barra_y, barra_w, barra_h)) # Fondo Rojo
        ancho_naranja = int((promedio_votos / 100) * barra_w)
        pygame.draw.rect(PANTALLA, NARANJA, (barra_x, barra_y, ancho_naranja, barra_h)) # Barra Naranja

        mostrar_texto(PANTALLA, mensaje, s(20), s(20), ALTO - s(40), DORADO)

        # Condiciones Fin
        if restante <= 0:
            if promedio_votos >= 50:
                return "GANASTE"
            else:
                return "PERDISTE"

        pygame.display.flip()
        RELOJ.tick(FPS)