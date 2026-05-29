"""Tests for the naked triples strategy."""

from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.naked import reduce_naked_triples


def make_group(candidate_sets: list[list[int]], group_index: int = 0) -> list[Cell]:
    """Build a group of unsolved cells with the given candidate sets."""
    cells = []
    for row, candidates in enumerate(candidate_sets):
        cell = create_cell(row, 0, group_index)
        cell.set_candidates(candidates)
        cells.append(cell)
    return cells


def test_naked_triple_removes_candidates_from_peers() -> None:
    """Ensure naked triple values are removed from all other cells in the group."""
    group = make_group([[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 4, 5]])
    reduce_naked_triples([group])
    assert 1 not in group[3].candidates
    assert 2 not in group[3].candidates
    assert 3 not in group[3].candidates


def test_naked_triple_cells_keep_their_candidates() -> None:
    """Ensure the three cells forming the triple keep their candidates."""
    group = make_group([[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 4]])
    reduce_naked_triples([group])
    assert group[0].candidates == {1, 2, 3}
    assert group[1].candidates == {1, 2, 3}
    assert group[2].candidates == {1, 2, 3}


def test_other_candidates_in_peer_left_intact() -> None:
    """Ensure only the triple values are removed from peers, not all candidates."""
    group = make_group([[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 4, 5]])
    reduce_naked_triples([group])
    assert group[3].candidates == {4, 5}


def test_no_removal_when_only_two_matching_cells() -> None:
    """Ensure nothing is removed when fewer than three cells
    share the same candidates."""
    group = make_group([[1, 2, 3], [1, 2, 3], [1, 2, 4]])
    before = [set(cell.candidates) for cell in group]
    reduce_naked_triples([group])
    for cell, original in zip(group, before):
        assert cell.candidates == original


def test_mixed_naked_triple_removes_candidates_from_peers() -> None:
    """Ensure a mixed naked triple (e.g. {1,2},{2,3},{1,3}) is detected."""
    group = make_group([[1, 2], [2, 3], [1, 3], [1, 2, 3, 4]])
    reduce_naked_triples([group])
    assert group[3].candidates == {4}


def test_mixed_naked_triple_with_full_cell_removes_candidates() -> None:
    """Ensure a triple where one cell has all three candidates is detected."""
    group = make_group([[1, 2], [1, 2, 3], [2, 3], [1, 2, 3, 4]])
    reduce_naked_triples([group])
    assert group[3].candidates == {4}


def test_non_triple_union_leaves_candidates_intact() -> None:
    """Ensure three cells whose union covers four values are not treated as a triple."""
    group = make_group([[1, 2], [2, 3], [1, 4], [1, 2, 3, 4]])
    before = set(group[3].candidates)
    reduce_naked_triples([group])
    assert group[3].candidates == before


def test_does_not_affect_other_groups() -> None:
    """Ensure naked triple elimination is isolated to the affected group."""
    group0 = make_group([[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3, 4]])
    group1 = make_group([[1, 2, 3, 5], [4, 6, 7]])
    reduce_naked_triples([group0, group1])
    assert 1 in group1[0].candidates
    assert 2 in group1[0].candidates
    assert 3 in group1[0].candidates
