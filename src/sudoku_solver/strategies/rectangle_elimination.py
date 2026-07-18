"""Rectangle-elimination candidate reduction strategy."""

from sudoku_solver.cell import Cell


def _candidate_cells(
    house: list[Cell],
    candidate: int,
) -> list[Cell]:
    """Return unsolved cells containing a candidate."""
    return [
        cell for cell in house if cell.value is None and candidate in cell.candidates
    ]


def _cells_see_each_other(
    first_cell: Cell,
    second_cell: Cell,
) -> bool:
    """Return whether two distinct cells share a house."""
    return first_cell is not second_cell and (
        first_cell.row == second_cell.row
        or first_cell.column == second_cell.column
        or first_cell.group == second_cell.group
    )


def _wings_empty_candidate_from_group(
    candidate: int,
    first_wing: Cell,
    second_wing: Cell,
    groups: list[list[Cell]],
    excluded_groups: set[int],
) -> bool:
    """Return whether both wings eliminate a candidate from an entire group."""
    for group in groups:
        if not group:
            continue

        group_index = group[0].group

        if group_index in excluded_groups:
            continue

        group_candidate_cells = _candidate_cells(
            group,
            candidate,
        )

        if not group_candidate_cells:
            continue

        if all(
            _cells_see_each_other(cell, first_wing)
            or _cells_see_each_other(cell, second_wing)
            for cell in group_candidate_cells
        ):
            return True

    return False


def _find_row_based_eliminations(
    candidate: int,
    rows: list[list[Cell]],
    columns: list[list[Cell]],
    groups: list[list[Cell]],
) -> set[Cell]:
    """Find rectangle eliminations based on row strong links."""
    eliminations: set[Cell] = set()

    for row in rows:
        strong_link_cells = _candidate_cells(
            row,
            candidate,
        )

        if len(strong_link_cells) != 2:
            continue

        first_cell, second_cell = strong_link_cells

        for hinge, strong_wing in (
            (first_cell, second_cell),
            (second_cell, first_cell),
        ):
            if hinge.group == strong_wing.group:
                continue

            weak_wings = _candidate_cells(
                columns[hinge.column],
                candidate,
            )

            for weak_wing in weak_wings:
                if weak_wing is hinge:
                    continue

                if len(weak_wing.candidates) <= 1:
                    continue

                if weak_wing.group in {
                    hinge.group,
                    strong_wing.group,
                }:
                    continue

                excluded_groups = {
                    hinge.group,
                    strong_wing.group,
                    weak_wing.group,
                }

                if _wings_empty_candidate_from_group(
                    candidate=candidate,
                    first_wing=strong_wing,
                    second_wing=weak_wing,
                    groups=groups,
                    excluded_groups=excluded_groups,
                ):
                    eliminations.add(weak_wing)

    return eliminations


def _find_column_based_eliminations(
    candidate: int,
    rows: list[list[Cell]],
    columns: list[list[Cell]],
    groups: list[list[Cell]],
) -> set[Cell]:
    """Find rectangle eliminations based on column strong links."""
    eliminations: set[Cell] = set()

    for column in columns:
        strong_link_cells = _candidate_cells(
            column,
            candidate,
        )

        if len(strong_link_cells) != 2:
            continue

        first_cell, second_cell = strong_link_cells

        for hinge, strong_wing in (
            (first_cell, second_cell),
            (second_cell, first_cell),
        ):
            if hinge.group == strong_wing.group:
                continue

            weak_wings = _candidate_cells(
                rows[hinge.row],
                candidate,
            )

            for weak_wing in weak_wings:
                if weak_wing is hinge:
                    continue

                if len(weak_wing.candidates) <= 1:
                    continue

                if weak_wing.group in {
                    hinge.group,
                    strong_wing.group,
                }:
                    continue

                excluded_groups = {
                    hinge.group,
                    strong_wing.group,
                    weak_wing.group,
                }

                if _wings_empty_candidate_from_group(
                    candidate=candidate,
                    first_wing=strong_wing,
                    second_wing=weak_wing,
                    groups=groups,
                    excluded_groups=excluded_groups,
                ):
                    eliminations.add(weak_wing)

    return eliminations


def reduce_rectangle_elimination(
    rows: list[list[Cell]],
    columns: list[list[Cell]],
    groups: list[list[Cell]],
) -> None:
    """Remove candidates using rectangle elimination.

    A rectangle elimination exists when a candidate in a weakly linked wing
    would force the other end of a strong link to be true, and those two
    candidates would eliminate every occurrence of that candidate from
    another group.
    """
    while True:
        eliminations: set[tuple[Cell, int]] = set()

        for candidate in range(1, 10):
            row_eliminations = _find_row_based_eliminations(
                candidate,
                rows,
                columns,
                groups,
            )
            column_eliminations = _find_column_based_eliminations(
                candidate,
                rows,
                columns,
                groups,
            )

            eliminations.update(
                (cell, candidate) for cell in row_eliminations | column_eliminations
            )

        if not eliminations:
            break

        reduction_found = False

        for cell, candidate in eliminations:
            if candidate not in cell.candidates:
                continue

            new_candidates = cell.candidates - {candidate}

            if not new_candidates:
                raise ValueError(f"Rectangle elimination emptied {cell!r}.")

            cell.set_candidates(new_candidates)

            if len(new_candidates) == 1:
                cell.set_deciding_rule("rectangle_elimination")

            reduction_found = True

        if not reduction_found:
            break
