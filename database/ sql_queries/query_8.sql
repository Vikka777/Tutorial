#Знайти середній бал, який ставить певний викладач зі своїх предметів.
teacher_id = <specific_teacher>  # Replace_with the specific teacher ID
sql8 = f"""
SELECT
    AVG(g.grade) AS avg_grade
FROM
    grades g
JOIN
    subjects sub ON g.subject_id = sub.subject_id
WHERE
    sub.teacher_id = {teacher_id};
"""

cursor.execute(sql8)
result8 = cursor.fetchall()