import json
from pathlib import Path

from task_manager import add_task, load_tasks, save_tasks


def test_add_task_creates_pending_task():
    tasks = []
    task = add_task(tasks, "Study Python", "2026-11-20")
    assert task["id"] == 1
    assert task["title"] == "Study Python"
    assert task["status"] == "pending"
    assert task["due"] == "2026-11-20"


def test_save_and_load_tasks(tmp_path):
    file_path = tmp_path / "data" / "tasks.json"
    tasks = [{"id": 1, "title": "Read", "status": "pending", "due": None}]
    save_tasks(tasks, file_path)
    assert load_tasks(file_path) == tasks


def test_missing_file_returns_empty_list(tmp_path):
    assert load_tasks(tmp_path / "missing.json") == []
