<div align="center">
    <h1>Reading Stats</h1>
</div>

This repository explores data related to my personal reading habits. All data is stored in a relational database at `data/raw/books.db`. Scripts for querying, data processing, and plotting are located in the `reading_stats/`.

* [Database](https://github.com/ffiza/reading-stats?tab=readme-ov-file#database)
    * [Graph](https://github.com/ffiza/reading-stats?tab=readme-ov-file#graph)
* [Showcase](https://github.com/ffiza/reading-stats?tab=readme-ov-file#showcase)
* [Genres](https://github.com/ffiza/reading-stats?tab=readme-ov-file#genres)
* [Next Reads](https://github.com/ffiza/reading-stats/blob/main/data/tables/next_reads.md)
* [Stephen King Bibliography](https://github.com/ffiza/reading-stats/blob/main/data/tables/stephen_king.md)

## Database

The database consists of the tables described below. Missing values are represented as `NULL`.

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
    - `WorkType`: The type of work. Possible values are: `Novella`, `Short Story`, `Novel`, `Novelette`, `Non-Fiction`, `Anthology`, `Graphic Novel`, or `Poetry`. Most works are classified based on [The Internet Speculative Fiction Database](https://www.isfdb.org/).
    - `Genre`: The (subjective) genre of the work. For example: `Fiction: Horror: Cosmic`. See below for a complete list of genres.
    - `Series`: The series to which the work belongs.
    - `NumberInSeries`: The order of the work within its series, as a float.
    - `PageCount`: The number of pages in the work.
    - `GoodreadsScore`: The Goodreads score for the work. For short stories or works contained in anthologies or collections, the score is that of the parent work. For example, the short story "What Brings the Void" uses the score of the *Cthulhu's Reign* anthology.
    - `Notes`: Optional notes about this work (e.g., recommendations, tropes, topics).
- `AUTHOR_WORK` links authors and works, and contains only two fields: `AuthorID` and `WorkID`.
- `READS` contains information about each reading instance:
    - `ReadID`: An integer serving as a unique identifier for the read.
    - `WorkID`: The work being read, as in `WORKS`.
    - `StartDate`: The start date of the reading, in `YYYY-MM-DD` format.
    - `FinishDate`: The finish date of the reading, in `YYYY-MM-DD` format.
    - `Score`: The score given to this reading, as a float.
    - `Status`: The current status of the reading. Possible values are `FINISHED`, `NOT FINISHED`, or `IN PROGRESS`.
    - `Notes`: Optional notes about this work (e.g., thoughts).
- `NEXT_READS` contains information about the works I want to read next:
    - `WorkID`: The work being read, as in `WORKS`.

### Graph

```mermaid
erDiagram
    AUTHORS {
        int AuthorID PK
        string Name
        string Country
        date BirthDate
        date DeathDate
    }

    WORKS {
        int WorkID PK
        string Name
        string PublishedOn
        string WorkType
        string Genre
        string Series
        float NumberInSeries
        int PageCount
        float GoodreadsScore
        string Notes
    }

    AUTHOR_WORK {
        int AuthorID FK
        int WorkID FK
    }

    READS {
        int ReadID PK
        int WorkID FK
        date StartDate
        date FinishDate
        float Score
        string Status
        string Notes
    }

    NEXT_READS {
        int WorkID FK
    }

    AUTHORS ||--o{ AUTHOR_WORK : "writes"
    WORKS ||--o{ AUTHOR_WORK : "written by"
    WORKS ||--o{ READS : "read as"
    WORKS ||--o{ NEXT_READS : "queued as"
```

## Showcase

<div align="center">
    <img src="https://github.com/ffiza/reading-stats/blob/main/images/top_rated_most_read.png?raw=true" width="800">
</div>

---

<div align="center">
    <img src="https://github.com/ffiza/reading-stats/blob/main/images/work_score_scatter.png?raw=true" width="800">
</div>

---

<div align="center">
    <img src="https://github.com/ffiza/reading-stats/blob/main/images/genres_scatter.png?raw=true" width="800">
</div>

---

<div align="center">
    <img src="https://github.com/ffiza/reading-stats/blob/main/images/stephen_king_bibliography.png?raw=true" width="800">
</div>

## Genres

- Fiction: Adventure
- Fiction: Contemporary
- Fiction: Crime
- Fiction: Drama
- Fiction: Fantasy
    - Fiction: Fantasy: Epic
    - Fiction: Fantasy: Grimdark
    - Fiction: Fantasy: High
    - Fiction: Fantasy: Historical
    - Fiction: Fantasy: Low
- Fiction: Historical
- Fiction: Horror
    - Fiction: Horror: Cosmic
    - Fiction: Horror: Folk
    - Fiction: Horror: Gothic
- Fiction: Literary
- Fiction: Magic Realism
- Fiction: Mystery
- Fiction: Science Fiction
    - Fiction: Science Fiction: Alternative History
    - Fiction: Science Fiction: Apocalyptic
    - Fiction: Science Fiction: Biopunk
    - Fiction: Science Fiction: Climate
    - Fiction: Science Fiction: Cyberpunk
    - Fiction: Science Fiction: Dystopian
    - Fiction: Science Fiction: Grimdark
    - Fiction: Science Fiction: Hard
    - Fiction: Science Fiction: Horror
    - Fiction: Science Fiction: Space Opera
    - Fiction: Science Fiction: Steampunk
- Fiction: Thriller
- Non-Fiction:
    - Non-Fiction: Biography
    - Non-Fiction: Biology
    - Non-Fiction: Crime
    - Non-Fiction: Games
    - Non-Fiction: History
    - Non-Fiction: Music
    - Non-Fiction: Mythology
    - Non-Fiction: Philosophy
    - Non-Fiction: Politics
    - Non-Fiction: Psychology
    - Non-Fiction: Religion
    - Non-Fiction: Science
    - Non-Fiction: Travel
    - Non-Fiction: Writing
- Play
- Poetry
