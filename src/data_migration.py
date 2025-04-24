import sqlite3
import pandas as pd
import re

# Connect to SQLite database
conn = sqlite3.connect('data/raw/books.db')
cursor = conn.cursor()

# Load CSV
csv_file = 'data/raw/books.csv'
df = pd.read_csv(csv_file)

# Ensure required columns are present
required_cols = ['Title', 'Type', 'Author', 'Genre', 'Status', 'Notes',
                 'Pages', 'Year', 'Score', 'Goodreads']
missing = [col for col in required_cols if col not in df.columns]
if missing:
    raise ValueError(f"Missing columns in CSV: {missing}")

# --- Insert AUTHORS ---
all_authors = set()
for authors_str in df['Author'].dropna():
    authors = [a.strip() for a in authors_str.split(',')]
    all_authors.update(authors)

for author_name in all_authors:
    try:
        cursor.execute("SELECT AuthorID FROM AUTHORS WHERE Name = ?",
                       (author_name,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO AUTHORS (Name) VALUES (?)",
                           (author_name,))
            print(f"Inserted author: {author_name}")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting author {author_name}: {e}")
        conn.rollback()

# --- Insert WORKS ---
for index, row in df.iterrows():
    try:
        title = row['Title']
        work_type = row['Type']
        genre = row['Genre']
        year = int(row['Year']) if not pd.isna(row['Year']) else None
        pages = int(row['Pages']) if not pd.isna(row['Pages']) else None
        goodreads = float(row['Goodreads']) \
            if not pd.isna(row['Goodreads']) else None

        # Parse Notes column for series and number in series
        series = None
        number_in_series = None
        notes = row['Notes']
        if isinstance(notes, str):
            match = re.search(r'^(.*?),\s*#(\d+)\.?$', notes.strip())
            if match:
                series = match.group(1).strip()
                number_in_series = int(match.group(2).strip())

        cursor.execute("""
            INSERT INTO WORKS (Name, Type, Genre, PublishedOn,
            PageCount, GoodreadsScore, Series, NumberInSeries)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, work_type, genre, year, pages, goodreads, series,
              number_in_series))
        print(f"Inserted work: {title}")
        conn.commit()

    except Exception as e:
        print(f"Error inserting work at row {index + 1} ({row['Title']}): {e}")
        conn.rollback()

# --- Insert AUTHOR_WORK ---
for index, row in df.iterrows():
    title = row['Title']
    try:
        cursor.execute("SELECT WorkID FROM WORKS WHERE Name = ?", (title,))
        work = cursor.fetchone()
        if work is None:
            raise ValueError(f"Work '{title}' not found.")
        work_id = work[0]

        authors = [a.strip() for a in row['Author'].split(',')]
        for author_name in authors:
            cursor.execute("SELECT AuthorID FROM AUTHORS WHERE Name = ?",
                           (author_name,))
            author = cursor.fetchone()
            if author is None:
                raise ValueError(f"Author '{author_name}' not found.")
            author_id = author[0]

            cursor.execute("INSERT INTO AUTHOR_WORK (AuthorID, WorkID) VALUES (?, ?)", (author_id, work_id))
            print(f"Linked {author_name} with {title}")

        conn.commit()
    except Exception as e:
        print(f"Error linking authors for {title}: {e}")
        conn.rollback()

# --- Insert into READS ---
valid_statuses = {"FINISHED", "IN PROGRESS", "NOT FINISHED"}
for index, row in df.iterrows():
    status = row['Status']
    score = row['Score']
    title = row['Title']

    if status == 'NOT STARTED' or pd.isna(score):
        print(f"Skipping READS for '{title}' — not started or no score.")
        continue

    try:
        if status not in valid_statuses:
            raise ValueError(f"Invalid status '{status}' for '{title}'")

        score = float(score)
        if not (0 <= score <= 10):
            raise ValueError(f"Score out of bounds for '{title}': {score}")

        cursor.execute("SELECT WorkID FROM WORKS WHERE Name = ?", (title,))
        work = cursor.fetchone()
        if work is None:
            raise ValueError(f"Work '{title}' not found.")
        work_id = work[0]

        cursor.execute("""
            INSERT INTO READS (WorkID, Status, Score)
            VALUES (?, ?, ?)
        """, (work_id, status, score))
        print(f"Inserted READS for {title}")
        conn.commit()
    except Exception as e:
        print(f"Error inserting READS for '{title}': {e}")
        conn.rollback()

# Done
conn.close()
print("Migration complete.")
