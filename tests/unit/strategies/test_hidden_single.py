"""Tests for the hidden single strategy."""

from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.hidden import reduce_hidden_single


def make_cells(candidate_sets: list[list[int]], group: int = 0) -> list[Cell]:
    """Build a list of unsolved cells with the given candidate sets."""
    cells = []
    for col, candidates in enumerate(candidate_sets):
        cell = create_cell(0, col, group)
        cell.set_candidates(candidates)
        cells.append(cell)
    return cells


def test_hidden_single_narrows_cell_in_row() -> None:
    """Ensure a cell is narrowed to one candidate when candidate is unique in a row."""
    cells = make_cells([[1, 2, 3], [4, 5, 9], [6, 7, 8]])
    reduce_hidden_single([cells], [], [])
    assert cells[1].candidates == {9}


def test_hidden_single_narrows_cell_in_column() -> None:
    """Ensure a cell is narrowed to one candidate when that
    candidate is unique in a column."""
    cell_a = create_cell(0, 0, 0)
    cell_a.set_candidates([1, 2, 3])
    cell_b = create_cell(1, 0, 0)
    cell_b.set_candidates([4, 5, 9])
    cell_c = create_cell(2, 0, 0)
    cell_c.set_candidates([6, 7, 8])
    column = (cell_a, cell_b, cell_c)
    reduce_hidden_single([], [column], [])
    assert cell_b.candidates == {9}


def test_hidden_single_narrows_cell_in_group() -> None:
    """Ensure a cell is narrowed to one candidate when that
    candidate is unique in a group."""
    cells = make_cells([[1, 2, 3], [4, 5, 9], [6, 7, 8]])
    reduce_hidden_single([], [], [cells])
    assert cells[1].candidates == {9}


def test_no_change_when_candidate_in_multiple_cells() -> None:
    """Ensure no cell is narrowed when every candidate appears in more than one cell."""
    cells = make_cells([[1, 2], [1, 2]])
    reduce_hidden_single([cells], [], [])
    assert cells[0].candidates == {1, 2}
    assert cells[1].candidates == {1, 2}


def test_no_change_when_cell_already_has_single_candidate() -> None:
    """Ensure a cell already at one candidate is not modified."""
    cell_a = create_cell(0, 0, 0)
    cell_a.set_candidates([9])
    cell_b = create_cell(0, 1, 0)
    cell_b.set_candidates([1, 2])
    cell_c = create_cell(0, 2, 0)
    cell_c.set_candidates([1, 2])
    reduce_hidden_single([[cell_a, cell_b, cell_c]], [], [])
    assert cell_a.candidates == {9}
    assert cell_b.candidates == {1, 2}
    assert cell_c.candidates == {1, 2}
