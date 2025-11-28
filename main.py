import pygame
import sys
from config import *
from utils import *

# Importar los niveles desde la carpeta 'niveles'
from niveles import nivel1, nivel2, nivel3, nivel4, nivel5, nivel6, nivel7, nivel8, nivel9

def mostrar_mensaje_final(texto, subtexto, color):
    PANTALLA.fill(NEGRO)
    mostrar_texto(PANTALLA, texto, 60, ANCHO//3 - 200, ALTO//3 - 50, color)
    mostrar_texto(PANTALLA, subtexto, 30, ANCHO//3 - 250, ALTO//3 + 20, BLANCO)
    pygame.display.flip()
    pygame.time.wait(3000)


def pantalla_final(resultado):
    musica_fondo = None
    imagen = None
    titulo = ""
    texto1 = ""
    texto2 = ""
    color_titulo = BLANCO
    
    if resultado == "VICTORIA":
        # Final Bueno: Asilo Político
        imagen = cargar_imagen("alan.jpg", (ANCHO, ALTO), (0, 200, 255)) # Azul cielo
        musica_fondo = cargar_sonido("musica_victoria.mp3") # Algo caribeño
        titulo = "¡LO LOGRASTE!"
        texto1 = "Te asilaste en una embajada amiga."
        texto2 = "Escribirás tus memorias: 'La verdad de mi verdad'."
        color_titulo = DORADO
    else:
        # Final Malo: Cárcel
        imagen = cargar_imagen("expresidentes.jpeg", (ANCHO, ALTO), (50, 50, 50)) # Gris rejas
        musica_fondo = cargar_sonido("musica_triste.mp3") # Violín triste
        titulo = "PRISIÓN PREVENTIVA"
        texto1 = "Te dictaron 36 meses mientras investigan."
        texto2 = "Compartirás celda con tus predecesores."
        color_titulo = ROJO

    if musica_fondo: musica_fondo.play(-1)

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Reiniciar juego
                    if musica_fondo: musica_fondo.stop()
                    esperando = False
                    return "REINICIAR"
                if event.key == pygame.K_ESCAPE: # Salir
                    pygame.quit(); sys.exit()

        PANTALLA.blit(imagen, (0,0))
        
        # Renderizado de texto con sombra
        mostrar_texto(PANTALLA, titulo, 80, ANCHO//2 - 250, 100, NEGRO)
        mostrar_texto(PANTALLA, titulo, 80, ANCHO//2 - 252, 98, color_titulo)
        
        mostrar_texto(PANTALLA, texto1, 40, 50, ALTO//2)
        mostrar_texto(PANTALLA, texto2, 30, 50, ALTO//2 + 50)
        
        mostrar_texto(PANTALLA, "PRESIONA [ESPACIO] PARA VOLVER A POSTULAR", 25, 150, ALTO - 50, BLANCO)
        
        pygame.display.flip()
        RELOJ.tick(15)


def main():
    while True:
        # --- NIVEL 1 ---
        accion = pantalla_intro(1, "NIVEL 1: LAS FIRMAS", "Consigue gaseosas para obtener firmas.")
        if accion == "JUGAR": res = nivel1.ejecutar_nivel()
        else: res = "GANASTE"

        if res == "PERDISTE":
            mostrar_mensaje_final("GAME OVER", "El JNE rechazó tu inscripción.", ROJO)
            continue # Reinicia el juego

        mostrar_mensaje_final("¡INSCRITO!", "Tienes personería jurídica.", VERDE)

        # --- NIVEL 2 ---
        accion = pantalla_intro(2, "NIVEL 2: EL MITIN", "Promete lo imposible y baila.")
        if accion == "JUGAR": res = nivel2.ejecutar_nivel()
        else: res = "GANASTE"

        if res == "PERDISTE":
            mostrar_mensaje_final("ABUCHEADO", "Te bajaron del escenario.", ROJO)
            continue

        mostrar_mensaje_final("¡POPULISMO PURO!", "Eres tendencia en TikTok.", VERDE)

        # --- NIVEL 3 ---
        accion = pantalla_intro(3, "NIVEL 3: EL DEBATE", "Terruqueo > Propuesta > Víctima.")
        if accion == "JUGAR": res = nivel3.ejecutar_nivel()
        else: res = "GANASTE"

        if res == "PERDISTE":
            mostrar_mensaje_final("HUMILLADO", "Perdiste el debate en vivo.", ROJO)
            continue

        mostrar_mensaje_final("¡GANADOR!", "Subiste en las encuestas. Pasamos a 1ra Vuelta.", DORADO)
        
        # --- NIVEL 4: 1RA VUELTA ---
        accion = pantalla_intro(4, "NIVEL 4: 1RA VUELTA", "Usa tu presupuesto para repartir Tapers en las regiones.")

        if accion == "JUGAR": res = nivel4.ejecutar_nivel()
        else: res = "GANASTE"

        if res == "PERDISTE":
            mostrar_mensaje_final("FRAUDE", "El Lápiz ganó en la sierra. Perdiste.", ROJO)
            continue

        mostrar_mensaje_final("¡PASASTE A 2DA VUELTA!", "Fue un empate técnico, pero entraste.", NARANJA)



        # --- NIVEL 5: SEGUNDA VUELTA (FRAUDE) ---
        accion = pantalla_intro(5, "NIVEL 5: EL ESCRUTINIO", 
                                "IZQUIERDA: Valida tus actas. DERECHA: Impugna las del rival.")
        
        if accion == "JUGAR": res = nivel5.ejecutar_nivel()
        else: res = "GANASTE"

        if res == "PERDISTE":
            mostrar_mensaje_final("PERDISTE LA ELECCIÓN", "La ONPE dice que perdiste por 40,000 votos.", ROJO)
            continue

        mostrar_mensaje_final("¡PRESIDENTE ELECTO!", "Ganaste por 0.01% gracias a las actas impugnadas.", DORADO)


        # --- NIVEL 6: OBRAS (TUBERÍAS) ---
        accion = pantalla_intro(6, "NIVEL 6: OBRAS FANTASMA", 
                                "Gira las tuberías para desviar el presupuesto a tu bolsillo.")
        
        if accion == "JUGAR": res = nivel6.ejecutar_nivel()
        else: res = "GANASTE"

        if res == "PERDISTE":
            mostrar_mensaje_final("DESTITUIDO", "La obra quedó inconclusa y no cobraste.", ROJO)
            continue

        mostrar_mensaje_final("¡OBRA 'TERMINADA'!", "Robaste millones, pero la gente está furiosa por la estafa.", VERDE)



        # --- NIVEL 7: PACIFICACIÓN (SHOOTER) ---
        accion = pantalla_intro(7, "NIVEL 7: RESTABLECER EL ORDEN", 
                                "Dispara gas a los manifestantes (Carteles). NO DISPARES a los Ternas (Capuchas).")
        
        if accion == "JUGAR": res = nivel7.ejecutar_nivel()
        else: res = "GANASTE"

        if res == "PERDISTE":
            mostrar_mensaje_final("GOBIERNO DÉBIL", "La plaza te superó. Renunciaste por fax.", ROJO)
            continue

        mostrar_mensaje_final("¡PLAZA LIMPIA!", "La prensa dice que 'triunfó la democracia' (a punta de gas).", DORADO)


        # --- NIVEL 8: LA VACANCIA (WHACK-A-MOLE) ---
        accion = pantalla_intro(8, "NIVEL 8: COMPRA DE CONCIENCIAS", 
                                "¡Te quieren vacar! Lanza 'Ministerios' a los congresistas para callarlos.")
        
        if accion == "JUGAR": res = nivel8.ejecutar_nivel()
        else: res = "GANASTE"

        if res == "PERDISTE":
            mostrar_mensaje_final("¡VACADO!", "Alcanzaron los 87 votos. Te vas preso.", ROJO)
            continue # Game Over

        mostrar_mensaje_final("¡SOBREVIVISTE!", "La moción no procedió. 'Aquí no ha pasado nada'.", VERDE)


        # --- NIVEL 8: VACANCIA ---
        accion = pantalla_intro(8, "NIVEL 8: COMPRA DE CONCIENCIAS", "Evita la vacancia comprando congresistas.")
        if accion == "JUGAR": res = nivel8.ejecutar_nivel()
        else: res = "GANASTE"
        
        if res == "PERDISTE":
            pantalla_final("DERROTA") # Cárcel directa
            continue 

        mostrar_mensaje_final("¡SOBREVIVISTE!", "Pero la Fiscalía ya viene...", VERDE)

        # --- NIVEL 9: LA FUGA ---
        accion = pantalla_intro(9, "NIVEL 9: LA FUGA DEL COFRE", 
                                "Salta con [ESPACIO] y llega a la embajada.")
        
        if accion == "JUGAR": res = nivel9.ejecutar_nivel()
        else: res = "GANASTE"

        # --- PANTALLAS FINALES ---
        if res == "GANASTE":
            opcion = pantalla_final("VICTORIA")
        else:
            opcion = pantalla_final("DERROTA")
        
        if opcion == "REINICIAR":
            continue # Vuelve al Nivel 1

if __name__ == "__main__":
    main()