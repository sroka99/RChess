import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import numpy as np
from chess.game import Board, translation

def test_pawn_capture():
    board = Board()
    board.set()
    board.move("e2", "e4")
    board.move("d7", "d5")
    board.move("e4", "d5")  # Pawn captures on diagonal
    assert board.board[translation("d5")[0]][translation("d5")[1]] is not None

def test_rook_capture():
    board = Board()
    board.set()
    board.move("a2", "a4")
    board.move("a7", "a5")
    board.move("a1", "a3")
    board.move("a3", "a5")  # Rook captures pawn
    assert board.board[translation("a5")[0]][translation("a5")[1]] is not None

def test_knight_capture():
    board = Board()
    board.set()
    board.move("g1", "f3")
    board.move("b8", "c6")
    board.move("f3", "e5")  # Knight captures pawn
    assert board.board[translation("e5")[0]][translation("e5")[1]] is not None

def test_bishop_capture():
    board = Board()
    board.set()
    board.move("d2", "d4")
    board.move("e7", "e5")
    board.move("c1", "g5")  # Bishop moves but should not capture
    assert board.board[translation("g5")[0]][translation("g5")[1]] is not None

def test_queen_capture():
    board = Board()
    board.set()
    board.move("d2", "d4")
    board.move("d7", "d5")
    board.move("d1", "d3")
    board.move("d3", "d5")  # Queen captures pawn
    assert board.board[translation("d5")[0]][translation("d5")[1]] is not None

def test_king_capture():
    board = Board()
    board.set()
    board.move("e2", "e3")
    board.move("e7", "e6")
    board.move("e1", "e2")
    board.move("e2", "e3")  # King captures pawn
    assert board.board[translation("e3")[0]][translation("e3")[1]] is not None
