"""Textual TUI for the step-by-step sudoku solver."""

from __future__ import annotations

from rich.text import Text
from textual.app import App, ComposeResult
from textual.timer import Timer
from textual.widgets import RichLog, Static

from sudoku_solver.puzzle import Puzzle, PuzzleData
from sudoku_solver.renderer import format_puzzle, format_step


class SudokuApp(App[None]):
    """Interactive Textual TUI for the sudoku solver."""

    CSS = """
    Screen { layout: vertical; }
    #grid-panel { height: auto; border: round $primary; padding: 0 1; }
    #steps-log  { border: round $primary; padding: 0 1; }
    #hint-bar   { height: 1; color: $text-muted; padding: 0 1; }
    """

    BINDINGS = [
        ("space", "step", "Step"),
        ("enter", "step", "Step"),
        ("a", "auto_solve", "Auto-solve"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, puzzle_data: PuzzleData) -> None:
        """Initialize the TUI with the given puzzle data."""
        super().__init__()
        self._puzzle = Puzzle(puzzle_data.values, puzzle_data.groups)
        self._auto_timer: Timer | None = None
        self._step_count = 0

    def compose(self) -> ComposeResult:
        """Build the widget tree."""
        yield Static(id="grid-panel")
        yield RichLog(id="steps-log", markup=True)
        yield Static(
            "[dim]space/enter[/]  step  ·  [dim]a[/]  auto-solve  ·  [dim]q[/]  quit",
            id="hint-bar",
        )

    def on_mount(self) -> None:
        """Render the initial grid once the DOM is ready."""
        self._refresh_grid()

    def _refresh_grid(self) -> None:
        self.query_one("#grid-panel", Static).update(
            Text.from_markup(format_puzzle(self._puzzle.rows))
        )

    def _apply_step(self) -> None:
        if self._puzzle.is_solved:
            self._stop_auto()
            return
        result = self._puzzle.solve_step()
        log = self.query_one("#steps-log", RichLog)
        if result is None:
            log.write(Text.from_markup("[yellow]Stuck — no more steps available.[/]"))
            self._stop_auto()
            return
        self._step_count += 1
        log.write(
            Text.from_markup(f"[bold]{self._step_count}.[/bold] {format_step(result)}")
        )
        self._refresh_grid()
        if self._puzzle.is_solved:
            log.write(Text.from_markup("[magenta bold]Puzzle solved![/]"))
            self._stop_auto()

    def _stop_auto(self) -> None:
        if self._auto_timer is not None:
            self._auto_timer.stop()
            self._auto_timer = None

    def action_step(self) -> None:
        """Apply one solver step (disabled while auto-solve is running)."""
        if self._auto_timer is None:
            self._apply_step()

    def action_auto_solve(self) -> None:
        """Toggle auto-solve: step every 0.3 s until solved or stuck."""
        if self._auto_timer is not None:
            self._stop_auto()
        elif not self._puzzle.is_solved:
            self._auto_timer = self.set_interval(0.3, self._apply_step)

    async def action_quit(self) -> None:
        """Exit the TUI."""
        self.exit()
