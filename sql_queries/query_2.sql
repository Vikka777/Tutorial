#Знайти студента із найвищим середнім балом з певного предмета.
subject_id = <specific_subject>  # Replace with the specific subject ID
sql2 = f"""
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
    g.subject_id = {subject_id}
GROUP BY
    s.student_id, s.first_name, s.last_name
ORDER BY
    avg_grade DESC
LIMIT 1;
"""

cursor.execute(sql2)
result2 = cursor.fetchall()