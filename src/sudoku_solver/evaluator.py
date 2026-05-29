"""Evaluator: run a batch of Kaggle puzzles and report solve rate + rule usage."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TimeRemainingColumn
from rich.table import Table

from sudoku_solver.loader import load_from_csv
from sudoku_solver.puzzle import Puzzle, PuzzleData

DEFAULT_BATCH_SIZE = 1000

RULE_TIERS: list[tuple[str, set[str]]] = [
    ("elimination", {"row elimination", "column elimination", "group elimination"}),
    ("+ hidden single", {"hidden single"}),
    ("+ pinned candidate", {"pinned candidate"}),
    ("+ naked pair", {"naked pair"}),
    ("+ naked triple", {"naked triple"}),
    ("+ hidden pair", {"hidden pair"}),
]


@dataclass
class BatchResult:
    """Aggregated statistics for a batch of evaluated puzzles."""

    total: int = 0
    solved: int = 0
    rule_counts: Counter[str] = field(default_factory=Counter)
    rules_per_solved: list[frozenset[str]] = field(default_factory=list)
    stuck: list[tuple[PuzzleData, list[list[int | None]]]] = field(default_factory=list)


def _solve_puzzle(
    pd: PuzzleData,
) -> tuple[bool, Counter[str], list[list[int | None]]]:
    puzzle = Puzzle(pd.values, pd.groups)
    counts: Counter[str] = Counter()
    while result := puzzle.solve_step():
        counts[result.rule] += 1
    partial = [[cell.value for cell in row] for row in puzzle.rows]
    return puzzle.is_solved, counts, partial


def evaluate_batch(
    puzzles: Iterable[PuzzleData],
    batch_size: int,
    console: Console,
) -> BatchResult:
    """Solve up to batch_size puzzles and return aggregated statistics."""
    result = BatchResult()
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        MofNCompleteColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Solving...", total=batch_size)
        for i, pd in enumerate(puzzles):
            if i >= batch_size:
                break
            solved, counts, partial = _solve_puzzle(pd)
            result.total += 1
            result.rule_counts += counts
            if solved:
                result.solved += 1
                result.rules_per_solved.append(frozenset(counts.keys()))
            else:
                result.stuck.append((pd, partial))
            progress.advance(task)
    return result


def _grid_to_str(grid: Sequence[Sequence[int | None]]) -> str:
    return "".join(str(v) if v is not None else "0" for row in grid for v in row)


def _write_stuck(
    stuck: list[tuple[PuzzleData, list[list[int | None]]]], path: Path
) -> None:
    rows = []
    for pd, partial in stuck:
        row: dict[str, str] = {
            "puzzle": _grid_to_str(pd.values),
            "partial": _grid_to_str(partial),
        }
        if pd.solution is not None:
            row["solution"] = _grid_to_str(pd.solution)
        rows.append(row)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Run evaluation for a batch of Kaggle sudoku puzzles."""
    parser = argparse.ArgumentParser(description="Evaluate sudoku solver performance.")
    parser.add_argument("csv", type=Path, metavar="FILE", help="Kaggle-format CSV file")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        metavar="N",
        help=f"Number of puzzles to evaluate (default: {DEFAULT_BATCH_SIZE})",
    )
    parser.add_argument(
        "--output", type=Path, metavar="FILE", help="Save stuck puzzles to this CSV"
    )
    args = parser.parse_args()

    console = Console()
    result = evaluate_batch(load_from_csv(args.csv), args.batch_size, console)

    if args.output and result.stuck:
        _write_stuck(result.stuck, args.output)
        console.print(
            f"Saved {len(result.stuck)} stuck puzzle(s) to [cyan]{args.output}[/cyan]"
        )

    solve_pct = 100 * result.solved // result.total if result.total else 0
    console.print(
        f"[bold]Solve rate:[/bold] {result.solved}/{result.total} ({solve_pct}%)"
    )

    if result.rule_counts:
        total_assignments = sum(result.rule_counts.values())
        usage_table = Table(title="Rule usage", header_style="bold")
        usage_table.add_column("Rule", style="cyan")
        usage_table.add_column("Count", justify="right")
        usage_table.add_column("Share", justify="right")
        for rule, count in result.rule_counts.most_common():
            usage_table.add_row(
                rule, str(count), f"{100 * count / total_assignments:.1f}%"
            )
        console.print()
        console.print(usage_table)

    if result.rules_per_solved:
        suff_table = Table(
            title="Rule sufficiency (solved puzzles)", header_style="bold"
        )
        suff_table.add_column("Rules available", style="cyan")
        suff_table.add_column("Puzzles solved", justify="right")
        suff_table.add_column("% of solved", justify="right")
        cumulative: set[str] = set()
        for tier_name, tier_rules in RULE_TIERS:
            cumulative |= tier_rules
            count = sum(1 for r in result.rules_per_solved if r.issubset(cumulative))
            suff_table.add_row(
                tier_name, str(count), f"{100 * count / result.solved:.1f}%"
            )
        console.print()
        console.print(suff_table)


if __name__ == "__main__":
    main()
