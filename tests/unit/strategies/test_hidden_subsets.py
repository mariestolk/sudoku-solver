"""Tests for the generalized hidden-subset strategy."""

import pytest
from sudoku_solver.cell import Cell, create_cell
from sudoku_solver.strategies.hidden import reduce_hidden_subsets


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
        reduce_hidden_subsets(
            rows=[house],
            columns=[],
            groups=[],
            max_subset_size=max_subset_size,
        )
        return

    if house_type == "column":
        reduce_hidden_subsets(
            rows=[],
            columns=[house],
            groups=[],
            max_subset_size=max_subset_size,
        )
        return

    if house_type == "group":
        reduce_hidden_subsets(
            rows=[],
            columns=[],
            groups=[house],
            max_subset_size=max_subset_size,
        )
        return

    raise ValueError(f"Unknown house type: {house_type}")


def test_hidden_single_restricts_cell_to_single_candidate() -> None:
    """Ensure a candidate appearing in one cell becomes a hidden single."""
    house = make_house(
        [
            [1, 2],
            *[[2, 3, 4, 5, 6, 7, 8, 9] for _ in range(8)],
        ]
    )

    apply_to_house(house)

    assert house[0].candidates == {1}
    assert house[0].deciding_rule == "hidden_single"


@pytest.mark.parametrize("house_type", ["row", "column", "group"])
def test_hidden_pair_is_found_in_every_house_type(
    house_type: str,
) -> None:
    """Ensure hidden pairs work in rows, columns, and groups."""
    house = make_house(
        [
            [1, 3, 5],
            [1, 3, 6],
            *[[2, 4, 5, 6, 7, 8, 9] for _ in range(7)],
        ],
        house_type=house_type,
    )

    apply_to_house(
        house,
        house_type=house_type,
    )

    assert house[0].candidates == {1, 3}
    assert house[1].candidates == {1, 3}


def test_hidden_pair_does_not_modify_other_cells() -> None:
    """Ensure cells outside a hidden pair remain unchanged."""
    other_candidates = {2, 4, 5, 6, 7, 8, 9}

    house = make_house(
        [
            [1, 3, 5],
            [1, 3, 6],
            *[list(other_candidates) for _ in range(7)],
        ]
    )

    apply_to_house(house)

    for cell in house[2:]:
        assert cell.candidates == other_candidates


def test_hidden_triple_uses_combined_candidate_locations() -> None:
    """Ensure triple candidates need not occur in identical cells."""
    house = make_house(
        [
            [1, 2, 5],
            [1, 3, 6],
            [2, 3, 7],
            *[[4, 5, 6, 7, 8, 9] for _ in range(6)],
        ]
    )

    apply_to_house(house)

    assert house[0].candidates == {1, 2}
    assert house[1].candidates == {1, 3}
    assert house[2].candidates == {2, 3}


def test_hidden_quadruple_restricts_four_cells() -> None:
    """Ensure a hidden quadruple restricts all four subset cells."""
    house = make_house(
        [
            [1, 2, 5],
            [2, 3, 6],
            [3, 4, 7],
            [1, 4, 8],
            *[[5, 6, 7, 8, 9] for _ in range(5)],
        ]
    )

    apply_to_house(house)

    assert house[0].candidates == {1, 2}
    assert house[1].candidates == {2, 3}
    assert house[2].candidates == {3, 4}
    assert house[3].candidates == {1, 4}


def test_no_change_when_no_hidden_subset_exists() -> None:
    """Ensure candidates remain unchanged without a hidden subset."""
    all_candidates = set(range(1, 10))
    house = make_house([list(all_candidates) for _ in range(9)])
    before = [cell.candidates.copy() for cell in house]

    apply_to_house(house)

    assert [cell.candidates for cell in house] == before


def test_already_reduced_hidden_pair_remains_unchanged() -> None:
    """Ensure an already reduced hidden pair remains unchanged."""
    other_candidates = {2, 4, 5, 6, 7, 8, 9}

    house = make_house(
        [
            [1, 3],
            [1, 3],
            *[list(other_candidates) for _ in range(7)],
        ]
    )
    before = [cell.candidates.copy() for cell in house]

    apply_to_house(house)

    assert [cell.candidates for cell in house] == before


def test_max_subset_size_can_disable_hidden_triples() -> None:
    """Ensure triples are skipped when the maximum size is two."""
    original_candidates = [
        [1, 2, 5],
        [1, 3, 6],
        [2, 3, 7],
        *[[4, 5, 6, 7, 8, 9] for _ in range(6)],
    ]
    house = make_house(original_candidates)

    apply_to_house(
        house,
        max_subset_size=2,
    )

    for cell, candidates in zip(house, original_candidates):
        assert cell.candidates == set(candidates)


def test_reductions_are_isolated_to_the_affected_house() -> None:
    """Ensure an unrelated house remains unchanged."""
    affected_house = make_house(
        [
            [1, 3, 5],
            [1, 3, 6],
            *[[2, 4, 5, 6, 7, 8, 9] for _ in range(7)],
        ],
        house_type="row",
    )

    unaffected_house = make_house(
        [list(range(1, 10)) for _ in range(9)],
        house_type="group",
    )
    unaffected_before = [cell.candidates.copy() for cell in unaffected_house]

    reduce_hidden_subsets(
        rows=[affected_house],
        columns=[],
        groups=[unaffected_house],
    )

    assert affected_house[0].candidates == {1, 3}
    assert affected_house[1].candidates == {1, 3}

    for cell, original_candidates in zip(
        unaffected_house,
        unaffected_before,
    ):
        assert cell.candidates == original_candidates
