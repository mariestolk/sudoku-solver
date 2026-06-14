"""Tests for the naked pairs strategy."""

from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.naked import reduce_naked_pairs


def make_group(candidate_sets: list[list[int]], group_index: int = 0) -> list[Cell]:
    """Build a group of unsolved cells with the given candidate sets."""
    cells = []
    for row, candidates in enumerate(candidate_sets):
        cell = create_cell(row, 0, group_index)
        cell.set_candidates(candidates)
        cells.append(cell)
    return cells


def test_naked_pair_removes_candidates_from_peers() -> None:
    """Ensure naked pair values are removed from all other cells in the group."""
    group = make_group([[3, 7], [3, 7], [1, 3, 5, 7]])
    reduce_naked_pairs([group])
    assert 3 not in group[2].candidates
    assert 7 not in group[2].candidates


def test_naked_pair_cells_keep_their_candidates() -> None:
    """Ensure the two cells forming the pair keep their candidates."""
    group = make_group([[3, 7], [3, 7], [1, 3, 5, 7]])
    reduce_naked_pairs([group])
    assert group[0].candidates == {3, 7}
    assert group[1].candidates == {3, 7}


def test_other_candidates_in_peer_left_intact() -> None:
    """Ensure only the pair values are removed from peers, not all candidates."""
    group = make_group([[3, 7], [3, 7], [1, 3, 5, 7]])
    reduce_naked_pairs([group])
    assert group[2].candidates == {1, 5}


def test_no_removal_when_cells_have_different_pairs() -> None:
    """Ensure nothing is removed when no two cells share the same two candidates."""
    group = make_group([[3, 7], [3, 8], [1, 2, 5]])
    before = [set(cell.candidates) for cell in group]
    reduce_naked_pairs([group])
    for cell, original in zip(group, before):
        assert cell.candidates == original


def test_does_not_affect_other_groups() -> None:
    """Ensure naked pair elimination is isolated to the affected group."""
    group0 = make_group([[3, 7], [3, 7], [1, 3, 7]])
    group1 = make_group([[3, 7, 9], [1, 2, 3]])
    reduce_naked_pairs([group0, group1])
    assert 3 in group1[0].candidates
    assert 7 in group1[0].candidates


def test_naked_pair_removes_candidates_from_row_peers() -> None:
    """Ensure naked pair elimination works when the unit is a row."""
    c0 = create_cell(0, 0, 0)
    c1 = create_cell(0, 1, 0)
    c2 = create_cell(0, 2, 1)
    c0.set_candidates([3, 7])
    c1.set_candidates([3, 7])
    c2.set_candidates([1, 3, 5, 7])
    reduce_naked_pairs([[c0, c1, c2]])
    assert 3 not in c2.candidates
    assert 7 not in c2.candidates


def test_naked_pair_removes_candidates_from_column_peers() -> None:
    """Ensure naked pair elimination works when the unit is a column."""
    c0 = create_cell(0, 0, 0)
    c1 = create_cell(1, 0, 0)
    c2 = create_cell(2, 0, 1)
    c0.set_candidates([3, 7])
    c1.set_candidates([3, 7])
    c2.set_candidates([1, 3, 5, 7])
    reduce_naked_pairs([[c0, c1, c2]])
    assert 3 not in c2.candidates
    assert 7 not in c2.candidates
