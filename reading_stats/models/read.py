from dataclasses import dataclass


@dataclass
class Read:
    read_id: int
    work_id: int
    start_date: str | None
    finish_date: str | None
    score: int | None
    status: str
    notes: str | None
