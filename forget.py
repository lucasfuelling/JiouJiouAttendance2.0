#!/usr/bin/env python
from datetime import datetime
from datetime import timedelta
import requests
import mariadb
import sys

token = "nhT4TzFE5b0NO3YMiMUlXexfqJrK23CAyyHuQyDEdP3"


def line_notify_message(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


def connect_to_mariadb():
    try:
        conn = mariadb.connect(
            user="jiou99",
            password="jiou99",
            host="localhost",
            port=3306,
            database="attendance"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn


def forget_clock_out():
    global token
    conn = connect_to_mariadb()
    cur = conn.cursor()
    yesterday = datetime.now() - timedelta(days=1)
    sql = "SELECT username FROM attendance WHERE clockout_B is NULL AND clockday =?"
    par = (yesterday.strftime("%Y-%m-%d"),)
    cur.execute(sql, par)
    rows = cur.fetchall()
    message = '\n'
    if rows:
        for row in rows:
            message = message + row[0] + '\n'
        message = message + "--昨天忘記打卡--"
        line_notify_message(token, message)


if __name__ == '__main__':
    forget_clock_out()
