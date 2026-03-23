# TwixT 2.1 🔴🔵

¡Bienvenido a **TwixT 2.1**! Este repositorio contiene una implementación en Python del clásico juego de mesa de conexión estratégica **TwixT**, desarrollado con un fuerte enfoque en Inteligencia Artificial y evaluación de rendimiento (benchmarking) entre distintos agentes.

## 📖 Descripción del Proyecto

TwixT es un juego de mesa abstracto para dos jugadores en el que el objetivo es conectar dos lados opuestos del tablero mediante una cadena continua de piezas (clavijas y puentes). En esta versión (2.1), no solo podrás ejecutar el juego, sino también enfrentar y evaluar diferentes agentes de Inteligencia Artificial que aplican distintas estrategias para ganar.

## 🗂 Estructura del Repositorio

El proyecto está organizado de forma modular dentro del directorio `twixt/`:

*   🤖 **`AI/`**: Contiene la lógica profunda y los algoritmos que potencian a los agentes (heurísticas, Minimax, Alpha-Beta Pruning, Monte Carlo, etc.).
*   🕵️ **`Agents/`**: Scripts que definen los diferentes tipos de jugadores o "agentes" (ej. Agente Aleatorio, Agente Pésimo, Agente Inteligente, Jugador Humano).
*   📊 **`Benchmark/`**: Herramientas y scripts para ejecutar múltiples partidas automatizadas y medir el rendimiento de los agentes (porcentaje de victorias, tiempo de cálculo, etc.).
*   🎮 **`Game/`**: El núcleo del juego. Aquí se encuentra la lógica del tablero, la validación de movimientos (colocación de clavijas y creación de puentes) y las condiciones de victoria.
*   🛠 **`Utils/`**: Funciones auxiliares y utilidades para el manejo de datos, visualización y otras operaciones comunes.
*   📄 **`main.py`**: El punto de entrada principal del programa para iniciar el juego o los tests.
*   📈 **Archivos `.csv`**: Resultados de los benchmarks (ej. `benchmark_resultados_vs_Vs IA Random.csv`), útiles para analizar estadísticas y comparar el rendimiento de las IAs.

## 🚀 Instalación y Uso

### Prerrequisitos
Asegúrate de tener instalado **Python 3.x** en tu sistema.

### Instrucciones

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/eudyyuniorramires/twixt-2.1.git
   cd twixt-2.1/twixt
   ```

2. **Ejecuta el juego principal:**
   Para iniciar una partida o el programa principal, simplemente ejecuta:
   ```bash
   python main.py
   ```

## 📊 Benchmarking y Pruebas de IA

Este proyecto destaca por su capacidad de medir y enfrentar distintas inteligencias artificiales. En la raíz del directorio encontrarás archivos CSV (como `benchmark_resultados_vs_Vs IA Pesima.csv`) que documentan el historial de enfrentamientos. 

Puedes usar los scripts dentro de la carpeta `Benchmark/` para:
- Realizar simulaciones masivas (ej. 100 partidas seguidas entre dos IAs).
- Ajustar y evaluar nuevas heurísticas.
- Exportar los resultados de los torneos a formatos tabulares para su análisis.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar la interfaz, optimizar los algoritmos de la IA, o agregar un nuevo tipo de agente:
1. Haz un Fork del proyecto.
2. Crea una rama para tu característica (`git checkout -b feature/NuevaIA`).
3. Haz commit de tus cambios (`git commit -m 'Añadido nuevo agente Minimax'`).
4. Haz push a la rama (`git push origin feature/NuevaIA`).
5. Abre un Pull Request.

## 👤 Autor

**Eudy Yunior Ramires**
* GitHub: [@eudyyuniorramires](https://github.com/eudyyuniorramires)

---
*Desarrollado para explorar la programación de juegos de tablero y algoritmos de inteligencia artificial aplicados.*
