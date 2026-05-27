"""Interactive step-by-step sudoku solver."""

import random
from pathlib import Path

from rich import print as rprint
from rich.prompt import Confirm, Prompt

from sudoku_solver.puzzle import Puzzle
from sudoku_solver.puzzles import PuzzleData
from sudoku_solver.puzzles.chaossudoku_3 import cs_3
from sudoku_solver.puzzles.chaossudoku_4 import cs_4
from sudoku_solver.puzzles.loader import load_from_csv
from sudoku_solver.renderer import print_puzzle, print_step

CSV_PATH = Path(__file__).parent / "puzzles" / "sudoku.csv"
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
    print_puzzle(puzzle.rows)

    i = 0
    while not puzzle.is_solved:
        if not Confirm.ask(f"\n[bold]Step {i + 1}[/bold] — continue?"):
            break

        result = puzzle.solve_step()
        if result is not None:
            print_step(result)
        rprint()
        print_puzzle(puzzle.rows)
        i += 1

    if puzzle.is_solved:
        rprint()
        rprint("[magenta]Puzzle is solved![/]")
        rprint()


def main() -> None:
    """Run the interactive step-by-step sudoku solver."""
    puzzle_data = select_puzzle()
    rprint()
    solve_interactively(puzzle_data)


if __name__ == "__main__":
    main()
