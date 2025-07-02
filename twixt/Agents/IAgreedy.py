from typing import List, Tuple
from copy import deepcopy
import time

Position = Tuple[int, int]
Link = Tuple[Position, Position]
MoveWithLinks = Tuple[Position, List[Link]]

class GreedyAI:
    def __init__(self, player_color: str = 'B', time_limit: float = None):
        self.player_color = player_color
        self.opponent_color = 'R' if player_color == 'B' else 'B'
        self.moves_evaluated = 0
        self.time_limit = time_limit  

    def get_move(self, game_state) -> MoveWithLinks:
        return self.get_best_move(game_state)

    def get_best_move(self, game_state) -> MoveWithLinks:
        self.moves_evaluated = 0
        possible_moves = game_state.get_all_possible_moves()
        if not possible_moves:
            return None

        best_move = None
        best_score = float('-inf')

        for move in possible_moves:
            self.moves_evaluated += 1
            position, links = move
            score = self._evaluate_move(game_state, position, links)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _evaluate_move(self, game_state, position: Position, links: List[Link]) -> float:
        row, col = position
        score = 0.0

        score += len(links) * 3.0
        score += self._evaluate_objective_progress(game_state, position) * 1.5
        score += self._evaluate_position_value(game_state, position) * 1.5
        score += self._evaluate_connectivity_potential(game_state, position, links) * 4.5
        score += self._evaluate_blocking_potential(game_state, position) * 1.8
        score += self._evaluate_central_position(game_state, position) * 1.0

        return score

    def _evaluate_objective_progress(self, game_state, position: Position) -> float:
        row, col = position
        size = game_state.size
        if self.player_color == 'R':
            if row == 0 or row == size - 1:
                return 10.0
            return max(0, 5.0 - min(row, size - 1 - row))
        else:
            if col == 0 or col == size - 1:
                return 10.0
            return max(0, 5.0 - min(col, size - 1 - col))

    def _evaluate_position_value(self, game_state, position: Position) -> float:
        row, col = position
        size = game_state.size
        center_row, center_col = size // 2, size // 2
        distance_to_center = abs(row - center_row) + abs(col - center_col)
        central_value = max(0, size - distance_to_center) / size

        if self.player_color == 'R':
            vertical_value = 1.0 - abs(row - center_row) / (size // 2) if size > 1 else 1.0
            return central_value + vertical_value
        else:
            horizontal_value = 1.0 - abs(col - center_col) / (size // 2) if size > 1 else 1.0
            return central_value + horizontal_value

    def _evaluate_connectivity_potential(self, game_state, position: Position, links: List[Link]) -> float:
        row, col = position
        connectivity_score = 0.0
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]

        friendly_neighbors = 0
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < game_state.size and 0 <= new_col < game_state.size:
                if game_state.board[new_row][new_col] == self.player_color:
                    friendly_neighbors += 1

        connectivity_score += friendly_neighbors * 1.5
        connectivity_score += len(links) * 2.0
        return connectivity_score

    def _evaluate_blocking_potential(self, game_state, position: Position) -> float:
        row, col = position
        blocking_score = 0.0
        size = game_state.size

        if self.opponent_color == 'R':
            vertical_blocking = 1.0 - abs(col - size // 2) / (size // 2) if size > 1 else 1.0
            blocking_score += vertical_blocking * 2.0
        else:
            horizontal_blocking = 1.0 - abs(row - size // 2) / (size // 2) if size > 1 else 1.0
            blocking_score += horizontal_blocking * 2.0

        return blocking_score

    def _evaluate_central_position(self, game_state, position: Position) -> float:
        row, col = position
        size = game_state.size
        center_row, center_col = size // 2, size // 2
        distance = ((row - center_row) ** 2 + (col - center_col) ** 2) ** 0.5
        max_distance = ((size // 2) ** 2 + (size // 2) ** 2) ** 0.5
        return 1.0 - (distance / max_distance) if max_distance != 0 else 1.0
