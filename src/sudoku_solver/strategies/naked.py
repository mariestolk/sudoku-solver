"""Naked pair and naked triple strategies."""

from itertools import combinations

from sudoku_solver.cell import Cell


def reduce_naked_pairs(groups: list[list[Cell]]) -> None:
    """Reduce candidates by identifying naked pairs in each group."""
    for group in groups:
        two_candidate_cells = [
            cell for cell in group if cell.value is None and len(cell.candidates) == 2
        ]
        candidate_pair_map: dict[tuple[int, ...], list[Cell]] = {}
        for cell in two_candidate_cells:
            key = tuple(sorted(cell.candidates))
            candidate_pair_map.setdefault(key, []).append(cell)
        for candidate_pair, cells in candidate_pair_map.items():
            if len(cells) == 2:
                for other_cell in group:
                    if other_cell not in cells and other_cell.value is None:
                        other_cell.candidates.difference_update(candidate_pair)


def reduce_naked_triples(groups: list[list[Cell]]) -> None:
    """Reduce candidates by identifying naked triples in each group.

    A naked triple is any three unsolved cells whose candidates collectively
    cover at most three values. Those values are removed from all other cells
    in the unit.
    """
    for group in groups:
        unsolved = [cell for cell in group if cell.value is None]
        eligible = [cell for cell in unsolved if len(cell.candidates) <= 3]
        for triple in combinations(eligible, 3):
            union = triple[0].candidates | triple[1].candidates | triple[2].candidates
            if len(union) <= 3:
                triple_cells = set(triple)
                for cell in unsolved:
                    if cell not in triple_cells:
                        cell.candidates -= union
