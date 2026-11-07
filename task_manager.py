"""A small command-line task manager."""

import argparse
import json
from datetime import date
from pathlib import Path

DEFAULT_FILE = Path.home() / ".cli-task-manager" / "tasks.json"


def load_tasks(path):
    """Load tasks from JSON; return an empty list if the file is missing."""
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("Task data must be a JSON list.")
        return data
    except FileNotFoundError:
        return []


def save_tasks(tasks, path):
    """Save tasks, creating the parent directory when needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def add_task(tasks, title, due=None):
    task_id = max((task["id"] for task in tasks), default=0) + 1
    task = {
        "id": task_id,
        "title": title,
        "status": "pending",
        "due": due,
    }
    tasks.append(task)
    return task


def build_parser():
    parser = argparse.ArgumentParser(
        prog="taskman",
        description="Manage tasks from your command line."
    )
    parser.add_argument(
        "--file", default=str(DEFAULT_FILE),
        help=f"JSON storage file (default: {DEFAULT_FILE})"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="Add a task")
    add.add_argument("title", help="Task description")
    add.add_argument("--due", help="Due date in YYYY-MM-DD format")

    subparsers.add_parser("list", help="List tasks")

    done = subparsers.add_parser("done", help="Mark a task as completed")
    done.add_argument("id", type=int, help="Task ID")

    delete = subparsers.add_parser("delete", help="Delete a task")
    delete.add_argument("id", type=int, help="Task ID")

    listing = subparsers.add_parser("filter", help="Filter tasks")
    listing.add_argument(
        "--status", choices=["pending", "completed"],
        help="Show tasks with this status"
    )
    listing.add_argument(
        "--due-before", metavar="YYYY-MM-DD",
        help="Show tasks due on or before this date"
    )

    return parser


def valid_date(value):
    try:
        date.fromisoformat(value)
        return value
    except ValueError:
        raise argparse.ArgumentTypeError("Date must be in YYYY-MM-DD format.")


def run(args):
    path = Path(args.file)
    tasks = load_tasks(path)

    if args.command == "add":
        if args.due:
            args.due = valid_date(args.due)
        task = add_task(tasks, args.title, args.due)
        save_tasks(tasks, path)
        print(f'Added task #{task["id"]}: {task["title"]}')

    elif args.command == "list":
        print_tasks(tasks)

    elif args.command == "done":
        task = next((item for item in tasks if item["id"] == args.id), None)
        if task is None:
            print(f"Task #{args.id} not found.")
            return 1
        task["status"] = "completed"
        save_tasks(tasks, path)
        print(f"Completed task #{args.id}.")

    elif args.command == "delete":
        updated = [item for item in tasks if item["id"] != args.id]
        if len(updated) == len(tasks):
            print(f"Task #{args.id} not found.")
            return 1
        save_tasks(updated, path)
        print(f"Deleted task #{args.id}.")

    elif args.command == "filter":
        if args.due_before:
            args.due_before = valid_date(args.due_before)
        filtered = tasks
        if args.status:
            filtered = [t for t in filtered if t["status"] == args.status]
        if args.due_before:
            filtered = [
                t for t in filtered
                if t.get("due") and t["due"] <= args.due_before
            ]
        print_tasks(filtered)

    return 0


def print_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        due = task.get("due") or "No due date"
        print(
            f'#{task["id"]} [{task["status"]}] {task["title"]} '
            f'(Due: {due})'
        )


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        raise SystemExit(run(args))
    except argparse.ArgumentTypeError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
