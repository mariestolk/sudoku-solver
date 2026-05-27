# CHANGELOG


## v0.3.0 (2026-05-27)

### Bug Fixes

- Add type hint for candidates parameter in set_candidates method
  ([`44a140b`](https://github.com/mariestolk/sudoku-solver/commit/44a140b97f919c298880a4db2db4b1fd96345a9b))

### Chores

- Update .gitignore to include cache files
  ([`4a24c2a`](https://github.com/mariestolk/sudoku-solver/commit/4a24c2a8e768447f6bbad7dcb39c283eafb84373))

### Features

- Add unit tests for various Sudoku strategies and implement CI workflows
  ([`57753e2`](https://github.com/mariestolk/sudoku-solver/commit/57753e2c3850a0967c0abc6ae1101d4272c3356e))

### Refactoring

- Format combination loop for better readability in reduce_hidden_pair function
  ([`4d40eed`](https://github.com/mariestolk/sudoku-solver/commit/4d40eedac01ff362d9bfdc01409732dbd1a21878))

- Split Puzzle class into strategies, renderer, and lean solver
  ([`71caf52`](https://github.com/mariestolk/sudoku-solver/commit/71caf528491dfef098a6224c8740bf46f7b2f927))

refactor: split Puzzle class into strategies, renderer, and lean solver


## v0.2.0 (2026-05-27)

### Features

- Included type hints and mypy
  ([`8741821`](https://github.com/mariestolk/sudoku-solver/commit/8741821712b76ac1e81f5a0848c6c3708890aa8d))

feat: included type hints and mypy

### Refactoring

- Restructure project and add interactive CLI for Sudoku solving
  ([`c3128d5`](https://github.com/mariestolk/sudoku-solver/commit/c3128d5aad45220c2cf2f7596c7a88ae0c334131))


## v0.1.0 (2026-05-26)

### Chores

- Initial commit
  ([`a01cd90`](https://github.com/mariestolk/sudoku-solver/commit/a01cd90c2ffed35b8fc8b731ac6665af7755f5ae))

Constraint-propagation sudoku solver with support for standard and chaos sudoku (irregular groups).
  Includes interactive CLI, Kaggle dataset loader, semantic versioning, and ruff-based CI pipeline.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
