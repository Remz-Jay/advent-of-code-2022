# Advent of Code 2022

*Beware, messy code ahead.*

## Disclaimer
- Code written at 6AM will never be my best :)
- I don't believe in refactoring of single-use code for the sake of showing off
- Python isn't my usual "weapon of choice"

In short: **If you're looking for a good example of how to elegantly solve the AoC puzzles; this is not it.**

It's just how I solved the puzzles with the knowledge I had at the time, and the code is heavily optimized for "speed of development" (= higher score) rather than anything else.

## Structure

- `./main.py` contains a small script to generate a set of new files for a new day of puzzles; it'll ask which day to generate for.
- `./templates/*` contains the Jinja templates `main.py` uses to generate a new Class + Tests.
- `./src/dayX.py` contains the main class for today's puzzles: `DayX`. Class methods `solve1()` and `solve2()` should contain the solutions for both puzzles respectively.
- `./src/input/dayX.txt` contains the personalized puzzle input for today.
- `./test/test_dayX.py` contains minimal tests to verify the puzzle example/explanation.
- `./test/input/dayX.txt` contains the example input data given by the puzzle's explanation.

## Usage

### Creating a new day
```shell
python main.py --day=6
```
### Deleting all scripts for a day
```shell
python main.py --delete=True --day=6
```
### Running day X's solution
```shell
python -m src.dayX
```
### Testing all days
```shell
 python -m unittest discover
```
### Testing day X
```shell
python -m unittest test.test_dayX
```
### Running a single test
```shell
python -m unittest test.test_dayX.TestDayX.test_solve1
```