"""Candidate reduction strategies for sudoku solving."""

from sudoku_solver.strategies.elimination import (
    reduce_columns,
    reduce_groups,
    reduce_rows,
)
from sudoku_solver.strategies.hidden import reduce_hidden_pair, reduce_hidden_single
from sudoku_solver.strategies.naked import reduce_naked_pairs, reduce_naked_triples
from sudoku_solver.strategies.pinned import reduce_pinned_candidate
from sudoku_solver.strategies.xwing import reduce_xwing

__all__ = [
    "reduce_rows",
    "reduce_columns",
    "reduce_groups",
    "reduce_naked_pairs",
    "reduce_naked_triples",
    "reduce_hidden_single",
    "reduce_hidden_pair",
    "reduce_pinned_candidate",
    "reduce_xwing",
]
