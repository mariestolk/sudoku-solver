"""Naked pair and naked triple strategies."""

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
    """Reduce candidates by identifying naked triples in each group."""
    for group in groups:
        three_candidate_cells = [
            cell for cell in group if cell.value is None and len(cell.candidates) == 3
        ]
        candidate_triplet_map: dict[tuple[int, ...], list[Cell]] = {}
        for cell in three_candidate_cells:
            key = tuple(sorted(cell.candidates))
            candidate_triplet_map.setdefault(key, []).append(cell)
        for candidate_triplet, cells in candidate_triplet_map.items():
            if len(cells) == 3:
                for other_cell in group:
                    if other_cell not in cells and other_cell.value is None:
                        other_cell.candidates.difference_update(candidate_triplet)
