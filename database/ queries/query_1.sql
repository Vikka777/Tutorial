#Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT
    s.student_id,
    s.first_name,
    s.last_name,
    AVG(g.grade) AS avg_grade
FROM
    students s
JOIN
    grades g ON s.student_id = g.student_id
GROUP BY
    s.student_id, s.first_name, s.last_name
ORDER BY
    avg_grade DESC
LIMIT 5;
