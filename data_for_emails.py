from db_request_handling import get_data_from_database
from water_check_date_math import check_watering_day
from notifications import send_email

# gets info to send in the email
data_for_email = get_data_from_database("""SELECT username, plant_type, watering_frequency, date_last_watered, email
FROM user_credentials as uc
JOIN user_plants as up
ON uc.user_id = up.user_id""")

# turns the tuples into lists so it's more accessible
tuples_into_list = []
for value in data_for_email:
    tuples_into_list.append(list(value))

# calls function CHECK_WATERING_DAY with watering_frequency and date_last_watered from new.
# if needs to be watered - appends all data to send_email_list
send_email_list = []
for i in tuples_into_list:
    if check_watering_day(i[3], i[2]):
        send_email_list.append(i)

# if there is data in list - it calls send_email for each value in send_email_list
if send_email_list:
    for i in send_email_list:
        user_name = i[0]
        plant_name = i[1]
        water_days = i[2]
        date_last_recorded = i[3]
        user_email = i[4]
        send_email(user_name,water_days,date_last_recorded,plant_name,user_email)





