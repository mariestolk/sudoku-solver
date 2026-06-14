"""Box/line reduction strategy."""

from sudoku_solver.cell import Cell


def reduce_box_line(
    rows: list[list[Cell]],
    columns: list[list[Cell]],
    groups: list[list[Cell]],
) -> None:
    """Reduce candidates in a group that are confined to one row or column.

    If all occurrences of a candidate in a row or column belong to the same group,
    that candidate can be eliminated from the rest of that group.
    """
    for line in (*rows, *columns):
        candidate_groups: dict[int, set[int]] = {}
        for cell in line:
            if cell.value is None:
                for candidate in cell.candidates:
                    candidate_groups.setdefault(candidate, set()).add(cell.group)

        line_set = frozenset(line)
        for candidate, group_ids in candidate_groups.items():
            if len(group_ids) == 1:
                group_id = next(iter(group_ids))
                for cell in groups[group_id]:
                    if cell not in line_set and candidate in cell.candidates:
                        cell.candidates.discard(candidate)
