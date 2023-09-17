#Знайти середній бал на потоці (по всій таблиці оцінок).
sql4 = """
SELECT
    AVG(grade) AS avg_grade
FROM
    grades;
"""

cursor.execute(sql4)
result4 = cursor.fetchall()