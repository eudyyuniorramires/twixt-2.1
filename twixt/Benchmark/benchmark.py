from Game.Twixt_game import TwixT, ImprovedMinimaxAI
from IPython.display import clear_output
import time

# Ajustar pesos de heuristicas
pesos_config_1 = {
    'connectivity': 1.5,
    'territory': 0.3,
    'progress': 1.2,
    'central': 0.6,
    'mobility': 0.4,
    'blocking': 0.8
}

pesos_config_2 = {
    'connectivity': 2.0,
    'territory': 0.1,
    'progress': 0.5,
    'central': 0.2,
    'mobility': 0.3,
    'blocking': 0.4
}

pesos_config_3 = {
    'connectivity': 1.8,
    'territory': 0.3,
    'progress': 2.5,
    'central': 0.2,
    'mobility': 0.5,
    'blocking': 1.5
}

class CustomHeuristicAI(ImprovedMinimaxAI):
    def __init__(self, heuristics_used, weights, **kwargs):
        super().__init__(**kwargs)
        self.heuristics_used = heuristics_used
        self.weights = weights

    def get_move(self, game_state):
        return self.get_best_move(game_state)

    def _evaluate_position(self, game_state):
        total = 0
        for h in self.heuristics_used:
            if h == 'connectivity':
                total += (self._evaluate_connectivity(game_state, self.player_color) -
                          self._evaluate_connectivity(game_state, self.opponent_color)) * self.weights.get('connectivity', 1)
            elif h == 'territory':
                total += (self._evaluate_territory(game_state, self.player_color) -
                          self._evaluate_territory(game_state, self.opponent_color)) * self.weights.get('territory', 1)
            elif h == 'progress':
                total += (self._evaluate_progress(game_state, self.player_color) -
                          self._evaluate_progress(game_state, self.opponent_color)) * self.weights.get('progress', 1)
            elif h == 'central':
                total += (self._evaluate_central_control(game_state, self.player_color) -
                          self._evaluate_central_control(game_state, self.opponent_color)) * self.weights.get('central', 1)
            elif h == 'mobility':
                total += (self._evaluate_mobility(game_state, self.player_color) -
                          self._evaluate_mobility(game_state, self.opponent_color)) * self.weights.get('mobility', 1)
            elif h == 'blocking':
                total += (self._evaluate_blocking(game_state, self.player_color) -
                          self._evaluate_blocking(game_state, self.opponent_color)) * self.weights.get('blocking', 1)
        return total

    def print_detailed_stats(self):
        if hasattr(self, 'search_stats'):
            print(f"Profundidad alcanzada: {self.search_stats.get('max_depth_reached', 'N/A')}")
        if hasattr(self, 'nodes_evaluated'):
            print(f"Nodos evaluados: {self.nodes_evaluated}")
