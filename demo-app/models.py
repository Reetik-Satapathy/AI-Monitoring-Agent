from flask_mysqldb import MySQL

mysql = MySQL()


def save_contact(name, email, message):
    cursor = mysql.connection.cursor()

    query = """
        INSERT INTO contacts(name, email, message)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, email, message))

    mysql.connection.commit()

    cursor.close()