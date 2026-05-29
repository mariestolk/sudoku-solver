"""Download the Kaggle sudoku dataset to a target directory."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from rich.console import Console

DATASET_REF = "rohanrao/sudoku"
DEFAULT_OUTPUT_DIR = Path("data")


def _check_credentials() -> None:
    """Raise SystemExit with a Rich error if Kaggle credentials are absent."""
    has_token = bool(os.environ.get("KAGGLE_API_TOKEN"))
    has_legacy = bool(
        os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY")
    )
    config_dir = Path(os.environ.get("KAGGLE_CONFIG_DIR", "~/.kaggle")).expanduser()
    has_json = (config_dir / "kaggle.json").exists() or (
        config_dir / "access_token"
    ).exists()
    if not has_token and not has_legacy and not has_json:
        console = Console(stderr=True)
        console.print(
            "[bold red]Kaggle credentials not found.[/bold red]\n\n"
            "Set the [cyan]KAGGLE_API_TOKEN[/cyan] environment variable,\n"
            "or place your token in [cyan]~/.kaggle/access_token[/cyan].\n\n"
            "Get your API token at: https://www.kaggle.com/settings"
        )
        raise SystemExit(1)


def download_dataset(output_dir: Path, *, force: bool = False) -> None:
    """Download the rohanrao/sudoku Kaggle dataset to output_dir.

    Skips the download if sudoku.csv already exists unless force is True.
    """
    from kaggle.api.kaggle_api_extended import KaggleApi
    from requests.exceptions import ConnectionError as RequestsConnectionError
    from requests.exceptions import HTTPError

    csv_path = output_dir / "sudoku.csv"
    console = Console()

    if csv_path.exists() and not force:
        console.print(
            f"[green]sudoku.csv already exists:[/green] [cyan]{csv_path}[/cyan]. "
            "Use [bold]--force[/bold] to re-download."
        )
        return

    _check_credentials()
    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(
        f"Downloading [cyan]{DATASET_REF}[/cyan] to [cyan]{output_dir}[/cyan]..."
    )
    api = KaggleApi()
    api.authenticate()
    try:
        api.dataset_download_files(DATASET_REF, path=str(output_dir), unzip=True)
    except HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        err = Console(stderr=True)
        if status in (401, 403):
            err.print(
                f"[bold red]Authentication failed (HTTP {status}).[/bold red] "
                "Check your credentials."
            )
        else:
            err.print(f"[bold red]Download failed (HTTP {status}):[/bold red] {exc}")
        raise SystemExit(1) from exc
    except RequestsConnectionError as exc:
        Console(stderr=True).print(f"[bold red]Network error:[/bold red] {exc}")
        raise SystemExit(1) from exc

    console.print(f"[green]Done.[/green] Dataset saved to [cyan]{csv_path}[/cyan]")


def main() -> None:
    """Entry point for the sudoku-download CLI command."""
    parser = argparse.ArgumentParser(
        description="Download the Kaggle rohanrao/sudoku dataset."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        metavar="DIR",
        help=f"Directory to save sudoku.csv (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download even if sudoku.csv already exists",
    )
    args = parser.parse_args()
    download_dataset(args.output_dir, force=args.force)
