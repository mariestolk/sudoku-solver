"""Tests for the pinned candidate strategy."""

from sudoku_solver.cell import create_cell
from sudoku_solver.strategies.pinned import reduce_pinned_candidate


def test_pinned_to_row_removes_candidate_outside_group() -> None:
    """Ensure a row-pinned candidate is removed from cells in that row outside the group."""
    # Group 0: candidate 5 appears only in row 0 (cells (0,0) and (0,1))
    cell_00 = create_cell(0, 0, 0)
    cell_01 = create_cell(0, 1, 0)
    cell_10 = create_cell(1, 0, 0)
    cell_10.candidates.discard(5)

    cell_02 = create_cell(0, 2, 1)  # row 0, outside group 0

    rows = [[cell_00, cell_01, cell_02], [cell_10]]
    columns = [(cell_00, cell_10), (cell_01,), (cell_02,)]
    reduce_pinned_candidate([[cell_00, cell_01, cell_10]], rows, columns)

    assert 5 not in cell_02.candidates


def test_pinned_to_row_group_cells_keep_candidate() -> None:
    """Ensure group cells keep the pinned candidate after elimination."""
    cell_00 = create_cell(0, 0, 0)
    cell_01 = create_cell(0, 1, 0)
    cell_10 = create_cell(1, 0, 0)
    cell_10.candidates.discard(5)

    cell_02 = create_cell(0, 2, 1)

    rows = [[cell_00, cell_01, cell_02], [cell_10]]
    columns = [(cell_00, cell_10), (cell_01,), (cell_02,)]
    reduce_pinned_candidate([[cell_00, cell_01, cell_10]], rows, columns)

    assert 5 in cell_00.candidates
    assert 5 in cell_01.candidates


def test_no_removal_when_candidate_spans_multiple_rows() -> None:
    """Ensure no candidate is removed when it appears in more than one row of the group."""
    cell_00 = create_cell(0, 0, 0)  # row 0, has 5
    cell_10 = create_cell(1, 0, 0)  # row 1, has 5

    cell_01 = create_cell(0, 1, 1)  # row 0, outside group
    cell_11 = create_cell(1, 1, 1)  # row 1, outside group

    rows = [[cell_00, cell_01], [cell_10, cell_11]]
    columns = [(cell_00, cell_10), (cell_01, cell_11)]
    reduce_pinned_candidate([[cell_00, cell_10]], rows, columns)

    assert 5 in cell_01.candidates
    assert 5 in cell_11.candidates


def test_pinned_to_column_removes_candidate_outside_group() -> None:
    """Ensure a column-pinned candidate is removed from cells in that column outside the group."""
    # Group 0: candidate 7 appears only in column 0 (cells (0,0) and (1,0))
    cell_00 = create_cell(0, 0, 0)
    cell_10 = create_cell(1, 0, 0)
    cell_01 = create_cell(0, 1, 0)
    cell_01.candidates.discard(7)

    cell_20 = create_cell(2, 0, 1)  # column 0, outside group 0

    rows = [[cell_00, cell_01], [cell_10], [cell_20]]
    columns = [(cell_00, cell_10, cell_20), (cell_01,)]
    reduce_pinned_candidate([[cell_00, cell_10, cell_01]], rows, columns)

    assert 7 not in cell_20.candidates
    assert 7 in cell_00.candidates
    assert 7 in cell_10.candidates
