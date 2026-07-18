"""Naked-subset candidate reduction strategies."""

from itertools import combinations

from sudoku_solver.cell import Cell

_subset_names = {
    2: "naked_pair",
    3: "naked_triple",
    4: "naked_quadruple",
}


def reduce_naked_subsets(
    rows: list[list[Cell]],
    columns: list[list[Cell]],
    groups: list[list[Cell]],
    max_subset_size: int = 4,
) -> None:
    """Reduce candidates using naked subsets.

    A naked subset of size n exists when n cells in a house collectively
    contain exactly n candidates. Those candidates can be removed from all
    other unsolved cells in the house.
    """
    houses = [*rows, *columns, *groups]

    for house in houses:
        while True:
            reduction_found = False

            unsolved_cells = [
                cell for cell in house if cell.value is None and cell.candidates
            ]

            largest_subset = min(
                max_subset_size,
                len(unsolved_cells) - 1,
            )

            for subset_size in range(2, largest_subset + 1):
                eligible_cells = [
                    cell
                    for cell in unsolved_cells
                    if 2 <= len(cell.candidates) <= subset_size
                ]

                for subset_cells_tuple in combinations(
                    eligible_cells,
                    subset_size,
                ):
                    subset_candidates: set[int] = set()

                    for cell in subset_cells_tuple:
                        subset_candidates.update(cell.candidates)

                    if len(subset_candidates) != subset_size:
                        continue

                    subset_cells = set(subset_cells_tuple)

                    restrictions = {
                        cell: cell.candidates - subset_candidates
                        for cell in unsolved_cells
                        if (
                            cell not in subset_cells
                            and cell.candidates & subset_candidates
                        )
                    }

                    if not restrictions:
                        continue

                    rule_name = _subset_names[subset_size]

                    for cell, new_candidates in restrictions.items():
                        cell.set_candidates(new_candidates)

                        if len(new_candidates) == 1:
                            cell.set_deciding_rule(rule_name)

                    reduction_found = True
                    break

                if reduction_found:
                    break

            if not reduction_found:
                break
