"""Unit tests for the Cell class."""

from sudoku_solver.cell import Cell, create_cell


def test_cell_initialization() -> None:
    """Test that Cell initializes with correct default values."""
    cell = Cell(row=2, column=4, group=1)

    assert cell.row == 2
    assert cell.column == 4
    assert cell.group == 1
    assert cell.value is None
    assert cell.candidates == set()
    assert cell.deciding_rule is None


def test_cell_repr() -> None:
    """Test that Cell repr returns the expected string representation."""
    cell = Cell(row=2, column=4, group=1)

    assert repr(cell) == "Cell(2, 4, 1, value=None)"


def test_set_value() -> None:
    """Test set_value correctly sets the cell value and clears candidates and rule."""
    cell = create_cell(row=0, column=0, group=0)
    cell.set_deciding_rule("hidden_single")

    cell.set_value(7)

    assert cell.value == 7
    assert cell.candidates == set()
    assert cell.deciding_rule is None


def test_set_candidates() -> None:
    """Test that set_candidates correctly sets the cell candidates."""
    cell = Cell(row=0, column=0, group=0)

    cell.set_candidates([2, 4, 4, 6])

    assert cell.candidates == {2, 4, 6}


def test_set_deciding_rule() -> None:
    """Test that set_deciding_rule assigns the deciding rule string."""

    cell = Cell(row=0, column=0, group=0)

    cell.set_deciding_rule("hidden_pair")

    assert cell.deciding_rule == "hidden_pair"


def test_create_unsolved_cell() -> None:
    """Test that create_cell creates an unsolved cell with all candidates."""
    cell = create_cell(row=3, column=5, group=4)

    assert cell.value is None
    assert cell.candidates == set(range(1, 10))


def test_create_solved_cell() -> None:
    """Test that create_cell creates a solved cell with no candidates."""
    cell = create_cell(row=3, column=5, group=4, value=8)

    assert cell.value == 8
    assert cell.candidates == set()
