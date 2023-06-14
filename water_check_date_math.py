from datetime import datetime, timedelta


def check_watering_day(date_str, water_frequency):
    # get current date
    current_date = datetime.now().date()
    # convert str into date time
    date_last_watered_str = date_str
    date_last_watered = datetime.strptime(date_last_watered_str, '%m-%d-%Y').date()

    # subtracts today's date from date last watered
    days_since_last_watered = (current_date - date_last_watered).days
    watering_frequency = water_frequency

    # if it needs to be watered - function will return True for call in data_for_emails.py
    if days_since_last_watered >= watering_frequency:
        return True


