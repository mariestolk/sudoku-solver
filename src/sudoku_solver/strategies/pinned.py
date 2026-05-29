"""Pinned candidate strategy."""

from collections.abc import Sequence

from sudoku_solver.cell import Cell


def _remove_from_line(
    candidate: int, line: Sequence[Cell], group_set: frozenset[Cell]
) -> None:
    """Remove a candidate from cells in a row or column that lie outside the group."""
    for cell in line:
        if cell not in group_set and candidate in cell.candidates:
            cell.candidates.discard(candidate)


def reduce_pinned_candidate(
    groups: list[list[Cell]],
    rows: list[list[Cell]],
    columns: list[list[Cell]],
) -> None:
    """Reduce candidates that only occur on one row or column within a group."""
    for group in groups:
        group_set = frozenset(group)
        candidate_rows: dict[int, set[int]] = {}
        candidate_cols: dict[int, set[int]] = {}

        for cell in group:
            if cell.value is None:
                for candidate in cell.candidates:
                    candidate_rows.setdefault(candidate, set()).add(cell.row)
                    candidate_cols.setdefault(candidate, set()).add(cell.column)

        for candidate, row_set in candidate_rows.items():
            if len(row_set) == 1:
                _remove_from_line(candidate, rows[next(iter(row_set))], group_set)
        for candidate, col_set in candidate_cols.items():
            if len(col_set) == 1:
                _remove_from_line(candidate, columns[next(iter(col_set))], group_set)
