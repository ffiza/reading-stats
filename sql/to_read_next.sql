SELECT
    A.Name                AS AuthorName,
    W.Name                AS WorkName,
    W.WorkType            AS WorkType,
    W.Series              AS Series,
    W.NumberInSeries      AS NumberInSeries,
    W.GoodreadsScore      AS GoodreadsScore,
    W.WorkID              AS WorkID
FROM NEXT_READS NR
JOIN WORKS W
    ON NR.WorkID = W.WorkID
JOIN AUTHOR_WORK AW
    ON W.WorkID = AW.WorkID
JOIN AUTHORS A
    ON AW.AuthorID = A.AuthorID;