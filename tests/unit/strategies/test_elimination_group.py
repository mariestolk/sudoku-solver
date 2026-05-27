"""Tests for the group elimination strategy."""

from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.elimination import reduce_groups


def make_group(values: list[int | None], group_index: int = 0) -> list[Cell]:
    """Build a group of cells; None means unsolved (candidates 1–9)."""
    return [create_cell(row, 0, group_index, v) for row, v in enumerate(values)]


def test_solved_cell_value_removed_from_peers() -> None:
    """Ensure a solved cell value is removed from its group peers."""
    group = make_group([5, None, None])
    reduce_groups([group])
    assert 5 not in group[1].candidates
    assert 5 not in group[2].candidates


def test_other_candidates_left_intact() -> None:
    """Ensure only the solved value is removed and other candidate values remain."""
    group = make_group([5, None, None])
    reduce_groups([group])
    assert group[1].candidates == {1, 2, 3, 4, 6, 7, 8, 9}
    assert group[2].candidates == {1, 2, 3, 4, 6, 7, 8, 9}


def test_does_not_affect_other_groups() -> None:
    """Ensure group elimination does not remove candidates from other groups."""
    group0 = make_group([5, None, None], group_index=0)
    group1 = make_group([None, None, None], group_index=1)
    reduce_groups([group0, group1])
    assert 5 in group1[0].candidates
    assert 5 in group1[1].candidates
    assert 5 in group1[2].candidates


def test_multiple_solved_cells_all_values_removed() -> None:
    """Ensure all solved values are removed from other group cells."""
    group = make_group([3, 7, None, None])
    reduce_groups([group])
    assert 3 not in group[2].candidates
    assert 7 not in group[2].candidates
    assert 3 not in group[3].candidates
    assert 7 not in group[3].candidates


def test_no_op_when_no_solved_cells() -> None:
    """Ensure no candidates are removed when the group has no solved cells."""
    group = make_group([None, None, None])
    before = [set(cell.candidates) for cell in group]
    reduce_groups([group])
    for cell, original in zip(group, before):
        assert cell.candidates == original
