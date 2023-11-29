"Connect 4 main game file"

import os
from typing import Tuple, List


class Board:
    """Connect 4 board"""

    def __init__(self, width: int = 7, height: int = 6):
        self.board = [["-" for i in range(width)] for j in range(height)]

    @property
    def num_rows(self) -> int:
        """Returns the height of the board"""
        return len(self.board)

    @property
    def num_cols(self) -> int:
        """Returns the width of the board"""
        return len(self.board[0])

    def __repr__(self) -> str:
        ret_string = "  "
        for column_index in range(self.num_cols):
            ret_string += f"{column_index+1} "
        ret_string += "\n"
        for index, row in enumerate(self.board):
            ret_string += f"{chr(index + 65)} "
            for slot in row:
                ret_string += str(slot) + " "
            ret_string += "\n"
        return ret_string

    @classmethod
    def convert_indicies_to_coordinates(cls, row, col) -> str:
        """Converts indices to coordinates

        Example:
            (0,0) => "A1"
            (3,2) => "D3"
        """
        row_letter = chr(row + 65)
        col_number = col + 1
        return f"{row_letter}{col_number}"

    @classmethod
    def convert_coordinates_to_indicies(cls, input_str: str) -> Tuple[int, int]:
        """Converts coordinates to indicies
        Example:
            "A1" => [0, 0]
            "D3" => [3, 2]
        """
        row_letter = input_str[0]
        row_index = ord(row_letter) - 65

        col_index = int(input_str[1]) - 1

        return row_index, col_index

    def get_list_of_valid_moves(self) -> List[str]:
        """Returns a list of valid moves"""
        valid_moves = []
        for row_index in range(self.num_rows):
            for col_index in range(self.num_cols):
                if self.board[row_index][col_index] == "-":
                    # is it bottom row?
                    if row_index == self.num_rows - 1:
                        valid_moves.append(
                            Board.convert_indicies_to_coordinates(row_index, col_index)
                        )
                    # is there something below it?
                    else:
                        if self.board[row_index + 1][col_index] != "-":
                            valid_moves.append(
                                Board.convert_indicies_to_coordinates(
                                    row_index, col_index
                                )
                            )

        return valid_moves

    def check_if_four_connected(self, symbol: str) -> bool:
        """Checks if there are 4 of symbol connected"""
        win_str = symbol * 4
        # check horozontal
        for row in self.board:
            for i in range(self.num_cols - 3):
                if "".join(row[i : i + 4]) == win_str:
                    return True

        # check vertical
        for col_index in range(self.num_cols):
            col_str = ""
            for row_index in range(self.num_rows):
                col_str += self.board[row_index][col_index]
            for i in range(self.num_rows - 3):
                if col_str[i : i + 4] == win_str:
                    return True

        # check diagonal

        return False

    def update(self, input_coords: str, symbol: str) -> None:
        row_index, col_index = Board.convert_coordinates_to_indicies(input_coords)
        self.board[row_index][col_index] = symbol


class Player:
    """Connect 4 player"""

    def __init__(self, name: str, symbol: str, is_human: bool = True):
        self.name = name
        self.symbol = symbol
        self.is_human = is_human

    def __repr__(self) -> str:
        return f"<{self.name}, is_human: {self.is_human}, symbol: {self.symbol}>"


class Game:
    """Connect 4 game"""

    def __init__(self):
        self.board = Board(15, 15)
        self.player_one = create_player(player_number="1", symbol="X")
        self.player_two = create_player(player_number="2", symbol="O")
        self.current_round_over = False
        self.current_player = self.player_one
        self.current_round_winner = None

    def __repr__(self) -> str:
        return str(self.board)

    def start_new_round(self) -> None:
        """Starts a new game"""
        self.board = Board()

    def toggle_current_player(self) -> None:
        """Toggles between player one and player two"""

        if self.current_player == self.player_one:
            self.current_player = self.player_two
        else:
            self.current_player = self.player_one


def create_player(player_number: str, symbol: str) -> Player:
    """Creates a player object from user input"""
    name = input(f"Enter Player {player_number} Name: ")
    return Player(
        name=name,
        symbol=symbol,
        is_human=(name != "bot"),
    )


def get_human_players_move(game: Game) -> str:
    """Gets the players move"""
    fill = "~"
    turn_msg = f"  {game.current_player.name}'s turn  "
    turn_status_bar = (
        f"(#1){fill*(len(turn_msg)-4)}"
        if game.current_player == game.player_one
        else f"{fill*(len(turn_msg)-4)}(#2)"
    )
    turn_lower_bar = fill * len(turn_msg)
    warn_msg = ""
    input_msg = "Enter your move: "

    def reprint():
        clear_screen()
        print(game)
        print(f"{turn_status_bar}\n{turn_msg}\n{turn_lower_bar}\n\n{warn_msg}")

    reprint()
    move = input(input_msg).upper()
    while move not in game.board.get_list_of_valid_moves():
        warn_msg = "Invalid move!"
        reprint()
        move = input(input_msg).upper()

    return move


def round_loop(game: Game) -> None:
    """Main game loop"""
    while not game.current_round_over:
        clear_screen()
        print(game)
        if game.current_player.is_human:
            players_move = get_human_players_move(game)
        else:
            pass
        game.board.update(input_coords=players_move, symbol=game.current_player.symbol)
        if game.board.check_if_four_connected(symbol=game.current_player.symbol):
            game.current_round_over = True
            game.current_round_winner = game.current_player
        game.toggle_current_player()
    clear_screen()
    print(game)
    print(f"{game.current_round_winner.name} Wins!!")


def clear_screen() -> None:
    """Clears the terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")


# def main() -> None:
#     pass


if __name__ == "__main__":
    g = Game()
    while True:
        round_loop(g)
        if input("PLay again? y/n: ").lower() == "y":
            g.start_new_round()
        else:
            print("Goodbye!")
            exit()
    # g.board.update("A1", "X")
    # g.board.update("A2", "X")
    # g.board.update("A3", "X")
    # g.board.update("A4", "X")
    # g.board.update("A7", "O")
    # g.board.update("B2", "O")
    # g.board.update("C1", "O")
    # g.board.update("D5", "X")
    # g.board.update("E2", "O")
    # g.board.update("D2", "O")
    # g.board.update("C2", "O")
