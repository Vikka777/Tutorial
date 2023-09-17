#Знайти оцінки студентів в окремій групі з певного предмета.
group_id = <specific_group>  # Replace_with the specific group ID
subject_id = <specific_subject>  # Replace_with the specific_subject ID
sql7 = f"""
SELECT
    s.first_name,
    s.last_name,
    g.grade
FROM
    students s
JOIN
    grades g ON s.student_id = g.student_id
WHERE
    s.group_id = {group_id}
    AND g.subject_id = {subject_id};
"""

cursor.execute(sql7)
result7 = cursor.fetchall()