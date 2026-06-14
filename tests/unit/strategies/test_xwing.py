"""Tests for the X-wing strategy."""

from sudoku_solver.cell import create_cell
from sudoku_solver.strategies.xwing import reduce_xwing


def test_xwing_row_eliminates_from_columns() -> None:
    """Row X-wing removes candidate from bystanders in the two columns."""
    # Row 0 and row 2: candidate 5 at cols 0 and 1 only (not col 2).
    # Row 1 (bystander row): 5 at all 3 columns → 3 positions → does not qualify.
    r0c0 = create_cell(0, 0, 0)
    r0c1 = create_cell(0, 1, 0)
    r0c2 = create_cell(0, 2, 0)
    r0c2.candidates.discard(5)

    r1c0 = create_cell(1, 0, 1)
    r1c1 = create_cell(1, 1, 1)
    r1c2 = create_cell(1, 2, 1)

    r2c0 = create_cell(2, 0, 0)
    r2c1 = create_cell(2, 1, 0)
    r2c2 = create_cell(2, 2, 0)
    r2c2.candidates.discard(5)

    rows = [[r0c0, r0c1, r0c2], [r1c0, r1c1, r1c2], [r2c0, r2c1, r2c2]]
    columns = [[r0c0, r1c0, r2c0], [r0c1, r1c1, r2c1], [r0c2, r1c2, r2c2]]

    reduce_xwing(rows, columns)

    assert 5 not in r1c0.candidates
    assert 5 not in r1c1.candidates
    # Wing cells must keep the candidate
    assert 5 in r0c0.candidates
    assert 5 in r0c1.candidates
    assert 5 in r2c0.candidates
    assert 5 in r2c1.candidates


def test_xwing_no_elimination_when_columns_differ() -> None:
    """No elimination when the two qualifying rows do not share the same column pair."""
    # Row 0: 5 at cols 0 and 1; row 2: 5 at cols 0 and 2 → different pairs, no X-wing.
    r0c0 = create_cell(0, 0, 0)
    r0c1 = create_cell(0, 1, 0)
    r0c2 = create_cell(0, 2, 0)
    r0c2.candidates.discard(5)

    r1c0 = create_cell(1, 0, 1)
    r1c1 = create_cell(1, 1, 1)
    r1c2 = create_cell(1, 2, 1)

    r2c0 = create_cell(2, 0, 0)
    r2c1 = create_cell(2, 1, 0)
    r2c1.candidates.discard(5)
    r2c2 = create_cell(2, 2, 0)

    rows = [[r0c0, r0c1, r0c2], [r1c0, r1c1, r1c2], [r2c0, r2c1, r2c2]]
    columns = [[r0c0, r1c0, r2c0], [r0c1, r1c1, r2c1], [r0c2, r1c2, r2c2]]

    reduce_xwing(rows, columns)

    assert 5 in r1c0.candidates
    assert 5 in r1c1.candidates
    assert 5 in r1c2.candidates


def test_xwing_column_eliminates_from_rows() -> None:
    """Column X-wing removes candidate from bystanders in the two rows."""
    # Col 0 and col 2: candidate 3 at rows 0 and 2 only (not row 1).
    # Col 1 (bystander col): 3 at all 3 rows → 3 positions → does not qualify.
    r0c0 = create_cell(0, 0, 0)
    r0c1 = create_cell(0, 1, 1)
    r0c2 = create_cell(0, 2, 0)

    r1c0 = create_cell(1, 0, 0)
    r1c0.candidates.discard(3)
    r1c1 = create_cell(1, 1, 1)
    r1c2 = create_cell(1, 2, 0)
    r1c2.candidates.discard(3)

    r2c0 = create_cell(2, 0, 0)
    r2c1 = create_cell(2, 1, 1)
    r2c2 = create_cell(2, 2, 0)

    rows = [[r0c0, r0c1, r0c2], [r1c0, r1c1, r1c2], [r2c0, r2c1, r2c2]]
    columns = [[r0c0, r1c0, r2c0], [r0c1, r1c1, r2c1], [r0c2, r1c2, r2c2]]

    reduce_xwing(rows, columns)

    assert 3 not in r0c1.candidates
    assert 3 not in r2c1.candidates
    # Wing cells must keep the candidate
    assert 3 in r0c0.candidates
    assert 3 in r0c2.candidates
    assert 3 in r2c0.candidates
    assert 3 in r2c2.candidates
