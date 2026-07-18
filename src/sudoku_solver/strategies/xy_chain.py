"""XY-chain candidate reduction strategy."""

from collections import deque

from sudoku_solver.cell import Cell

ChainResult = tuple[
    tuple[Cell, ...],
    int,
    set[Cell],
]


def reduce_xy_chains(
    rows: list[list[Cell]],
    columns: list[list[Cell]],
    groups: list[list[Cell]],
    max_chain_length: int = 12,
) -> None:
    """Reduce candidates using open XY-chains.

    An XY-chain is a sequence of bivalue cells in which consecutive cells
    see one another and share the candidate used to continue the chain.

    When the unlinked candidate at both ends is the same, that candidate
    can be removed from every other cell that sees both endpoints.
    """
    if max_chain_length < 3:
        raise ValueError("An XY-chain must contain at least three cells.")

    peer_map = _build_peer_map(
        rows,
        columns,
        groups,
    )

    while True:
        result = _find_xy_chain(
            rows=rows,
            peer_map=peer_map,
            max_chain_length=max_chain_length,
        )

        if result is None:
            break

        _, target_candidate, elimination_cells = result

        for cell in elimination_cells:
            new_candidates = cell.candidates - {target_candidate}

            if not new_candidates:
                raise ValueError("XY-chain elimination left a cell without candidates.")

            cell.set_candidates(sorted(new_candidates))

            if len(new_candidates) == 1:
                cell.set_deciding_rule("xy_chain")


def _build_peer_map(
    rows: list[list[Cell]],
    columns: list[list[Cell]],
    groups: list[list[Cell]],
) -> dict[Cell, set[Cell]]:
    """Map every cell to the cells sharing one of its houses."""
    cells = [cell for row in rows for cell in row]

    peer_map: dict[Cell, set[Cell]] = {cell: set() for cell in cells}

    houses = [
        *rows,
        *columns,
        *groups,
    ]

    for house in houses:
        for cell in house:
            peer_map[cell].update(house)
            peer_map[cell].discard(cell)

    return peer_map


def _find_xy_chain(
    rows: list[list[Cell]],
    peer_map: dict[Cell, set[Cell]],
    max_chain_length: int,
) -> ChainResult | None:
    """Return the first XY-chain that produces an elimination."""
    all_cells = [cell for row in rows for cell in row]

    bivalue_cells = {
        cell for cell in all_cells if (cell.value is None and len(cell.candidates) == 2)
    }

    ordered_bivalue_cells = sorted(
        bivalue_cells,
        key=_cell_key,
    )

    for start_cell in ordered_bivalue_cells:
        for target_candidate in sorted(start_cell.candidates):
            outgoing_candidate = _other_candidate(
                start_cell,
                target_candidate,
            )

            result = _search_from_start(
                start_cell=start_cell,
                target_candidate=target_candidate,
                outgoing_candidate=outgoing_candidate,
                all_cells=all_cells,
                bivalue_cells=bivalue_cells,
                peer_map=peer_map,
                max_chain_length=max_chain_length,
            )

            if result is not None:
                return result

    return None


def _search_from_start(
    start_cell: Cell,
    target_candidate: int,
    outgoing_candidate: int,
    all_cells: list[Cell],
    bivalue_cells: set[Cell],
    peer_map: dict[Cell, set[Cell]],
    max_chain_length: int,
) -> ChainResult | None:
    """Search for a valid XY-chain beginning at one cell."""
    queue: deque[
        tuple[
            Cell,
            int,
            tuple[Cell, ...],
        ]
    ] = deque(
        [
            (
                start_cell,
                outgoing_candidate,
                (start_cell,),
            )
        ]
    )

    while queue:
        (
            current_cell,
            linking_candidate,
            path,
        ) = queue.popleft()

        if len(path) >= max_chain_length:
            continue

        next_cells = sorted(
            peer_map[current_cell] & bivalue_cells,
            key=_cell_key,
        )

        for next_cell in next_cells:
            if next_cell in path:
                continue

            if linking_candidate not in next_cell.candidates:
                continue

            next_outgoing_candidate = _other_candidate(
                next_cell,
                linking_candidate,
            )

            new_path = (*path, next_cell)

            if len(new_path) >= 3 and next_outgoing_candidate == target_candidate:
                elimination_cells = _find_elimination_cells(
                    start_cell=start_cell,
                    end_cell=next_cell,
                    target_candidate=target_candidate,
                    path=new_path,
                    all_cells=all_cells,
                    peer_map=peer_map,
                )

                if elimination_cells:
                    return (
                        new_path,
                        target_candidate,
                        elimination_cells,
                    )

            queue.append(
                (
                    next_cell,
                    next_outgoing_candidate,
                    new_path,
                )
            )

    return None


def _find_elimination_cells(
    start_cell: Cell,
    end_cell: Cell,
    target_candidate: int,
    path: tuple[Cell, ...],
    all_cells: list[Cell],
    peer_map: dict[Cell, set[Cell]],
) -> set[Cell]:
    """Find cells that see both ends of an XY-chain."""
    chain_cells = set(path)

    return {
        cell
        for cell in all_cells
        if (
            cell not in chain_cells
            and cell.value is None
            and len(cell.candidates) > 1
            and target_candidate in cell.candidates
            and cell in peer_map[start_cell]
            and cell in peer_map[end_cell]
        )
    }


def _other_candidate(
    cell: Cell,
    candidate: int,
) -> int:
    """Return the other candidate in a bivalue cell."""
    other_candidates = cell.candidates - {candidate}

    if len(other_candidates) != 1:
        raise ValueError("XY-chain links require bivalue cells.")

    return next(iter(other_candidates))


def _cell_key(
    cell: Cell,
) -> tuple[int, int]:
    """Return a stable sorting key for a cell."""
    return cell.row, cell.column
