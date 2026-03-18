import tomllib
from pathlib import Path

_ROOT = Path(__file__).parent.parent

with open(_ROOT / "config.toml", "rb") as f:
    _cfg = tomllib.load(f)


def _path(value: str) -> Path:
    return _ROOT / value


db_path = _path(_cfg["database"]["file_path"])
authors_data_file = _path(_cfg["authors"]["data_output_file"])
authors_fig_file = _path(_cfg["authors"]["fig_output_file"])
works_data_file = _path(_cfg["works"]["data_output_file"])
works_fig_file = _path(_cfg["works"]["fig_output_file"])
read_history_file = _path(_cfg["read_history"]["data_file"])
recent_reads_file = _path(_cfg["read_history"]["recent_reads_file"])
next_reads_file = _path(_cfg["next_reads"]["output_file"])
genres_data_file = _path(_cfg["genres"]["data_output_file"])
genres_fig_file = _path(_cfg["genres"]["fig_output_file"])
sql_author_bibliography = _path(_cfg["author_bibliography"]["query_path"])
author_biblio_output_dir = _path(_cfg["author_bibliography"]["output_dir"])
sql_read_history = _path(_cfg["read_history"]["query_path"])
sql_next_reads = _path(_cfg["next_reads"]["query_path"])
