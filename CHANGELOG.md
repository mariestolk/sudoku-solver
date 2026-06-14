# CHANGELOG


## v0.8.0 (2026-06-14)

### Features

- Implement box/line reduction strategy and corresponding tests
  ([#28](https://github.com/mariestolk/sudoku-solver/pull/28),
  [`c8f68e7`](https://github.com/mariestolk/sudoku-solver/commit/c8f68e70da92923906a5ec5357a99c1170f62688))


## v0.7.0 (2026-06-14)

### Features

- Add functionality to load unsolved puzzles from JSON and save first stuck puzzle
  ([#27](https://github.com/mariestolk/sudoku-solver/pull/27),
  [`c2eebb8`](https://github.com/mariestolk/sudoku-solver/commit/c2eebb8fb853ed0c7ec43fc0b4ee17d5f8f7e598))


## v0.6.0 (2026-06-14)

### Features

- Implement naked quads rule ([#26](https://github.com/mariestolk/sudoku-solver/pull/26),
  [`d5bc8fe`](https://github.com/mariestolk/sudoku-solver/commit/d5bc8fea80b4444b37c555b1a2c1cbd899122c09))


## v0.5.1 (2026-06-14)

### Bug Fixes

- Update iteration rules for naked pairs, triples, and hidden pairs to support row and column units
  ([#25](https://github.com/mariestolk/sudoku-solver/pull/25),
  [`fa0df53`](https://github.com/mariestolk/sudoku-solver/commit/fa0df53537a729b3ef308867efd667fa66a71d76))

### Documentation

- Update evaluator statistics description in README
  ([#23](https://github.com/mariestolk/sudoku-solver/pull/23),
  [`0d248cf`](https://github.com/mariestolk/sudoku-solver/commit/0d248cf53846c52ff861735302c467f53d5c5887))


## v0.5.0 (2026-05-30)

### Chores

- Add environment handling for API token authentication
  ([#19](https://github.com/mariestolk/sudoku-solver/pull/19),
  [`86ba0b1`](https://github.com/mariestolk/sudoku-solver/commit/86ba0b17c3b07b50f9a1906a94e63e65b7a6a902))

### Features

- Add tui to improve the cli and update sudoku grid
  ([#22](https://github.com/mariestolk/sudoku-solver/pull/22),
  [`c30658d`](https://github.com/mariestolk/sudoku-solver/commit/c30658de21fc238a69f526799de538e6fd1d2bf1))

### Refactoring

- Improve efficiency of solver strategies and data structures
  ([#18](https://github.com/mariestolk/sudoku-solver/pull/18),
  [`cb3f085`](https://github.com/mariestolk/sudoku-solver/commit/cb3f0857454c46ea3633913ee2c904c3920344fe))

- Remove unused candidate formatting functions from renderer
  ([#21](https://github.com/mariestolk/sudoku-solver/pull/21),
  [`426e86b`](https://github.com/mariestolk/sudoku-solver/commit/426e86bf9cc4bf4f24e42bfa947595627c8f265e))

- Remove unused set_value method from Puzzle class
  ([#20](https://github.com/mariestolk/sudoku-solver/pull/20),
  [`2657eb2`](https://github.com/mariestolk/sudoku-solver/commit/2657eb2ba66bebb64c6b8a5d99ebe679a6edcee6))


## v0.4.1 (2026-05-29)

### Bug Fixes

- Correct naked triples to detect mixed-candidate patterns
  ([#17](https://github.com/mariestolk/sudoku-solver/pull/17),
  [`b7eb63f`](https://github.com/mariestolk/sudoku-solver/commit/b7eb63f604f67ecdb5db61058159deb8ea853523))

### Refactoring

- Move PuzzleData to puzzle.py and loader to top-level package
  ([#16](https://github.com/mariestolk/sudoku-solver/pull/16),
  [`35a224f`](https://github.com/mariestolk/sudoku-solver/commit/35a224ffa504fb60f82fe1b69199ba3f0e84a72e))


## v0.4.0 (2026-05-29)

### Bug Fixes

- Add python-semantic-release build command
  ([`4330df2`](https://github.com/mariestolk/sudoku-solver/commit/4330df2476f2defa9eec887bd15e99af52c7080a))

fix: add python-semantic-release build command

- Add token to checkout step in release workflow
  ([#15](https://github.com/mariestolk/sudoku-solver/pull/15),
  [`1840340`](https://github.com/mariestolk/sudoku-solver/commit/1840340d1e614d0e26de217f769a01cdbcab7861))

- Remove push trigger from lint and test workflows
  ([`cca6084`](https://github.com/mariestolk/sudoku-solver/commit/cca6084362d18efc5ff36e12b71a89054820d9ef))

- Semantic release build error
  ([`c246acc`](https://github.com/mariestolk/sudoku-solver/commit/c246acc1b2245e49213b4ddde3bc65132e54bc54))

fix: semantic release update

- Semantic release build error ([#11](https://github.com/mariestolk/sudoku-solver/pull/11),
  [`2099454`](https://github.com/mariestolk/sudoku-solver/commit/20994545721dd7b855c4cf2cff797485a7103afb))

- Update optional dependencies and build command in pyproject.toml
  ([`fc03de5`](https://github.com/mariestolk/sudoku-solver/commit/fc03de5a9a9e57072c55a4dd11bd7e497ed20c82))

- Update type hint for _grid_to_str function to use Sequence
  ([`beb44ce`](https://github.com/mariestolk/sudoku-solver/commit/beb44cec1c531266cd85aad931d40a3f5006b58d))

- Update version to 0.3.0 and add optional dependency for build
  ([`66be818`](https://github.com/mariestolk/sudoku-solver/commit/66be818f07198b27542f50e8465dbe6a5a341bf2))

### Chores

- Add release workflow and update version to 0.3.0
  ([`33f4708`](https://github.com/mariestolk/sudoku-solver/commit/33f47082c11375651ba6b64a88446931a89b61bf))

chore: add release workflow and update version to 0.3.0

- Add release workflow and update version to 0.3.0
  ([`54f8382`](https://github.com/mariestolk/sudoku-solver/commit/54f83821e1f514f809a6f7375b38d63148b51980))

- Remove unnecessary setup-uv step and update build command
  ([#12](https://github.com/mariestolk/sudoku-solver/pull/12),
  [`8167865`](https://github.com/mariestolk/sudoku-solver/commit/8167865fcc15e5d10f6866849752893f49a8d156))

- Update release workflow to remove setup-uv step and adjust build
  ([#13](https://github.com/mariestolk/sudoku-solver/pull/13),
  [`08d3d59`](https://github.com/mariestolk/sudoku-solver/commit/08d3d59868c23c0eb14bf8004aedd036356d128c))

- Update release workflow to remove unnecessary sync step and specify package name for uv lock
  ([`eedb5d1`](https://github.com/mariestolk/sudoku-solver/commit/eedb5d10d99d0aabe248da55465d9dcca2ddfd1e))

- Update workflows to trigger only on pull requests and adjust optional dependencies in
  pyproject.toml and uv.lock
  ([`1e81ec1`](https://github.com/mariestolk/sudoku-solver/commit/1e81ec1f687fea936f541e557aeee72a453e252d))

### Documentation

- Add known limitations section regarding hidden pairs in rule statistics
  ([`0713c09`](https://github.com/mariestolk/sudoku-solver/commit/0713c092b5a2b76e6a39ceaee0dcb355788f0945))

### Features

- Add Docker support and sudoku-download CLI command
  ([#14](https://github.com/mariestolk/sudoku-solver/pull/14),
  [`1be4ce1`](https://github.com/mariestolk/sudoku-solver/commit/1be4ce1ce603da8916a1571a7853f44a107aab97))

- Add evaluator for batch processing of Kaggle puzzles and report statistics
  ([`f84c724`](https://github.com/mariestolk/sudoku-solver/commit/f84c724e65e74062de5de8eca9d49b98db91ee15))

- Add is_valid_solution method and corresponding unit tests
  ([`bab5532`](https://github.com/mariestolk/sudoku-solver/commit/bab55326b341d8d26d82ab99d322657caba00c88))

- Add pytest configuration and new tests for chaos and CSV puzzles
  ([`d241597`](https://github.com/mariestolk/sudoku-solver/commit/d2415974e9a19c8626521fc67c2d69e1773b450d))


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
