#Знайти середній бал у групах з певного предмета.
subject_id = <specific_subject>  # Replace with the specific subject ID
sql3 = f"""
SELECT
    g.group_name,
    AVG(gr.grade) AS avg_grade
FROM
    groups g
JOIN
    students s ON g.group_id = s.group_id
JOIN
    grades gr ON s.student_id = gr.student_id
WHERE
    gr.subject_id = {subject_id}
GROUP BY
    g.group_name;
"""

cursor.execute(sql3)
result3 = cursor.fetchall()