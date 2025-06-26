class Settings:
    DATABASE_PATH = "data/raw/books.db"
    FONTNAME = "Segoe UI"
    TITLE_FONTSIZE = 5.5
    TICK_LABELS_FONTSIZE = 3.5
    PLURAL_WORK_NAME: dict = {
        "Novel": "Novels",
        "Short Story": "Short Stories",
        "Novella": "Novellas",
        "Novelette": "Novelettes",
        "Non-Fiction": "Non-Fiction Books",
        "Graphic Novel": "Graphic Novels",
        "Anthology": "Anthologies",
        "Poetry": "Poems",
    }
