from pathlib import Path
import pandas as pd
from reading_stats.utils.paths import ensure_dir


def to_markdown(df: pd.DataFrame, output_path: Path) -> None:
    ensure_dir(output_path)
    output_path.write_text(df.to_markdown(index=False), encoding="utf-8")
