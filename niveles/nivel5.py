import pygame
import random
import sys
from config import *
from utils import *

class Acta(pygame.sprite.Sprite):
    def __init__(self, es_mia):
        super().__init__()
        self.es_mia = es_mia # True (Naranja) o False (Rival)
        
        if self.es_mia:
            self.image = cargar_imagen("acta_naranja.png", (100, 140), (255, 200, 150))
            # Dibujamos una marquita naranja si no hay imagen
            if "acta_naranja" not in self.image.get_at((0,0)): # Fallback visual simple
                pygame.draw.circle(self.image, NARANJA, (50, 70), 20)
        else:
            self.image = cargar_imagen("acta_roja.png", (100, 140), (200, 200, 200))
            # Marquita roja
            if "acta_roja" not in self.image.get_at((0,0)):
                pygame.draw.circle(self.image, ROJO, (50, 70), 20)

        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.y = -150 # Empieza arriba fuera de pantalla
        self.velocidad = 7
        self.procesada = False

    def update(self):
        self.rect.y += self.velocidad

def ejecutar_nivel():
    # Sonidos
    snd_sello = cargar_sonido("sello.wav")
    snd_error = cargar_sonido("error.wav")
    
    actas_group = pygame.sprite.Group()
    
    # Variables de Juego
    votos_totales = 0
    votos_mios = 0 # Debes superar el 50% de los válidos
    tiempo = 40
    start = pygame.time.get_ticks()
    
    # Feedback visual
    sello_visual = None # (imagen, x, y, tiempo)
    mensaje_feedback = ""
    color_feedback = BLANCO
    
    # Ritmo de aparición
    timer_spawn = 0
    
    img_sello_ok = cargar_imagen("sello_ok.png", (120, 120), VERDE)
    img_sello_fail = cargar_imagen("sello_nulo.png", (120, 120), ROJO)

    while True:
        restante = tiempo - (pygame.time.get_ticks() - start) / 1000
        
        # Generar actas
        timer_spawn += 1
        if timer_spawn > 40: # Cada X frames sale una nueva
            es_mia = random.choice([True, False])
            nueva_acta = Acta(es_mia)
            actas_group.add(nueva_acta)
            timer_spawn = 0
            # Aumentar dificultad (más rápido) con el tiempo
            if restante < 20: timer_spawn = 10 

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1: return "GANASTE"
                
                # ZONA DE DECISIÓN
                # Solo interactuamos con el acta que esté más abajo y visible
                actas_visibles = [a for a in actas_group if a.rect.y > 0 and a.rect.y < ALTO - 50]
                # Ordenamos por Y (la que está más abajo es la prioritaria)
                actas_visibles.sort(key=lambda x: x.rect.y, reverse=True)
                
                if actas_visibles:
                    acta_actual = actas_visibles[0]
                    
                    accion = None
                    if event.key == pygame.K_LEFT: accion = "VALIDAR"
                    if event.key == pygame.K_RIGHT: accion = "IMPUGNAR"
                    
                    if accion:
                        if snd_sello: snd_sello.play()
                        
                        # LÓGICA DEL FRAUDE
                        es_acierto = False
                        
                        if accion == "VALIDAR":
                            sello_visual = (img_sello_ok, acta_actual.rect.x, acta_actual.rect.y, 20)
                            if acta_actual.es_mia:
                                es_acierto = True
                                votos_mios += 1
                                votos_totales += 1
                                mensaje_feedback = "¡VOTO SUMADO!"
                                color_feedback = VERDE
                            else:
                                # Validaste al rival (ERROR GRAVE)
                                es_acierto = False
                                votos_totales += 1 # Cuenta para el universo, pero no para ti
                                mensaje_feedback = "¡ERES UN INFILTRADO! (Voto al rival)"
                                color_feedback = ROJO
                                if snd_error: snd_error.play()

                        elif accion == "IMPUGNAR":
                            sello_visual = (img_sello_fail, acta_actual.rect.x, acta_actual.rect.y, 20)
                            if not acta_actual.es_mia:
                                # Impugnaste al rival (BIEN HECHO, FRAUDE EXITOSO)
                                es_acierto = True
                                # Al impugnar, reducimos el universo de votos del rival,
                                # lo que matemáticamente sube tu porcentaje.
                                mensaje_feedback = "¡Firma falsa detectada! (Anulado)"
                                color_feedback = NARANJA
                            else:
                                # Anulaste tu propio voto (ERROR)
                                es_acierto = False
                                mensaje_feedback = "¿POR QUÉ ANULAS LO TUYO?"
                                color_feedback = ROJO
                                if snd_error: snd_error.play()
                        
                        # Eliminar el acta procesada
                        acta_actual.kill()

        # Updates
        actas_group.update()
        
        # Si un acta se pasa sin procesar
        for a in actas_group:
            if a.rect.top > ALTO:
                a.kill()
                # Si se pasó una roja, cuenta para el rival
                if not a.es_mia:
                    votos_totales += 1
                    mensaje_feedback = "¡Se escapó un voto rojo!"
                    color_feedback = ROJO

        # DIBUJAR
        # Fondo: Mesa de madera
        PANTALLA.fill((100, 60, 20)) 
        
        # Faja transportadora (Gris oscuro al centro)
        pygame.draw.rect(PANTALLA, (50, 50, 50), (ANCHO//2 - 60, 0, 120, ALTO))
        
        # Zona de validación (Línea verde)
        pygame.draw.line(PANTALLA, VERDE, (0, ALTO - 150), (ANCHO, ALTO - 150), 2)
        mostrar_texto(PANTALLA, "ZONA DE SELLADO", 20, ANCHO//2 - 60, ALTO - 140)

        actas_group.draw(PANTALLA)
        
        # Dibujar Sello Visual (Efecto temporal)
        if sello_visual:
            img, x, y, frames = sello_visual
            PANTALLA.blit(img, (x, y))
            sello_visual = (img, x, y, frames - 1)
            if frames <= 1: sello_visual = None

        # UI
        # Instrucciones
        mostrar_texto(PANTALLA, "← VALIDAR (Izquierda)", 40, 50, ALTO//2, VERDE)
        mostrar_texto(PANTALLA, "IMPUGNAR (Derecha) →", 40, ANCHO - 350, ALTO//2, ROJO)
        
        # Cálculo de Porcentaje en Tiempo Real
        # Porcentaje = (Mis Votos / Votos Totales) * 100
        # Evitar división por cero
        if votos_totales > 0:
            porcentaje = (votos_mios / votos_totales) * 100
        else:
            porcentaje = 50.0 # Empate inicial

        pygame.draw.rect(PANTALLA, NEGRO, (0, 0, ANCHO, 80))
        mostrar_texto(PANTALLA, f"ACTAS PROCESADAS: {votos_mios}/{votos_totales}", 30, 20, 20)
        mostrar_texto(PANTALLA, f"TU PORCENTAJE: {porcentaje:.2f}%", 40, ANCHO//2 - 150, 20, NARANJA if porcentaje > 50.1 else ROJO)
        mostrar_texto(PANTALLA, f"Tiempo: {int(restante)}", 30, ANCHO - 120, 20)
        
        # Mensaje Feedback
        mostrar_texto(PANTALLA, mensaje_feedback, 30, ANCHO//2 - 150, ALTO - 50, color_feedback)

        # Condiciones Fin
        if restante <= 0:
            if porcentaje >= 50.1: # Ganas con 50% + 1
                return "GANASTE"
            else:
                return "PERDISTE"

        pygame.display.flip()
        RELOJ.tick(FPS)