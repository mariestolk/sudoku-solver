"""Tests for the naked quads strategy."""

from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.naked import reduce_naked_quads


def make_group(candidate_sets: list[list[int]], group_index: int = 0) -> list[Cell]:
    """Build a group of unsolved cells with the given candidate sets."""
    cells = []
    for row, candidates in enumerate(candidate_sets):
        cell = create_cell(row, 0, group_index)
        cell.set_candidates(candidates)
        cells.append(cell)
    return cells


def test_naked_quad_removes_candidates_from_peers() -> None:
    """Ensure naked quad values are removed from all other cells in the group."""
    group = make_group([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 4, 5]])
    reduce_naked_quads([group])
    assert 1 not in group[4].candidates
    assert 2 not in group[4].candidates
    assert 4 not in group[4].candidates


def test_naked_quad_cells_keep_their_candidates() -> None:
    """Ensure the four cells forming the quad keep their candidates."""
    group = make_group([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 4, 5]])
    reduce_naked_quads([group])
    assert group[0].candidates == {1, 2, 3, 4}
    assert group[1].candidates == {1, 2, 3, 4}
    assert group[2].candidates == {1, 2, 3, 4}
    assert group[3].candidates == {1, 2, 3, 4}


def test_other_candidates_in_peer_left_intact() -> None:
    """Ensure only the quad values are removed from peers, not all candidates."""
    group = make_group([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 4, 5]])
    reduce_naked_quads([group])
    assert group[4].candidates == {5}


def test_mixed_naked_quad_removes_candidates_from_peers() -> None:
    """Ensure a mixed quad (subsets distributed across four cells) is detected."""
    group = make_group([[1, 2], [3, 4], [1, 3], [2, 4], [1, 2, 3, 4, 5]])
    reduce_naked_quads([group])
    assert group[4].candidates == {5}


def test_no_removal_when_only_three_matching_cells() -> None:
    """Ensure nothing is removed when fewer than four cells share the same candidates."""
    group = make_group([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4, 5]])
    before = [set(cell.candidates) for cell in group]
    reduce_naked_quads([group])
    for cell, original in zip(group, before):
        assert cell.candidates == original


def test_non_quad_union_leaves_candidates_intact() -> None:
    """Ensure four cells whose union covers five values are not treated as a quad."""
    group = make_group([[1, 2], [2, 3], [3, 4], [4, 5], [1, 2, 3, 4, 5]])
    before = set(group[4].candidates)
    reduce_naked_quads([group])
    assert group[4].candidates == before


def test_does_not_affect_other_groups() -> None:
    """Ensure naked quad elimination is isolated to the affected group."""
    group0 = make_group(
        [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
    )
    group1 = make_group([[1, 2, 3, 4, 6], [5, 7, 8]])
    reduce_naked_quads([group0, group1])
    assert 1 in group1[0].candidates
    assert 2 in group1[0].candidates
    assert 3 in group1[0].candidates
    assert 4 in group1[0].candidates


def test_naked_quad_removes_candidates_from_row_peers() -> None:
    """Ensure naked quad elimination works when the unit is a row."""
    c0 = create_cell(0, 0, 0)
    c1 = create_cell(0, 1, 0)
    c2 = create_cell(0, 2, 0)
    c3 = create_cell(0, 3, 0)
    c4 = create_cell(0, 4, 1)
    c0.set_candidates([1, 2])
    c1.set_candidates([3, 4])
    c2.set_candidates([1, 3])
    c3.set_candidates([2, 4])
    c4.set_candidates([1, 2, 3, 4, 5])
    reduce_naked_quads([[c0, c1, c2, c3, c4]])
    assert c4.candidates == {5}


def test_naked_quad_removes_candidates_from_column_peers() -> None:
    """Ensure naked quad elimination works when the unit is a column."""
    c0 = create_cell(0, 0, 0)
    c1 = create_cell(1, 0, 0)
    c2 = create_cell(2, 0, 0)
    c3 = create_cell(3, 0, 0)
    c4 = create_cell(4, 0, 1)
    c0.set_candidates([1, 2])
    c1.set_candidates([3, 4])
    c2.set_candidates([1, 3])
    c3.set_candidates([2, 4])
    c4.set_candidates([1, 2, 3, 4, 5])
    reduce_naked_quads([[c0, c1, c2, c3, c4]])
    assert c4.candidates == {5}
