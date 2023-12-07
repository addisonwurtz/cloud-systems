import requests
from datetime import date, timedelta, datetime, timezone


def get_due_date(orbit):
    """
    :param orbit: contact freqency (daily, weekly, etc.)
    :return: formatted datetime string representing task due date
    """
    if orbit == "daily":
        delta = timedelta(days=1)
    elif orbit == "weekly":
        delta = timedelta(weeks=1)
    elif orbit == "monthly":
        delta = timedelta(days=30)
    elif orbit == "quarterly":
        delta = timedelta(weeks=12)
    elif orbit == "semi_annually":
        delta = timedelta(weeks=24)
    elif orbit == "annually":
        delta = timedelta(weeks=56)
    else:
        delta = timedelta(days=0)

    due_date = datetime.now(timezone.utc).astimezone() + delta
    return due_date.isoformat()


def conversation_starter(first_name, orbit):
    """
    :param first_name: Contacts name
    :param orbit: contact frequency
    :return: a string containing a random fact about dogs
    """
    response = requests.get('https://dog-api.kinduff.com/api/facts').json()
    return response['facts'][0]


def get_task_json(first_name, last_name, orbit):
    """
    :param first_name: contact first name
    :param last_name: contact last name
    :param orbit: contact frequency
    :return: json object for task creation post request
    """
    # Build task fields from contact info
    title = str(first_name) + ' ' + str(last_name)
    message = conversation_starter(first_name, orbit)
    due_date = get_due_date(orbit)
    # Create json request body
    task_info = {
        "title": f"{title}",
        "due": f"{due_date}",
        "notes": f"{message}"
    }
    return task_info
