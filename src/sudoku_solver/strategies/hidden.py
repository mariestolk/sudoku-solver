"""Hidden-subset candidate reduction strategies."""

from itertools import combinations

from sudoku_solver.cell import Cell

_subset_names = {
    1: "hidden_single",
    2: "hidden_pair",
    3: "hidden_triple",
    4: "hidden_quadruple",
}


def reduce_hidden_subsets(
    rows: list[list[Cell]],
    columns: list[list[Cell]],
    groups: list[list[Cell]],
    max_subset_size: int = 4,
) -> None:
    """Reduce candidates using hidden subsets.

    A hidden subset of size n exists when n candidates occur only within
    the same n cells of a house.
    """
    houses = [*rows, *columns, *groups]

    for house in houses:
        while True:
            reduction_found = False

            unsolved_cells = [
                cell for cell in house if cell.value is None and cell.candidates
            ]

            candidate_to_cells_map: dict[int, set[Cell]] = {}

            for cell in unsolved_cells:
                for candidate in cell.candidates:
                    candidate_to_cells_map.setdefault(candidate, set()).add(cell)

            largest_subset = min(
                max_subset_size,
                len(unsolved_cells) - 1,
            )

            for subset_size in range(1, largest_subset + 1):
                eligible_candidates = [
                    candidate
                    for candidate, candidate_cells in candidate_to_cells_map.items()
                    if 1 <= len(candidate_cells) <= subset_size
                ]

                for subset_candidates in combinations(
                    eligible_candidates,
                    subset_size,
                ):
                    subset_cells: set[Cell] = set()

                    for candidate in subset_candidates:
                        subset_cells.update(candidate_to_cells_map[candidate])

                    if len(subset_cells) != subset_size:
                        continue

                    allowed_candidates = set(subset_candidates)

                    restrictions = {
                        cell: cell.candidates & allowed_candidates
                        for cell in subset_cells
                        if cell.candidates - allowed_candidates
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
