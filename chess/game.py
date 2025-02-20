import numpy as np

def translation(position:str):
    row_id = 8-eval(position[1])
    col_id = 0
    if len(position) != 2:
        raise Exception("Incorrect format")
    if row_id > 8:
        raise Exception("incorrect column")
    for i in "abcdefgh"+"x":
        if position[0] == i:
            break
        col_id = col_id+1
    if col_id == 9:
        raise Exception("incorrect row")
    return (row_id,col_id)

def reverse_translation(coordinate:tuple) -> str:
    if not (0 <= coordinate[0] <= 7 and 0 <= coordinate[1] <= 7):
        raise Exception("Invalid coordinates")
    
    column_letters = "abcdefgh"  
    row_number = str(8 - coordinate[0])  
    col_letter = column_letters[coordinate[1]]  
    return col_letter + row_number

def translation(position: str):
    columns = "abcdefgh"
    return (8 - int(position[1]), columns.index(position[0]))

class Board():
    def __init__(self):
        self.board = np.empty((8, 8), dtype=object) 
        self.columns = "abcdefgh"
        self.turn = 1 # white 1, black -1
    
    def set(self):
        for col, col_name in enumerate(self.columns):
            self.board[1][col] = Pawn(-1, f"{col_name}7")
            self.board[6][col] = Pawn(1, f"{col_name}2")
        
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece in enumerate(piece_order):
            self.board[0][col] = piece(-1, f"{self.columns[col]}8")
            self.board[7][col] = piece(1, f"{self.columns[col]}1")
        
    def move(self, old_pos: str, new_pos: str):
        tup_old_pos = translation(old_pos)
        tup_new_pos = translation(new_pos)
        if self.board[tup_old_pos[0]][tup_old_pos[1]] is None:
            raise Exception(f"No piece on {old_pos}")
        piece: Piece = self.board[tup_old_pos[0]][tup_old_pos[1]]
        if piece.color != self.turn:
            raise Exception("Incorrect color")
        
        captured_piece = self.board[tup_new_pos[0]][tup_new_pos[1]]
        if captured_piece is not None and captured_piece.color == piece.color:
            raise Exception("Cannot capture own piece")
        
        if piece.move(new_pos, captured_piece) == 0:
            raise Exception("Illegal move")
        
        self.board[tup_old_pos[0]][tup_old_pos[1]] = None
        self.board[tup_new_pos[0]][tup_new_pos[1]] = piece
        piece.position = (tup_new_pos[0], tup_new_pos[1])
        self.turn *= -1

    def display(self):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if isinstance(piece, Pawn):
                    symbol = "p" if piece.color == -1 else "P"
                elif isinstance(piece, Rook):
                    symbol = "r" if piece.color == -1 else "R"
                elif isinstance(piece, Knight):
                    symbol = "n" if piece.color == -1 else "N"
                elif isinstance(piece, Bishop):
                    symbol = "b" if piece.color == -1 else "B"
                elif isinstance(piece, Queen):
                    symbol = "q" if piece.color == -1 else "Q"
                elif isinstance(piece, King):
                    symbol = "k" if piece.color == -1 else "K"
                else:
                    symbol = "."
                print(symbol, end=" ")
            print()
       

class Piece():
    def __init__(self, color, position):
        self.color = color
        self.position = translation(position)
        self.moved = 0
    
    def move(self, new_position, captured_piece=None):   
        return 0

class Pawn(Piece):
    def move(self, new_position, captured_piece=None):
        row_id, col_id = translation(new_position)
        row_diff = self.position[0] - row_id
        col_diff = abs(self.position[1] - col_id)
        
        if col_diff == 0 and captured_piece is None:
            if row_diff == self.color or (row_diff == 2 * self.color and self.moved == 0):
                self.moved = 1
                return 1
        elif col_diff == 1 and row_diff == self.color and captured_piece is not None:
            return 1
        return 0

class Rook(Piece):
    def move(self, new_position, captured_piece=None):
        row_id, col_id = translation(new_position)
        if self.position[0] == row_id or self.position[1] == col_id:
            return 1
        return 0

class Knight(Piece):
    def move(self, new_position, captured_piece=None):
        row_id, col_id = translation(new_position)
        row_diff = abs(self.position[0] - row_id)
        col_diff = abs(self.position[1] - col_id)
        if (row_diff, col_diff) in [(2, 1), (1, 2)]:
            return 1
        return 0

class Bishop(Piece):
    def move(self, new_position, captured_piece=None):
        row_id, col_id = translation(new_position)
        if abs(self.position[0] - row_id) == abs(self.position[1] - col_id):
            return 1
        return 0

class Queen(Piece):
    def move(self, new_position, captured_piece=None):
        row_id, col_id = translation(new_position)
        if self.position[0] == row_id or self.position[1] == col_id or abs(self.position[0] - row_id) == abs(self.position[1] - col_id):
            return 1
        return 0

class King(Piece):
    def move(self, new_position, captured_piece=None):
        row_id, col_id = translation(new_position)
        row_diff = abs(self.position[0] - row_id)
        col_diff = abs(self.position[1] - col_id)
        if max(row_diff, col_diff) == 1:
            return 1
        return 0
