from Utils.used import MoveWithLinks
import time
from AI.MinimaxAIBase import MinimaxAIBase
from typing import Any, List, Tuple

class ImprovedMinimaxAI(MinimaxAIBase):
    def __init__(self, max_depth: int = 5, player_color: str = 'B', time_limit: float = 5.0):
        super().__init__(max_depth, player_color)
        self.time_limit = time_limit
        self.start_time = None
        
        self.search_stats = {
            'depths_searched': [],
            'nodes_per_depth': [],
            'time_per_depth': [],
            'best_scores_per_depth': [],
            'total_nodes': 0,
            'max_depth_reached': 0,
            'iterations_completed': 0,
            'time_cutoff_occurred': False
        }
    
    def get_best_move(self, game_state) -> MoveWithLinks:
        self.start_time = time.time()
        self.nodes_evaluated = 0
        self._reset_search_stats()
        
        best_move = None
        best_score = float('-inf')
        
        for depth in range(1, self.max_depth + 1):
            if self._time_exceeded():
                self.search_stats['time_cutoff_occurred'] = True
                break
            
            depth_start_time = time.time()
            depth_nodes_start = self.nodes_evaluated
            
            try:
                score, move = self._minimax_with_timeout(
                    game_state, depth, True, float('-inf'), float('inf')
                )
                
                if move is not None and score > best_score:
                    best_score = score
                    best_move = move
                
                depth_time = time.time() - depth_start_time
                depth_nodes = self.nodes_evaluated - depth_nodes_start
                
                self._update_depth_stats(depth, depth_nodes, depth_time, score)
                
                if score >= 1000:
                    print(f"Victoria garantizada encontrada en profundidad {depth}")
                    break
                    
            except TimeoutError:
                self.search_stats['time_cutoff_occurred'] = True
                break
        
        self._finalize_search_stats()
        return best_move
    
    def get_move(self, game_state):
        return self.get_best_move(game_state)

    def _minimax_with_timeout(self, game_state, depth: int, is_maximizing: bool, 
                             alpha: float, beta: float) -> Tuple[float, Any]:
        if self._time_exceeded():
            raise TimeoutError("Tiempo límite excedido")
        
        self.nodes_evaluated += 1
        
        if depth == 0:
            return self._evaluate_position(game_state), None
        
        winner = self._check_game_over(game_state)
        if winner is not None:
            if winner == self.player_color:
                return 1000 + depth, None  
            elif winner == self.opponent_color:
                return -1000 - depth, None  
            else:
                return 0, None  
        
        current_player = self.player_color if is_maximizing else self.opponent_color
        original_player = game_state.current_player
        game_state.current_player = current_player
        possible_moves = game_state.get_all_possible_moves()
        game_state.current_player = original_player
        
        if not possible_moves:
            return self._evaluate_position(game_state), None
        
        possible_moves = self._order_moves(game_state, possible_moves, current_player)
        best_move = None
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in possible_moves:
                if self._time_exceeded():
                    raise TimeoutError("Tiempo límite excedido")
                
                pos, links = move
                child_state = self._apply_move(game_state, pos, links, current_player)
                eval_score, _ = self._minimax_with_timeout(
                    child_state, depth - 1, False, alpha, beta
                )
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  
            
            return max_eval, best_move
        
        else:
            min_eval = float('inf')
            for move in possible_moves:
                if self._time_exceeded():
                    raise TimeoutError("Tiempo límite excedido")
                
                pos, links = move
                child_state = self._apply_move(game_state, pos, links, current_player)
                eval_score, _ = self._minimax_with_timeout(
                    child_state, depth - 1, True, alpha, beta
                )
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break 
            
            return min_eval, best_move
    
    def _time_exceeded(self) -> bool:
        return time.time() - self.start_time >= self.time_limit
    
    def _order_moves(self, game_state, moves: List[MoveWithLinks], player: str) -> List[MoveWithLinks]:
        def move_priority(move):
            pos, links = move
            row, col = pos
            
            link_bonus = len(links) * 8
            center_distance = abs(row - game_state.size//2) + abs(col - game_state.size//2)
            central_bonus = max(0, game_state.size - center_distance) * 0.3
            
            objective_bonus = 0
            if player == 'R':
                if row == 0 or row == game_state.size-1:
                    objective_bonus = 2  
            else:
                if col == 0 or col == game_state.size-1:
                    objective_bonus = 2  
            
            blocking_bonus = self._calculate_blocking_value(game_state, pos, player)
            
            return link_bonus + central_bonus + objective_bonus + blocking_bonus
        
        return sorted(moves, key=move_priority, reverse=True)
    
    def _calculate_blocking_value(self, game_state, pos: Tuple[int, int], player: str) -> float:
        row, col = pos
        opponent = 'R' if player == 'B' else 'B'
        
        blocking_value = 0
        
        if opponent == 'R':
            vertical_importance = 1.0 - abs(row - game_state.size/2) / (game_state.size/2)
            blocking_value += vertical_importance * 1.5
        else:
            horizontal_importance = 1.0 - abs(col - game_state.size/2) / (game_state.size/2)
            blocking_value += horizontal_importance * 1.5
        
        return blocking_value
    
    def _reset_search_stats(self):
        self.search_stats = {
            'depths_searched': [],
            'nodes_per_depth': [],
            'time_per_depth': [],
            'best_scores_per_depth': [],
            'total_nodes': 0,
            'max_depth_reached': 0,
            'iterations_completed': 0,
            'time_cutoff_occurred': False
        }
    
    def _update_depth_stats(self, depth: int, nodes: int, time_taken: float, score: float):
        self.search_stats['depths_searched'].append(depth)
        self.search_stats['nodes_per_depth'].append(nodes)
        self.search_stats['time_per_depth'].append(time_taken)
        self.search_stats['best_scores_per_depth'].append(score)
        self.search_stats['max_depth_reached'] = depth
        self.search_stats['iterations_completed'] += 1
    
    def _finalize_search_stats(self):
        self.search_stats['total_nodes'] = self.nodes_evaluated
        
        if len(self.search_stats['depths_searched']) > 0:
            print(f"IDS completado: Profundidad máxima {self.search_stats['max_depth_reached']}, "
                  f"Nodos totales: {self.search_stats['total_nodes']}, "
                  f"Iteraciones: {self.search_stats['iterations_completed']}")
    
    def get_search_statistics(self) -> dict:
        return self.search_stats.copy()
    
    def print_detailed_stats(self):
        stats = self.search_stats
        
        print(f"\n{'='*50}")
        print(f"ESTADÍSTICAS DETALLADAS DE BÚSQUEDA IDS")
        print(f"{'='*50}")
        print(f"Tiempo límite: {self.time_limit}s")
        print(f"Profundidad máxima alcanzada: {stats['max_depth_reached']}")
        print(f"Iteraciones completadas: {stats['iterations_completed']}")
        print(f"Nodos totales evaluados: {stats['total_nodes']}")
        print(f"Tiempo cortado: {'Sí' if stats['time_cutoff_occurred'] else 'No'}")
        
        if stats['depths_searched']:
            print(f"\nDetalle por profundidad:")
            print(f"{'Prof.':<6} {'Nodos':<8} {'Tiempo(s)':<10} {'Puntuación':<12}")
            print(f"{'-'*40}")
            
            for i, depth in enumerate(stats['depths_searched']):
                nodes = stats['nodes_per_depth'][i]
                time_taken = stats['time_per_depth'][i]
                score = stats['best_scores_per_depth'][i]
                print(f"{depth:<6} {nodes:<8} {time_taken:<10.3f} {score:<12.2f}")
        
        print(f"{'='*50}\n")