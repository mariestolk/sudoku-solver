"""Hidden single and hidden pair strategies."""

from sudoku_solver.cell import Cell


def reduce_hidden_single(
    rows: list[list[Cell]],
    columns: list[tuple[Cell, ...]],
    groups: list[list[Cell]],
) -> None:
    """Reduce candidates by finding single candidates in rows, columns, and groups."""
    units: list[list[Cell]] = [
        *rows,
        *[list(col) for col in columns],
        *groups,
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


def reduce_hidden_pair(groups: list[list[Cell]]) -> None:
    """Reduce candidates by finding hidden pairs in each group."""
    for group in groups:
        candidate_map: dict[int, list[Cell]] = {}
        for cell in group:
            if cell.value is None:
                for candidate in cell.candidates:
                    candidate_map.setdefault(candidate, []).append(cell)
        for candidate, cells in candidate_map.items():
            if len(cells) == 2:
                for other_cell in group:
                    if other_cell not in cells and candidate in other_cell.candidates:
                        other_cell.candidates.discard(candidate)
