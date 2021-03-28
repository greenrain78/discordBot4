from logging import getLogger

import mysql.connector

from settings import mariaDB_ID, mariaDB_password, mariaDB_IP, mariaDB_DB_name, mariaDB_port

log = getLogger(__name__)

config = {
    'user': mariaDB_ID,
    'password': mariaDB_password,
    'host': mariaDB_IP,
    'database': mariaDB_DB_name,
    'port': mariaDB_port,
}


def getConn():
    # ** 가변인자 전달 방법
    conn = mysql.connector.connect(**config)
    return conn


def runSQL(sql):
    try:
        conn = getConn()
        cur = conn.cursor()

        cur.execute(sql)
        print("run sql: ", sql)
        conn.commit()
        conn.close()
        log.debug("(run): %s", sql)
        return sql
    except Exception as e:
        log.exception("run error: %s", sql)


def getSQL(sql):
    try:
        conn = getConn()
        cur = conn.cursor()

        cur.execute(sql)
        result = cur.fetchall()

        conn.commit()
        conn.close()

        log.debug("(get): %s \n \t %s", sql, result)
        return result
    except Exception as e:
        log.exception("get error: %s", sql)


def getOneSQL(sql):
    try:
        conn = getConn()
        cur = conn.cursor()

        cur.execute(sql)
        result = cur.fetchall()

        conn.commit()
        conn.close()
        log.debug("(get): %s \n \t %s", sql, result)
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        log.exception("get error: %s", sql)
