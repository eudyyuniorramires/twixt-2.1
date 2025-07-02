import math
from typing import List, Tuple
from Utils.used import Link

class MoveOptions:
    def __init__(self, position: Tuple[int, int]):
        self.position = position
        self.possible_links = []
    
    def add_link(self, link: Tuple[Tuple[int, int], Tuple[int, int]]):
        self.possible_links.append(link)
    
    def get_limited_combinations(self, max_combinations: int = 25) -> List[List[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        from itertools import combinations
        
        all_combinations = [[]]

        # Añadir enlaces individuales
        for link in self.possible_links:
            all_combinations.append([link])
        
        # Añadir algunas combinaciones de dos enlaces (limitado)
        if len(self.possible_links) >= 2:
            count = 0
            for combo in combinations(self.possible_links, 2):
                if count >= max_combinations // 2:
                    break
                all_combinations.append(list(combo))
                count += 1
            
        return all_combinations[:max_combinations]
    
    def validate_combination(self, combination: List[Link], game_state) -> bool:
        seen_links = set()

        for i in range(len(combination)):
            link_i = tuple(sorted(combination[i]))
            if link_i in seen_links:
                return False  # Enlace duplicado dentro de la combinación
            seen_links.add(link_i)

            for j in range(i + 1, len(combination)):
                if game_state.links_intersect(combination[i], combination[j]):
                    return False  # Intersección dentro de la combinación

        for link in combination:
            normalized_link = tuple(sorted(link))
            for color in ['R', 'B']:
                for existing_link in game_state.links[color]:
                    existing_normalized = tuple(sorted(existing_link))
                    if normalized_link == existing_normalized:
                        return False  # Enlace ya existe
                    if game_state.links_intersect(link, existing_link):
                        return False  # Se cruza con un enlace existente

        return True
    
    def get_valid_combinations(self, game_state) -> List[List[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        all_combos = self.get_limited_combinations()
        valid_combos = []
        
        for combo in all_combos:
            if self.validate_combination(combo, game_state):
                valid_combos.append(combo)
        
        return valid_combos