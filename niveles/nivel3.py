import pygame
import random
import sys
from config import *
from utils import *

class BotonDebate:
    def __init__(self, txt, x, y, tipo, color, w=200, h=60):
        self.rect = pygame.Rect(x, y, w, h)
        self.w = w; self.h = h
        self.texto = txt; self.tipo = tipo; self.color = color
    
    def dibujar(self, pantalla, font_size=28):
        pygame.draw.rect(pantalla, self.color, self.rect, border_radius=10)
        # Centrar texto dentro del botón con un pequeño padding
        texto_x = self.rect.x + int(self.w * 0.08)
        texto_y = self.rect.y + int(self.h * 0.18)
        mostrar_texto(pantalla, self.texto, font_size, texto_x, texto_y)
    
    def clic(self, pos): return self.rect.collidepoint(pos)

def ejecutar_nivel():
    musica = cargar_sonido("noticiero_intro.mp3")
    if musica: musica.play(-1)
    # Escala UI según resolución
    scale = min(ANCHO / 800, ALTO / 600)
    btn_w = int(max(160, ANCHO * 0.22))
    btn_h = int(max(48, 60 * scale))
    btn_y = ALTO - int(ALTO * 0.18)
    gap = int(ANCHO * 0.08)
    start_x = (ANCHO - (3 * btn_w + 2 * gap)) // 2

    botones = [
        BotonDebate("TERRUQUEO", start_x, btn_y, "TERRUQUEO", ROJO, btn_w, btn_h),
        BotonDebate("PROPUESTA", start_x + (btn_w + gap), btn_y, "PROPUESTA", AZUL_POLICIA, btn_w, btn_h),
        BotonDebate("VICTIMA", start_x + 2 * (btn_w + gap), btn_y, "VICTIMA", (150, 50, 150), btn_w, btn_h)
    ]
    
    votos_p, votos_r = 50, 50
    turno = True
    msg = "Tu turno. Elige estrategia."
    timer = 0
    # Última elección del rival (para mostrar en pantalla)
    ultima_eleccion_rival = None
    # Mapa de colores por tipo para mostrar un indicador
    tipo_color = {b.tipo: b.color for b in botones}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                if musica: musica.stop()
                return "GANASTE"

            if event.type == pygame.MOUSEBUTTONDOWN and turno and timer == 0:
                for btn in botones:
                    if btn.clic(pygame.mouse.get_pos()):
                        rival = random.choice(["TERRUQUEO", "PROPUESTA", "VICTIMA"])
                        ultima_eleccion_rival = rival
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

                        turno = False; timer = int(120 * scale)

        if timer > 0:
            timer -= 1
            if timer == 0:
                turno = True
                msg = "Tu turno..."
                # limpiar la indicación del rival al volver al turno del jugador
                ultima_eleccion_rival = None

        PANTALLA.fill((20, 20, 60)) # Fondo estudio TV

        # Barras (escalables)
        bar_h = max(24, int(40 * scale))
        bar_w_total = ANCHO - 40
        pygame.draw.rect(PANTALLA, NARANJA, (20, 20, int(votos_p/100 * bar_w_total), bar_h))
        mostrar_texto(PANTALLA, f"TÚ: {votos_p}%", max(16, int(30 * scale)), 30, 20)
        mostrar_texto(PANTALLA, msg, max(20, int(40 * scale)), 50, int(ALTO * 0.45), DORADO)

        # Mostrar elección del rival cuando está visible (durante el turno de resolución)
        if not turno and ultima_eleccion_rival:
            panel_w = int(250 * scale)
            panel_h = int(80 * scale)
            x = ANCHO - panel_w - 20
            y = 20
            # cuadro de fondo para destacar
            pygame.draw.rect(PANTALLA, (10,10,30), (x-10, y-10, panel_w, panel_h), border_radius=8)
            # indicador de color según tipo
            color = tipo_color.get(ultima_eleccion_rival, BLANCO)
            pygame.draw.rect(PANTALLA, color, (x, y, int(60 * scale), int(60 * scale)), border_radius=8)
            mostrar_texto(PANTALLA, "RIVAL", max(14, int(24 * scale)), x+int(75 * scale), y+int(6 * scale))
            mostrar_texto(PANTALLA, ultima_eleccion_rival, max(12, int(22 * scale)), x+int(75 * scale), y+int(36 * scale))

        if turno:
            for b in botones: b.dibujar(PANTALLA, max(12, int(24 * scale)))

        if votos_p >= 80: 
            if musica: musica.stop()
            return "GANASTE"
        if votos_p <= 20: 
            if musica: musica.stop()
            return "PERDISTE"

        pygame.display.flip()
        RELOJ.tick(FPS)