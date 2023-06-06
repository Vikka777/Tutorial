import datetime
from datetime import datetime, timedelta

def get_birthdays_per_week(users):
    today = datetime.now().date() # Monday is the first day of the week
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    birthdays_this_week = {day: [] for day in weekdays}

    for user, birthday in users.items():
        birthday_date = datetime.strptime(birthday, "%d.%m.%Y").date()

        if start_of_week <= birthday_date <= end_of_week:
            birthday_weekday = weekdays[birthday_date.weekday()]
        else:
            # If the birthday falls on a weekend, congratulate on Monday
            if birthday_date.weekday() >= 5:
                birthday_weekday = weekdays[0]
            else:
                continue  # Skip users whose birthdays are outside the current week

        birthdays_this_week[birthday_weekday].append(user)

    if len(birthdays_this_week) > 0:
        print("Birthdays this week:")
        for day, users in birthdays_this_week.items():
            if len(users) > 0:
                users_str = ", ".join(users)
                print(f"{day}: {users_str}")
    else:
        print("No birthdays this week.")

# Test dictionary with names and birthdays
users = {
    "Viktoriia": "30.08.1999",
    "Edhar": "14.08.1996",
    "aleksandr": "31.07.1970",
    "Tatiana": "01.08.1979"
}

get_birthdays_per_week(users)