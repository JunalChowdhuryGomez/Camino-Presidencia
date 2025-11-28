
# Camino a la Presidencia: Estilo Peruano

> *"El único juego donde robar es una mecánica, no un bug."*

## Integrantes:
- Chodury Gómez, Junal  
- Llanos Rosadio, José  
- Zapata Inga, Janio  
- Silva Rojas, Juan 

Este es una colección de minijuegos satíricos desarrollados en **Python** y **Pygame** que simulan la caótica carrera política en el Perú. Desde recolectar firmas falsas a cambio de gaseosas, hasta escapar de la justicia en el auto presidencial.

## 🎮 Descripción

El jugador asume el rol de un político genérico (pero sospechosamente familiar) que debe atravesar 9 niveles de dificultad incremental. Cada nivel representa una etapa de la vida política peruana, con mecánicas de juego distintas (Arcade, Puzzle, Shooter, Strategy).

El objetivo es llegar a la Embajada de México (o al asilo político) antes de que la Fiscalía te atrape.

## 🕹️ Niveles y Mecánicas

| Nivel | Título | Mecánica | Sátira |
| :--- | :--- | :--- | :--- |
| **1** | **Recolección de Firmas** | *Trading* | Cambia gaseosas por firmas en planillones en blanco. Evita a la policía. |
| **2** | **El Gran Mitin** | *Ritmo / QTE* | Promete "Plata como cancha" y baila al ritmo de la cumbia para ganar euforia. |
| **3** | **El Debate Final** | *RPG / Piedra-Papel-Tijera* | Usa "Terruqueo" para vencer a "Propuesta Técnica". Victimízate para ganar rating. |
| **4** | **1ra Vuelta (Campaña)** | *Tower Defense / Gestión* | Distribuye Tapers en el mapa del Perú para pintar las regiones de Naranja. |
| **5** | **2da Vuelta (El Fraude)** | *Sorting (Papers Please)* | Valida tus actas e impugna las del rival por "manchas de tinta". |
| **6** | **Obras Fantasma** | *Pipe Puzzle* | Conecta las tuberías del Tesoro Público directamente a tu Bolsillo (Suiza). |
| **7** | **Pacificación** | *Shooter (Duck Hunt)* | Dispara gas a los manifestantes, pero cuidado con darle a los "Ternas" infiltrados. |
| **8** | **La Vacancia** | *Whack-a-Mole* | Golpea a los congresistas con "Ministerios" para evitar que lleguen a los 87 votos. |
| **9** | **La Fuga del Cofre** | *Endless Runner* | Salta miguelitos y evade fiscales en la Panamericana Sur rumbo a la embajada. |

## 🛠️ Requisitos e Instalación

### Prerrequisitos

  * **Python 3.8+**
  * **Pygame**

### Instalación

1.  **Clonar el repositorio** (o descargar los archivos):

    ```bash
    git clone https://github.com/tu-usuario/camino-presidencia-peru.git
    cd camino-presidencia-peru
    ```

2.  **Instalar dependencias:**

    ```bash
    pip install pygame
    ```

3.  **Configurar Assets:**
    El juego requiere una carpeta `assets/` con imágenes y sonidos.

    > *Nota: Si no tienes las imágenes, el juego usará rectángulos de colores (placeholders) automáticamente para que no crashee.*

4.  **Ejecutar el juego:**

    ```bash
    python main.py
    ```

## Estructura del Proyecto


```text
CaminoPresidencia/
│
├── main.py              # Archivo principal (Orquestador de niveles y finales)
├── config.py            # Constantes globales (Colores, Pantalla, FPS)
├── utils.py             # Herramientas de carga de recursos y textos
│
├── niveles/             # Lógica encapsulada de cada minijuego
│   ├── __init__.py
│   ├── nivel1.py        # Firmas
│   ├── nivel2.py        # Mitin
│   ├── ...
│   └── nivel9.py        # Fuga
│
└── assets/              # (Debes crearla) Aquí van tus .png y .wav
    ├── candidato.png
    ├── taper.png
    ├── cumbia_fondo.mp3
    └── ...
```

## Controles

  * **Flechas Dirección:** Moverse (Niveles 1, 2, 9) / Seleccionar (Nivel 5).
  * **Espacio:** Acción principal (Entregar gaseosa, Saltar, Iniciar).
  * **Mouse:** Apuntar y Disparar (Nivel 7), Golpear curules (Nivel 8), Girar tuberías (Nivel 6).
  * **F1 (Cheat):** Saltar nivel automáticamente (ideal para debug o si eres muy malo robando).
  * **ESC:** Salir del juego.

