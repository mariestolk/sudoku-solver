"""Basic elimination strategies: row, column, and group."""

from sudoku_solver.cell import Cell


def reduce_rows(rows: list[list[Cell]]) -> None:
    """Reduce candidates in each row based on current values."""
    for row in rows:
        for cell in row:
            if cell.value is not None:
                for other_cell in row:
                    if other_cell is not cell and cell.value in other_cell.candidates:
                        other_cell.candidates.discard(cell.value)


def reduce_columns(columns: list[tuple[Cell, ...]]) -> None:
    """Reduce candidates in each column based on current values."""
    for column in columns:
        for cell in column:
            if cell.value is not None:
                for other_cell in column:
                    if other_cell is not cell and cell.value in other_cell.candidates:
                        other_cell.candidates.discard(cell.value)


def reduce_groups(groups: list[list[Cell]]) -> None:
    """Reduce candidates in each group based on current values."""
    for group in groups:
        for cell in group:
            if cell.value is not None:
                for other_cell in group:
                    if other_cell is not cell and cell.value in other_cell.candidates:
                        other_cell.candidates.discard(cell.value)
