"""Pure formatting functions for sudoku puzzle display.

Each function returns a Rich markup string. Callers are responsible for
printing via rprint.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku_solver.cell import Cell

if TYPE_CHECKING:
    from sudoku_solver.puzzle import SolveResult

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


def format_puzzle(rows: list[list[Cell]]) -> str:
    """Return a Rich markup string of the full puzzle grid."""
    grid: list[list[Cell | None]] = [[None for _ in range(9)] for _ in range(9)]
    for puzzle_row in rows:
        for cell in puzzle_row:
            grid[cell.row][cell.column] = cell

    lines = []
    for row in grid:
        row_output = ""
        for maybe_cell in row:
            if maybe_cell is not None and maybe_cell.value is not None:
                color = color_map[maybe_cell.group]
                row_output += f"[{color}]{maybe_cell.value}[/] "
            elif maybe_cell is not None:
                row_output += f"[{color_map[maybe_cell.group]}].[/] "
        lines.append(row_output)
    return "\n".join(lines)


def format_step(result: SolveResult) -> str:
    """Return a Rich markup string describing a single solve step."""
    return (
        f"[{color_map[result.group]}]Cell ({result.row}, {result.column})"
        f" → {result.value}[/]  \\[{result.rule}]"
    )
