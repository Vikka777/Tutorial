#Знайти оцінки студентів в окремій групі з певного предмета.
SELECT
    s.first_name,
    s.last_name,
    g.grade
FROM
    students s
JOIN
    grades g ON s.student_id = g.student_id
WHERE
    s.group_id = <certain group>
    AND g.subject_id = <certain_subject>;
