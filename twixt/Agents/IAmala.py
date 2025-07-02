import time
from copy import deepcopy
from typing import Tuple, Set, Optional
from Game.Twixt_game import TwixT
from Utils.colors import Colors

# Inyección dinámica de funciones si no están definidas en TwixT
def calculate_connectivity_score(self, player_color: str) -> float:
    return len(self.links[player_color])

def calculate_progress_score(self, player_color: str) -> float:
    return sum(row.count(player_color) for row in self.board)

TwixT.calculate_connectivity_score = calculate_connectivity_score
TwixT.calculate_progress_score = calculate_progress_score


awful_heuristics_weights = {
    'own_connectivity': -1.0,
    'own_progress': -1.0,
    'opp_connectivity': 1.0,
    'opp_progress': 1.0
}

class AwfulMinimaxAI:
    def __init__(self, player_color: str, max_depth: int = 2, time_limit: float = None):
        self.player_color = player_color
        self.opponent_color = 'R' if player_color == 'B' else 'B'
        self.max_depth = max_depth
        self.time_limit = time_limit  # No se usa, pero se acepta para compatibilidad
        self.start_time = 0.0
        self.nodes_searched = 0
        self.prunings = 0
        self.awful_heuristics_weights = awful_heuristics_weights

    def get_best_move(self, game_state) -> Optional[Tuple[Tuple[int, int], Set[Tuple[Tuple[int, int], Tuple[int, int]]]]]:
        self.start_time = time.time()
        self.nodes_searched = 0
        self.prunings = 0

        best_move = None
        best_value = float('-inf')

        possible_moves = game_state.get_all_possible_moves()
        if not possible_moves:
            return None

        possible_moves.sort(key=lambda x: (x[0][0], x[0][1]))

        for move in possible_moves:
            self.nodes_searched += 1
            peg_pos, links = move

            new_state = deepcopy(game_state)
            new_state.place_peg(*peg_pos)
            for link in links:
                new_state.links[self.player_color].add(link)
            new_state.switch_player()

            value = self._alpha_beta(new_state, self.max_depth - 1, float('-inf'), float('inf'), False)

            if value > best_value:
                best_value = value
                best_move = move

        if not best_move and possible_moves:
            import random
            return random.choice(possible_moves)
        return best_move

    def get_move(self, game_state):
        return self.get_best_move(game_state)

    def _alpha_beta(self, state, depth, alpha, beta, maximizing_player: bool) -> float:
        if depth == 0 or state.game_over:
            return self._evaluate(state)

        possible_moves = state.get_all_possible_moves()
        if not possible_moves:
            return self._evaluate(state)

        if maximizing_player:
            max_eval = float('-inf')
            for move in sorted(possible_moves, key=lambda x: (x[0][0], x[0][1])):
                self.nodes_searched += 1
                peg_pos, links = move

                new_state = deepcopy(state)
                new_state.place_peg(*peg_pos)
                for link in links:
                    new_state.links[state.current_player].add(link)
                new_state.switch_player()

                eval = self._alpha_beta(new_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    self.prunings += 1
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in sorted(possible_moves, key=lambda x: (x[0][0], x[0][1])):
                self.nodes_searched += 1
                peg_pos, links = move

                new_state = deepcopy(state)
                new_state.place_peg(*peg_pos)
                for link in links:
                    new_state.links[state.current_player].add(link)
                new_state.switch_player()

                eval = self._alpha_beta(new_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    self.prunings += 1
                    break
            return min_eval

    def _evaluate(self, game_state) -> float:
        if game_state.winner == self.player_color:
            return float('-inf')
        elif game_state.winner == self.opponent_color:
            return float('inf')
        elif game_state.game_over:
            return 0.0

        score = 0.0
        score += self.awful_heuristics_weights['own_connectivity'] * game_state.calculate_connectivity_score(self.player_color)
        score += self.awful_heuristics_weights['own_progress'] * game_state.calculate_progress_score(self.player_color)
        score += self.awful_heuristics_weights['opp_connectivity'] * game_state.calculate_connectivity_score(self.opponent_color)
        score += self.awful_heuristics_weights['opp_progress'] * game_state.calculate_progress_score(self.opponent_color)
        return score

    def print_detailed_stats(self):
        duration = time.time() - self.start_time
        print(f"{Colors.CYAN}--- Estadísticas de la IA Pésima (Minimax Invertido) ---{Colors.END}")
        print(f"{Colors.CYAN}Tiempo de cálculo: {duration:.4f} segundos{Colors.END}")
        print(f"{Colors.CYAN}Nodos explorados: {self.nodes_searched}{Colors.END}")
        print(f"{Colors.CYAN}Podas Alpha-Beta: {self.prunings}{Colors.END}")
        print(f"{Colors.CYAN}Profundidad máxima: {self.max_depth}{Colors.END}")
        print(f"{Colors.CYAN}-----------------------------------------{Colors.END}")
