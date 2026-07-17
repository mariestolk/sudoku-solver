"""Chaos Sudoku puzzle #4."""

from sudoku_solver.puzzle import PuzzleData

value_map = [
    [0, 5, 6, 0, 0, 0, 7, 0, 0],
    [3, 0, 1, 8, 0, 7, 6, 0, 5],
    [7, 0, 0, 2, 6, 5, 0, 0, 1],
    [0, 6, 4, 0, 0, 0, 9, 0, 0],
    [0, 7, 0, 0, 0, 6, 0, 1, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 0, 0, 6, 0, 3, 0, 0, 0],
    [6, 0, 0, 5, 8, 1, 0, 0, 2],
    [0, 8, 0, 0, 0, 0, 0, 6, 0],
]

group_map = None

sudoku_1_summit = PuzzleData(values=value_map, groups=group_map)
