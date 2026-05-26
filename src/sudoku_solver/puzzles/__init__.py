"""Puzzle data types and built-in chaos sudoku puzzles."""

from typing import NamedTuple


class PuzzleData(NamedTuple):
    """A sudoku puzzle defined by its initial values and group layout."""

    values: list[list[int]]
    groups: list[list[int]]
    solution: list[list[int]] | None = None

    def validate_solution(self) -> bool:
        """Return True if the stored solution satisfies all sudoku constraints."""
        if self.solution is None:
            return False

        expected = set(range(1, 10))

        for row in self.solution:
            if set(row) != expected:
                return False

        for c in range(9):
            if {self.solution[r][c] for r in range(9)} != expected:
                return False

        group_values: dict[int, set] = {}
        for r in range(9):
            for c in range(9):
                g = self.groups[r][c]
                group_values.setdefault(g, set()).add(self.solution[r][c])
        for values in group_values.values():
            if values != expected:
                return False

        for r in range(9):
            for c in range(9):
                if self.values[r][c] != 0 and self.values[r][c] != self.solution[r][c]:
                    return False

        return True
