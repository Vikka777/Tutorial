#Знайти список курсів, які відвідує студент.
student_id = <specific_student>  # Replace_with the specific student ID
sql9 = f"""
SELECT
    sub.subject_name
FROM
    subjects sub
JOIN
    grades g ON sub.subject_id = g.subject_id
WHERE
    g.student_id = {student_id};
"""

cursor.execute(sql9)
result9 = cursor.fetchall()
