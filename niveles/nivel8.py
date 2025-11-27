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
        
        if self.es_jefe:
            self.image = cargar_imagen("congresista_jefe.png", (100, 100), (200, 0, 0)) # Rojo oscuro
            # Fallback visual
            if "congresista_jefe" not in self.image.get_at((0,0)):
                pygame.draw.circle(self.image, DORADO, (50, 20), 10) # Corona
        else:
            self.image = cargar_imagen("congresista_1.png", (90, 90), (100, 100, 100)) # Gris
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        
        # Tiempo que permanece en pantalla antes de votar por vacancia
        self.tiempo_vida = 120 if es_jefe else 80 # Frames (aprox 1.5 - 2 seg)
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
    img_cursor = cargar_imagen("martillo_billete.png", (50, 50), VERDE)
    cursor_rect = img_cursor.get_rect()
    
    snd_grito = cargar_sonido("vacancia_grito.wav")
    snd_soborno = cargar_sonido("kaching_soborno.wav")
    
    # Posiciones de los curules (Escaños) en el Hemiciclo (Coordenadas X, Y)
    # Organizamos en 3 filas
    posiciones = [
        (200, 300), (400, 300), (600, 300), # Fila Arriba
        (150, 450), (300, 450), (500, 450), (650, 450), # Fila Medio
        (250, 580), (550, 580) # Fila Abajo
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
    img_curul = cargar_imagen("curul.png", (100, 50), (139, 69, 19)) # Marrón madera

    while True:
        restante = tiempo_juego - (pygame.time.get_ticks() - start_ticks) / 1000
        mouse_pos = pygame.mouse.get_pos()
        cursor_rect.center = mouse_pos
        
        # SPAWN LOGIC
        timer_spawn -= 1
        # Se pone más difícil (más rápido) mientras menos tiempo queda
        rate_actual = max(20, int(spawn_rate * (restante / tiempo_juego)))
        
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
                    target = golpeados[0] # Solo uno a la vez
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
        # Fondo Barra
        pygame.draw.rect(PANTALLA, NEGRO, (ANCHO//2 - 150, 20, 300, 30))
        # Relleno Barra (Rojo)
        pct_vacancia = votos_vacancia / meta_vacancia
        pygame.draw.rect(PANTALLA, ROJO, (ANCHO//2 - 150, 20, 300 * pct_vacancia, 30))
        
        mostrar_texto(PANTALLA, f"VOTOS VACANCIA: {votos_vacancia}/87", 30, ANCHO//2 - 110, 25, BLANCO)
        
        mostrar_texto(PANTALLA, f"Tiempo: {int(restante)}s", 30, ANCHO - 150, 20)
        
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