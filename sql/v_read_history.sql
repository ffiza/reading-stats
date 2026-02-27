CREATE VIEW V_READ_HISTORY AS
SELECT
    A.Name                AS AuthorName,
    W.Name                AS WorkName,
    W.WorkType            AS WorkType,
    W.Series              AS Series,
    W.NumberInSeries      AS NumberInSeries,
    R.Score               AS ReadScore,
    W.GoodreadsScore      AS GoodreadsScore
FROM READS R
JOIN WORKS W
    ON R.WorkID = W.WorkID
JOIN AUTHOR_WORK AW
    ON W.WorkID = AW.WorkID
JOIN AUTHORS A
    ON AW.AuthorID = A.AuthorID;