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
    0: "#e03524",
    1: "#4040a0",
    2: "#ffc200",
    3: "#90bc1a",
    4: "#0095ac",
    5: "#21b534",
    6: "#1f64ad",
    7: "#f07c12",
    8: "#903498",
}


def format_puzzle(rows: list[list[Cell]]) -> str:
    """Return a Rich markup string of the full puzzle grid."""
    grid: list[list[Cell | None]] = [[None for _ in range(9)] for _ in range(9)]
    for puzzle_row in rows:
        for cell in puzzle_row:
            grid[cell.row][cell.column] = cell

    pad = " "

    def cell_str(cell: Cell | None) -> str:
        if cell is None:
            return f"{pad}.{pad}"
        char = str(cell.value) if cell.value is not None else "."
        return f"[{color_map[cell.group]}]{pad}{char}{pad}[/]"

    def diff(a: Cell | None, b: Cell | None) -> bool:
        return a is not None and b is not None and a.group != b.group

    def v_sep(r: int, c: int) -> str:
        return "┃" if diff(grid[r][c], grid[r][c + 1]) else "│"

    def h_char(r: int, c: int) -> str:
        return "━" if diff(grid[r][c], grid[r + 1][c]) else "─"

    def intersection(r: int, c: int) -> str:
        h = diff(grid[r][c], grid[r + 1][c]) or diff(grid[r][c + 1], grid[r + 1][c + 1])
        v = diff(grid[r][c], grid[r][c + 1]) or diff(grid[r + 1][c], grid[r + 1][c + 1])
        if h and v:
            return "╋"
        if h:
            return "┿"
        if v:
            return "╂"
        return "┼"

    lines = []
    for r in range(9):
        row_output = cell_str(grid[r][0])
        for c in range(8):
            row_output += v_sep(r, c) + cell_str(grid[r][c + 1])
        lines.append(row_output)
        if r < 8:
            sep_parts = []
            for c in range(9):
                sep_parts.append(h_char(r, c) * 3)
                if c < 8:
                    sep_parts.append(intersection(r, c))
            lines.append("".join(sep_parts))

    return "\n".join(lines)


def format_step(result: SolveResult) -> str:
    """Return a Rich markup string describing a single solve step."""
    return (
        f"[{color_map[result.group]}]Cell ({result.row}, {result.column})"
        f" → {result.value}[/]  \\[{result.rule}]"
    )
