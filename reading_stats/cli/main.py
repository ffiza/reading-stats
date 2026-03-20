import typer
from reading_stats.reports import (
    authors_scatter,
    genres_scatter,
    works_scatter,
    author_bibliography,
    next_reads,
)

app = typer.Typer(help="Reading stats report generator.")


@app.command()
def authors():
    authors_scatter.run()


@app.command()
def genres():
    genres_scatter.run()


@app.command()
def works():
    works_scatter.run()


@app.command()
def bibliography(
    author: str = typer.Option(
        ...,
        help="Author name.",
        ),
    table: bool = typer.Option(
        False,
        help="Export markdown table.",
        ),
        ):
    author_bibliography.run(author)
    if table:
        author_bibliography.run_table(author)


@app.command()
def next_reads_report():
    next_reads.run()


@app.command()
def all():
    authors_scatter.run()
    genres_scatter.run()
    works_scatter.run()
    next_reads.run()
    author_bibliography.run("Stephen King")
    author_bibliography.run_table("Stephen King")


if __name__ == "__main__":
    app()
