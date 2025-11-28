import pygame
import random
import sys
from config import *
from utils import *

class Candidato(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cargar_imagen("candidato.png", (250, 250), NARANJA)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 50
        self.velocidad = 15
        self.cooldown_soborno = 0

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
        if self.cooldown_soborno > 0:
            self.cooldown_soborno -= 1

class Peaton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        es_policia = random.random() < 0.30
        if es_policia:
            self.tipo = "policia"
            self.image = cargar_imagen("policia.png", (250, 250), AZUL_POLICIA)
            self.velocidad = 12
        else:
            self.tipo = "ciudadano"
            self.image = cargar_imagen("peruano.png", (250, 250), VERDE)
            self.velocidad = 10
        
        self.rect = self.image.get_rect()
        if random.choice([True, False]):
            self.rect.x = -50; self.direccion = 1
        else:
            self.rect.x = ANCHO + 50; self.direccion = -1
        self.rect.bottom = ALTO - 50 + random.randint(-20, 20)

    def update(self):
        self.rect.x += self.velocidad * self.direccion
        if self.rect.right < -100 or self.rect.left > ANCHO + 100:
            self.kill()

def ejecutar_nivel():
    snd_firma = cargar_sonido("firma.mp3")
    snd_policia = cargar_sonido("error.mp3")
    
    jugador = Candidato()
    peatones = pygame.sprite.Group()
    todos = pygame.sprite.Group()
    todos.add(jugador)

    firmas = 0
    meta = 10
    tiempo_limite = 40
    start_ticks = pygame.time.get_ticks()
    mensaje_feedback, timer_feedback = "", 0

    while True:
        tiempo_restante = tiempo_limite - (pygame.time.get_ticks() - start_ticks) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1: return "GANASTE"
                if event.key == pygame.K_SPACE and jugador.cooldown_soborno == 0:
                    # Obtener todos los peatones en colisión pero no matarlos aún
                    hits = pygame.sprite.spritecollide(jugador, peatones, False)
                    if hits:
                        jugador.cooldown_soborno = 30
                        # Elegir el peatón que esté visualmente al frente (mayor rect.bottom)
                        p = max(hits, key=lambda q: q.rect.bottom)
                        # Eliminar solamente al seleccionado
                        p.kill()
                        if p.tipo == "ciudadano":
                            firmas += 1
                            mensaje_feedback = "+1 FIRMA"
                            timer_feedback = 30
                            if snd_firma: snd_firma.play()
                        else:
                            firmas -= 2
                            mensaje_feedback = "¡POLICÍA!"
                            timer_feedback = 60
                            if snd_policia: snd_policia.play()
        
        todos.update()
        if random.random() < 0.03:
            p = Peaton(); peatones.add(p); todos.add(p)

        fondo = cargar_imagen("fondo_calle.png", (ANCHO, ALTO), GRIS_CALLE)
        PANTALLA.blit(fondo, (0,0))
        todos.draw(PANTALLA)
        
        mostrar_texto(PANTALLA, f"Firmas: {firmas}/{meta}", 40, 20, 20)
        mostrar_texto(PANTALLA, f"Tiempo: {int(tiempo_restante)}s", 40, ANCHO-200, 20)
        
        if timer_feedback > 0:
            mostrar_texto(PANTALLA, mensaje_feedback, 30, jugador.rect.x, jugador.rect.y-40, ROJO if "POLICÍA" in mensaje_feedback else VERDE)
            timer_feedback -= 1

        if firmas >= meta: return "GANASTE"
        if tiempo_restante <= 0: return "PERDISTE"
        
        pygame.display.flip()
        RELOJ.tick(FPS)