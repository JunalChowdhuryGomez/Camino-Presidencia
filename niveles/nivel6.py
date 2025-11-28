import pygame
import os
import random
import sys
from config import *
from utils import *

# Tipos de Tubería
RECTO = 0
CURVO = 1
# Direcciones: Arriba(0), Derecha(1), Abajo(2), Izquierda(3)
# Conexiones [Norte, Este, Sur, Oeste]
TIPOS = {
    RECTO: [True, False, True, False], # Conecta Norte-Sur por defecto
    CURVO: [False, True, True, False]  # Conecta Sur-Este por defecto (Forma de L)
}

class Celda(pygame.sprite.Sprite):
    def __init__(self, x, y, tamaño, tipo):
        super().__init__()
        self.tipo_tubo = tipo
        self.rotacion = random.choice([0, 1, 2, 3]) # Rotación aleatoria inicial 0-3
        self.tamaño = tamaño
        self.conectado = False # Si fluye dinero por aquí
        
        # Cargar imágenes base (comprobar si el asset existe; si no, crear fallback)
        if tipo == RECTO:
            ruta = os.path.join("assets", "tubo_recto.png")
            if os.path.exists(ruta):
                self.img_base = cargar_imagen("tubo_recto.png", (tamaño, tamaño), (150, 150, 150))
            else:
                # Fallback: superficie simple con recto dibujado
                self.img_base = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
                self.img_base.fill((150, 150, 150))
                pygame.draw.rect(self.img_base, (100,100,100), (tamaño//3, 0, tamaño//3, tamaño))
        else:
            ruta = os.path.join("assets", "tubo_curvo.png")
            if os.path.exists(ruta):
                self.img_base = cargar_imagen("tubo_curvo.png", (tamaño, tamaño), (150, 150, 150))
            else:
                # Fallback: superficie simple con curvo dibujado
                self.img_base = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
                self.img_base.fill((150, 150, 150))
                pygame.draw.rect(self.img_base, (100,100,100), (tamaño//3, tamaño//3, tamaño//3, 2*tamaño//3))
                pygame.draw.rect(self.img_base, (100,100,100), (tamaño//3, tamaño//3, 2*tamaño//3, tamaño//3))

        self.image = self.img_base
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.actualizar_imagen()

    def clic(self):
        self.rotacion = (self.rotacion + 1) % 4
        self.actualizar_imagen()

    def actualizar_imagen(self):
        # Rotar la imagen base
        self.image = pygame.transform.rotate(self.img_base, -90 * self.rotacion)
        # Si está conectado (flujo activo), le ponemos un tinte dorado/verde
        if self.conectado:
            tinte = pygame.Surface(self.image.get_size())
            tinte.fill((0, 255, 0)) # Verde billete
            self.image.blit(tinte, (0,0), special_flags=pygame.BLEND_MULT)
        
        # Re-centrar el rect si la rotación cambia dimensiones (aunque aquí es cuadrado)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def obtener_salidas(self):
        # Devuelve [N, E, S, O] ajustado a la rotación
        base = TIPOS[self.tipo_tubo] # Ejemplo Recto: [T, F, T, F]
        # Rotar la lista de conexiones hacia la derecha según self.rotacion
        # Si rotacion es 1 (90 grados horario), Norte pasa a Este.
        # Python list slicing para rotar
        salidas = base[-self.rotacion:] + base[:-self.rotacion]
        return salidas

def verificar_flujo(matriz, filas, cols):
    # Reset estado
    for fila in matriz:
        for c in fila:
            c.conectado = False
    
    # Iniciar flujo desde (0, 0) - El Tesoro (Arriba Izquierda)
    # Asumimos que la entrada al sistema es por ARRIBA de la celda (0,0)
    # Por lo tanto, la celda (0,0) debe tener conexión NORTE para recibir
    # PERO para simplificar, decimos que el flujo nace en (0,0) y se expande
    
    stack = [(0, 0)]
    matriz[0][0].conectado = True
    llego_al_final = False
    
    visitados = set()
    visitados.add((0,0))

    while stack:
        fil, col = stack.pop()
        celda_actual = matriz[fil][col]
        salidas_actual = celda_actual.obtener_salidas() # [N, E, S, O]
        
        # Direcciones vecinas: Arriba, Derecha, Abajo, Izquierda
        vecinos_coords = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for i, (d_fil, d_col) in enumerate(vecinos_coords):
            # i = 0 (Norte), 1 (Este), 2 (Sur), 3 (Oeste)
            
            # Si mi celda actual tiene salida en esa dirección...
            if salidas_actual[i]:
                n_fil, n_col = fil + d_fil, col + d_col
                
                # Verificar límites
                if 0 <= n_fil < filas and 0 <= n_col < cols:
                    vecino = matriz[n_fil][n_col]
                    salidas_vecino = vecino.obtener_salidas()
                    
                    # Verificar si el vecino tiene ENTRADA conectada a mi SALIDA
                    # La entrada del vecino es la dirección opuesta.
                    # Opuestos: Norte(0)<->Sur(2), Este(1)<->Oeste(3)
                    indice_entrada_vecino = (i + 2) % 4
                    
                    if salidas_vecino[indice_entrada_vecino]:
                        if (n_fil, n_col) not in visitados:
                            vecino.conectado = True
                            vecino.actualizar_imagen()
                            visitados.add((n_fil, n_col))
                            stack.append((n_fil, n_col))
                            
                            # Condición de Victoria: Llegar a la última celda (Abajo Derecha)
                            if n_fil == filas - 1 and n_col == cols - 1:
                                llego_al_final = True
    
    # Actualizar imagen del origen también
    matriz[0][0].actualizar_imagen()
    return llego_al_final

def ejecutar_nivel():
    snd_flujo = cargar_sonido("cumbia_fondo.mp3")
    
    filas, cols = 5, 6
    # Tamaño de celda escalable según pantalla y matriz
    tam_celda = max(40, min((ANCHO - 100) // cols, (ALTO - 160) // filas))
    offset_x = (ANCHO - cols * tam_celda) // 2
    offset_y = (ALTO - filas * tam_celda) // 2 + s(30)
    
    # Crear Matriz
    matriz = []
    grupo_sprites = pygame.sprite.Group()
    
    for f in range(filas):
        fila_lista = []
        for c in range(cols):
            tipo = random.choice([RECTO, CURVO])
            # La primera y ultima celda forzamos que sean fáciles o fijas? No, aleatorio es mas divertido.
            celda = Celda(offset_x + c * tam_celda, offset_y + f * tam_celda, tam_celda, tipo)
            fila_lista.append(celda)
            grupo_sprites.add(celda)
        matriz.append(fila_lista)

    tiempo = 60
    start = pygame.time.get_ticks()
    
    ganado = False
    
    # Imágenes decorativas (escaladas)
    img_tesoro = cargar_imagen("perudinero.jpg", (s(100), s(100)), DORADO)
    img_bolsillo = cargar_imagen("billetera.jpg", (s(100), s(100)), NEGRO)

    while True:
        restante = tiempo - (pygame.time.get_ticks() - start) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F1: return "GANASTE"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for celda in grupo_sprites:
                    if celda.rect.collidepoint(pos):
                        celda.clic()
                        # Recalcular flujo en cada clic
                        conectado_final = verificar_flujo(matriz, filas, cols)
                        if conectado_final:
                            ganado = True
                            if snd_flujo: snd_flujo.play()

        # DIBUJAR
        PANTALLA.fill((30, 30, 30))

        # Conexiones visuales externas
        # Tesoro -> (0,0)
        PANTALLA.blit(img_tesoro, (offset_x - s(90), offset_y - s(20)))
        pygame.draw.line(PANTALLA, VERDE, (offset_x - s(10), offset_y + s(40)), (offset_x, offset_y + s(40)), s(10))

        # (Final) -> Bolsillo
        fin_x = offset_x + cols * tam_celda
        fin_y = offset_y + (filas - 1) * tam_celda
        pygame.draw.line(PANTALLA, VERDE if ganado else (100,100,100), (fin_x, fin_y + s(40)), (fin_x + s(20), fin_y + s(40)), s(10))
        PANTALLA.blit(img_bolsillo, (fin_x + s(20), fin_y - s(10)))

        grupo_sprites.draw(PANTALLA)
        
        # UI
        mostrar_texto(PANTALLA, "CONECTA EL DESVÍO DE FONDOS", s(36), ANCHO//2 - s(200), s(20), DORADO)
        mostrar_texto(PANTALLA, f"Tiempo: {int(restante)}", s(24), ANCHO - s(150), s(20))

        if ganado:
            mostrar_texto(PANTALLA, "¡CONEXIÓN ESTABLECIDA!", s(50), ANCHO//2 - s(200), ALTO - s(80), VERDE)
            # Pequeña espera para que el jugador vea su obra maestra
            pygame.display.flip()
            pygame.time.wait(s(2000) if hasattr(__builtins__, 'round') else 2000)
            return "GANASTE"

        if restante <= 0:
            return "PERDISTE"

        pygame.display.flip()
        RELOJ.tick(FPS)