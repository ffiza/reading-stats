import pandas as pd

from reading_stats import config
from reading_stats.db.connection import get_connection


def _load_sql(path) -> str:
    return path.read_text(encoding="utf-8")


def get_read_history() -> pd.DataFrame:
    sql = _load_sql(config.sql_read_history)
    return pd.read_sql(sql, get_connection(config.db_path))


def get_next_reads() -> pd.DataFrame:
    sql = _load_sql(config.sql_next_reads)
    return pd.read_sql(sql, get_connection(config.db_path))


def get_author_bibliography(author: str) -> pd.DataFrame:
    sql = _load_sql(config.sql_author_bibliography)
    return pd.read_sql(sql, get_connection(config.db_path), params=(author,))
