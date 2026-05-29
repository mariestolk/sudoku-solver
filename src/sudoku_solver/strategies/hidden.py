"""Hidden single and hidden pair strategies."""

from itertools import combinations

from sudoku_solver.cell import Cell


def reduce_hidden_single(
    rows: list[list[Cell]],
    columns: list[list[Cell]],
    groups: list[list[Cell]],
) -> None:
    """Reduce candidates by finding single candidates in rows, columns, and groups."""
    units: list[list[Cell]] = [*rows, *columns, *groups]
    for unit in units:
        candidate_map: dict[int, list[Cell]] = {}
        for cell in unit:
            if cell.value is None:
                for candidate in cell.candidates:
                    candidate_map.setdefault(candidate, []).append(cell)
        for candidate, cells in candidate_map.items():
            if len(cells) == 1 and len(cells[0].candidates) > 1:
                cells[0].set_candidates([candidate])


def reduce_hidden_pair(groups: list[list[Cell]]) -> None:
    """Narrow a cell pair to only its hidden pair values.

    A hidden pair exists when two candidates each appear in exactly the same
    two cells within a group. Those two cells must contain those two values,
    so all other candidates can be removed from them.
    """
    for group in groups:
        candidate_map: dict[int, list[Cell]] = {}
        for cell in group:
            if cell.value is None:
                for candidate in cell.candidates:
                    candidate_map.setdefault(candidate, []).append(cell)

        two_cell_candidates = [
            (cand, cells) for cand, cells in candidate_map.items() if len(cells) == 2
        ]
        for (cand_a, cells_a), (cand_b, cells_b) in combinations(
            two_cell_candidates,
            2,
        ):
            if {id(c) for c in cells_a} == {id(c) for c in cells_b}:
                pair_values = {cand_a, cand_b}
                for cell in cells_a:
                    cell.candidates &= pair_values
