# turing-machine-solver
A solver for board game: Turing Machine

See [the board game website](http://turingmachine.info)

## Usage

Call `turing-machine-solver.py` with args of validator card numbers.
E.g. The first problem on the rule book should be solved by:
```
python turing-machine-solver.py 4 9 11 14
```
And follow the instruction of the solver. Manually validate each question and input `0`/`1` for answers.
```
...
> (1, 1, 1) A: 0         # <= input 0 here because manually checking (1, 1, 1) with validator A (card 4) does not pass
Solved:
 - hidden: (1, 0, 0, 2)  # <= which criterions each validator checks
 - option: (2, 4, 1)     # <= the answer code
```

## Algorithm

Each validator has a hidden variable to determine which criterion it validates. For $n$ validators, their hidden variables form an $n$-dimensional vector, which we call `hidden`.
The algorithm goes as:
- Find all `hidden`s that can determine at least one code.
- Filter all `hidden`s and select the ones that can determine exactly one code. (By rule: `Only one code respects all the criteria`. Can be disabled by `--skip-filter-unique`.)
- Filter all `hidden`s and select the ones that contain no useless validators. (By rule: `No criterion is superfluous`. Can be disabled by `--skip=filter-useless`.)
- While not solved (more than one `hidden` left):
  - Recursively find all possible (and useful) queries. (A query is less than three questions that share the same proposal.)
  - Find a query with the greatest entropy.
  - Ask user to check each question of that query. Filter `hidden`s again.
  - If a question is not useful anymore, skip that question.
  - If only one `hidden` left, that is the answer. Output corresponding code.

## To Do

- [ ] Update questions within a round
- [ ] Extreme and Nightmare modes
