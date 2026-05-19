# 2K Random Generator

Python helper that **randomizes NBA 2K23 MyLeague player attributes** by reading `NBA2K23.exe` memory (`pymeow`) using offsets from `PLAYER.json`—speeds up roster experiments.

## What it does

- Randomizes stats, potential, age, and related fields in memory
- Loops while the game process is running

## Why it exists

Manual roster tweaking for MyLeague tests was slow. The script automates randomization for quick iteration.

## Quick start

1. Install `pymeow` and dependencies for your environment.
2. Start NBA 2K23 with MyLeague loaded.
3. Run:

```bash
python 2KRandomGenerator.py
```

## Requirements

- Windows
- Python 3
- `pymeow`
- NBA 2K23 running (`NBA2K23.exe`)

## Project status

Niche personal tool. See commit history.

## License

See repository license file.
