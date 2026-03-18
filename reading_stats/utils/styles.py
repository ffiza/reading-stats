from reading_stats.utils.colors import Colors


class Styles:
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

    WORK_TYPE_COLOR_MAPPING = {
        "Novel": Colors.BLUE,
        "Short Story": Colors.GREEN,
        "Novella": Colors.ORANGE,
        "Novelette": Colors.PURPLE,
    }
    WORK_TYPE_SYMBOLS = {
        "Novel": "o",
        "Short Story": "s",
        "Novella": "^",
        "Novelette": "D",
    }

    GENRE_COLOR_MAPPING = {
        "Fiction: Fantasy": Colors.BLUE,
        "Fiction: Horror": Colors.GREEN,
        "Fiction: Science Fiction": Colors.ORANGE,
        "Fiction: Historical": Colors.RED,
        "Non-Fiction": Colors.PURPLE,
    }
    GENRE_SYMBOLS = {
        "Fiction: Fantasy": "o",
        "Fiction: Horror": "s",
        "Fiction: Science Fiction": "^",
        "Fiction: Historical": "v",
        "Non-Fiction": "D",
    }
