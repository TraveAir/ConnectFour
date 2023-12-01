"Connect 4 main game file"

import os
from typing import Tuple, List
import sys
import time
import random
import msvcrt
import keyboard

EMPTY_SYMBOL = "-"
PLAYER_ONE_SYMBOL = "X"
PLAYER_TWO_SYMBOL = "O"


class Board:
    """Connect 4 board"""

    def __init__(self, width: int = 7, height: int = 6):
        self.board = [[EMPTY_SYMBOL for i in range(width)] for j in range(height)]

    @property
    def num_rows(self) -> int:
        """Returns the height of the board"""
        return len(self.board)

    @property
    def num_cols(self) -> int:
        """Returns the width of the board"""
        return len(self.board[0])

    def __repr__(self) -> str:
        ret_string = "\n"
        for row in self.board:
            ret_string += ""
            for slot in row:
                ret_string += str(slot) + " "
            ret_string += "\n"
        return ret_string

    def get_move_indicies(self, col: int) -> Tuple[int, int]:
        """Gets the indicies for the lowes open spot in the selected col"""
        for row_index in range(self.num_rows):
            if self.board[(row_index + 1) * -1][col] == EMPTY_SYMBOL:
                return self.num_rows - row_index - 1, col
        raise ValueError("Column move error")

    def check_if_four_connected(self, symbol: str) -> bool:
        """Returns true if there are four of the same provided symbol connected"""
        win_string = symbol * 4
        board_layout = self.create_list_of_all_rows_cols_diags()
        for line in board_layout:
            if win_string in line:
                return True
        return False

    def create_list_of_all_rows_cols_diags(self) -> List[str]:
        """Creates a list with the current state of all rows, cols, and diags"""
        return_list = []
        # get rows
        for row in self.board:
            return_list.append("".join(row))

        # get cols
        for col_index in range(self.num_cols):
            col_str = "".join(
                self.board[row_index][col_index] for row_index in range(self.num_rows)
            )
            return_list.append(col_str)

        # get diags
        # Get diagonals to the right and down
        for diag_row in range(self.num_rows):
            diagonal = []
            i = 0
            while diag_row + i < self.num_rows and i < self.num_cols:
                diagonal.append(self.board[diag_row + i][i])
                i += 1
            created_list = "".join(diagonal)
            if len(created_list) >= 4:
                return_list.append(created_list)

        for col in range(1, self.num_cols):
            diagonal = []
            i = 0
            while col + i < self.num_cols and i < self.num_rows:
                diagonal.append(self.board[i][col + i])
                i += 1
            created_list = "".join(diagonal)
            if len(created_list) >= 4:
                return_list.append(created_list)

        # Get diagonals to the right and up
        for diag_row in range(self.num_rows):
            diagonal = []
            i = 0
            while diag_row - i >= 0 and i < self.num_cols:
                diagonal.append(self.board[diag_row - i][i])
                i += 1
            created_list = "".join(diagonal)
            if len(created_list) >= 4:
                return_list.append(created_list)

        for col in range(1, self.num_cols):
            diagonal = []
            i = 0
            while col + i < self.num_cols and i < self.num_rows:
                diagonal.append(self.board[self.num_rows - 1 - i][col + i])
                i += 1
            created_list = "".join(diagonal)
            if len(created_list) >= 4:
                return_list.append(created_list)
        return return_list

    def check_for_stalemate(self) -> bool:
        """Returns true if all slots on top row are full"""
        if len(self.get_legal_moves()) == 0:
            return True
        return False

    def update(self, row_index: int, col_index: int, symbol: str) -> None:
        """Update the board at the specified location to the specified symbol"""
        self.board[row_index][col_index] = symbol

    def get_legal_moves(self) -> List[int]:
        """Returns a list of columns where a move is legal"""
        legal_moves = []
        for index, slot in enumerate(self.board[0]):
            if slot == EMPTY_SYMBOL:
                legal_moves.append(index)
        return legal_moves


class Player:
    """Connect 4 player"""

    def __init__(
        self, name: str, symbol: str, is_human: bool = True, bot_difficulty: int = 0
    ):
        self.name = name
        self.symbol = symbol
        self.is_human = is_human
        self.bot_difficulty = bot_difficulty
        self.win_streak = 0

    def __repr__(self) -> str:
        return f"<{self.name}, is_human: {self.is_human}, symbol: {self.symbol}>"


class Game:
    """Connect 4 game"""

    def __init__(self):
        self.board = Board()
        self.player_one = create_player(player_number="1", symbol=PLAYER_ONE_SYMBOL)
        self.player_two = create_player(player_number="2", symbol=PLAYER_TWO_SYMBOL)
        self.current_round_over = False
        self.current_player = self.player_one
        self.current_round_winner = None

    def __repr__(self) -> str:
        return f"[{self.player_one.win_streak}] {self.player_one.name[0:1]} vs {self.player_two.name[0:1]} [{self.player_two.win_streak}]\n\n"

    def start_new_round(self) -> None:
        """Starts a new game"""
        self.board = Board()
        self.current_round_over = False

    def toggle_current_player(self) -> None:
        """Toggles between player one and player two"""

        if self.current_player == self.player_one:
            self.current_player = self.player_two
        else:
            self.current_player = self.player_one


def create_player(player_number: str, symbol: str) -> Player:
    """Creates a player object from user input"""
    name = input(f"Enter Player {player_number} Name: ")
    if "bot" in name.lower():
        is_human = False
        bot_difficulty_input = input(
            "Enter bot difficulty (1: Easy, 2: Medium, 3: Hard): "
        )
        while bot_difficulty_input not in ["1", "2", "3"]:
            bot_difficulty_input = input(
                "Error!\nEnter bot difficulty (1: Easy, 2: Medium, 3: Hard): "
            )
        bot_difficulty = int(bot_difficulty_input)
    else:
        is_human = True
        bot_difficulty = 0
    return Player(
        name=name,
        symbol=symbol,
        is_human=is_human,
        bot_difficulty=bot_difficulty,
    )


def get_turn_status_bar(game: Game) -> str:
    """returns the turn bar"""
    fill = "~"
    turn_msg = f"  {game.current_player.name}'s turn  "
    turn_status_bar = (
        f"(#1){fill*(len(turn_msg)-4)}"
        if game.current_player == game.player_one
        else f"{fill*(len(turn_msg)-4)}(#2)"
    )
    turn_lower_bar = fill * len(turn_msg)
    return f"{turn_status_bar}\n{turn_msg}\n{turn_lower_bar}"


def print_board_and_turn(game: Game, arrow: List[str]) -> None:
    """Prints the board and turn status bar"""
    clear_screen()
    print(game)
    for x in arrow:
        print(x + " ", end="")
    print(game.board)
    print(get_turn_status_bar(game))


def get_human_players_move(game: Game) -> int:
    """Gets the players desired column"""
    time.sleep(0.3)
    arrow_disp = []
    for _ in range(game.board.num_cols):
        arrow_disp.append(" ")
    arrow_disp[0] = "↓"
    arrow_min = 0
    arrow_max = game.board.num_cols - 1

    while True:
        print_board_and_turn(game, arrow_disp)
        print("Make your move!")
        key = keyboard.read_key()

        if key in ["left", "a", "A"] and arrow_disp[arrow_min] != "↓":
            index = arrow_disp.index("↓")
            arrow_disp[index] = " "
            arrow_disp[index - 1] = "↓"
        if key in ["right", "d", "D"] and arrow_disp[arrow_max] != "↓":
            index = arrow_disp.index("↓")
            arrow_disp[index] = " "
            arrow_disp[index + 1] = "↓"
        if key in ["enter", "space", "return"]:
            if arrow_disp.index("↓") in game.board.get_legal_moves():
                return arrow_disp.index("↓")
        time.sleep(0.2)


def flush_input():
    """Flushes the input buffer. Needed due to capturing keypresses during move selection"""
    while msvcrt.kbhit():
        msvcrt.getch()


def bot_move_easy(game: Game) -> int:
    """Bot makes a random move"""
    return random.choice(game.board.get_legal_moves())


def bot_move_medium(game: Game) -> int:
    """Bot makes a move based on a few rules
    1. If bot can win, make that move
    2. If enemy can win, block that move
    3. If bot can make a move that will result in enemy winning on their next move,
        don't make that move
    4. Otherwise, make a random move
    """
    legal_moves = game.board.get_legal_moves()
    enemy_symbol = (
        PLAYER_TWO_SYMBOL
        if game.current_player.symbol == PLAYER_ONE_SYMBOL
        else PLAYER_ONE_SYMBOL
    )
    # Check for 1 away from win
    for possible_move in legal_moves:
        row, col = game.board.get_move_indicies(possible_move)
        game.board.update(row, col, game.current_player.symbol)
        if game.board.check_if_four_connected(game.current_player.symbol):
            game.board.update(row, col, EMPTY_SYMBOL)
            return possible_move
        game.board.update(row, col, EMPTY_SYMBOL)
    # Check for other player about to win
    for possible_move in legal_moves:
        row, col = game.board.get_move_indicies(possible_move)
        game.board.update(row, col, enemy_symbol)
        if game.board.check_if_four_connected(enemy_symbol):
            game.board.update(row, col, EMPTY_SYMBOL)
            return possible_move
        game.board.update(row, col, EMPTY_SYMBOL)
    # Check if move will result in enemy winning
    undesired_moves = []
    for possible_move in legal_moves:
        row, col = game.board.get_move_indicies(possible_move)
        game.board.update(row, col, game.current_player.symbol)
        new_legal_moves = game.board.get_legal_moves()
        for new_move in new_legal_moves:
            new_row, new_col = game.board.get_move_indicies(new_move)
            game.board.update(new_row, new_col, enemy_symbol)
            if game.board.check_if_four_connected(enemy_symbol):
                undesired_moves.append(possible_move)
            game.board.update(new_row, new_col, EMPTY_SYMBOL)
        game.board.update(row, col, EMPTY_SYMBOL)
    if len(undesired_moves) == len(legal_moves):
        return random.choice(legal_moves)
    return random.choice([move for move in legal_moves if move not in undesired_moves])


def bot_move_hard(game: Game) -> int:
    """Bot makes a move based off minimax algorithm"""
    scores = {"win": 1000, "lose": -1000, "tie": 0, "three": 20, "two": 5}
    winning_symbol = game.current_player.symbol
    losing_symbol = (
        PLAYER_TWO_SYMBOL
        if game.current_player.symbol == PLAYER_ONE_SYMBOL
        else PLAYER_ONE_SYMBOL
    )

    def score_current_board(board: Board) -> int:
        board_layout = board.create_list_of_all_rows_cols_diags()
        score = 0
        for line in board_layout:
            if winning_symbol * 4 in line:
                score += scores["win"]
            if losing_symbol * 4 in line:
                score += scores["lose"]
            if winning_symbol * 3 in line:
                score += scores["three"]
            if losing_symbol * 3 in line:
                score += scores["three"] * -1
            if winning_symbol * 2 in line:
                score += scores["two"]
            if losing_symbol * 2 in line:
                score += scores["two"] * -1
        return score

    def minimax(
        board: Board, depth: int, alpha: int, beta: int, is_maximizing: bool
    ) -> Tuple[int, int]:
        if board.check_if_four_connected(winning_symbol):
            return scores["win"], -1
        if board.check_if_four_connected(losing_symbol):
            return scores["lose"], -1
        if board.check_for_stalemate():
            return scores["tie"], -1
        if depth == 0:
            score = score_current_board(board)
            return score, -1
        if is_maximizing:
            best_score = -100000
            best_col = -1
            for move in board.get_legal_moves():
                row, col = board.get_move_indicies(move)
                board.update(row, col, winning_symbol)
                score = minimax(board, depth - 1, alpha, beta, False)[0]
                board.update(row, col, EMPTY_SYMBOL)
                if score > best_score:
                    best_score = score
                    best_col = move
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return best_score, best_col

        best_score = 100000
        best_col = -1
        for move in board.get_legal_moves():
            row, col = board.get_move_indicies(move)
            board.update(row, col, losing_symbol)
            score = minimax(board, depth - 1, alpha, beta, True)[0]
            board.update(row, col, EMPTY_SYMBOL)
            if score < best_score:
                best_score = score
                best_col = move
            beta = min(beta, score)
            if alpha >= beta:
                break
        return best_score, best_col

    return minimax(game.board, 6, -100000, 100000, True)[1]


def get_bot_move_choice(game: Game) -> int:
    """Gets a move from the bot based on the bots difficulty"""
    if game.current_player.bot_difficulty == 1:
        return bot_move_easy(game)

    elif game.current_player.bot_difficulty == 2:
        return bot_move_medium(game)
    else:
        return bot_move_hard(game)


def animate_bot_move(game: Game, move: int) -> None:
    """Animates the bot move"""
    arrow_disp = []
    for _ in range(game.board.num_cols):
        arrow_disp.append(" ")
    arrow_disp[0] = "↓"
    print_board_and_turn(game, arrow_disp)
    print("Thinking...")
    time.sleep(1)
    while arrow_disp.index("↓") != move:
        index = arrow_disp.index("↓")
        arrow_disp[index] = " "
        arrow_disp[index + 1] = "↓"
        print_board_and_turn(game, arrow_disp)
        print("Thinking...")
        time.sleep(0.2)
    time.sleep(0.5)


def game_loop(game: Game) -> None:
    """Main game loop"""
    while not game.current_round_over:
        if game.current_player.is_human:
            selected_move = get_human_players_move(game)
            flush_input()
        else:
            print_board_and_turn(game, [" " for _ in range(game.board.num_cols)])
            print("Thinking...")
            selected_move = get_bot_move_choice(game)
            animate_bot_move(game, selected_move)
        game.board.update(
            *game.board.get_move_indicies(selected_move),
            symbol=game.current_player.symbol,
        )
        if game.board.check_if_four_connected(symbol=game.current_player.symbol):
            game.current_round_over = True
            game.current_round_winner = game.current_player
        if game.board.check_for_stalemate():
            game.current_round_over = True
            game.current_round_winner = None
        game.toggle_current_player()
    clear_screen()
    print(game)
    print(game.board)
    if game.current_round_winner is None:
        print("Stalemate!!")
    else:
        print(f"{game.current_round_winner.name} Wins!!")
        game.current_round_winner.win_streak += 1


def clear_screen() -> None:
    """Clears the terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    clear_screen()
    g = Game()
    while True:
        game_loop(g)
        flush_input()
        while True:
            play_again = input("Play again? y/n: ").lower()
            if play_again not in ["y", "n"]:
                continue
            if play_again == "y":
                g.start_new_round()
                break
            print("Goodbye!")
            sys.exit()
