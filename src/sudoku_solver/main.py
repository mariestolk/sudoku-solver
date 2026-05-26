"""Interactive step-by-step sudoku solver."""

import random
from pathlib import Path

from puzzle import Puzzle
from puzzles import PuzzleData
from puzzles.chaossudoku_3 import cs_3
from puzzles.chaossudoku_4 import cs_4
from puzzles.loader import load_from_csv
from rich import print as rprint
from rich.prompt import Confirm, Prompt

CSV_PATH = (
    Path(__file__).parent.parent.parent
    / "src"
    / "sudoku_solver"
    / "puzzles"
    / "sudoku.csv"
)
KAGGLE_SAMPLE_SIZE = 1000


def select_puzzle() -> PuzzleData:
    """Prompt the user to select a puzzle and return the corresponding PuzzleData."""
    rprint("\n[bold]Select a puzzle to solve:[/bold]")
    rprint("  [cyan]1[/] Chaos Sudoku #3")
    rprint("  [cyan]2[/] Chaos Sudoku #4")
    rprint("  [cyan]3[/] Random puzzle from Kaggle dataset")

    choice = Prompt.ask("\nEnter choice", choices=["1", "2", "3"])

    if choice == "1":
        return cs_3
    if choice == "2":
        return cs_4

    if not CSV_PATH.exists():
        rprint(f"\n[red]Dataset not found at {CSV_PATH}[/]")
        rprint("Download it with:")
        rprint("  uv run kaggle datasets download rohanrao/sudoku ")
        rprint("  --unzip --path puzzles")
        raise SystemExit(1)

    rprint(f"\n[dim]Sampling {KAGGLE_SAMPLE_SIZE} puzzles from dataset...[/]")
    sample = []
    for puzzle in load_from_csv(CSV_PATH):
        sample.append(puzzle)
        if len(sample) >= KAGGLE_SAMPLE_SIZE:
            break

    return random.choice(sample)


def solve_interactively(puzzle_data: PuzzleData) -> None:
    """Run the step-by-step solving loop for the given puzzle."""
    puzzle = Puzzle(puzzle_data.values, puzzle_data.groups)
    puzzle.print_puzzle()

    i = 0
    while not puzzle.is_solved():
        if not Confirm.ask(f"\n[bold]Step {i + 1}[/bold] — continue?"):
            break

        puzzle.solve_step()
        rprint()
        puzzle.print_puzzle()
        i += 1


def main():
    """Run the interactive step-by-step sudoku solver."""
    puzzle_data = select_puzzle()
    rprint()
    solve_interactively(puzzle_data)


if __name__ == "__main__":
    main()
