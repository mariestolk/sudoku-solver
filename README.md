# Sudoku Solver

An interactive, step-by-step sudoku solver using constraint propagation. Supports both standard sudoku and **chaos sudoku**, a variant where the nine groups are irregular shapes rather than fixed 3×3 boxes.

## Setup

Requires Python 3.11.5 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Running

```bash
cd src/sudoku_solver
uv run python main.py
```

On startup, you choose a puzzle:

```
Select a puzzle to solve:
  1  Chaos Sudoku #3
  2  Chaos Sudoku #4
  3  Random puzzle from Kaggle dataset
```

The solver then works through the puzzle one step at a time, printing the grid after each step and showing which rule determined the placed value:

```
Cell (4, 2) → 7  [hidden single]
```

## Kaggle dataset

To enable option 3, download the [9 Million Sudoku Puzzles](https://www.kaggle.com/datasets/rohanrao/sudoku) dataset from the project root:

```bash
kaggle datasets download rohanrao/sudoku --unzip --path src/sudoku_solver/puzzles
```

This requires a Kaggle account. Place your `kaggle.json` credentials at `%USERPROFILE%\.kaggle\kaggle.json` (Windows) or `~/.kaggle/kaggle.json` (Linux/macOS).

## How the solver works

Each empty cell starts with candidates `{1–9}`. After every value is placed, `reduce_candidates()` runs a pipeline of constraint-propagation rules in order:

| Rule | Description |
|---|---|
| Row / column / group elimination | Remove a placed value from peers in the same row, column, and group |
| Naked pairs / triples | If N cells in a group share exactly N candidates, remove those from all other cells in the group |
| Hidden singles | If a candidate appears in only one cell within a row, column, or group, lock that cell to that candidate |
| Hidden pairs | If a candidate appears in exactly two cells within a group, remove it from all other cells in the group |
| Pinned candidates | If all cells holding a candidate within a group share a row or column, eliminate that candidate from the rest of that row/column |

`solve_step()` picks a random cell that has been reduced to a single candidate, places the value, and triggers another round of reduction. The process repeats until the puzzle is solved or no more naked singles remain.

> **Note:** the solver uses constraint propagation only — there is no backtracking. Puzzles that require guessing will stall.

## Adding puzzles

Puzzles are represented as a `PuzzleData` named tuple of two 9×9 grids: `values` (initial numbers, `0` for empty) and `groups` (group ID `0–8` per cell). Standard 3×3 box groups are the default when `groups` is omitted.

```python
from puzzles import PuzzleData

my_puzzle = PuzzleData(
    values=[[0, 0, 3, ...], ...],
    groups=[[0, 0, 0, ...], ...],  # omit for standard sudoku
)
```

See `src/sudoku_solver/puzzles/chaossudoku_3.py` for a full example.
