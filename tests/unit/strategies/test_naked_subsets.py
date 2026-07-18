"""Tests for the generalized naked-subset strategy."""

import pytest
from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.naked import reduce_naked_subsets


def make_house(
    candidate_sets: list[list[int]],
    house_type: str = "row",
) -> list[Cell]:
    """Create one row, column, or group with the given candidates."""
    cells: list[Cell] = []

    for index, candidates in enumerate(candidate_sets):
        if house_type == "row":
            row = 0
            column = index
            group = index // 3
        elif house_type == "column":
            row = index
            column = 0
            group = (index // 3) * 3
        elif house_type == "group":
            row = index // 3
            column = index % 3
            group = 0
        else:
            raise ValueError(f"Unknown house type: {house_type}")

        cell = create_cell(row, column, group)
        cell.set_candidates(candidates)
        cells.append(cell)

    return cells


def apply_to_house(
    house: list[Cell],
    house_type: str = "row",
    max_subset_size: int = 4,
) -> None:
    """Run the strategy with the house in the appropriate argument."""
    if house_type == "row":
        reduce_naked_subsets(
            rows=[house],
            columns=[],
            groups=[],
            max_subset_size=max_subset_size,
        )
        return

    if house_type == "column":
        reduce_naked_subsets(
            rows=[],
            columns=[house],
            groups=[],
            max_subset_size=max_subset_size,
        )
        return

    if house_type == "group":
        reduce_naked_subsets(
            rows=[],
            columns=[],
            groups=[house],
            max_subset_size=max_subset_size,
        )
        return

    raise ValueError(f"Unknown house type: {house_type}")


@pytest.mark.parametrize("house_type", ["row", "column", "group"])
def test_naked_pair_is_found_in_every_house_type(
    house_type: str,
) -> None:
    """Ensure naked pairs work in rows, columns, and groups."""
    house = make_house(
        [
            [3, 7],
            [3, 7],
            [1, 3, 5, 7],
        ],
        house_type=house_type,
    )

    apply_to_house(
        house,
        house_type=house_type,
    )

    assert house[0].candidates == {3, 7}
    assert house[1].candidates == {3, 7}
    assert house[2].candidates == {1, 5}


def test_naked_pair_removes_candidates_from_all_other_cells() -> None:
    """Ensure pair candidates are removed from every other affected cell."""
    house = make_house(
        [
            [3, 7],
            [3, 7],
            [1, 3, 5],
            [2, 4, 7, 8],
            [1, 2, 8, 9],
        ]
    )

    apply_to_house(house)

    assert house[2].candidates == {1, 5}
    assert house[3].candidates == {2, 4, 8}
    assert house[4].candidates == {1, 2, 8, 9}


def test_naked_pair_cells_keep_their_candidates() -> None:
    """Ensure the cells forming a naked pair remain unchanged."""
    house = make_house(
        [
            [3, 7],
            [3, 7],
            [1, 3, 5, 7],
        ]
    )

    apply_to_house(house)

    assert house[0].candidates == {3, 7}
    assert house[1].candidates == {3, 7}


def test_naked_triple_uses_combined_cell_candidates() -> None:
    """Ensure three cells with three combined candidates form a triple."""
    house = make_house(
        [
            [1, 2],
            [1, 3],
            [2, 3],
            [1, 2, 3, 4, 5],
        ]
    )

    apply_to_house(house)

    assert house[0].candidates == {1, 2}
    assert house[1].candidates == {1, 3}
    assert house[2].candidates == {2, 3}
    assert house[3].candidates == {4, 5}


def test_naked_quadruple_restricts_other_cells() -> None:
    """Ensure four cells with four combined candidates form a quadruple."""
    house = make_house(
        [
            [1, 2],
            [2, 3],
            [3, 4],
            [1, 4],
            [1, 2, 3, 4, 5, 6],
        ]
    )

    apply_to_house(house)

    assert house[0].candidates == {1, 2}
    assert house[1].candidates == {2, 3}
    assert house[2].candidates == {3, 4}
    assert house[3].candidates == {1, 4}
    assert house[4].candidates == {5, 6}


def test_reduction_records_rule_when_cell_becomes_single() -> None:
    """Ensure the subset rule is recorded when a peer becomes resolved."""
    house = make_house(
        [
            [1, 2],
            [1, 2],
            [1, 2, 5],
        ]
    )

    apply_to_house(house)

    assert house[2].candidates == {5}
    assert house[2].deciding_rule == "naked_pair"


def test_no_change_when_no_naked_subset_exists() -> None:
    """Ensure candidates remain unchanged without a naked subset."""
    candidate_sets = [
        [1, 2],
        [1, 3],
        [2, 4, 5],
    ]
    house = make_house(candidate_sets)
    before = [cell.candidates.copy() for cell in house]

    apply_to_house(house)

    assert [cell.candidates for cell in house] == before


def test_already_reduced_naked_pair_causes_no_change() -> None:
    """Ensure a pair with no affected peers leaves the house unchanged."""
    candidate_sets = [
        [1, 2],
        [1, 2],
        [3, 4, 5],
    ]
    house = make_house(candidate_sets)
    before = [cell.candidates.copy() for cell in house]

    apply_to_house(house)

    assert [cell.candidates for cell in house] == before


def test_max_subset_size_can_disable_naked_triples() -> None:
    """Ensure triples are skipped when the maximum size is two."""
    candidate_sets = [
        [1, 2],
        [1, 3],
        [2, 3],
        [1, 2, 3, 4, 5],
    ]
    house = make_house(candidate_sets)

    apply_to_house(
        house,
        max_subset_size=2,
    )

    for cell, candidates in zip(house, candidate_sets):
        assert cell.candidates == set(candidates)


def test_reductions_are_isolated_to_the_affected_house() -> None:
    """Ensure an unrelated house remains unchanged."""
    affected_house = make_house(
        [
            [3, 7],
            [3, 7],
            [1, 3, 5, 7],
        ],
        house_type="row",
    )

    unaffected_house = make_house(
        [
            [3, 7, 9],
            [1, 2, 3],
            [4, 5, 6],
        ],
        house_type="group",
    )
    unaffected_before = [cell.candidates.copy() for cell in unaffected_house]

    reduce_naked_subsets(
        rows=[affected_house],
        columns=[],
        groups=[unaffected_house],
    )

    assert affected_house[2].candidates == {1, 5}

    for cell, original_candidates in zip(
        unaffected_house,
        unaffected_before,
    ):
        assert cell.candidates == original_candidates
