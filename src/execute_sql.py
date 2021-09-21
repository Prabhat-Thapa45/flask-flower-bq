from src.config import mysql


def query_handler_fetch(query: str, values: tuple = ()) -> tuple:
    cur = mysql.connection.cursor()
    if values:
        cur.execute(query, values)
        mysql.connection.commit()
        results = cur.fetchall()
        cur.close()
        return results
    else:
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results


def query_handler_no_fetch(query: str, values: tuple = ()):
    cur = mysql.connection.cursor()
    if values:
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()
