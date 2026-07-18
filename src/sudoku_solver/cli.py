"""Interactive step-by-step sudoku solver."""

import random
from pathlib import Path

from rich import print as rprint
from rich.prompt import Prompt

from sudoku_solver.loader import load_from_csv, load_from_json
from sudoku_solver.puzzle import PuzzleData
from sudoku_solver.puzzles.chaossudoku_3 import cs_3
from sudoku_solver.puzzles.chaossudoku_4 import cs_4
from sudoku_solver.puzzles.sudoku_1_summit import sudoku_1_summit as sud_1_summ
from sudoku_solver.tui import SudokuApp

CSV_PATH = Path("data") / "sudoku.csv"
DATA_DIR = Path("data")
KAGGLE_SAMPLE_SIZE = 1000


def _find_unsolved_puzzles() -> list[tuple[int, Path]]:
    """Return sorted list of saved unsolved puzzle JSON files."""
    if not DATA_DIR.exists():
        return []
    results = []
    for f in sorted(DATA_DIR.glob("unsolved_puzzle_*.json")):
        try:
            results.append((int(f.stem.split("_")[-1]), f))
        except ValueError:
            pass
    return results


def select_puzzle() -> PuzzleData:
    """Prompt the user to select a puzzle and return the corresponding PuzzleData."""
    unsolved = _find_unsolved_puzzles()

    rprint("\n[bold]Select a puzzle to solve:[/bold]")
    rprint("  [cyan]1[/] Chaos Sudoku #3")
    rprint("  [cyan]2[/] Chaos Sudoku #4")
    rprint("  [cyan]3[/] Sudoku #1 Summit")
    rprint("  [cyan]4[/] Random puzzle from Kaggle dataset")

    for menu_index, (puzzle_index, _) in enumerate(unsolved, start=5):
        rprint(f"  [cyan]{menu_index}[/] Unsolved puzzle #{puzzle_index}")

    choices = [
        "1",
        "2",
        "3",
        "4",
        *[str(menu_index) for menu_index in range(5, 5 + len(unsolved))],
    ]

    choice = Prompt.ask("\nEnter choice", choices=choices)

    if choice == "1":
        return cs_3

    if choice == "2":
        return cs_4

    if choice == "3":
        return sud_1_summ

    if choice != "4":
        puzzle_index, path = unsolved[int(choice) - 5]
        rprint(f"\n[dim]Loading unsolved puzzle #{puzzle_index}.[/]")
        return load_from_json(path)

    if not CSV_PATH.exists():
        rprint(f"\n[red]Dataset not found at {CSV_PATH}[/]")
        rprint("Download it with:")
        rprint("  uv run sudoku-download")
        raise SystemExit(1)

    sample = []

    for puzzle in load_from_csv(CSV_PATH):
        sample.append(puzzle)

        if len(sample) >= KAGGLE_SAMPLE_SIZE:
            break

    chosen = random.choice(sample)
    rprint("\n[dim]Randomly selected a puzzle from the dataset.[/]")
    return chosen


def solve_interactively(puzzle_data: PuzzleData) -> None:
    """Launch the Textual TUI for the given puzzle."""
    SudokuApp(puzzle_data).run()


def main() -> None:
    """Run the interactive step-by-step sudoku solver."""
    puzzle_data = select_puzzle()
    rprint()
    solve_interactively(puzzle_data)


if __name__ == "__main__":
    main()
