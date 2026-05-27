"""Tests for the row elimination strategy."""

from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.elimination import reduce_rows


def make_row(values: list[int | None], row_index: int = 0) -> list[Cell]:
    """Build a row of cells; None means unsolved (candidates 1–9)."""
    return [create_cell(row_index, col, 0, v) for col, v in enumerate(values)]


def test_solved_cell_value_removed_from_peers() -> None:
    """Ensure a solved cell value is removed from its row peers."""
    row = make_row([5, None, None])
    reduce_rows([row])
    assert 5 not in row[1].candidates
    assert 5 not in row[2].candidates


def test_other_candidates_left_intact() -> None:
    """Ensure only the solved value is removed and other candidate values remain."""
    row = make_row([5, None, None])
    reduce_rows([row])
    assert row[1].candidates == {1, 2, 3, 4, 6, 7, 8, 9}
    assert row[2].candidates == {1, 2, 3, 4, 6, 7, 8, 9}


def test_does_not_affect_other_rows() -> None:
    """Ensure row elimination does not remove candidates from other rows."""
    row0 = make_row([5, None, None], row_index=0)
    row1 = make_row([None, None, None], row_index=1)
    reduce_rows([row0, row1])
    assert 5 in row1[0].candidates
    assert 5 in row1[1].candidates
    assert 5 in row1[2].candidates


def test_multiple_solved_cells_all_values_removed() -> None:
    """Ensure all solved values are removed from other row cells."""
    row = make_row([3, 7, None, None])
    reduce_rows([row])
    assert 3 not in row[2].candidates
    assert 7 not in row[2].candidates
    assert 3 not in row[3].candidates
    assert 7 not in row[3].candidates


def test_no_op_when_no_solved_cells() -> None:
    """Ensure no candidates are removed when the row has no solved cells."""
    row = make_row([None, None, None])
    before = [set(cell.candidates) for cell in row]
    reduce_rows([row])
    for cell, original in zip(row, before):
        assert cell.candidates == original
