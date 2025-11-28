import os
import pygame
import random
import sys
from config import *
from utils import *

class Congresista(pygame.sprite.Sprite):
    def __init__(self, x, y, es_jefe):
        super().__init__()
        self.es_jefe = es_jefe
        self.vida = 2 if es_jefe else 1 # El jefe necesita 2 sobornos
        # Cargar imagenes escaladas; si no existe el asset, crear un fallback Surface
        if self.es_jefe:
            path = os.path.join("assets", "Corrupto.png")
            if os.path.exists(path):
                self.image = cargar_imagen("Corrupto.png", (s(100), s(100)), (200, 0, 0))
            else:
                self.image = pygame.Surface((s(100), s(100)), pygame.SRCALPHA)
                self.image.fill((200, 0, 0))
                # Dibujar corona simple como fallback
                pygame.draw.circle(self.image, DORADO, (s(50), s(20)), s(10))
        else:
            path = os.path.join("assets", "Corrupto.png")
            if os.path.exists(path):
                self.image = cargar_imagen("Corrupto.png", (s(90), s(90)), (100, 100, 100))
            else:
                self.image = pygame.Surface((s(90), s(90)), pygame.SRCALPHA)
                self.image.fill((100, 100, 100))
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

        # Tiempo que permanece en pantalla antes de votar por vacancia (escalado)
        base_jefe = int(120 * ui_scale())
        base_regular = int(80 * ui_scale())
        self.tiempo_vida = base_jefe if es_jefe else base_regular
        self.max_tiempo = self.tiempo_vida

    def update(self):
        self.tiempo_vida -= 1
        if self.tiempo_vida <= 0:
            self.kill()
            return "VOTO_VACANCIA" # Retorna señal de daño
        return None

def ejecutar_nivel():
    # Ocultar cursor y poner billete
    pygame.mouse.set_visible(False)
    img_cursor = cargar_imagen("billetes.jpg", (s(50), s(50)), VERDE)
    cursor_rect = img_cursor.get_rect()
    
    snd_grito = cargar_sonido("vacancia_grito.wav")
    snd_soborno = cargar_sonido("kaching_soborno.wav")
    
    # Posiciones de los curules (Escaños) en el Hemiciclo (Coordenadas X, Y)
    # Usar porcentajes de ancho/alto para que escale bien
    posiciones = [
        (sx(0.125), sy(0.45)), (sx(0.375), sy(0.45)), (sx(0.625), sy(0.45)), # Fila Arriba
        (sx(0.09), sy(0.6)), (sx(0.25), sy(0.6)), (sx(0.45), sy(0.6)), (sx(0.65), sy(0.6)), # Fila Medio
        (sx(0.22), sy(0.78)), (sx(0.55), sy(0.78)) # Fila Abajo
    ]
    
    moles_group = pygame.sprite.Group()
    
    votos_vacancia = 0
    meta_vacancia = 87 # Si llega a 87, pierdes (Te vacan)
    
    tiempo_juego = 45 # Segundos para sobrevivir
    start_ticks = pygame.time.get_ticks()
    
    timer_spawn = 0
    spawn_rate = 60 # Frames entre apariciones
    
    feedback_txt = ""
    feedback_timer = 0
    
    # Fondo decorativo (Curules vacíos)
    img_curul = cargar_imagen("curul.png", (s(100), s(50)), (139, 69, 19)) # Marrón madera

    while True:
        restante = tiempo_juego - (pygame.time.get_ticks() - start_ticks) / 1000
        mouse_pos = pygame.mouse.get_pos()
        cursor_rect.center = mouse_pos
        
        # SPAWN LOGIC
        timer_spawn -= 1
        # Se pone más difícil (más rápido) mientras menos tiempo queda
        rate_actual = max(int(20 * ui_scale()), int(spawn_rate * max(0.2, (restante / tiempo_juego))))

        if timer_spawn <= 0:
            timer_spawn = rate_actual
            
            # Elegir posición que no esté ocupada
            pos_libres = [p for p in posiciones if not any(m.rect.midbottom == p for m in moles_group)]
            
            if pos_libres:
                pos = random.choice(pos_libres)
                es_jefe = random.random() < 0.2 # 20% chance de jefe
                mole = Congresista(pos[0], pos[1], es_jefe)
                moles_group.add(mole)
                if snd_grito and random.random() < 0.4: snd_grito.play()

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F1: 
                pygame.mouse.set_visible(True); return "GANASTE"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Hit check
                golpeados = [m for m in moles_group if m.rect.collidepoint(mouse_pos)]
                if golpeados:
                    # Elegir el congresista que esté más al frente visualmente
                    target = max(golpeados, key=lambda m: m.rect.bottom)
                    target.vida -= 1
                    
                    if target.vida <= 0:
                        target.kill()
                        feedback_txt = "¡COMPRADO!"
                        feedback_timer = 20
                        if snd_soborno: snd_soborno.play()
                        # Bajar votos de vacancia un poco (calmar las aguas)
                        votos_vacancia = max(0, votos_vacancia - 1)
                    else:
                        feedback_txt = "¡QUIERE MÁS!"
                        feedback_timer = 20
                        if snd_soborno: snd_soborno.play() # Sonido pero sigue vivo

        # UPDATE
        for mole in moles_group:
            resultado = mole.update()
            if resultado == "VOTO_VACANCIA":
                votos_vacancia += 5 # Castigo fuerte si se te escapa
                feedback_txt = "¡+5 VOTOS EN CONTRA!"
                feedback_timer = 30
                # Temblor de pantalla o sonido error opcional

        # DRAW
        PANTALLA.fill((20, 20, 40)) # Fondo oscuro
        fondo = cargar_imagen("fondo_congreso.png", (ANCHO, ALTO), (30, 30, 30))
        PANTALLA.blit(fondo, (0,0))

        # Dibujar curules de fondo en las posiciones
        for pos in posiciones:
            rect_c = img_curul.get_rect(midbottom=pos)
            PANTALLA.blit(img_curul, rect_c)

        moles_group.draw(PANTALLA)

        # Dibujar Cursor
        PANTALLA.blit(img_cursor, cursor_rect)

        # UI
        # Barra de Vacancia (Peligro)
        bar_w = s(300)
        bar_h = s(30)
        bar_x = ANCHO//2 - bar_w//2
        bar_y = s(20)
        pygame.draw.rect(PANTALLA, NEGRO, (bar_x, bar_y, bar_w, bar_h))
        # Relleno Barra (Rojo)
        pct_vacancia = votos_vacancia / meta_vacancia
        pygame.draw.rect(PANTALLA, ROJO, (bar_x, bar_y, int(bar_w * pct_vacancia), bar_h))

        mostrar_texto(PANTALLA, f"VOTOS VACANCIA: {votos_vacancia}/{meta_vacancia}", s(20), bar_x + s(10), bar_y + s(4), BLANCO)
        mostrar_texto(PANTALLA, f"Tiempo: {int(restante)}s", s(20), ANCHO - s(150), s(8))
        
        if feedback_timer > 0:
            color = VERDE if "COMPRADO" in feedback_txt else ROJO
            mostrar_texto(PANTALLA, feedback_txt, 30, mouse_pos[0], mouse_pos[1]-40, color)
            feedback_timer -= 1

        # CHECK WIN/LOSE
        if votos_vacancia >= 87:
            pygame.mouse.set_visible(True)
            return "PERDISTE"
        
        if restante <= 0:
            pygame.mouse.set_visible(True)
            return "GANASTE"

        pygame.display.flip()
        RELOJ.tick(FPS)