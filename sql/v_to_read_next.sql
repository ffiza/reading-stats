CREATE VIEW V_TO_READ_NEXT AS
SELECT
    A.Name                AS AuthorName,
    W.Name                AS WorkName,
    W.WorkType            AS WorkType,
    W.Series              AS Series,
    W.NumberInSeries      AS NumberInSeries,
    W.GoodreadsScore      AS GoodreadsScore,
    R.Notes               AS Notes
FROM READS R
JOIN WORKS W
    ON R.WorkID = W.WorkID
JOIN AUTHOR_WORK AW
    ON W.WorkID = AW.WorkID
JOIN AUTHORS A
    ON AW.AuthorID = A.AuthorID
WHERE R.Status = 'NEXT';