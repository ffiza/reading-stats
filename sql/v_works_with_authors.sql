CREATE VIEW V_WORKS_WITH_AUTHORS AS
SELECT
    W.WorkID,
    W.Name               AS WorkName,
    W.WorkType,
    W.Series,
    W.NumberInSeries,
    W.PublishedOn,
    W.Genre,
    W.PageCount,
    W.GoodreadsScore,
    A.AuthorID,
    A.Name               AS AuthorName
FROM WORKS W
JOIN AUTHOR_WORK AW
    ON W.WorkID = AW.WorkID
JOIN AUTHORS A
    ON AW.AuthorID = A.AuthorID;