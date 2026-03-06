SELECT
    A.Name                AS AuthorName,
    A.AuthorID            AS AuthorID,
    W.Name                AS WorkName,
    W.WorkType            AS WorkType,
    W.Series              AS Series,
    W.NumberInSeries      AS NumberInSeries,
    W.PublishedOn         AS PublishedOn,
    W.Genre               AS Genre,
    W.PageCount           AS PageCount,
    R.Score               AS ReadScore,
    W.GoodreadsScore      AS GoodreadsScore,
    W.WorkID              AS WorkID,
    R.StartDate           AS StartDate,
    R.FinishDate          AS FinishDate,
    R.Status              AS ReadStatus
FROM WORKS W
LEFT JOIN READS R
    ON R.WorkID = W.WorkID
JOIN AUTHOR_WORK AW
    ON W.WorkID = AW.WorkID
JOIN AUTHORS A
    ON AW.AuthorID = A.AuthorID
WHERE A.Name = ?
ORDER BY A.Name, W.Name, R.StartDate;