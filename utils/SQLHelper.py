import pymysql
from dbutils.pooled_db import PooledDB
from datetime import datetime
import os
class SQLHelper:

    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=int(os.environ.get('mysql.maxconnections')),
            mincached=int(os.environ.get('mysql.mincached')),
            blocking=True,
            ping=0,
            host=os.environ.get('mysql.host'),
            port=int(os.environ.get('mysql.port')),
            user=os.environ.get('mysql.user'),
            password=os.environ.get('mysql.password'),
            database=os.environ.get('mysql.database'),
            charset=os.environ.get('mysql.charset')
        )

    def open(self):
        conn = self.pool.connection()
        cur = conn.cursor()
        return conn, cur
    
    def close(self, conn, cur):
        cur.close()
        conn.close()

    def get_list(self, sql, *args):
        conn, cur = self.open()
        try:
            cur.execute(sql, args)
            results = cur.fetchall()
            return results
        finally:
            self.close(conn,cur)
    
    def get_one(self, sql, *args):
        conn, cur = self.open()
        try:
            cur.execute(sql, args)
            result = cur.fetchone()
            return result
        finally:
            self.close(conn,cur)
    
    def update(self, sql, *args):
        conn, cur = self.open()
        try:
            result = cur.execute(sql, args)
            conn.commit()
            return result
        finally:
            self.close(conn,cur)
    
    def insert(self, sql, *args):
        conn, cur = self.open()
        try:
            cur.execute(sql, args)
            conn.commit()
            return cur.lastrowid
        finally:
            self.close(conn,cur)
    
sqlHelper = SQLHelper()

def task_test():
    now = datetime.now()
    print(f'task start at {now}')