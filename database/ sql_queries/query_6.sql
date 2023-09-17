#Знайти список студентів у певній групі.
group_id = <specific_group>  #Replace_with the specific group ID
sql6 = f"""
SELECT
    first_name,
    last_name
FROM
    students
WHERE
    group_id = {group_id};
"""

cursor.execute(sql6)
result6 = cursor.fetchall()