"""Tests for the column elimination strategy."""

from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.elimination import reduce_columns


def make_column(values: list[int | None], column_index: int = 0) -> tuple[Cell, ...]:
    """Build a column of cells; None means unsolved (candidates 1–9)."""
    return tuple(create_cell(row, column_index, 0, v) for row, v in enumerate(values))


def test_solved_cell_value_removed_from_peers() -> None:
    """Ensure a solved cell value is removed from its column peers."""
    column = make_column([5, None, None])
    reduce_columns([column])
    assert 5 not in column[1].candidates
    assert 5 not in column[2].candidates


def test_other_candidates_left_intact() -> None:
    """Ensure only the solved value is removed and other candidate values remain."""
    column = make_column([5, None, None])
    reduce_columns([column])
    assert column[1].candidates == {1, 2, 3, 4, 6, 7, 8, 9}
    assert column[2].candidates == {1, 2, 3, 4, 6, 7, 8, 9}


def test_does_not_affect_other_columns() -> None:
    """Ensure column elimination does not remove candidates from other columns."""
    col0 = make_column([5, None, None], column_index=0)
    col1 = make_column([None, None, None], column_index=1)
    reduce_columns([col0, col1])
    assert 5 in col1[0].candidates
    assert 5 in col1[1].candidates
    assert 5 in col1[2].candidates


def test_multiple_solved_cells_all_values_removed() -> None:
    """Ensure all solved values are removed from other column cells."""
    column = make_column([3, 7, None, None])
    reduce_columns([column])
    assert 3 not in column[2].candidates
    assert 7 not in column[2].candidates
    assert 3 not in column[3].candidates
    assert 7 not in column[3].candidates


def test_no_op_when_no_solved_cells() -> None:
    """Ensure no candidates are removed when the column has no solved cells."""
    column = make_column([None, None, None])
    before = [set(cell.candidates) for cell in column]
    reduce_columns([column])
    for cell, original in zip(column, before):
        assert cell.candidates == original
