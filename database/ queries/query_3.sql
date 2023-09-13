#Знайти середній бал у групах з певного предмета.
SELECT
    g.group_name,
    AVG(grade) AS avg_grade
FROM
    grades gr
JOIN
    students s ON gr.student_id = s.student_id
JOIN
    groups g ON s.group_id = g.group_id
WHERE
    gr.subject_id = <certain_subject>
GROUP BY
    g.group_name;
