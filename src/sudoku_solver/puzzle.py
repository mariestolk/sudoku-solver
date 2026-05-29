"""Sudoku puzzle representation and constraint-propagation solver."""

import random
from collections.abc import Callable
from typing import NamedTuple

from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.elimination import (
    reduce_columns,
    reduce_groups,
    reduce_rows,
)
from sudoku_solver.strategies.hidden import reduce_hidden_pair, reduce_hidden_single
from sudoku_solver.strategies.naked import reduce_naked_pairs, reduce_naked_triples
from sudoku_solver.strategies.pinned import reduce_pinned_candidate

STANDARD_GROUP_MAP: list[list[int]] = [
    [(r // 3) * 3 + (c // 3) for c in range(9)] for r in range(9)
]


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

        group_values: dict[int, set[int]] = {}
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


class SolveResult(NamedTuple):
    """The outcome of a single solve step."""

    row: int
    column: int
    group: int
    value: int
    rule: str


class Puzzle:
    """Represents a sudoku puzzle and its constraint-propagation solver."""

    def __init__(
        self, value_map: list[list[int]], group_map: list[list[int]] | None = None
    ) -> None:
        """Initialize the puzzle from a value map and an optional group map."""
        if group_map is None:
            group_map = STANDARD_GROUP_MAP
        grid = self._initialize_cells(value_map, group_map)

        self.rows: list[list[Cell]] = grid
        self.columns: list[tuple[Cell, ...]] = list(zip(*grid))
        self.groups: list[list[Cell]] = self._build_groups()

        self.reduce_candidates()

    def _initialize_cells(
        self, value_map: list[list[int]], group_map: list[list[int]]
    ) -> list[list[Cell]]:
        """Initialize the cells of the Sudoku puzzle."""
        rows = []
        for row_index, row_values in enumerate(value_map):
            row = []
            for col_index, value in enumerate(row_values):
                cell_value: int | None = value if value != 0 else None
                group = group_map[row_index][col_index]
                cell = create_cell(row_index, col_index, group, cell_value)
                row.append(cell)
            rows.append(row)
        return rows

    def _build_groups(self) -> list[list[Cell]]:
        """Build a list of cell groups from the initialized grid."""
        group_map: dict[int, list[Cell]] = {i: [] for i in range(9)}
        for row in self.rows:
            for cell in row:
                group_map[cell.group].append(cell)
        return list(group_map.values())

    @property
    def is_solved(self) -> bool:
        """Return True if every cell has a value."""
        return all(cell.value is not None for row in self.rows for cell in row)

    @property
    def is_valid_solution(self) -> bool:
        """Return True if every row, column, and group contains each digit
        1–9 exactly once.
        """
        expected = set(range(1, 10))
        return all(
            {cell.value for cell in unit} == expected
            for unit in (*self.rows, *self.columns, *self.groups)
        )

    def is_valid_assignment(self, row: int, column: int, value: int) -> bool:
        """Return True if placing value at (row, column) violates no constraints."""
        target_cell = self.rows[row][column]

        for cell in self.rows[row]:
            if cell is not target_cell and cell.value == value:
                return False

        for cell in self.columns[column]:
            if cell is not target_cell and cell.value == value:
                return False

        for cell in self.groups[target_cell.group]:
            if cell is not target_cell and cell.value == value:
                return False

        return True

    def set_value(self, row: int, column: int, value: int) -> None:
        """Set the value of a cell and propagate constraints."""
        cell = self.rows[row][column]
        if cell.value is None and value in cell.candidates:
            cell.set_value(value)
            self.reduce_candidates()

    def reduce_candidates(self) -> None:
        """Run all reduction strategies, tracking which rule resolves each cell."""
        rules: list[tuple[str, Callable[[], None]]] = [
            ("row elimination", lambda: reduce_rows(self.rows)),
            ("column elimination", lambda: reduce_columns(self.columns)),
            ("group elimination", lambda: reduce_groups(self.groups)),
            ("naked pair", lambda: reduce_naked_pairs(self.groups)),
            ("naked triple", lambda: reduce_naked_triples(self.groups)),
            (
                "hidden single",
                lambda: reduce_hidden_single(self.rows, self.columns, self.groups),
            ),
            ("hidden pair", lambda: reduce_hidden_pair(self.groups)),
            (
                "pinned candidate",
                lambda: reduce_pinned_candidate(self.groups, self.rows, self.columns),
            ),
        ]
        for rule_name, rule_fn in rules:
            pre_multi: set[Cell] = {
                cell
                for row in self.rows
                for cell in row
                if cell.value is None and len(cell.candidates) != 1
            }
            rule_fn()
            for row in self.rows:
                for cell in row:
                    if cell in pre_multi and len(cell.candidates) == 1:
                        cell.set_deciding_rule(rule_name)

    def solve_step(self) -> SolveResult | None:
        """Pick a random single-candidate cell, assign it, and return the result."""
        solvable_cells = [
            cell
            for row in self.rows
            for cell in row
            if cell.value is None and len(cell.candidates) == 1
        ]

        if not solvable_cells:
            return None

        cell = random.choice(solvable_cells)
        value = next(iter(cell.candidates))
        result = SolveResult(
            row=cell.row,
            column=cell.column,
            group=cell.group,
            value=value,
            rule=cell.deciding_rule or "unknown",
        )

        cell.set_value(value)
        self.reduce_candidates()

        return result
