import mysql.connector

# Establish a connection to the database
cnx = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="thirst_trap"
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

# Test 1: Select all records from user_credentials table
query = "SELECT * FROM user_credentials"
cursor.execute(query)
records = cursor.fetchall()
print("User Credentials:")
for record in records:
    print(record)

# Test 2: Select all records from user_plants table
query = "SELECT * FROM user_plants"
cursor.execute(query)
records = cursor.fetchall()
print("User Plants:")
for record in records:
    print(record)

# Test 3: Insert a new record into user_credentials table
query = "INSERT INTO user_credentials (username, password, email) VALUES (%s, %s, %s)"
values = ("lezlee_lowpez", "blue123", "lopez.lesley96@yahoo.com")
cursor.execute(query, values)
cnx.commit()
print("New user inserted.")

# Test 4: Verify the new record in user_credentials table
query = "SELECT * FROM user_credentials WHERE username = %s"
values = ("test_user",)
cursor.execute(query, values)
record = cursor.fetchone()
print("New User:")
print(record)

# Close the cursor and connection
cursor.close()
cnx.close()
