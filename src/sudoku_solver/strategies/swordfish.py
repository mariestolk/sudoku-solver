"""Swordfish strategy."""

from itertools import combinations

from sudoku_solver.cell import Cell


def reduce_swordfish(rows: list[list[Cell]], columns: list[list[Cell]]) -> None:
    """Reduce candidates using the Swordfish pattern.

    If a candidate appears in 2 or 3 cells in each of three rows, and the union
    of those column positions is exactly 3, eliminate the candidate from all
    other cells in those three columns. Applies symmetrically for columns.
    """
    _reduce_swordfish_in_lines(rows, columns)
    _reduce_swordfish_in_lines(columns, rows)


def _reduce_swordfish_in_lines(
    primary: list[list[Cell]], secondary: list[list[Cell]]
) -> None:
    """Scan primary lines for Swordfish patterns and eliminate from secondary lines."""
    for candidate in range(1, 10):
        eligible: list[tuple[int, frozenset[int]]] = []
        for line_idx, line in enumerate(primary):
            positions = frozenset(
                i
                for i, cell in enumerate(line)
                if cell.value is None and candidate in cell.candidates
            )
            if 2 <= len(positions) <= 3:
                eligible.append((line_idx, positions))

        for (i1, p1), (i2, p2), (i3, p3) in combinations(eligible, 3):
            union = p1 | p2 | p3
            if len(union) != 3:
                continue
            fish_cells = {
                primary[idx][pos]
                for idx, pos_set in ((i1, p1), (i2, p2), (i3, p3))
                for pos in pos_set
            }
            for sec_idx in union:
                for cell in secondary[sec_idx]:
                    if cell not in fish_cells:
                        cell.candidates.discard(candidate)
