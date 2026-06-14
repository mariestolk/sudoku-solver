"""Tests for the Swordfish strategy."""

from sudoku_solver.cell import create_cell
from sudoku_solver.strategies.swordfish import reduce_swordfish


def _make_grid(
    rows: int, cols: int, group_fn: callable = lambda r, c: r
) -> list[list]:
    """Create a rows×cols grid of fresh cells."""
    return [[create_cell(r, c, group_fn(r, c)) for c in range(cols)] for r in range(rows)]


def test_swordfish_row_eliminates_from_columns() -> None:
    """Row swordfish removes candidate 5 from bystander cells in the three columns."""
    # 4 columns so the bystander (row 1) can have 5 in all 4 cols → 4 positions →
    # ineligible for swordfish, making it a true bystander.
    # Swordfish rows 0, 2, 3:
    #   row 0: 5 in cols 0, 1             → {0, 1}
    #   row 2: 5 in cols 1, 2             → {1, 2}
    #   row 3: 5 in cols 0, 2             → {0, 2}
    # Union = {0, 1, 2} → valid swordfish → eliminate 5 from row 1 in cols 0, 1, 2.
    # (Col 3 is outside the swordfish; row 1 keeps 5 there.)
    grid = _make_grid(4, 4)
    # Row 0: 5 only in cols 0, 1
    grid[0][2].candidates.discard(5)
    grid[0][3].candidates.discard(5)
    # Row 1 (bystander): 5 in all 4 cols (4 positions → not eligible for swordfish)
    # Row 2: 5 only in cols 1, 2
    grid[2][0].candidates.discard(5)
    grid[2][3].candidates.discard(5)
    # Row 3: 5 only in cols 0, 2
    grid[3][1].candidates.discard(5)
    grid[3][3].candidates.discard(5)

    rows = grid
    columns = [[grid[r][c] for r in range(4)] for c in range(4)]

    reduce_swordfish(rows, columns)

    # Bystander row 1 loses 5 in the three swordfish columns
    assert 5 not in grid[1][0].candidates
    assert 5 not in grid[1][1].candidates
    assert 5 not in grid[1][2].candidates
    # Col 3 is not part of the swordfish; row 1 keeps 5 there
    assert 5 in grid[1][3].candidates

    # Swordfish cells keep their candidate
    assert 5 in grid[0][0].candidates
    assert 5 in grid[0][1].candidates
    assert 5 in grid[2][1].candidates
    assert 5 in grid[2][2].candidates
    assert 5 in grid[3][0].candidates
    assert 5 in grid[3][2].candidates


def test_swordfish_row_cells_in_fish_keep_candidate() -> None:
    """Cells that are part of the swordfish pattern are not modified."""
    grid = _make_grid(4, 4)
    grid[0][2].candidates.discard(5)
    grid[0][3].candidates.discard(5)
    grid[2][0].candidates.discard(5)
    grid[2][3].candidates.discard(5)
    grid[3][1].candidates.discard(5)
    grid[3][3].candidates.discard(5)

    rows = grid
    columns = [[grid[r][c] for r in range(4)] for c in range(4)]

    reduce_swordfish(rows, columns)

    for r, c in [(0, 0), (0, 1), (2, 1), (2, 2), (3, 0), (3, 2)]:
        assert 5 in grid[r][c].candidates, f"Swordfish cell ({r},{c}) lost candidate 5"


def test_swordfish_no_elimination_when_union_exceeds_three() -> None:
    """No elimination when no three rows cover exactly three columns."""
    # Rows 0, 2, 3: candidate 5 in positions whose union is 4 — no swordfish.
    #   row 0: cols 0, 1  → {0, 1}
    #   row 2: cols 2, 3  → {2, 3}
    #   row 3: cols 0, 3  → {0, 3}
    # Union = {0, 1, 2, 3} for every triplet → not a swordfish.
    grid = _make_grid(4, 4)
    grid[0][2].candidates.discard(5)
    grid[0][3].candidates.discard(5)
    grid[2][0].candidates.discard(5)
    grid[2][1].candidates.discard(5)
    grid[3][1].candidates.discard(5)
    grid[3][2].candidates.discard(5)

    rows = grid
    columns = [[grid[r][c] for r in range(4)] for c in range(4)]

    reduce_swordfish(rows, columns)

    # Row 1 keeps 5 everywhere — no valid swordfish
    for c in range(4):
        assert 5 in grid[1][c].candidates


def test_swordfish_column_eliminates_from_rows() -> None:
    """Column swordfish removes candidate 7 from bystander cells in the three rows."""
    # 4 rows so the bystander (col 1) can have 7 in all 4 rows → 4 positions →
    # ineligible, making it a true bystander.
    # Swordfish cols 0, 2, 3:
    #   col 0: 7 in rows 0, 1  → {0, 1}
    #   col 2: 7 in rows 1, 2  → {1, 2}
    #   col 3: 7 in rows 0, 2  → {0, 2}
    # Union = {0, 1, 2} → eliminate 7 from col 1 in rows 0, 1, 2.
    grid = _make_grid(4, 4)
    # Col 0: 7 only in rows 0, 1
    grid[2][0].candidates.discard(7)
    grid[3][0].candidates.discard(7)
    # Col 1 (bystander): 7 in all 4 rows
    # Col 2: 7 only in rows 1, 2
    grid[0][2].candidates.discard(7)
    grid[3][2].candidates.discard(7)
    # Col 3: 7 only in rows 0, 2
    grid[1][3].candidates.discard(7)
    grid[3][3].candidates.discard(7)

    rows = grid
    columns = [[grid[r][c] for r in range(4)] for c in range(4)]

    reduce_swordfish(rows, columns)

    # Bystander col 1 loses 7 in the three swordfish rows
    assert 7 not in grid[0][1].candidates
    assert 7 not in grid[1][1].candidates
    assert 7 not in grid[2][1].candidates
    # Row 3 is not part of the swordfish; col 1 keeps 7 there
    assert 7 in grid[3][1].candidates

    # Swordfish cells keep their candidate
    assert 7 in grid[0][0].candidates
    assert 7 in grid[1][0].candidates
    assert 7 in grid[1][2].candidates
    assert 7 in grid[2][2].candidates
    assert 7 in grid[0][3].candidates
    assert 7 in grid[2][3].candidates
