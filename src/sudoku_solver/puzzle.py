"""Sudoku puzzle solver using constraint propagation.

This module provides the Puzzle class for representing and solving
Sudoku puzzles through candidate reduction and constraint propagation.
"""

import random
from collections.abc import Callable, Sequence

from rich import print as rprint

from sudoku_solver.cell import Cell, create_cell

STANDARD_GROUP_MAP: list[list[int]] = [
    [(r // 3) * 3 + (c // 3) for c in range(9)] for r in range(9)
]

color_map: dict[int, str] = {
    0: "red",
    1: "green",
    2: "blue",
    3: "yellow",
    4: "magenta",
    5: "cadet_blue",
    6: "orange1",
    7: "bright_black",
    8: "white",
}


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
        self.solved: bool = False

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

    def is_solved(self) -> bool:
        """Check if the puzzle is solved."""
        for row in self.rows:
            if any(cell.value is None for cell in row):
                return False
        self.solved = True
        return True

    def is_valid_assignment(self, row: int, column: int, value: int) -> bool:
        """Check if assigning a value to a cell is valid."""
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
        """Set the value of a cell at the specified row and column."""
        cell = self.rows[row][column]
        if cell.value is None and value in cell.candidates:
            cell.set_value(value)
            self.reduce_candidates()
            self.is_solved()

    def print_puzzle(self) -> None:
        """Print the Sudoku puzzle row by row, coloring cells by group."""
        grid: list[list[Cell | None]] = [[None for _ in range(9)] for _ in range(9)]

        for puzzle_row in self.rows:
            for cell in puzzle_row:
                grid[cell.row][cell.column] = cell

        for row in grid:
            row_output = ""
            for maybe_cell in row:
                if maybe_cell is not None and maybe_cell.value is not None:
                    color = color_map[maybe_cell.group]
                    row_output += f"[{color}]{maybe_cell.value}[/] "
                elif maybe_cell is not None:
                    row_output += f"[{color_map[maybe_cell.group]}].[/] "
            rprint(row_output)

    def print_candidate(self, row: int, column: int) -> None:
        """Print the candidates of a specific cell."""
        cell = self.rows[row][column]
        if cell.candidates:
            rprint(
                f"[{color_map[cell.group]}]Candidates for cell ({row}, {column}): "
                f"{sorted(cell.candidates)}[/]"
            )
        else:
            rprint(
                f"[{color_map[cell.group]}]No candidates for cell ({row}, {column})[/]"
            )

    def print_candidate_group(self, group: int) -> None:
        """Print the candidates for all cells in a specific group."""
        rprint(f"[{color_map[group]}]Candidates for group {group}:[/]")
        for cell in self.groups[group]:
            if cell.candidates:
                rprint(f"Cell ({cell.row}, {cell.column}): {sorted(cell.candidates)}")
            else:
                rprint(f"Cell ({cell.row}, {cell.column}): No candidates")

    def print_candidates(self) -> None:
        """Print the candidates for every cell in the grid."""
        for row in self.rows:
            for cell in row:
                if cell.candidates:
                    rprint(
                        f"[{color_map[cell.group]}]{sorted(cell.candidates)}[/]",
                        end=" ",
                    )
                    rprint()
                else:
                    rprint("[grey].[/]", end=" ")
                    rprint()

    def _reduce_row_candidates(self) -> None:
        """Reduce candidates in each row based on current values."""
        for row in self.rows:
            for cell in row:
                if cell.value is not None:
                    for other_cell in row:
                        if (
                            other_cell is not cell
                            and cell.value in other_cell.candidates
                        ):
                            other_cell.candidates.discard(cell.value)

    def _reduce_column_candidates(self) -> None:
        """Reduce candidates in each column based on current values."""
        for column in self.columns:
            for cell in column:
                if cell.value is not None:
                    for other_cell in column:
                        if (
                            other_cell is not cell
                            and cell.value in other_cell.candidates
                        ):
                            other_cell.candidates.discard(cell.value)

    def _reduce_group_candidates(self) -> None:
        """Reduce candidates in each group based on current values."""
        for group in self.groups:
            for cell in group:
                if cell.value is not None:
                    for other_cell in group:
                        if (
                            other_cell is not cell
                            and cell.value in other_cell.candidates
                        ):
                            other_cell.candidates.discard(cell.value)

    def _reduce_hidden_single(self) -> None:
        """Reduce candidates by finding single candidates in groups."""
        units: list[list[Cell]] = [
            *self.rows,
            *[list(col) for col in self.columns],
            *self.groups,
        ]
        for unit in units:
            candidate_map: dict[int, list[Cell]] = {}
            for cell in unit:
                if cell.value is None:
                    for candidate in cell.candidates:
                        candidate_map.setdefault(candidate, []).append(cell)
            for candidate, cells in candidate_map.items():
                if len(cells) == 1 and len(cells[0].candidates) > 1:
                    cells[0].set_candidates([candidate])

    def _reduce_naked_pairs(self) -> None:
        """Reduce candidates by identifying naked pairs (clingy sets) in each group."""
        for group in self.groups:
            two_candidate_cells = [
                cell
                for cell in group
                if cell.value is None and len(cell.candidates) == 2
            ]

            candidate_pair_map: dict[tuple[int, ...], list[Cell]] = {}
            for cell in two_candidate_cells:
                key = tuple(sorted(cell.candidates))
                candidate_pair_map.setdefault(key, []).append(cell)

            for candidate_pair, cells in candidate_pair_map.items():
                if len(cells) == 2:
                    for other_cell in group:
                        if other_cell not in cells and other_cell.value is None:
                            other_cell.candidates.difference_update(candidate_pair)

    def _reduce_naked_triples(self) -> None:
        """Reduce candidates by identifying naked triples in each group."""
        for group in self.groups:
            three_candidate_cells = [
                cell
                for cell in group
                if cell.value is None and len(cell.candidates) == 3
            ]

            candidate_triplet_map: dict[tuple[int, ...], list[Cell]] = {}
            for cell in three_candidate_cells:
                key = tuple(sorted(cell.candidates))
                candidate_triplet_map.setdefault(key, []).append(cell)

            for candidate_triplet, cells in candidate_triplet_map.items():
                if len(cells) == 3:
                    for other_cell in group:
                        if other_cell not in cells and other_cell.value is None:
                            other_cell.candidates.difference_update(candidate_triplet)

    def _reduce_hidden_pair(self) -> None:
        """Reduce candidates by finding hidden pairs in each group."""
        for group in self.groups:
            candidate_map: dict[int, list[Cell]] = {}
            for cell in group:
                if cell.value is None:
                    for candidate in cell.candidates:
                        candidate_map.setdefault(candidate, []).append(cell)

            for candidate, cells in candidate_map.items():
                if len(cells) == 2:
                    for other_cell in group:
                        if (
                            other_cell not in cells
                            and candidate in other_cell.candidates
                        ):
                            other_cell.candidates.discard(candidate)

    def _remove_candidate_from_line(
        self, candidate: int, line: Sequence[Cell], group: list[Cell]
    ) -> None:
        """Helper to remove candidate from a row or column outside the current group."""
        for cell in line:
            if cell not in group and candidate in cell.candidates:
                cell.candidates.discard(candidate)

    def _reduce_pinned_candidate(self) -> None:
        """Reduce candidates that only occur on one row or column within a group."""
        for group in self.groups:
            candidate_map: dict[int, dict[str, set[int]]] = {}
            for cell in group:
                if cell.value is None:
                    for candidate in cell.candidates:
                        if candidate not in candidate_map:
                            candidate_map[candidate] = {"rows": set(), "columns": set()}
                        candidate_map[candidate]["rows"].add(cell.row)
                        candidate_map[candidate]["columns"].add(cell.column)

            for candidate, positions in candidate_map.items():
                if len(positions["rows"]) == 1:
                    row = next(iter(positions["rows"]))
                    self._remove_candidate_from_line(candidate, self.rows[row], group)

                if len(positions["columns"]) == 1:
                    column = next(iter(positions["columns"]))
                    self._remove_candidate_from_line(
                        candidate, self.columns[column], group
                    )

    def reduce_candidates(self) -> None:
        """Reduce candidates based on current values in the puzzle."""
        rules: list[tuple[str, Callable[[], None]]] = [
            ("row elimination", self._reduce_row_candidates),
            ("column elimination", self._reduce_column_candidates),
            ("group elimination", self._reduce_group_candidates),
            ("naked pair", self._reduce_naked_pairs),
            ("naked triple", self._reduce_naked_triples),
            ("hidden single", self._reduce_hidden_single),
            ("hidden pair", self._reduce_hidden_pair),
            ("pinned candidate", self._reduce_pinned_candidate),
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
                        cell.deciding_rule = rule_name

    def solve_step(self) -> bool:
        """Perform a single step of solving the Sudoku puzzle."""
        solvable_cells = [
            cell
            for row in self.rows
            for cell in row
            if cell.value is None and len(cell.candidates) == 1
        ]

        if not solvable_cells:
            return False

        cell = random.choice(solvable_cells)
        value = next(iter(cell.candidates))
        rule = cell.deciding_rule or "unknown"

        rprint(
            f"[{color_map[cell.group]}]Cell ({cell.row}, {cell.column}) → {value}[/]"
            f"  \\[{rule}]"
        )
        cell.set_value(value)
        self.reduce_candidates()

        if self.is_solved():
            rprint()
            rprint("[magenta]Puzzle is solved![/]")
            rprint()

        return True
