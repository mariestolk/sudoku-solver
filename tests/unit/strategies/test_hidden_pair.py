"""Tests for the hidden pair strategy."""

from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.hidden import reduce_hidden_pair


def make_group(candidate_sets: list[list[int]], group_index: int = 0) -> list[Cell]:
    """Build a group of unsolved cells with the given candidate sets."""
    cells = []
    for row, candidates in enumerate(candidate_sets):
        cell = create_cell(row, 0, group_index)
        cell.set_candidates(candidates)
        cells.append(cell)
    return cells


def test_hidden_pair_narrows_pair_cells_to_pair_values() -> None:
    """Ensure pair cells are narrowed to only the two shared values."""
    # 1 and 3 appear only in cells 0 and 1; cells 0 and 1 must contain {1, 3}
    group = make_group([[1, 3, 5], [1, 3, 7], [2, 4, 5]])
    reduce_hidden_pair([group])
    assert group[0].candidates == {1, 3}
    assert group[1].candidates == {1, 3}


def test_non_pair_cell_is_not_modified() -> None:
    """Ensure cells outside the hidden pair keep all their candidates."""
    group = make_group([[1, 3, 5], [1, 3, 7], [2, 4, 5]])
    reduce_hidden_pair([group])
    assert group[2].candidates == {2, 4, 5}


def test_no_change_when_no_hidden_pair_exists() -> None:
    """Ensure nothing is removed when no hidden pair exists."""
    group = make_group([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
    before = [set(cell.candidates) for cell in group]
    reduce_hidden_pair([group])
    for cell, original in zip(group, before):
        assert cell.candidates == original


def test_does_not_affect_other_groups() -> None:
    """Ensure hidden pair elimination is isolated to the affected group."""
    group0 = make_group([[1, 3, 5], [1, 3, 7], [2, 4, 5]])
    group1 = make_group([[6, 7, 8], [5, 9]])
    reduce_hidden_pair([group0, group1])
    assert group1[0].candidates == {6, 7, 8}
    assert group1[1].candidates == {5, 9}


def test_hidden_pair_narrows_cells_in_row() -> None:
    """Ensure hidden pair elimination works when the unit is a row."""
    c0 = create_cell(0, 0, 0)
    c1 = create_cell(0, 1, 0)
    c2 = create_cell(0, 2, 1)
    c0.set_candidates([1, 3, 5])
    c1.set_candidates([1, 3, 7])
    c2.set_candidates([2, 4, 5])
    reduce_hidden_pair([[c0, c1, c2]])
    assert c0.candidates == {1, 3}
    assert c1.candidates == {1, 3}
    assert c2.candidates == {2, 4, 5}


def test_hidden_pair_narrows_cells_in_column() -> None:
    """Ensure hidden pair elimination works when the unit is a column."""
    c0 = create_cell(0, 0, 0)
    c1 = create_cell(1, 0, 0)
    c2 = create_cell(2, 0, 1)
    c0.set_candidates([1, 3, 5])
    c1.set_candidates([1, 3, 7])
    c2.set_candidates([2, 4, 5])
    reduce_hidden_pair([[c0, c1, c2]])
    assert c0.candidates == {1, 3}
    assert c1.candidates == {1, 3}
    assert c2.candidates == {2, 4, 5}
