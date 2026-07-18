"""Tests for the rectangle-elimination strategy."""

from collections.abc import Iterable

from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.rectangle_elimination import (
    reduce_rectangle_elimination,
)


def make_cell(
    row: int,
    column: int,
    group: int,
    candidates: Iterable[int],
) -> Cell:
    """Create an unsolved cell with the given candidates."""
    cell = create_cell(row, column, group)
    cell.set_candidates(candidates)
    return cell


def build_houses(
    cells: Iterable[Cell],
) -> tuple[
    list[list[Cell]],
    list[list[Cell]],
    list[list[Cell]],
]:
    """Build row, column, and group houses from a collection of cells."""
    rows: list[list[Cell]] = [[] for _ in range(9)]
    columns: list[list[Cell]] = [[] for _ in range(9)]
    groups: list[list[Cell]] = [[] for _ in range(9)]

    for cell in cells:
        rows[cell.row].append(cell)
        columns[cell.column].append(cell)
        groups[cell.group].append(cell)

    return rows, columns, groups


def make_row_based_pattern(
    weak_wing_candidates: Iterable[int] = (3, 9),
) -> tuple[
    list[list[Cell]],
    list[list[Cell]],
    list[list[Cell]],
    dict[str, Cell],
]:
    """Create a controlled row-based rectangle-elimination pattern."""
    cells = {
        "hinge": make_cell(0, 0, 0, [1, 9]),
        "strong_wing": make_cell(0, 4, 1, [2, 9]),
        "weak_wing": make_cell(
            4,
            0,
            3,
            weak_wing_candidates,
        ),
        # These additional candidates prevent the sparse fixture from
        # accidentally creating unrelated rectangle eliminations.
        "column_extra": make_cell(7, 0, 6, [4, 9]),
        "weak_group_extra": make_cell(5, 2, 3, [5, 9]),
        "column_extra_group_peer": make_cell(8, 2, 6, [6, 9]),
        "target_seen_by_strong_wing": make_cell(
            3,
            4,
            4,
            [7, 9],
        ),
        "target_seen_by_weak_wing": make_cell(
            4,
            3,
            4,
            [8, 9],
        ),
        "strong_wing_group_peer": make_cell(2, 5, 1, [1, 9]),
        "hinge_group_peer": make_cell(1, 1, 0, [2, 9]),
    }

    rows, columns, groups = build_houses(cells.values())

    return rows, columns, groups, cells


def make_column_based_pattern() -> tuple[
    list[list[Cell]],
    list[list[Cell]],
    list[list[Cell]],
    dict[str, Cell],
]:
    """Create the transposed version of the row-based pattern."""
    _, _, _, original_cells = make_row_based_pattern()

    cells = {
        name: make_cell(
            row=cell.column,
            column=cell.row,
            group=cell.group,
            candidates=cell.candidates,
        )
        for name, cell in original_cells.items()
    }

    rows, columns, groups = build_houses(cells.values())

    return rows, columns, groups, cells


def test_row_based_rectangle_eliminates_weak_wing() -> None:
    """Ensure a row strong link can eliminate a perpendicular weak wing."""
    rows, columns, groups, cells = make_row_based_pattern()

    reduce_rectangle_elimination(
        rows,
        columns,
        groups,
    )

    assert cells["weak_wing"].candidates == {3}


def test_column_based_rectangle_eliminates_weak_wing() -> None:
    """Ensure the transposed column-based pattern is also detected."""
    rows, columns, groups, cells = make_column_based_pattern()

    reduce_rectangle_elimination(
        rows,
        columns,
        groups,
    )

    assert cells["weak_wing"].candidates == {3}


def test_only_rectangle_candidate_is_removed() -> None:
    """Ensure unrelated candidates remain in the eliminated cell."""
    rows, columns, groups, cells = make_row_based_pattern(
        weak_wing_candidates=[3, 5, 9],
    )

    reduce_rectangle_elimination(
        rows,
        columns,
        groups,
    )

    assert cells["weak_wing"].candidates == {3, 5}


def test_pattern_cells_remain_unchanged() -> None:
    """Ensure the hinge, strong wing, and target group are unchanged."""
    rows, columns, groups, cells = make_row_based_pattern()

    reduce_rectangle_elimination(
        rows,
        columns,
        groups,
    )

    assert cells["hinge"].candidates == {1, 9}
    assert cells["strong_wing"].candidates == {2, 9}
    assert cells["target_seen_by_strong_wing"].candidates == {7, 9}
    assert cells["target_seen_by_weak_wing"].candidates == {8, 9}


def test_rule_is_recorded_when_elimination_resolves_cell() -> None:
    """Ensure the deciding rule is set when one candidate remains."""
    rows, columns, groups, cells = make_row_based_pattern()

    reduce_rectangle_elimination(
        rows,
        columns,
        groups,
    )

    assert cells["weak_wing"].candidates == {3}
    assert cells["weak_wing"].deciding_rule == "rectangle_elimination"


def test_rule_is_not_recorded_when_cell_remains_unresolved() -> None:
    """Ensure no deciding rule is set when multiple candidates remain."""
    rows, columns, groups, cells = make_row_based_pattern(
        weak_wing_candidates=[3, 5, 9],
    )

    reduce_rectangle_elimination(
        rows,
        columns,
        groups,
    )

    assert cells["weak_wing"].candidates == {3, 5}
    assert cells["weak_wing"].deciding_rule is None


def test_no_elimination_without_strong_link() -> None:
    """Ensure no elimination occurs when every house has many candidates."""
    cells = [
        make_cell(
            row=row,
            column=column,
            group=(row // 3) * 3 + column // 3,
            candidates=[1, 9],
        )
        for row in range(9)
        for column in range(9)
    ]
    rows, columns, groups = build_houses(cells)

    before = [cell.candidates.copy() for cell in cells]

    reduce_rectangle_elimination(
        rows,
        columns,
        groups,
    )

    assert [cell.candidates for cell in cells] == before


def test_no_elimination_when_target_group_is_not_fully_covered() -> None:
    """Ensure every target-group candidate must see one of the wings."""
    _, _, _, cells = make_row_based_pattern()

    cells["uncovered_target"] = make_cell(
        row=5,
        column=5,
        group=4,
        candidates=[4, 9],
    )

    rows, columns, groups = build_houses(cells.values())

    reduce_rectangle_elimination(
        rows,
        columns,
        groups,
    )

    assert cells["weak_wing"].candidates == {3, 9}


def test_weak_wing_in_hinge_group_is_ignored() -> None:
    """Ensure the weak wing must belong to a different group."""
    cells = {
        "hinge": make_cell(0, 0, 0, [1, 9]),
        "strong_wing": make_cell(0, 4, 1, [2, 9]),
        "weak_wing": make_cell(4, 0, 0, [3, 9]),
        "target_by_strong": make_cell(3, 4, 4, [4, 9]),
        "target_by_weak": make_cell(4, 3, 4, [5, 9]),
    }
    rows, columns, groups = build_houses(cells.values())

    reduce_rectangle_elimination(
        rows,
        columns,
        groups,
    )

    assert cells["weak_wing"].candidates == {3, 9}
