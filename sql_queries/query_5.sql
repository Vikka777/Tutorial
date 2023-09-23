#Знайти, які курси читає певний викладач.
teacher_id = <specific_teacher>  # Replace_with the specific teacher ID
sql5 = f"""
SELECT
    subject_name
FROM
    subjects
WHERE
    teacher_id = {teacher_id};
"""

cursor.execute(sql5)
result5 = cursor.fetchall()