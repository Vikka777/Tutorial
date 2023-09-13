#Список курсів, які певному студенту читає певний викладач.
SELECT
    sub.subject_name
FROM
    subjects sub
JOIN
    grades g ON sub.subject_id = g.subject_id
JOIN
    students s ON g.student_id = s.student_id
WHERE
    s.student_id = <certain student>
    AND sub.teacher_id = <certain teacher>;

