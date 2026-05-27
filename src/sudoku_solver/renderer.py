"""Display functions for rendering sudoku puzzles."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich import print as rprint

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


def print_puzzle(rows: list[list[Cell]]) -> None:
    """Print the Sudoku puzzle row by row, coloring cells by group."""
    grid: list[list[Cell | None]] = [[None for _ in range(9)] for _ in range(9)]
    for puzzle_row in rows:
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


def print_candidate(rows: list[list[Cell]], row: int, column: int) -> None:
    """Print the candidates of a specific cell."""
    cell = rows[row][column]
    if cell.candidates:
        rprint(
            f"[{color_map[cell.group]}]Candidates for cell ({row}, {column}): "
            f"{sorted(cell.candidates)}[/]"
        )
    else:
        rprint(f"[{color_map[cell.group]}]No candidates for cell ({row}, {column})[/]")


def print_candidate_group(groups: list[list[Cell]], group: int) -> None:
    """Print the candidates for all cells in a specific group."""
    rprint(f"[{color_map[group]}]Candidates for group {group}:[/]")
    for cell in groups[group]:
        if cell.candidates:
            rprint(f"Cell ({cell.row}, {cell.column}): {sorted(cell.candidates)}")
        else:
            rprint(f"Cell ({cell.row}, {cell.column}): No candidates")


def print_step(result: SolveResult) -> None:
    """Print the outcome of a single solve step."""
    rprint(
        f"[{color_map[result.group]}]Cell ({result.row}, {result.column})"
        f" → {result.value}[/]  \\[{result.rule}]"
    )


def print_candidates(rows: list[list[Cell]]) -> None:
    """Print the candidates for every cell in the grid."""
    for row in rows:
        for cell in row:
            if cell.candidates:
                rprint(
                    f"[{color_map[cell.group]}]{sorted(cell.candidates)}[/]", end=" "
                )
                rprint()
            else:
                rprint("[grey].[/]", end=" ")
                rprint()
