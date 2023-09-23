#Список курсів, які певному студенту читає певний викладач.
student_id = <specific_student>  # Replace_with the specific student ID
teacher_id = <specific_teacher>  # Replace_with the specific teacher ID
sql10 = f"""
SELECT
    sub.subject_name
FROM
    subjects sub
JOIN
    grades g ON sub.subject_id = g.subject_id
JOIN
    students s ON g.student_id = s.student_id
WHERE
    s.student_id = {student_id}
    AND sub.teacher_id = {teacher_id};
"""

cursor.execute(sql10)
result10 = cursor.fetchall()