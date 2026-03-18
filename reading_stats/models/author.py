from dataclasses import dataclass


@dataclass
class Author:
    author_id: int
    name: str
    country: str | None
    birth_date: str | None
    death_date: str | None
