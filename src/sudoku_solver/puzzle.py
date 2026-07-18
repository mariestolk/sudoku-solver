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
from sudoku_solver.strategies.hidden import reduce_hidden_subsets
from sudoku_solver.strategies.intersection import reduce_box_line
from sudoku_solver.strategies.naked import reduce_naked_subsets
from sudoku_solver.strategies.pinned import reduce_pinned_candidate
from sudoku_solver.strategies.rectangle_elimination import (
    reduce_rectangle_elimination,
)
from sudoku_solver.strategies.swordfish import reduce_swordfish
from sudoku_solver.strategies.xwing import reduce_xwing
from sudoku_solver.strategies.xy_chain import reduce_xy_chains

STANDARD_GROUP_MAP: list[list[int]] = [
    [(r // 3) * 3 + (c // 3) for c in range(9)] for r in range(9)
]


class PuzzleData(NamedTuple):
    """A sudoku puzzle defined by its initial values and group layout."""

    values: list[list[int]]
    groups: list[list[int]] | None = None
    solution: list[list[int]] | None = None


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
        self.columns: list[list[Cell]] = [list(col) for col in zip(*grid)]
        self.groups: list[list[Cell]] = self._build_groups()
        self._naked_singles: set[Cell] = set()

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

    def reduce_candidates(self) -> None:
        """Run all reduction strategies, tracking which rule resolves each cell."""
        rules: list[tuple[str, Callable[[], None]]] = [
            ("row elimination", lambda: reduce_rows(self.rows)),
            ("column elimination", lambda: reduce_columns(self.columns)),
            ("group elimination", lambda: reduce_groups(self.groups)),
            (
                "naked subset",
                lambda: reduce_naked_subsets(
                    self.rows,
                    self.columns,
                    self.groups,
                ),
            ),
            (
                "hidden subset",
                lambda: reduce_hidden_subsets(
                    self.rows,
                    self.columns,
                    self.groups,
                ),
            ),
            ("x-wing", lambda: reduce_xwing(self.rows, self.columns)),
            ("swordfish", lambda: reduce_swordfish(self.rows, self.columns)),
            (
                "pinned candidate",
                lambda: reduce_pinned_candidate(
                    self.groups,
                    self.rows,
                    self.columns,
                ),
            ),
            (
                "rectangle elimination",
                lambda: reduce_rectangle_elimination(
                    self.rows,
                    self.columns,
                    self.groups,
                ),
            ),
            (
                "box/line reduction",
                lambda: reduce_box_line(
                    self.rows,
                    self.columns,
                    self.groups,
                ),
            ),
            (
                "xy-chain",
                lambda: reduce_xy_chains(
                    self.rows,
                    self.columns,
                    self.groups,
                ),
            ),
        ]

        multi: set[Cell] = {
            cell
            for row in self.rows
            for cell in row
            if cell.value is None and len(cell.candidates) > 1
        }

        for rule_name, rule_fn in rules:
            rule_fn()

            resolved = {cell for cell in multi if len(cell.candidates) == 1}

            for cell in resolved:
                if cell.deciding_rule is None:
                    cell.set_deciding_rule(rule_name)

            self._naked_singles.update(resolved)
            multi.difference_update(resolved)

    def solve_step(self) -> SolveResult | None:
        """Pick a random single-candidate cell, assign it, and return the result."""
        if not self._naked_singles:
            return None

        cell = random.choice(tuple(self._naked_singles))
        self._naked_singles.discard(cell)
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
