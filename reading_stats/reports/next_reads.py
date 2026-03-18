from reading_stats import config
from reading_stats.charts.table import to_markdown
from reading_stats.services.next_reads import get_next_reads_for_table


def run() -> None:
    df = get_next_reads_for_table()
    to_markdown(df, config.next_reads_file)


if __name__ == "__main__":
    run()
