#Знайти студента із найвищим середнім балом з певного предмета.
SELECT
    s.student_id,
    s.first_name,
    s.last_name,
    AVG(g.grade) AS avg_grade
FROM
    students s
JOIN
    grades g ON s.student_id = g.student_id
WHERE
    g.subject_id = <certain_subject>
GROUP BY
    s.student_id, s.first_name, s.last_name
ORDER BY
    avg_grade DESC
LIMIT 1;
