"""Pinned candidate strategy."""

from collections.abc import Sequence

from sudoku_solver.cell import Cell


def _remove_from_line(
    candidate: int, line: Sequence[Cell], group: list[Cell]
) -> None:
    """Remove a candidate from cells in a row or column that lie outside the group."""
    for cell in line:
        if cell not in group and candidate in cell.candidates:
            cell.candidates.discard(candidate)


def reduce_pinned_candidate(
    groups: list[list[Cell]],
    rows: list[list[Cell]],
    columns: list[tuple[Cell, ...]],
) -> None:
    """Reduce candidates that only occur on one row or column within a group."""
    for group in groups:
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
                _remove_from_line(candidate, rows[row], group)
            if len(positions["columns"]) == 1:
                column = next(iter(positions["columns"]))
                _remove_from_line(candidate, columns[column], group)
