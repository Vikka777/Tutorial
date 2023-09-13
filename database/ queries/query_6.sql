#Знайти список студентів у певній групі.
SELECT
    first_name,
    last_name
FROM
    students
WHERE
    group_id = <certain group>;
