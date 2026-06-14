"""Evaluator: run a batch of Kaggle puzzles and report solve rate + rule usage."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TimeRemainingColumn
from rich.table import Table

from sudoku_solver.loader import load_from_csv
from sudoku_solver.puzzle import Puzzle, PuzzleData

DEFAULT_BATCH_SIZE = 500
DEFAULT_CSV_PATH = Path("data") / "sudoku.csv"


@dataclass
class BatchResult:
    """Aggregated statistics for a batch of evaluated puzzles."""

    total: int = 0
    solved: int = 0
    rule_counts: Counter[str] = field(default_factory=Counter)
    stuck: list[tuple[PuzzleData, list[list[int | None]]]] = field(default_factory=list)
    first_stuck_index: int | None = None


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
            else:
                if result.first_stuck_index is None:
                    result.first_stuck_index = i
                result.stuck.append((pd, partial))
            progress.advance(task)
    return result


def _grid_to_str(grid: Sequence[Sequence[int | None]]) -> str:
    return "".join(str(v) if v is not None else "0" for row in grid for v in row)


def _save_first_stuck(pd: PuzzleData, index: int, directory: Path) -> Path:
    """Save a single stuck puzzle as unsolved_puzzle_{index}.json."""
    data: dict[str, str | int] = {
        "index": index,
        "puzzle": _grid_to_str(pd.values),
    }
    if pd.solution is not None:
        data["solution"] = _grid_to_str(pd.solution)
    path = directory / f"unsolved_puzzle_{index}.json"
    path.write_text(json.dumps(data, indent=2))
    return path


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
    parser.add_argument(
        "csv",
        type=Path,
        metavar="FILE",
        nargs="?",
        default=DEFAULT_CSV_PATH,
        help=f"Kaggle-format CSV file (default: {DEFAULT_CSV_PATH})",
    )
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
    parser.add_argument(
        "--save-first-stuck",
        action="store_true",
        help=(
            "Save the first unsolvable puzzle to the data folder as "
            "unsolved_puzzle_<N>.json"
        ),
    )
    args = parser.parse_args()

    console = Console()
    if not args.csv.exists():
        console.print(
            f"[bold red]File not found:[/bold red] [cyan]{args.csv}[/cyan]\n"
            "Download it with: [bold]uv run sudoku-download[/bold]"
        )
        raise SystemExit(1)
    result = evaluate_batch(load_from_csv(args.csv), args.batch_size, console)

    if args.save_first_stuck and result.stuck and result.first_stuck_index is not None:
        pd, _ = result.stuck[0]
        saved = _save_first_stuck(pd, result.first_stuck_index, args.csv.parent)
        console.print(f"Saved first stuck puzzle to [cyan]{saved}[/cyan]")

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


if __name__ == "__main__":
    main()
