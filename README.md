# CLI Task Manager

A command-line task manager built with Python's `argparse`. Tasks are stored in a
JSON file, so they remain available after the program exits.

## Requirements

- Python 3.8 or newer
- `pytest` to run the tests

## Installation

No external package is required to use the task manager.

1. Download or clone this project.
2. Open a terminal in the project folder.
3. (Optional) Install pytest for tests:

```bash
python3 -m pip install pytest
```

## Usage

Run commands from the project folder. By default, tasks are stored at
`~/.cli-task-manager/tasks.json`.

Add a task:

```bash
python3 task_manager.py add "Complete internship task" --due 2026-11-20
```

List all tasks:

```bash
python3 task_manager.py list
```

Mark a task as completed:

```bash
python3 task_manager.py done 1
```

Filter by status:

```bash
python3 task_manager.py filter --status pending
```

Filter by due date (on or before the date):

```bash
python3 task_manager.py filter --due-before 2026-11-30
```

Combine filters:

```bash
python3 task_manager.py filter --status pending --due-before 2026-11-30
```

Delete a task:

```bash
python3 task_manager.py delete 1
```

Use a custom JSON file (place `--file` before the subcommand):

```bash
python3 task_manager.py --file ./tasks.json add "Practice DSA"
python3 task_manager.py --file ./tasks.json list
```

## Tests

Run at least three tests with pytest:

```bash
python3 -m pytest -v
```

The test suite covers adding a task, saving/loading JSON data, and starting
with an empty list when the storage file is missing.
