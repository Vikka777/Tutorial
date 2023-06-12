import datetime
from datetime import timedelta

def get_birthdays_per_week(users):
    today = datetime.date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    birthdays_this_week = {day: [] for day in weekdays}

    current_year = today.year

    for user, birthday in users.items():
        birthday_date = datetime.datetime.strptime(birthday, "%d.%m.%Y").date().replace(year=current_year)

        if start_of_week <= birthday_date <= end_of_week:
            birthday_weekday = weekdays[birthday_date.weekday()]
        else:
            if birthday_date.weekday() >= 5:
                birthday_weekday = weekdays[0]
            else:
                continue

        birthdays_this_week[birthday_weekday].append(user)

    return birthdays_this_week

users = {
    "Viktoriia": "30.08.1999",
    "Edhar": "14.08.1996",
    "Aleksandr": "31.07.1970",
    "Tatiana": "01.08.1970"
}

birthdays = get_birthdays_per_week(users)
if len(birthdays) > 0:
    print("Birthdays this week:")
    for day, users in birthdays.items():
        if len(users) > 0:
            users_str = ", ".join(users)
            print(f"{day}: {users_str}")
else:
    print("No birthdays this week.")