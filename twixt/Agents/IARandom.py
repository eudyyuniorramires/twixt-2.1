# IARandom.py

import time
import random 
from typing import Tuple, Set
from Utils.colors import Colors


class RandomAI:
    """
    IA que juega de forma completamente aleatoria.
    Selecciona movimientos válidos al azar sin ninguna estrategia ni evaluación.
    """
    def __init__(self, player_color: str, time_limit: float = None):
        self.player_color = player_color
        self.opponent_color = 'R' if player_color == 'B' else 'B'
        self.time_limit = time_limit  # Mantenido por consistencia con otras IAs
        self.start_time = 0.0
        self.nodes_searched = 0  # Siempre será 1 para IA aleatoria (solo ve el estado actual)
        self.prunings = 0  # Siempre será 0 para IA aleatoria
        self.max_depth = 1  # Profundidad fija para IA aleatoria

    def get_best_move(self, game_state) -> Tuple[Tuple[int, int], Set[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        """
        Obtiene un movimiento completamente aleatorio de todos los movimientos posibles.
        
        Args:
            game_state: Estado actual del juego
            
        Returns:
            Tupla con la posición de la clavija y el conjunto de enlaces (elegido al azar)
        """
        self.start_time = time.time()
        self.nodes_searched = 1  # Solo "explora" el estado actual
        self.prunings = 0

        # Obtener todos los movimientos posibles del juego
        possible_moves = game_state.get_all_possible_moves()

        if not possible_moves:
            print(f"{Colors.RED}¡Advertencia! No hay movimientos posibles para la IA aleatoria ({self.player_color}).{Colors.END}")
            return None

        # Seleccionar un movimiento completamente al azar
        chosen_move = random.choice(possible_moves)
        
        return chosen_move
    
    def get_move(self, game_state):
        return self.get_best_move(game_state)

    def print_detailed_stats(self):
        """
        Imprime estadísticas detalladas de la IA aleatoria.
        """
        end_time = time.time()
        duration = end_time - self.start_time
        
        print(f"{Colors.CYAN}--- Estadísticas de la IA Aleatoria ({self.player_color}) ---{Colors.END}")
        print(f"{Colors.CYAN}Tiempo de cálculo: {duration:.4f} segundos{Colors.END}")
        print(f"{Colors.CYAN}Nodos explorados: {self.nodes_searched} (IA Aleatoria){Colors.END}")
        print(f"{Colors.CYAN}Podas Alpha-Beta: {self.prunings} (No aplicable a IA aleatoria){Colors.END}")
        print(f"{Colors.CYAN}--------------------------{Colors.END}")