import os
from typing import List, Tuple
from Utils.colors import Colors
from AI.ImprovedMinimaxAI import ImprovedMinimaxAI
from Game.MoveOptions import MoveOptions
from Utils.used import MoveWithLinks    


class TwixT:
    def __init__(self, size: int = 12):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.links = {'R': set(), 'B': set()}
        self.current_player = 'R'
        self.game_over = False
        self.winner = 'Empate'
        
    def display_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        current_color = Colors.RED if self.current_player == 'R' else Colors.BLUE
        player_name = 'ROJO' if self.current_player == 'R' else 'AZUL'
        print(f"\n{Colors.BOLD}=== TwixT - Turno del jugador {current_color}{player_name}{Colors.END}{Colors.BOLD} ==={Colors.END}\n")
        
        print(f"{Colors.RED}ROJO{Colors.END}: Conectar {Colors.YELLOW}ARRIBA{Colors.END} ↕ {Colors.YELLOW}ABAJO{Colors.END}")
        print(f"{Colors.BLUE}AZUL{Colors.END}: Conectar {Colors.YELLOW}IZQUIERDA{Colors.END} ↔ {Colors.YELLOW}DERECHA{Colors.END}\n")
        
        print("   ", end="")
        for j in range(self.size):
            if j < 10:
                print(f"{Colors.CYAN}{j:2}{Colors.END}", end=" ")
            else:
                print(f"{Colors.CYAN}{j}{Colors.END}", end=" ")
        print()
        
        for i in range(self.size):
            print(f"{Colors.CYAN}{i:2}{Colors.END} ", end="")
            
            for j in range(self.size):

                if (i == 0 and j == 0) or \
                (i == 0 and j == self.size - 1) or \
                (i == self.size - 1 and j == 0) or \
                (i == self.size - 1 and j == self.size - 1):
                    print("   ", end="")  # Espacio vacío para esquinas
                    continue

                cell = self.board[i][j]
                if cell == 'R':
                    print(f"{Colors.BG_RED}{Colors.WHITE} ● {Colors.END}", end="")
                elif cell == 'B':
                    print (f"{Colors.BG_BLUE}{Colors.WHITE} ● {Colors.END}", end="")
                else:
                    link_display = self.get_link_display(i, j)
                    print(f"{link_display}", end="")
            
            print(f" {Colors.CYAN}{i}{Colors.END}")
        
        print("   ", end="")
        for j in range(self.size):
            if j < 10:
                print(f"{Colors.CYAN}{j:2}{Colors.END}", end=" ")
            else:
                print(f"{Colors.CYAN}{j}{Colors.END}", end=" ")
        print("\n")
        
        self.show_links_info()
    
    def get_link_display(self, row: int, col: int) -> str:
        link_chars = self.get_link_characters(row, col)
        if link_chars:
            return link_chars
        
        if row == 0 or row == self.size - 1:
            return f"{Colors.YELLOW} · {Colors.END}"
        elif col == 0 or col == self.size - 1:
            return f"{Colors.YELLOW} · {Colors.END}"
        else:
            return f"{Colors.WHITE} · {Colors.END}"
    
    def get_link_characters(self, row: int, col: int) -> str:
        red_chars = []
        blue_chars = []
        
        for link in self.links['R']:
            char = self.get_link_char_at_position(link, row, col)
            if char:
                red_chars.append(char)
        
        for link in self.links['B']:
            char = self.get_link_char_at_position(link, row, col)
            if char:
                blue_chars.append(char)
        
        if red_chars and blue_chars:
            return f"{Colors.MAGENTA} ✕ {Colors.END}"
        elif red_chars:
            char = self.choose_best_char(red_chars)
            return f"{Colors.RED}{char}{Colors.END}"
        elif blue_chars:
            char = self.choose_best_char(blue_chars)
            return f"{Colors.BLUE}{char}{Colors.END}"
        
        return ""
    
    def get_link_char_at_position(self, link: Tuple, row: int, col: int) -> str:
        (r1, c1), (r2, c2) = link
        
        if not self.position_on_link_line(row, col, r1, c1, r2, c2):
            return ""
        
        dr = r2 - r1
        dc = c2 - c1
        
        if abs(dr) == 2 and abs(dc) == 1:
            if dr > 0: 
                return " ╲ " if dc > 0 else " ╱ "
            else:  
                return " ╱ " if dc > 0 else " ╲ "
        elif abs(dr) == 1 and abs(dc) == 2:
            if dc > 0:  
                return " ╲ " if dr > 0 else " ╱ "
            else:  
                return " ╱ " if dr > 0 else " ╲ "
        
        return " ─ "  
    
    def position_on_link_line(self, row: int, col: int, r1: int, c1: int, r2: int, c2: int) -> bool:
        if r1 == r2 and c1 == c2:
            return False
        
        area = abs((r2 - r1) * (col - c1) - (c2 - c1) * (row - r1))
        
        if area > 1:
            return False
        
        min_r, max_r = min(r1, r2), max(r1, r2)
        min_c, max_c = min(c1, c2), max(c1, c2)
        
        return min_r <= row <= max_r and min_c <= col <= max_c
    
    def choose_best_char(self, chars: List[str]) -> str:
        if not chars:
            return " · "
        
        for char in [" ╲ ", " ╱ ", " │ ", " ─ "]:
            if char in chars:
                return char
        
        return chars[0]
    
    def show_links_info(self):
        print(f"{Colors.RED}Enlaces ROJOS{Colors.END}: {Colors.BOLD}{len(self.links['R'])}{Colors.END}")
        print(f"{Colors.BLUE}Enlaces AZULES{Colors.END}: {Colors.BOLD}{len(self.links['B'])}{Colors.END}")
        print(f"\n{Colors.GREEN}Objetivos:{Colors.END}")
        print(f"- {Colors.RED}ROJO{Colors.END}: Conectar {Colors.YELLOW}ARRIBA{Colors.END} (fila 0) con {Colors.YELLOW}ABAJO{Colors.END} (fila {self.size-1})")
        print(f"- {Colors.BLUE}AZUL{Colors.END}: Conectar {Colors.YELLOW}IZQUIERDA{Colors.END} (col 0) con {Colors.YELLOW}DERECHA{Colors.END} (col {self.size-1})")
        print(f"\n{Colors.MAGENTA}Leyenda:{Colors.END}")
        print(f"  {Colors.BG_RED}{Colors.WHITE} ● {Colors.END} = Clavija roja")
        print(f"  {Colors.BG_BLUE}{Colors.WHITE} ● {Colors.END} = Clavija azul")
        print(f"  {Colors.RED}╲ ╱{Colors.END} = Enlaces rojos")
        print(f"  {Colors.BLUE}╲ ╱{Colors.END} = Enlaces azules")
        print(f"  {Colors.MAGENTA}✕{Colors.END} = Enlaces cruzados")
        print(f"  {Colors.YELLOW}·{Colors.END} = Zona objetivo")
    
    def is_valid_position(self, row: int, col: int) -> bool:
        
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False

        if (row == 0 and col == 0) or \
        (row == 0 and col == self.size - 1) or \
        (row == self.size - 1 and col == 0) or \
        (row == self.size - 1 and col == self.size - 1):
            return False
      
        if self.board[row][col] != ' ':
            return False
     
        for color in ['R', 'B']:
            for link in self.links[color]:
                if self.position_on_link_line(row, col, link[0][0], link[0][1], link[1][0], link[1][1]):
                    if (row, col) not in [link[0], link[1]]:
                        return False
     
        if self.current_player == 'R' and (col == 0 or col == self.size - 1):
            return False  
        if self.current_player == 'B' and (row == 0 or row == self.size - 1):
            return False  

        return True
         
    def place_peg(self, row: int, col: int) -> bool:
        if not self.is_valid_position(row, col):
            return False
        
        self.board[row][col] = self.current_player
        return True
    
    def get_possible_links(self, row: int, col: int) -> List[Tuple[int, int]]:
        moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        possible = []
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self.size and 0 <= new_col < self.size and
                self.board[new_row][new_col] == self.current_player):
                possible.append((new_row, new_col))
        
        return possible
    
    def links_intersect(self, link1: Tuple, link2: Tuple) -> bool:
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        
        def intersect(A, B, C, D):
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
        
        return intersect(link1[0], link1[1], link2[0], link2[1])
    
    def can_add_link(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        new_link = (pos1, pos2)
        
        for color in ['R', 'B']:
            for existing_link in self.links[color]:
                if self.links_intersect(new_link, existing_link):
                    return False
        
        return True
    
    def add_links(self, row: int, col: int):
        possible_connections = self.get_possible_links(row, col)

        if not possible_connections:
            print(f"{Colors.YELLOW}No hay conexiones posibles.{Colors.END}")
            return

        current_color = Colors.RED if self.current_player == 'R' else Colors.BLUE
        print(f"\n{current_color}Conexiones posibles desde ({row}, {col}):{Colors.END}")

        for i, (r, c) in enumerate(possible_connections):
            can_add = self.can_add_link((row, col), (r, c))
            status = f"{Colors.GREEN}✓{Colors.END}" if can_add else f"{Colors.RED}✗ (se cruza){Colors.END}"
            print(f"{Colors.CYAN}{i+1}.{Colors.END} ({r}, {c}) {status}")

        while True:
            try:
                prompt = f"\n{Colors.BOLD}Selecciona conexiones{Colors.END} (ej: {Colors.YELLOW}1,3{Colors.END} o '{Colors.MAGENTA}n{Colors.END}' para ninguna): "
                choice = input(prompt).strip()

                if choice.lower() == 'n':
                    break

                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                valid_links = []

                for idx in indices:
                    if 0 <= idx < len(possible_connections):
                        target = possible_connections[idx]
                        if self.can_add_link((row, col), target):
                            valid_links.append(((row, col), target))
                        else:
                            print(f"{Colors.RED}No se puede conectar con {target} (se cruza con otro enlace).{Colors.END}")

                for link in valid_links:
                    self.links[self.current_player].add(link)

                if valid_links:
                    print(f"{Colors.GREEN}Se añadieron {len(valid_links)} enlaces válidos.{Colors.END}")
                break

            except (ValueError, IndexError):
                print(f"{Colors.RED}Entrada inválida. Usa números separados por comas o 'n'.{Colors.END}")


    def get_all_possible_moves(self) -> List[MoveWithLinks]:
        from copy import deepcopy
        
        original_board = deepcopy(self.board)
        original_links = deepcopy(self.links)
        all_moves = []
        
        try:
            for row in range(self.size):
                for col in range(self.size):
                    if self.is_valid_position(row, col):
                        move_option = self._create_move_option(row, col)
                        valid_combinations = move_option.get_valid_combinations(self)
                        
                        for combination in valid_combinations:
                            all_moves.append((move_option.position, combination))
        
        finally:
            self.board = original_board
            self.links = original_links
        
        return all_moves

    def _create_move_option(self, row: int, col: int):
        self.board[row][col] = self.current_player
        move_option = MoveOptions((row, col))
        possible_connections = self.get_possible_links(row, col)
        
        for target_pos in possible_connections:
            if self.can_add_link((row, col), target_pos):
                move_option.add_link(((row, col), target_pos))
        
        self.board[row][col] = ' '
        return move_option

    def check_victory(self) -> bool:
        # Verificar si el jugador actual ha ganado

        if self.current_player == 'R':
            if self.check_red_victory():
                self.winner = 'R'
                self.game_over = True
                return True
        else:
            if self.check_black_victory():
                self.winner = 'B'
                self.game_over = True
                return True

        # Verificar si el tablero está lleno y no hay ganador → empate
        tablero_lleno = not any(
            self.is_valid_position(r, c)
            for r in range(self.size)
            for c in range(self.size)
        )

        if tablero_lleno:
            self.winner = 'Empate'
            self.game_over = True
            return True

        return False

    
    def check_red_victory(self) -> bool:
        top_pegs = [(0, c) for c in range(self.size) if self.board[0][c] == 'R']
        if not top_pegs:
            return False
        
        visited = set()
        queue = top_pegs.copy()
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            if current[0] == self.size - 1:
                return True
            
            for link in self.links['R']:
                if current in link:
                    other = link[1] if link[0] == current else link[0]
                    if other not in visited:
                        queue.append(other)
        
        return False
    
    def check_black_victory(self) -> bool:
        left_pegs = [(r, 0) for r in range(self.size) if self.board[r][0] == 'B']
        if not left_pegs:
            return False
        
        visited = set()
        queue = left_pegs.copy()
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            if current[1] == self.size - 1:
                return True
            
            for link in self.links['B']:
                if current in link:
                    other = link[1] if link[0] == current else link[0]
                    if other not in visited:
                        queue.append(other)
        
        return False
    
    def switch_player(self):
        self.current_player = 'B' if self.current_player == 'R' else 'R'
    
    def play(self):
        print(f"{Colors.BOLD}{Colors.CYAN}¡Bienvenido a TwixT!{Colors.END}")
        print(f"\n{Colors.GREEN}Instrucciones:{Colors.END}")
        print(f"- Coloca clavijas alternando turnos")
        print(f"- Después de colocar, puedes crear enlaces con tus clavijas")
        print(f"- Los enlaces se hacen en movimientos de caballo (2+1)")
        print(f"- {Colors.RED}ROJO{Colors.END}: conecta {Colors.YELLOW}arriba{Colors.END} con {Colors.YELLOW}abajo{Colors.END}")
        print(f"- {Colors.BLUE}AZUL{Colors.END}: conecta {Colors.YELLOW}izquierda{Colors.END} con {Colors.YELLOW}derecha{Colors.END}")
        print(f"- No se pueden colocar fichas en las esquinas del tablero")
        print(f"- Escribe '{Colors.MAGENTA}quit{Colors.END}' para salir")
        
        input(f"\n{Colors.BOLD}Presiona Enter para comenzar...{Colors.END}")

        self.current_player = 'R'  
        ai = None

        ai_player = input("¿Quieres jugar contra la IA? (s/n): ").strip().lower()
        if ai_player == 's':
            while True:
                ai_color = input("¿Qué color quieres que juegue la IA? (R/B): ").strip().upper()
                if ai_color in ['R', 'B']:
                    break
                print(f"{Colors.RED}Color inválido. Elige 'R' o 'B'.{Colors.END}")

            while True:
                try:
                    ai_time = float(input("¿Cuántos segundos debe pensar la IA? (ej: 5.0): ").strip())
                    if ai_time > 0:
                        break
                    print(f"{Colors.RED}El tiempo debe ser mayor a 0{Colors.END}")
                except ValueError:
                    print(f"{Colors.RED}Entrada inválida. Usa números (ej: 2.5){Colors.END}")

            ai = ImprovedMinimaxAI(max_depth=10, player_color=ai_color, time_limit=ai_time)

            
            if self.current_player == ai.player_color:
                self.display_board()
                print(f"\n{Colors.CYAN}La IA está pensando...{Colors.END}")
                ai_move = ai.get_best_move(self)

                if ai_move:
                    position, links = ai_move
                    row, col = position
                    self.place_peg(row, col)

                    for link in links:
                        self.links[self.current_player].add(link)

                    print(f"{Colors.GREEN}La IA colocó en ({row}, {col}) con {len(links)} enlaces{Colors.END}")
                    ai.print_detailed_stats()
                    self.display_board()

                    if self.check_victory():
                        winner_color = Colors.RED
                        print(f"\n{Colors.BOLD}{Colors.RED}¡La IA ROJO ha ganado!{Colors.END}")
                        self.game_over = True
                        self.winner = self.current_player
                    else:
                        self.switch_player()

       
        while not self.game_over:
            self.display_board()
            try:
                if ai and self.current_player == ai.player_color:
                    print(f"\n{Colors.CYAN}La IA está pensando...{Colors.END}")
                    ai_move = ai.get_best_move(self)

                    if ai_move:
                        position, links = ai_move
                        row, col = position
                        self.place_peg(row, col)

                        for link in links:
                            self.links[self.current_player].add(link)

                        print(f"{Colors.GREEN}La IA colocó en ({row}, {col}) con {len(links)} enlaces{Colors.END}")
                        ai.print_detailed_stats()
                        self.display_board()

                        if self.check_victory():
                            winner_color = Colors.RED if self.current_player == 'R' else Colors.BLUE
                            winner_name = 'ROJO' if self.current_player == 'R' else 'AZUL'
                            print(f"\n{Colors.BOLD}{Colors.RED}¡La IA {winner_color}{winner_name}{Colors.END}{Colors.BOLD} ha ganado!{Colors.END}")
                            self.game_over = True
                            self.winner = self.current_player
                        else:
                            self.switch_player()
                else:
                    current_color = Colors.RED if self.current_player == 'R' else Colors.BLUE
                    player_name = 'ROJO' if self.current_player == 'R' else 'AZUL'

                    prompt = f"\n{Colors.BOLD}Jugador {current_color}{player_name}{Colors.END}{Colors.BOLD}, " \
                            f"ingresa posición{Colors.END} ({Colors.YELLOW}fila,columna{Colors.END}): "
                    move = input(prompt).strip()

                    if move.lower() == 'quit':
                        print(f"{Colors.CYAN}¡Gracias por jugar!{Colors.END}")
                        self.game_over = True
                        return

                    row, col = map(int, move.split(','))

                    if self.place_peg(row, col):
                        self.add_links(row, col)

                        if self.check_victory():
                            self.display_board()
                            winner_color = Colors.RED if self.current_player == 'R' else Colors.BLUE
                            winner_name = 'ROJO' if self.current_player == 'R' else 'AZUL'

                            print(f"\n{Colors.BOLD}{Colors.GREEN}¡¡¡FELICIDADES!!!{Colors.END}")
                            print(f"{Colors.BOLD}El jugador {winner_color}{winner_name}{Colors.END}{Colors.BOLD} ha ganado!{Colors.END}")
                            print(f"{Colors.YELLOW}🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉{Colors.END}")

                            self.game_over = True
                            self.winner = self.current_player
                        else:
                            self.switch_player()
                    else:
                        print(f"{Colors.RED}Posición inválida. Intenta de nuevo.{Colors.END}")
                        input(f"{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")

            except (ValueError, IndexError):
                print(f"{Colors.RED}Formato inválido. Usa: fila,columna (ej: 5,10){Colors.END}")
                input(f"{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")
            except KeyboardInterrupt:
                print(f"\n{Colors.CYAN}¡Gracias por jugar!{Colors.END}")
                self.game_over = True



