"""Unit tests for the XY-chain strategy."""

from collections.abc import Iterable

import pytest
from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.xy_chain import reduce_xy_chains

_GRID_SIZE = 9
_DEFAULT_CANDIDATES = [7, 8, 9]


def _make_grid() -> tuple[
    list[list[Cell]],
    list[list[Cell]],
    list[list[Cell]],
]:
    """Create a standard grid with no initial bivalue cells."""
    rows: list[list[Cell]] = []

    for row_index in range(_GRID_SIZE):
        row: list[Cell] = []

        for column_index in range(_GRID_SIZE):
            group_index = (
                row_index // 3
            ) * 3 + column_index // 3

            cell = create_cell(
                row_index,
                column_index,
                group_index,
            )
            cell.set_candidates(_DEFAULT_CANDIDATES)
            row.append(cell)

        rows.append(row)

    columns = [
        list(column)
        for column in zip(*rows)
    ]

    groups: list[list[Cell]] = [
        []
        for _ in range(_GRID_SIZE)
    ]

    for row in rows:
        for cell in row:
            groups[cell.group].append(cell)

    return rows, columns, groups


def _set_candidates(
    rows: list[list[Cell]],
    row: int,
    column: int,
    candidates: Iterable[int],
) -> Cell:
    """Set candidates for one cell and return it."""
    cell = rows[row][column]
    cell.set_candidates(list(candidates))
    return cell


def _candidate_snapshot(
    rows: list[list[Cell]],
) -> list[list[set[int]]]:
    """Return a copy of all candidate sets."""
    return [
        [
            cell.candidates.copy()
            for cell in row
        ]
        for row in rows
    ]


def test_three_cell_xy_chain_eliminates_from_common_peer() -> None:
    """Ensure a three-cell XY-chain eliminates from a common peer."""
    rows, columns, groups = _make_grid()

    # {1, 2} → {2, 3} → {3, 1}
    _set_candidates(rows, 0, 0, [1, 2])
    _set_candidates(rows, 0, 4, [2, 3])
    _set_candidates(rows, 4, 4, [1, 3])

    # Sees the first endpoint through column 0 and the second
    # endpoint through row 4.
    target = _set_candidates(rows, 4, 0, [1, 6])

    reduce_xy_chains(
        rows,
        columns,
        groups,
    )

    assert target.candidates == {6}
    assert target.deciding_rule == "xy_chain"


def test_xy_chain_removes_only_the_endpoint_candidate() -> None:
    """Ensure unrelated candidates remain in the target cell."""
    rows, columns, groups = _make_grid()

    _set_candidates(rows, 0, 0, [1, 2])
    _set_candidates(rows, 0, 4, [2, 3])
    _set_candidates(rows, 4, 4, [1, 3])

    target = _set_candidates(
        rows,
        4,
        0,
        [1, 5, 6],
    )

    reduce_xy_chains(
        rows,
        columns,
        groups,
    )

    assert target.candidates == {5, 6}
    assert target.deciding_rule is None


def test_xy_chain_cells_keep_their_candidates() -> None:
    """Ensure cells forming the chain are not modified."""
    rows, columns, groups = _make_grid()

    start = _set_candidates(rows, 0, 0, [1, 2])
    middle = _set_candidates(rows, 0, 4, [2, 3])
    end = _set_candidates(rows, 4, 4, [1, 3])
    _set_candidates(rows, 4, 0, [1, 6])

    reduce_xy_chains(
        rows,
        columns,
        groups,
    )

    assert start.candidates == {1, 2}
    assert middle.candidates == {2, 3}
    assert end.candidates == {1, 3}


def test_xy_chain_can_use_group_link() -> None:
    """Ensure consecutive chain cells may be linked through a group."""
    rows, columns, groups = _make_grid()

    # The first two cells share group 0 but not a row or column.
    _set_candidates(rows, 0, 0, [1, 2])
    _set_candidates(rows, 1, 1, [2, 3])

    # The second and third cells share row 1.
    _set_candidates(rows, 1, 4, [1, 3])

    # Sees the first endpoint through row 0 and the second
    # endpoint through column 4.
    target = _set_candidates(rows, 0, 4, [1, 6])

    reduce_xy_chains(
        rows,
        columns,
        groups,
    )

    assert target.candidates == {6}


def test_longer_xy_chain_eliminates_candidate() -> None:
    """Ensure chains longer than three cells are detected."""
    rows, columns, groups = _make_grid()

    # {1, 2} → {2, 3} → {3, 4} → {4, 1}
    _set_candidates(rows, 0, 0, [1, 2])
    _set_candidates(rows, 0, 4, [2, 3])
    _set_candidates(rows, 4, 4, [3, 4])
    _set_candidates(rows, 4, 8, [1, 4])

    target = _set_candidates(rows, 0, 8, [1, 6])

    reduce_xy_chains(
        rows,
        columns,
        groups,
    )

    assert target.candidates == {6}
    assert target.deciding_rule == "xy_chain"


def test_max_chain_length_can_disable_longer_chain() -> None:
    """Ensure chains exceeding the configured maximum are ignored."""
    rows, columns, groups = _make_grid()

    _set_candidates(rows, 0, 0, [1, 2])
    _set_candidates(rows, 0, 4, [2, 3])
    _set_candidates(rows, 4, 4, [3, 4])
    _set_candidates(rows, 4, 8, [1, 4])

    target = _set_candidates(rows, 0, 8, [1, 6])

    reduce_xy_chains(
        rows,
        columns,
        groups,
        max_chain_length=3,
    )

    assert target.candidates == {1, 6}
    assert target.deciding_rule is None


def test_no_elimination_when_target_sees_only_one_endpoint() -> None:
    """Ensure an elimination cell must see both chain endpoints."""
    rows, columns, groups = _make_grid()

    _set_candidates(rows, 0, 0, [1, 2])
    _set_candidates(rows, 0, 4, [2, 3])
    _set_candidates(rows, 4, 4, [1, 3])

    # Sees the first endpoint through row 0, but does not see
    # the endpoint at r4c4.
    target = _set_candidates(
        rows,
        0,
        8,
        [1, 5, 6],
    )

    reduce_xy_chains(
        rows,
        columns,
        groups,
    )

    assert target.candidates == {1, 5, 6}


def test_no_elimination_when_endpoint_candidates_differ() -> None:
    """Ensure both chain endpoints must expose the same candidate."""
    rows, columns, groups = _make_grid()

    # The unlinked endpoint candidates are 1 and 4, so this is
    # not a completed XY-chain.
    _set_candidates(rows, 0, 0, [1, 2])
    _set_candidates(rows, 0, 4, [2, 3])
    _set_candidates(rows, 4, 4, [3, 4])

    target = _set_candidates(
        rows,
        4,
        0,
        [1, 5, 6],
    )

    reduce_xy_chains(
        rows,
        columns,
        groups,
    )

    assert target.candidates == {1, 5, 6}


def test_non_bivalue_cell_cannot_be_part_of_chain() -> None:
    """Ensure every chain cell must contain exactly two candidates."""
    rows, columns, groups = _make_grid()

    _set_candidates(rows, 0, 0, [1, 2])

    # Three candidates: this cell cannot act as an XY-chain link.
    _set_candidates(rows, 0, 4, [2, 3, 5])

    _set_candidates(rows, 4, 4, [1, 3])

    target = _set_candidates(
        rows,
        4,
        0,
        [1, 5, 6],
    )

    reduce_xy_chains(
        rows,
        columns,
        groups,
    )

    assert target.candidates == {1, 5, 6}


def test_consecutive_chain_cells_must_see_each_other() -> None:
    """Ensure sharing a candidate is insufficient without a peer link."""
    rows, columns, groups = _make_grid()

    start = _set_candidates(rows, 0, 0, [1, 2])

    # Does not share a row, column, or group with the start.
    middle = _set_candidates(rows, 2, 4, [2, 3])

    _set_candidates(rows, 4, 4, [1, 3])

    target = _set_candidates(
        rows,
        4,
        0,
        [1, 5, 6],
    )

    assert start.row != middle.row
    assert start.column != middle.column
    assert start.group != middle.group

    reduce_xy_chains(
        rows,
        columns,
        groups,
    )

    assert target.candidates == {1, 5, 6}


def test_xy_chain_is_idempotent() -> None:
    """Ensure rerunning the strategy causes no additional changes."""
    rows, columns, groups = _make_grid()

    _set_candidates(rows, 0, 0, [1, 2])
    _set_candidates(rows, 0, 4, [2, 3])
    _set_candidates(rows, 4, 4, [1, 3])
    _set_candidates(rows, 4, 0, [1, 6])

    reduce_xy_chains(
        rows,
        columns,
        groups,
    )
    after_first_run = _candidate_snapshot(rows)

    reduce_xy_chains(
        rows,
        columns,
        groups,
    )
    after_second_run = _candidate_snapshot(rows)

    assert after_second_run == after_first_run


def test_max_chain_length_must_be_at_least_three() -> None:
    """Ensure invalid chain-length limits are rejected."""
    rows, columns, groups = _make_grid()

    with pytest.raises(
        ValueError,
        match="at least three",
    ):
        reduce_xy_chains(
            rows,
            columns,
            groups,
            max_chain_length=2,
        )