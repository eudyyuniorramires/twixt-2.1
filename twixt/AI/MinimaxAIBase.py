from Utils.used import MoveWithLinks, ai_color
from typing import List, Tuple, Optional
import math
from copy import deepcopy

class MinimaxAIBase:
    def __init__(self, max_depth: int = 1, player_color: str = ai_color):
        self.max_depth = max_depth
        self.player_color = player_color
        self.opponent_color = 'R' if player_color == 'B' else 'B'
        self.nodes_evaluated = 0
    
    def get_best_move(self, game_state) -> MoveWithLinks:
        self.nodes_evaluated = 0
        possible_moves = game_state.get_all_possible_moves()
        
        if not possible_moves:
            return None
        
        best_move = None
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf
        
        for move in possible_moves:
            position, links = move
            temp_state = self._apply_move(game_state, position, links, self.player_color)
            score = self._minimax(temp_state, self.max_depth - 1, False, alpha, beta)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
            if beta <= alpha:
                break  
        
        print(f"Nodos evaluados: {self.nodes_evaluated}")
        return best_move
    
    def _minimax(self, game_state, depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
        self.nodes_evaluated += 1
        
        if depth == 0:
            return self._evaluate_position(game_state)
        
        winner = self._check_game_over(game_state)
        if winner is not None:
            if winner == self.player_color:
                return 1000 + depth  
            elif winner == self.opponent_color:
                return -1000 - depth  
            else:
                return 0  
        
        current_player = self.player_color if is_maximizing else self.opponent_color
        original_player = game_state.current_player
        game_state.current_player = current_player
        possible_moves = game_state.get_all_possible_moves()
        game_state.current_player = original_player
        
        if not possible_moves:
            return self._evaluate_position(game_state)
        
        if is_maximizing:
            max_eval = -math.inf
            for move in possible_moves:
                position, links = move
                temp_state = self._apply_move(game_state, position, links, current_player)
                eval_score = self._minimax(temp_state, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  
            return max_eval
        else:
            min_eval = math.inf
            for move in possible_moves:
                position, links = move
                temp_state = self._apply_move(game_state, position, links, current_player)
                eval_score = self._minimax(temp_state, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  
            return min_eval
    
    def _apply_move(self, game_state, position: Tuple[int, int], 
                links: List[Tuple[Tuple[int, int], Tuple[int, int]]], 
                player: str):
        new_state = deepcopy(game_state)
        row, col = position
        new_state.board[row][col] = player
    
        for link in links:
            if new_state.can_add_link(*link):  
                new_state.links[player].add(link)

        return new_state

    
    def _evaluate_position(self, game_state) -> float:
        score = 0
        
        # 1. Conectividad (peso: 1.5)
        ai_connectivity = self._evaluate_connectivity(game_state, self.player_color)
        opponent_connectivity = self._evaluate_connectivity(game_state, self.opponent_color)
        score += (ai_connectivity - opponent_connectivity) * 1.8
        
        # 2. Control de territorio (peso: 0.3)
        ai_territory = self._evaluate_territory(game_state, self.player_color)
        opponent_territory = self._evaluate_territory(game_state, self.opponent_color)
        score += (ai_territory - opponent_territory) * 0.3
        
        # 3. Progreso hacia objetivo (peso: 1.2)
        ai_progress = self._evaluate_progress(game_state, self.player_color)
        opponent_progress = self._evaluate_progress(game_state, self.opponent_color)
        score += (ai_progress - opponent_progress) * 2.5
        
        # 4. Control central (peso: 0.6)
        ai_central = self._evaluate_central_control(game_state, self.player_color)
        opponent_central = self._evaluate_central_control(game_state, self.opponent_color)
        score += (ai_central - opponent_central) * 0.2

        # 5. Movilidad (peso: 0.4)
        ai_mobility = self._evaluate_mobility(game_state, self.player_color)
        opponent_mobility = self._evaluate_mobility(game_state, self.opponent_color)
        score += (ai_mobility - opponent_mobility) * 0.5

        # 6. Bloqueo del oponente (peso: 0.8)
        ai_blocking = self._evaluate_blocking(game_state, self.player_color)
        opponent_blocking = self._evaluate_blocking(game_state, self.opponent_color)
        score += (ai_blocking - opponent_blocking) * 1.5

        return score
    
    def _evaluate_connectivity(self, game_state, player: str) -> float:
        links_count = len(game_state.links[player])
        pegs = [(r, c) for r in range(game_state.size) for c in range(game_state.size) 
                if game_state.board[r][c] == player]
        
        if not pegs:
            return 0
        
        components = self._count_connected_components(game_state, player, pegs)
        connectivity_score = links_count * 2 - components
        
        return connectivity_score
    
    def _evaluate_territory(self, game_state, player: str) -> float:
        territory_score = 0
        
        for r in range(game_state.size):
            for c in range(game_state.size):
                if game_state.board[r][c] == player:
                    if player == 'R':
                        territory_score += self._get_vertical_position_value(r, game_state.size)
                    else:
                        territory_score += self._get_horizontal_position_value(c, game_state.size)
        
        return territory_score
    
    def _evaluate_progress(self, game_state, player: str) -> float:
        progress_score = 0
        
        if player == 'R':
            top_pegs = [(0, c) for c in range(game_state.size) if game_state.board[0][c] == player]
            bottom_pegs = [(game_state.size-1, c) for c in range(game_state.size) if game_state.board[game_state.size-1][c] == player]
            
            progress_score += len(top_pegs) * 1.5 + len(bottom_pegs) * 1.5
            
            if top_pegs:
                max_progress = self._get_deepest_connection(game_state, top_pegs, player, 'vertical')
                progress_score += max_progress * 2
            
            if bottom_pegs:
                max_progress = self._get_deepest_connection(game_state, bottom_pegs, player, 'vertical_reverse')
                progress_score += max_progress * 2
        
        else: 
            left_pegs = [(r, 0) for r in range(game_state.size) if game_state.board[r][0] == player]
            right_pegs = [(r, game_state.size-1) for r in range(game_state.size) if game_state.board[r][game_state.size-1] == player]
            
            progress_score += len(left_pegs) * 1.5 + len(right_pegs) * 1.5
            
            if left_pegs:
                max_progress = self._get_deepest_connection(game_state, left_pegs, player, 'horizontal')
                progress_score += max_progress * 2
            
            if right_pegs:
                max_progress = self._get_deepest_connection(game_state, right_pegs, player, 'horizontal_reverse')
                progress_score += max_progress * 2
        
        return progress_score

    def _get_deepest_connection(self, game_state, start_pegs: List[Tuple[int, int]], 
                              player: str, direction: str) -> float:
        if not start_pegs:
            return 0
        
        visited = set()
        queue = start_pegs.copy()
        max_progress = 0
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            if direction == 'vertical':
                progress = current[0] / game_state.size
            elif direction == 'vertical_reverse':
                progress = (game_state.size - 1 - current[0]) / game_state.size
            elif direction == 'horizontal':
                progress = current[1] / game_state.size
            elif direction == 'horizontal_reverse':
                progress = (game_state.size - 1 - current[1]) / game_state.size
            else:
                progress = 0
            
            max_progress = max(max_progress, progress)
            
            for link in game_state.links[player]:
                if current in link:
                    other = link[1] if link[0] == current else link[0]
                    if other not in visited:
                        queue.append(other)
        
        return max_progress
    
    def _evaluate_central_control(self, game_state, player: str) -> float:
        center_score = 0.0
        size = game_state.size
        center_r, center_c = size // 2, size // 2
        max_distance = ((size // 2) ** 2 + (size // 2) ** 2) ** 0.5

        if max_distance == 0:
            max_distance = 1  
        
        for r in range(size):
            for c in range(size):
                if game_state.board[r][c] == player:
                    distance = ((r - center_r) ** 2 + (c - center_c) ** 2) ** 0.5
                    position_value = 1.0 - (distance / max_distance)
                    center_score += position_value
        
        return center_score
    
    def _evaluate_mobility(self, game_state, player: str) -> float:
        mobility_score = 0.0
        size = game_state.size
        center_r, center_c = size // 2, size // 2

        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for r in range(size):
            for c in range(size):
                if game_state.board[r][c] == player:
                    accesible_positions = 0

                    for dr, dc in knight_moves:
                        new_r, new_c = r + dr, c + dc
                        if (0 <= new_r < size and 0 <= new_c < size and
                            game_state.board[new_r][new_c] == ' '):
                            accesible_positions += 1

                    mobility_score += accesible_positions
                    distance_to_center = abs(r - center_r) + abs(c - center_c)
                    centrality_bonus = max(0, size - distance_to_center) * 0.1
                    mobility_score += centrality_bonus

        return mobility_score

    def _evaluate_blocking(self, game_state, player: str) -> float:
        opponent = 'R' if player == 'B' else 'B'
        blocking_score = 0
        
        if opponent == 'R':
            for row in range(1, game_state.size - 1):
                for col in range(game_state.size):
                    if game_state.board[row][col] == player:
                        vertical_importance = 1.0 - abs(row - game_state.size/2) / (game_state.size/2)
                        blocking_score += vertical_importance * 0.5
        else:
            for row in range(game_state.size):
                for col in range(1, game_state.size - 1):
                    if game_state.board[row][col] == player:
                        horizontal_importance = 1.0 - abs(col - game_state.size/2) / (game_state.size/2)
                        blocking_score += horizontal_importance * 0.5
        
        return blocking_score
     
    def _count_connected_components(self, game_state, player: str, pegs: List[Tuple[int, int]]) -> int:
        if not pegs:
            return 0
        
        visited = set()
        components = 0
        
        for peg in pegs:
            if peg not in visited:
                components += 1
                self._dfs_component(game_state, player, peg, visited)
        
        return components
    
    def _dfs_component(self, game_state, player: str, start_peg: Tuple[int, int], visited: set):
        stack = [start_peg]
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            
            visited.add(current)
            
            for link in game_state.links[player]:
                if current in link:
                    other = link[1] if link[0] == current else link[0]
                    if other not in visited:
                        stack.append(other)
    
    def _get_vertical_position_value(self, row: int, size: int) -> float:
        center = size // 2
        distance_from_center = abs(row - center)
        return max(0, size - distance_from_center * 2) / size
    
    def _get_horizontal_position_value(self, col: int, size: int) -> float:
        center = size // 2
        distance_from_center = abs(col - center)
        return max(0, size - distance_from_center * 2) / size
    
    def _has_path_towards_bottom(self, game_state, start_pegs: List[Tuple[int, int]], player: str) -> bool:
        visited = set()
        queue = start_pegs.copy()
        max_row_reached = 0
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            max_row_reached = max(max_row_reached, current[0])
            
            for link in game_state.links[player]:
                if current in link:
                    other = link[1] if link[0] == current else link[0]
                    if other not in visited:
                        queue.append(other)
        
        return max_row_reached > game_state.size // 3
    
    def _has_path_towards_right(self, game_state, start_pegs: List[Tuple[int, int]], player: str) -> bool:
        visited = set()
        queue = start_pegs.copy()
        max_col_reached = 0
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            max_col_reached = max(max_col_reached, current[1])
            
            for link in game_state.links[player]:
                if current in link:
                    other = link[1] if link[0] == current else link[0]
                    if other not in visited:
                        queue.append(other)
        
        return max_col_reached > game_state.size // 3
    
    def _check_game_over(self, game_state) -> Optional[str]:
        if self._check_victory_for_player(game_state, 'R'):
            return 'R'
        
        if self._check_victory_for_player(game_state, 'B'):
            return 'B'
        
        # Verificar si el tablero está lleno y no hay ganador
        tablero_lleno = not any(
            game_state.board[r][c] == ' ' and game_state.is_valid_position(r, c)
            for r in range(game_state.size)
            for c in range(game_state.size)
        )

        if tablero_lleno:
            return 'Empate'

        return None

    
    def _check_victory_for_player(self, game_state, player: str) -> bool:
        if player == 'R':
            return self._check_red_victory(game_state)
        else:
            return self._check_black_victory(game_state)
    
    def _check_red_victory(self, game_state) -> bool:
        top_pegs = [(0, c) for c in range(game_state.size) if game_state.board[0][c] == 'R']
        if not top_pegs:
            return False
        
        visited = set()
        queue = top_pegs.copy()
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            if current[0] == game_state.size - 1:
                return True
            
            for link in game_state.links['R']:
                if current in link:
                    other = link[1] if link[0] == current else link[0]
                    if other not in visited:
                        queue.append(other)
        
        return False
    
    def _check_black_victory(self, game_state) -> bool:
        left_pegs = [(r, 0) for r in range(game_state.size) if game_state.board[r][0] == 'B']
        if not left_pegs:
            return False
        
        visited = set()
        queue = left_pegs.copy()
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            if current[1] == game_state.size - 1:
                return True
            
            for link in game_state.links['B']:
                if current in link:
                    other = link[1] if link[0] == current else link[0]
                    if other not in visited:
                        queue.append(other)
        
        return False