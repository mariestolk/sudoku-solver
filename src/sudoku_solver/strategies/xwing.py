"""X-wing strategy."""

from sudoku_solver.cell import Cell


def reduce_xwing(rows: list[list[Cell]], columns: list[list[Cell]]) -> None:
    """Reduce candidates using the X-wing pattern.

    If a candidate appears in exactly two cells in each of two rows, and those
    cells share the same two columns, eliminate the candidate from all other
    cells in those two columns. Applies symmetrically for columns.
    """
    _reduce_xwing_in_lines(rows, columns)
    _reduce_xwing_in_lines(columns, rows)


def _reduce_xwing_in_lines(
    primary: list[list[Cell]], secondary: list[list[Cell]]
) -> None:
    """Scan primary lines for X-wing patterns and eliminate from secondary lines."""
    for candidate in range(1, 10):
        position_groups: dict[tuple[int, int], list[int]] = {}
        for line_idx, line in enumerate(primary):
            positions = [
                i
                for i, cell in enumerate(line)
                if cell.value is None and candidate in cell.candidates
            ]
            if len(positions) == 2:
                key = (positions[0], positions[1])
                position_groups.setdefault(key, []).append(line_idx)

        for (pos0, pos1), line_indices in position_groups.items():
            if len(line_indices) >= 2:
                wing_cells = {
                    primary[idx][pos] for idx in line_indices for pos in (pos0, pos1)
                }
                for sec_idx in (pos0, pos1):
                    for cell in secondary[sec_idx]:
                        if cell not in wing_cells:
                            cell.candidates.discard(candidate)
