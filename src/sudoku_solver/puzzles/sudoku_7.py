"""Chaos Sudoku puzzle #4."""

from sudoku_solver.puzzle import PuzzleData

value_map = [
    [0, 0, 0, 0, 7, 2, 0, 0, 0],
    [8, 0, 0, 0, 0, 6, 0, 7, 4],
    [3, 6, 7, 8, 0, 0, 0, 0, 1],
    [0, 7, 1, 0, 0, 0, 0, 8, 0],
    [5, 0, 0, 7, 0, 0, 4, 0, 0],
    [0, 0, 3, 0, 2, 5, 0, 0, 7],
    [0, 0, 0, 0, 0, 7, 1, 0, 3],
    [0, 3, 0, 9, 0, 0, 0, 0, 6],
    [0, 5, 0, 0, 0, 0, 0, 0, 0],
]

group_map = None

sudoku_7 = PuzzleData(values=value_map, groups=group_map)
