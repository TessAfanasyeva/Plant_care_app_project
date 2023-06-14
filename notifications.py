"""
Module: email_handling

This module provides functions for sending reminder emails to users regarding watering their plants.

Dependencies:
- smtplib
- ssl
- email.message.EmailMessage
- email.utils.formataddr
- db_request_handling.SQLDataHandler

Functions:
- initiate_email(plant_id, next_watering_date): Fetches user and plant information from the database using the provided plant_id and sends an email reminder to the user.
- send_email(user_name, next_watering_date, plant_name, user_email): Sends an email reminder to the user with the provided details.

"""
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr

from db_request_handling import SQLDataHandler


def initiate_email(plant_id, next_watering_date):
    """
    Fetches user and plant information from the database using the provided plant_id and sends an email reminder to the user.

    Args:
        plant_id (int): The ID of the plant for which the reminder email needs to be sent.
        next_watering_date (str): The date of the next watering for the plant.

    Returns:
        None
    """
    sql_request = SQLDataHandler()
    sql_request.query = f"SELECT up.plant_nickname, uc.username, uc.email FROM user_credentials uc JOIN user_plants up ON uc.user_id = up.user_id WHERE up.plant_id = {plant_id};"
    plant_name, user_name, user_email = sql_request.db_get_record()

    send_email(user_name=user_name, next_watering_date=next_watering_date, plant_name=plant_name, user_email=user_email)


def send_email(user_name, next_watering_date, plant_name, user_email):
    """
    Sends an email reminder to the user with the provided details.

    Args:
        user_name (str): The name of the user.
        next_watering_date (str): The date of the next watering for the plant.
        plant_name (str): The nickname of the plant.
        user_email (str): The email address of the user.

    Returns:
        None
    """
    try:
        print("Sending you am email reminder! ")
        # the info for sending email
        email_sender = 'thirst.trap.app@gmail.com'
        password = 'dkzynbbqlcwyidji'
        email_receiver = user_email
        subject = "Reminder to water your plant!"

        em = EmailMessage()
        em['From'] = formataddr(("Thirst Trap Inc.", f"{email_sender}"))
        em['To'] = email_receiver
        em['Subject'] = subject
        # this is the body of our email
        em.set_content(f"The next time you need to water your plant friend {plant_name} is {next_watering_date}. \n"
                       f"Thirst Trap Inc.")
        # This is the html version that will display if allowed.
        em.add_alternative(f"""
        <!DOCTYPE html>
            <html lang="en">
        <h4>Reminder:</h4>
                <body>
                <p>Hello <strong>{user_name}</strong>, 
                The next time you need to water your plant friend {plant_name} is {next_watering_date}.
                           <p><em>Seriously.</em> Add it to your calendar. Don't make us call PPS. 
                    <br>
                    <strong>Plant Protective Services.</strong>
                    </p>
                <footer>Thirst Trap Inc. <br></footer>
                <img src='https://i.ibb.co/gMcBTqy/Img-1460-720.png' width = '50' height = '50' alt = 'picture of logo'>
                </body>
            </html>
        """, subtype="html")

        # this sends the email and sends it securely with the ssl we imported
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
    except Exception as e:
        print("There's a problem with the user's email:", e)
        return None
