<div align="center">
    <h1>Reading Stats</h1>
</div>

This repository explores data related to my personal reading habits. All data is stored in a relational database at `data/raw/books.db`. Scripts for querying, data processing, and plotting are located in the `src/` directory.

## Database

The database consists of four tables, as described below. Missing values are represented as `NULL`.

- `AUTHORS` contains information about individual authors:
    - `AuthorID`: An integer serving as a unique identifier for the author.
    - `Name`: The author's name as a string.
    - `Country`: The country of birth, coded using the [ISO 3166-1 alpha-3 standard](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3).
    - `BirthDate`: The date of birth in `YYYY-MM-DD` format. If only the year is known (e.g., 1954), the month and day are set to `01`, resulting in `1954-01-01`.
    - `DeathDate`: The date of death in `YYYY-MM-DD` format. If only the year is known (e.g., 1954), the month and day are set to `01`, resulting in `1954-01-01`.
- `WORKS` contains information about individual works:
    - `WorkID`: An integer serving as a unique identifier for the work.
    - `Name`: The name of the work as a string.
    - `PublishedOn`: The year of publication in `YYYY` format.
    - `Type`: The type of work. Possible values include `Novella`, `Short Story`, `Novel`, `Novelette`, `Non-Fiction`, `Anthology`, `Graphic Novel`, or `Poetry`. Most works are classified based on [The Internet Speculative Fiction Database](https://www.isfdb.org/).
    - `Genre`: The (subjective) genre of the work. For example: `Fiction: Horror: Cosmic`.
    - `Series`: The series to which the work belongs.
    - `NumberInSeries`: The order of the work within its series, as a float.
    - `PageCount`: The number of pages in the work.
    - `GoodreadsScore`: The Goodreads score for the work. For short stories or works contained in anthologies or collections, the score is that of the parent work. For example, the short story "What Brings the Void" uses the score of the *Cthulhu's Reign* anthology.
- `AUTHOR_WORK` links authors and works, and contains only two fields: `AuthorID` and `WorkID`.
- `READS` contains information about each reading instance:
    - `WorkID`: The work being read, as in `WORKS`.
    - `StartDate`: The start date of the reading, in `YYYY-MM-DD` format.
    - `FinishDate`: The finish date of the reading, in `YYYY-MM-DD` format.
    - `Score`: The score given to this reading, as a float.
    - `Status`: The current status of the reading. Possible values are `FINISHED`, `NOT FINISHED`, or `IN PROGRESS`.

## Showcase

<div align="center">
    <img src="https://github.com/ffiza/reading-stats/blob/main/images/most_read_authors.png?raw=true" width="650">
</div>

---

<div align="center">
    <img src="https://github.com/ffiza/reading-stats/blob/main/images/authors_scores.png?raw=true" width="650">
</div>

---

<div align="center">
    <img src="https://github.com/ffiza/reading-stats/blob/main/images/highest_rated_novels.png?raw=true" width="650">
</div>

---

<div align="center">
    <img src="https://github.com/ffiza/reading-stats/blob/main/images/highest_rated_short_stories.png?raw=true" width="650">
</div>

---

<div align="center">
    <img src="https://github.com/ffiza/reading-stats/blob/main/images/highest_rated_novelettes.png?raw=true" width="650">
</div>