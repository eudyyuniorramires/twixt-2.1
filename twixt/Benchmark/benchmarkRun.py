
from Game.Twixt_game import TwixT
from AI.ImprovedMinimaxAI import ImprovedMinimaxAI as MinimaxAI
from Utils.colors import Colors
from Benchmark.benchmark import CustomHeuristicAI as GoodAI, pesos_config_1, pesos_config_2, pesos_config_3
from Agents.IARandom import RandomAI
from Agents.IAmala import AwfulMinimaxAI 
from Agents.IAgreedy import GreedyAI
from datetime import timedelta
import time
import csv


bots_disponibles = {
    'Vs IA Random': RandomAI,
    'Vs IA Pesima': AwfulMinimaxAI,
    'Vs IA Minmax': MinimaxAI,
    'Vs IA Codiciosa': GreedyAI
}


benchmark_configs = [
    {
        'nombre': 'GoodAI_Pesos1_vs_BotSeleccionado',
        'ia_R_config': {
            'tipo': 'GoodAI',
            'heuristicas': ['connectivity', 'progress'],
            'pesos': pesos_config_1,
            'tiempo': 3.0,
            'profundidad': 10
        },
        'ia_B_config': {
            'tipo': None,  # ← Se define dinámicamente desde el menú
            'tiempo': 0.1,
            'profundidad': 1
        }
    },
    {
        'nombre': 'GoodAI_Pesos2_vs_BotSeleccionado',
        'ia_R_config': {
            'tipo': 'GoodAI',
            'heuristicas': ['connectivity', 'progress'],
            'pesos': pesos_config_2,
            'tiempo': 3.0,
            'profundidad': 10
        },
        'ia_B_config': {
            'tipo': None,
            'tiempo': 0.1,
            'profundidad': 1
        }
    },
    {
        'nombre': 'GoodAI_Pesos3_vs_BotSeleccionado',
        'ia_R_config': {
            'tipo': 'GoodAI',
            'heuristicas': ['connectivity', 'progress'],
            'pesos': pesos_config_3,
            'tiempo': 3.0,
            'profundidad': 10
        },
        'ia_B_config': {
            'tipo': None,
            'tiempo': 0.1,
            'profundidad': 1
        }
    },
    {
        'nombre': 'GoodAI_Tiempo3s_vs_BotSeleccionado',
        'ia_R_config': {
            'tipo': 'GoodAI',
            'heuristicas': ['connectivity', 'progress'],
            'pesos': pesos_config_1,
            'tiempo': 3.0,
            'profundidad': 5
        },
        'ia_B_config': {
            'tipo': None,
            'tiempo': 0.1,
            'profundidad': 1
        }
    },
    {
        'nombre': 'GoodAI_Tiempo10s_vs_BotSeleccionado',
        'ia_R_config': {
            'tipo': 'GoodAI',
            'heuristicas': ['connectivity', 'progress'],
            'pesos': pesos_config_1,
            'tiempo': 10.0,
            'profundidad': 10
        },
        'ia_B_config': {
            'tipo': None,
            'tiempo': 0.1,
            'profundidad': 1
        }
    }
]


def seleccionar_bot():
    print("\nSelecciona el bot contra el que jugará la IA principal:")
    for i, nombre in enumerate(bots_disponibles.keys(), 1):
        print(f"  {i}. {nombre}")
    while True:
        try:
            seleccion = int(input("Ingresa el número del bot: "))
            if 1 <= seleccion <= len(bots_disponibles):
                bot_nombre = list(bots_disponibles.keys())[seleccion - 1]
                return bot_nombre, bots_disponibles[bot_nombre]
            else:
                print("Número fuera de rango. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingresa un número.")


def correr_benchmark_vs_bot(configs, bot_oponente_nombre, BotOponente, partidas_por_config=3):
    resultados_totales = []

    for config in configs:
        print(f"\n{Colors.BOLD}{Colors.CYAN} Ejecutando configuración: {config['nombre']} contra {bot_oponente_nombre}{Colors.END}")
        for i in range(partidas_por_config):
            print(f"{Colors.YELLOW}   Partida {i+1}/{partidas_por_config}{Colors.END}")
            juego = TwixT(size=13)
            juego.current_player = 'R'
            tiempo_inicio_total = time.time()

            # IA Roja (GoodAI fija)
            ia_R = GoodAI(
                heuristics_used=config['ia_R_config']['heuristicas'],
                weights=config['ia_R_config']['pesos'],
                max_depth=config['ia_R_config']['profundidad'],
                player_color='R',
                time_limit=config['ia_R_config']['tiempo']
            )

            # IA Azul (bot oponente seleccionado dinámicamente)
            try:
                if BotOponente.__name__ == 'CustomHeuristicAI':
                    ia_B = BotOponente(
                        heuristics_used=config['ia_B_config'].get('heuristicas', []),
                        weights=config['ia_B_config'].get('pesos', {}),
                        player_color='B',
                        time_limit=config['ia_B_config']['tiempo'],
                        max_depth=config['ia_B_config']['profundidad']
                    )
                elif 'max_depth' in BotOponente.__init__.__code__.co_varnames:
                    ia_B = BotOponente(
                        player_color='B',
                        time_limit=config['ia_B_config']['tiempo'],
                        max_depth=config['ia_B_config']['profundidad']
                    )
                else:
                    ia_B = BotOponente(
                        player_color='B',
                        time_limit=config['ia_B_config']['tiempo']
                    )
            except Exception as e:
                print(f"{Colors.RED}Error al instanciar el bot oponente: {e}{Colors.END}")
                continue

            for ia_instance in [ia_R, ia_B]:
                if not hasattr(ia_instance, 'nodes_searched'):
                    ia_instance.nodes_searched = 0
                if not hasattr(ia_instance, 'prunings'):
                    ia_instance.prunings = 0
                if not hasattr(ia_instance, 'start_time'):
                    ia_instance.start_time = 0.0
                if not hasattr(ia_instance, 'print_detailed_stats'):
                    ia_instance.print_detailed_stats = lambda: print(f"Estadísticas no disponibles para {type(ia_instance).__name__}")

            while not juego.game_over:
                current_player_color = juego.current_player
                current_ia = ia_R if current_player_color == 'R' else ia_B

                print(f"\n{Colors.BOLD}Turno de {Colors.RED if current_player_color == 'R' else Colors.BLUE}{current_player_color}{Colors.END}{Colors.BOLD}...{Colors.END}")
                juego.display_board()

                move = current_ia.get_move(juego)

                if move is None:
                    print(f"{Colors.RED}   El jugador {current_player_color} no tiene movimientos válidos. ¡El otro jugador gana!{Colors.END}")
                    juego.winner = 'B' if current_player_color == 'R' else 'R'
                    juego.game_over = True
                    break

                pos, links = move
                print(f"{Colors.GREEN}   {current_player_color} movió a {pos} y creó {len(links)} enlaces.{Colors.END}")
                juego.place_peg(*pos)

                for link in links:
                    juego.links[current_player_color].add(link)

                current_ia.print_detailed_stats()

                if juego.check_victory():
                    if juego.winner == 'Empate':
                        print(f"{Colors.YELLOW}La partida terminó en empate. No hay más movimientos posibles.{Colors.END}")
                    else:
                        print(f"{Colors.GREEN}¡Ganó el jugador {juego.winner}!{Colors.END}")

                    juego.display_board()
                    break

                juego.switch_player()

            tiempo_total = time.time() - tiempo_inicio_total
            puntos_R = sum(row.count('R') for row in juego.board)
            puntos_B = sum(row.count('B') for row in juego.board)

            resultado = {
                'nombre_config': config['nombre'],
                'bot_oponente': bot_oponente_nombre,
                'partida_numero': i + 1,
                'ganador': juego.winner,
                'puntos_R': puntos_R,
                'puntos_B': puntos_B,
                'enlaces_R': len(juego.links['R']),
                'enlaces_B': len(juego.links['B']),
                'tiempo_total': tiempo_total,
                'nodos_R': getattr(ia_R, 'nodes_searched', 0),
                'nodos_B': getattr(ia_B, 'nodes_searched', 0),
                'podas_R': getattr(ia_R, 'prunings', 0),
                'podas_B': getattr(ia_B, 'prunings', 0),
                'profundidad_R': getattr(ia_R, 'max_depth', 0),
                'profundidad_B': getattr(ia_B, 'max_depth', 0),
            }
            resultados_totales.append(resultado)

            print(f"\n{Colors.CYAN}--- Resumen Partida {i+1} de '{config['nombre']}' ---{Colors.END}")
            if juego.winner == 'Empate':
                print(f"{Colors.YELLOW} Resultado: ¡EMPATE!{Colors.END}")
            elif juego.winner:
                winner_color_display = Colors.RED if juego.winner == 'R' else Colors.BLUE
                print(f"{Colors.GREEN} Resultado: ¡Ganador: {winner_color_display}{juego.winner}{Colors.END}{Colors.GREEN}!{Colors.END}")
            else:
                print(f"{Colors.YELLOW} Resultado: Partida finalizada sin ganador claro (posiblemente interrumpida).{Colors.END}")

            duracion_formateada = str(timedelta(seconds=int(tiempo_total)))
            print(f"{Colors.CYAN} Duración: {duracion_formateada}{Colors.END}")

            print(f"{Colors.CYAN}--------------------------------------------------{Colors.END}\n")

    return resultados_totales


import csv
from datetime import timedelta

def guardar_resultados_csv(resultados, nombre_archivo="benchmark_resultados.csv"):
    if not resultados:
        print("No hay resultados para guardar.")
        return

    # Convertir tiempo_total a formato h:mm:ss antes de guardar
    resultados_convertidos = []
    for fila in resultados:
        fila_copia = fila.copy()
        segundos = int(fila_copia.get('tiempo_total', 0))
        fila_copia['tiempo_total'] = str(timedelta(seconds=segundos))
        resultados_convertidos.append(fila_copia)

    campos = resultados_convertidos[0].keys()

    try:
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            for fila in resultados_convertidos:
                escritor.writerow(fila)
        print(f"    Resultados guardados correctamente en {nombre_archivo}")
    except Exception as e:
        print(f"    Error al guardar el archivo CSV: {e}")

if __name__ == "__main__":
    print(f"{Colors.BOLD}{Colors.MAGENTA}   INICIANDO BENCHMARK DE IA TWIXT{Colors.END}")
    
    bot_nombre, BotOponente = seleccionar_bot()

    for config in benchmark_configs:
        config['ia_B_config']['tipo'] = bot_nombre

    resultados_benchmark = correr_benchmark_vs_bot(
        benchmark_configs,
        bot_nombre,
        BotOponente,
        partidas_por_config=3
    )

    nombre_archivo = f"benchmark_resultados_vs_{bot_nombre}.csv"
    guardar_resultados_csv(resultados_benchmark, nombre_archivo)
    print(f"{Colors.GREEN}Resultados guardados en {nombre_archivo}{Colors.END}")
