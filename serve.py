import pymysql

# Replace these values with your actual PythonAnywhere MySQL connection details
host = 'baragu.mysql.pythonanywhere-services.com'
user = 'baragu'  # Replace with your MySQL username
password = 'mooncake'  # Replace with your MySQL password
database = 'baragu$chatbot'

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    with connection.cursor() as cursor:
        cursor.execute('SHOW STATUS;')
        result = cursor.fetchall()
        for row in result:
            print(row)

except pymysql.MySQLError as e:
    print(f"Error: {e}")

# Move the connection.close() outside the try-except block
finally:
    if 'connection' in locals():
        connection.close()

