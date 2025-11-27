import pygame
import random
import sys
from config import *
from utils import *

class BotonDebate:
    def __init__(self, txt, x, y, tipo, color):
        self.rect = pygame.Rect(x, y, 200, 60)
        self.texto = txt; self.tipo = tipo; self.color = color
    
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect, border_radius=10)
        mostrar_texto(pantalla, self.texto, 28, self.rect.x+20, self.rect.y+20)
    
    def clic(self, pos): return self.rect.collidepoint(pos)

def ejecutar_nivel():
    musica = cargar_sonido("noticiero_intro.mp3")
    if musica: musica.play(-1)

    botones = [
        BotonDebate("TERRUQUEO", 50, 450, "TERRUQUEO", ROJO),
        BotonDebate("PROPUESTA", 300, 450, "PROPUESTA", AZUL_POLICIA),
        BotonDebate("VICTIMA", 550, 450, "VICTIMA", (150, 50, 150))
    ]
    
    votos_p, votos_r = 50, 50
    turno = True
    msg = "Tu turno. Elige estrategia."
    timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                if musica: musica.stop()
                return "GANASTE"
            
            if event.type == pygame.MOUSEBUTTONDOWN and turno and timer == 0:
                for btn in botones:
                    if btn.clic(pygame.mouse.get_pos()):
                        rival = random.choice(["TERRUQUEO", "PROPUESTA", "VICTIMA"])
                        # Lógica Piedra Papel Tijera
                        win = False
                        if (btn.tipo == "TERRUQUEO" and rival == "PROPUESTA") or \
                           (btn.tipo == "PROPUESTA" and rival == "VICTIMA") or \
                           (btn.tipo == "VICTIMA" and rival == "TERRUQUEO"):
                            win = True
                        
                        if btn.tipo == rival:
                            msg = "¡Empate! Nadie gana votos."
                        elif win:
                            votos_p += 15; votos_r -= 15; msg = f"¡Ganaste! {btn.tipo} vence a {rival}"
                        else:
                            votos_p -= 15; votos_r += 15; msg = f"¡Perdiste! {rival} vence a {btn.tipo}"
                        
                        turno = False; timer = 120

        if timer > 0:
            timer -= 1
            if timer == 0: turno = True; msg = "Tu turno..."

        PANTALLA.fill((20, 20, 60)) # Fondo estudio TV
        
        # Barras
        pygame.draw.rect(PANTALLA, NARANJA, (20, 20, int(votos_p/100 * 760), 40))
        mostrar_texto(PANTALLA, f"TÚ: {votos_p}%", 30, 30, 25)
        mostrar_texto(PANTALLA, msg, 40, 50, 350, DORADO)

        if turno:
            for b in botones: b.dibujar(PANTALLA)

        if votos_p >= 80: 
            if musica: musica.stop()
            return "GANASTE"
        if votos_p <= 20: 
            if musica: musica.stop()
            return "PERDISTE"

        pygame.display.flip()
        RELOJ.tick(FPS)