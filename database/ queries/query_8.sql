#Знайти середній бал, який ставить певний викладач зі своїх предметів.
SELECT
    AVG(g.grade) AS avg_grade
FROM
    grades g
JOIN
    subjects sub ON g.subject_id = sub.subject_id
WHERE
    sub.teacher_id = <certain teacher>;
