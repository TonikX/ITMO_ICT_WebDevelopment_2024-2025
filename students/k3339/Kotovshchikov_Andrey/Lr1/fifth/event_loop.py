import enum
from select import select
from typing import Generator


class TaskType(enum.StrEnum):
    TO_READ = "to_read"
    TO_WRITE = "to_write"


class EventLoop:
    _tasks: list[Generator]
    _to_read: dict
    _to_write: dict

    def __init__(self, main: Generator) -> None:
        self._tasks = [main]
        self._to_read = dict()
        self._to_write = dict()

    def run(self):
        while any([self._to_read, self._to_write, self._tasks]):
            while not self._tasks:
                ready_to_read, ready_to_write, _ = select(
                    self._to_read,
                    self._to_write,
                    [],
                )

                for socket in ready_to_read:
                    self._tasks.append(self._to_read.pop(socket))

                for socket in ready_to_write:
                    self._tasks.append(self._to_write.pop(socket))

            current_task = self._tasks.pop(0)
            try:
                task_type, socket = next(current_task)
            except StopIteration:
                continue

            if task_type == TaskType.TO_READ:
                self._to_read[socket] = current_task

            elif task_type == TaskType.TO_WRITE:
                self._to_write[socket] = current_task

    def create_task(self, task: Generator):
        self._tasks.append(task)
