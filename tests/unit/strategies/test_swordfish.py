"""Unit tests for the Swordfish strategy."""

from collections.abc import Iterable

from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.swordfish import reduce_swordfish

_GRID_SIZE = 9
_BASE_CANDIDATES = [1, 2, 3, 4]

Position = tuple[int, int]


def _make_grid() -> list[list[Cell]]:
    """Create a standard 9×9 grid with controlled candidate sets."""
    grid: list[list[Cell]] = []

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
            cell.set_candidates(_BASE_CANDIDATES)
            row.append(cell)

        grid.append(row)

    return grid


def _build_columns(
    grid: list[list[Cell]],
) -> list[list[Cell]]:
    """Build columns from a row-oriented grid."""
    return [
        list(column)
        for column in zip(*grid)
    ]


def _add_candidate(
    grid: list[list[Cell]],
    candidate: int,
    positions: Iterable[Position],
) -> None:
    """Add a candidate to the specified cells."""
    for row_index, column_index in positions:
        cell = grid[row_index][column_index]
        new_candidates = cell.candidates | {candidate}
        cell.set_candidates(sorted(new_candidates))


def test_row_swordfish_eliminates_from_cover_columns() -> None:
    """Ensure a row-based Swordfish eliminates from its three columns."""
    grid = _make_grid()

    fish_positions = {
        (0, 1),
        (0, 4),
        (3, 4),
        (3, 7),
        (6, 1),
        (6, 7),
    }
    bystander_positions = {
        (8, 1),
        (8, 4),
        (8, 7),
        (8, 8),
    }

    _add_candidate(
        grid,
        candidate=5,
        positions=fish_positions | bystander_positions,
    )

    reduce_swordfish(
        rows=grid,
        columns=_build_columns(grid),
    )

    assert 5 not in grid[8][1].candidates
    assert 5 not in grid[8][4].candidates
    assert 5 not in grid[8][7].candidates

    # Column 8 is outside the Swordfish.
    assert 5 in grid[8][8].candidates

    # The cells forming the Swordfish remain unchanged.
    for row_index, column_index in fish_positions:
        assert 5 in grid[row_index][column_index].candidates


def test_column_swordfish_eliminates_from_cover_rows() -> None:
    """Ensure a column-based Swordfish eliminates from its three rows."""
    grid = _make_grid()

    fish_positions = {
        (1, 0),
        (4, 0),
        (4, 3),
        (7, 3),
        (1, 6),
        (7, 6),
    }
    bystander_positions = {
        (1, 8),
        (4, 8),
        (7, 8),
        (8, 8),
    }

    _add_candidate(
        grid,
        candidate=7,
        positions=fish_positions | bystander_positions,
    )

    reduce_swordfish(
        rows=grid,
        columns=_build_columns(grid),
    )

    assert 7 not in grid[1][8].candidates
    assert 7 not in grid[4][8].candidates
    assert 7 not in grid[7][8].candidates

    # Row 8 is outside the Swordfish.
    assert 7 in grid[8][8].candidates

    for row_index, column_index in fish_positions:
        assert 7 in grid[row_index][column_index].candidates


def test_swordfish_supports_three_two_three_distribution() -> None:
    """Ensure a 3-2-3 candidate distribution forms a Swordfish."""
    grid = _make_grid()

    fish_positions = {
        # Three occurrences in row 0.
        (0, 1),
        (0, 4),
        (0, 7),
        # Two occurrences in row 3.
        (3, 1),
        (3, 7),
        # Three occurrences in row 6.
        (6, 1),
        (6, 4),
        (6, 7),
    }
    bystander_positions = {
        (8, 1),
        (8, 4),
        (8, 7),
        (8, 8),
    }

    _add_candidate(
        grid,
        candidate=6,
        positions=fish_positions | bystander_positions,
    )

    reduce_swordfish(
        rows=grid,
        columns=_build_columns(grid),
    )

    assert 6 not in grid[8][1].candidates
    assert 6 not in grid[8][4].candidates
    assert 6 not in grid[8][7].candidates
    assert 6 in grid[8][8].candidates


def test_no_elimination_when_positions_cover_four_columns() -> None:
    """Ensure three rows covering four columns do not form a Swordfish."""
    grid = _make_grid()

    candidate_positions = {
        (0, 1),
        (0, 4),
        (3, 4),
        (3, 7),
        (6, 1),
        (6, 8),
        (8, 1),
        (8, 4),
        (8, 7),
        (8, 8),
    }

    _add_candidate(
        grid,
        candidate=5,
        positions=candidate_positions,
    )

    before = {
        position: grid[position[0]][position[1]].candidates.copy()
        for position in candidate_positions
    }

    reduce_swordfish(
        rows=grid,
        columns=_build_columns(grid),
    )

    for position, original_candidates in before.items():
        row_index, column_index = position
        assert (
            grid[row_index][column_index].candidates
            == original_candidates
        )


def test_swordfish_removes_only_the_pattern_candidate() -> None:
    """Ensure unrelated candidates remain in an affected cell."""
    grid = _make_grid()

    fish_positions = {
        (0, 1),
        (0, 4),
        (3, 4),
        (3, 7),
        (6, 1),
        (6, 7),
    }
    bystander_positions = {
        (8, 1),
        (8, 4),
        (8, 7),
        (8, 8),
    }

    _add_candidate(
        grid,
        candidate=5,
        positions=fish_positions | bystander_positions,
    )

    before = grid[8][1].candidates.copy()

    reduce_swordfish(
        rows=grid,
        columns=_build_columns(grid),
    )

    assert grid[8][1].candidates == before - {5}


def test_swordfish_is_idempotent() -> None:
    """Ensure rerunning the strategy causes no additional changes."""
    grid = _make_grid()

    fish_positions = {
        (0, 1),
        (0, 4),
        (3, 4),
        (3, 7),
        (6, 1),
        (6, 7),
    }
    bystander_positions = {
        (8, 1),
        (8, 4),
        (8, 7),
        (8, 8),
    }

    _add_candidate(
        grid,
        candidate=5,
        positions=fish_positions | bystander_positions,
    )

    columns = _build_columns(grid)

    reduce_swordfish(grid, columns)

    after_first_reduction = [
        [
            cell.candidates.copy()
            for cell in row
        ]
        for row in grid
    ]

    reduce_swordfish(grid, columns)

    after_second_reduction = [
        [
            cell.candidates.copy()
            for cell in row
        ]
        for row in grid
    ]

    assert after_second_reduction == after_first_reduction