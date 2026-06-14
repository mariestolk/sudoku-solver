"""Tests for the box/line reduction strategy."""

from sudoku_solver.cell import create_cell
from sudoku_solver.strategies.intersection import reduce_box_line


def test_row_confined_candidate_removes_from_group() -> None:
    """Candidate confined to one group in a row is removed from the rest of that group."""
    # Row 0: cell_00 (group 0, has 5), cell_01 (group 1, no 5)
    # Group 0: cell_00 + cell_10 (row 1, has 5) -> cell_10 should lose candidate 5
    cell_00 = create_cell(0, 0, 0)
    cell_01 = create_cell(0, 1, 1)
    cell_01.candidates.discard(5)
    cell_10 = create_cell(1, 0, 0)

    rows = [[cell_00, cell_01], [cell_10]]
    columns = [[cell_00, cell_10], [cell_01]]
    groups = [[cell_00, cell_10], [cell_01]]

    reduce_box_line(rows, columns, groups)

    assert 5 not in cell_10.candidates


def test_row_confined_candidate_keeps_in_row_cells() -> None:
    """Cells within the row that triggered the elimination keep their candidate."""
    cell_00 = create_cell(0, 0, 0)
    cell_01 = create_cell(0, 1, 1)
    cell_01.candidates.discard(5)
    cell_10 = create_cell(1, 0, 0)

    rows = [[cell_00, cell_01], [cell_10]]
    columns = [[cell_00, cell_10], [cell_01]]
    groups = [[cell_00, cell_10], [cell_01]]

    reduce_box_line(rows, columns, groups)

    assert 5 in cell_00.candidates


def test_no_removal_when_candidate_spans_multiple_groups_in_row() -> None:
    """No elimination when a candidate appears in more than one group within the row."""
    # Row 0: cell_00 (group 0, has 5), cell_01 (group 1, has 5) -> spans two groups
    cell_00 = create_cell(0, 0, 0)
    cell_01 = create_cell(0, 1, 1)
    cell_10 = create_cell(1, 0, 0)  # group 0, not in row 0

    rows = [[cell_00, cell_01], [cell_10]]
    columns = [[cell_00, cell_10], [cell_01]]
    groups = [[cell_00, cell_10], [cell_01]]

    reduce_box_line(rows, columns, groups)

    assert 5 in cell_10.candidates


def test_column_confined_candidate_removes_from_group() -> None:
    """Candidate confined to one group in a column is removed from the rest of that group."""
    # Col 0: cell_00 (group 0), cell_10 (group 0) — candidate 7 confined to group 0 in col 0
    # Col 1: cell_01 (group 1), cell_11 (group 1) — spans only group 1
    # Col 2: cell_02 (group 0), cell_12 (group 1) — spans both groups, no col-level reduction
    # Each row spans groups 0 and 1, so row-level box/line does not fire.
    # Expectation: col 0 processing removes 7 from cell_02 (group 0, outside col 0).
    cell_00 = create_cell(0, 0, 0)
    cell_01 = create_cell(0, 1, 1)
    cell_02 = create_cell(0, 2, 0)
    cell_10 = create_cell(1, 0, 0)
    cell_11 = create_cell(1, 1, 1)
    cell_12 = create_cell(1, 2, 1)

    rows = [[cell_00, cell_01, cell_02], [cell_10, cell_11, cell_12]]
    columns = [[cell_00, cell_10], [cell_01, cell_11], [cell_02, cell_12]]
    groups = [[cell_00, cell_10, cell_02], [cell_01, cell_11, cell_12]]

    reduce_box_line(rows, columns, groups)

    assert 7 not in cell_02.candidates
    assert 7 in cell_00.candidates
    assert 7 in cell_10.candidates
