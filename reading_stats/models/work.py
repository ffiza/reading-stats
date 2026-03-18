from dataclasses import dataclass


@dataclass
class Work:
    work_id: int
    name: str
    published_on: int | None
    work_type: str
    genre: str | None
    series: str | None
    number_in_series: float | None
    page_count: int | None
    goodreads_score: float | None
    notes: str | None
