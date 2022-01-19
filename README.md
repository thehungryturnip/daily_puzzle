# Daily Puzzle

Solves [Daily
Puzzle](https://smile.amazon.com/Calendar-Different-Difficult-Christmas-Birthday/dp/B09MRM4GTW)
using depth-first-search. Run `./daily_puzzle.py -h` for more information.

This repo also uses Actions to generate the daily solution at 00:00 UTC-5.
Generated solutions can be found
[here](https://github.com/thehungryturnip/daily_puzzle/blob/main/solutions.md).

## Notes
- Use `argparse.ArgumentParser` to interact with CLI arguments
- Use `sqlite3` to store known solutions
