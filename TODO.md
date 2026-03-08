# Database

* [x] Add a next table called `NEXT_READS` and remove the `NEXT` option in the `READS` table. `READS` should only contains finished and unfinished books, not books I want to read soon.

# Codebase

* [x] Add `StartedOn`, `FinishedOn` and `Status` to `V_READ_HISTORY`.
* [x] Change shell in Makefile to Bash.
* [x] Update `README.md`.
* [x] `Queries` class?

# Analysis

* [ ] Replicate some figures from the statistics section of The StoryGraph.
    * [ ] Most read authors by numbers of pages read.
    * [ ] Number of works and number of pages read by year (or month).
    * [ ] Score distributions (for different authors and genres).
    * [ ] Publication year be read date.
* [x] Compare genres - Same figure as `top_rated_most_read` but for each genre.
* [x] Update figure styles.
* [x] Create `data/results/recent_reads.csv`.
* [x] Create `data/results/top_authors.csv`.