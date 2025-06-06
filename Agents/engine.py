import mysql.connector
from tabulate import tabulate

# Connect to MySQL Database
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Arun@mysql2004",
    database="empdb"
)
cursor = db_connection.cursor()

# SQL Query to retrieve relevant roles
query = """
SELECT 
  `Member ID`, `Name`, `Experience (Years)`, `Roles`, `Preferences`, `Projects`
FROM 
  employeerecords
WHERE 
  `Roles` REGEXP 'Frontend Developer|User Experience \\(UX\\) Designer|User Interface \\(UI\\) Designer|Full Stack Developer|Interaction Designer|Web Developer|Responsive Web Designer|JavaScript Developer|HTML/CSS Developer|Product Recommendation System Integrator|Software Engineer';

"""

cursor.execute(query)
records = cursor.fetchall()

headers = ["Member ID", "Name", "Experience (Years)", "Roles", "Preferences", "Projects"]

# Format output as a table
response = tabulate(records, headers=headers, tablefmt="grid")

print(response)  # Modify this to return the response in your application

# Close the connection
cursor.close()
db_connection.close()
