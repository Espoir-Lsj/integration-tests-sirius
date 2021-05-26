import threading

from psycopg2 import pool
from test_config import param_config

host = param_config.host
port = param_config.port
user = param_config.user
password = param_config.password
database = param_config.database
schema = param_config.schema


class PostgresSql:
    # 加锁
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with PostgresSql._instance_lock:
                PostgresSql._instance = super().__new__(cls)
                try:
                    PostgresSql._instance.connectPool = pool.SimpleConnectionPool(2, 10, host=host,
                                                                                  port=port,
                                                                                  user=user, password=password,
                                                                                  database=database,
                                                                                  options='-c search_path={schema}'.format(
                                                                                      schema=schema),
                                                                                  keepalives=1, keepalives_idle=30,
                                                                                  keepalives_interval=10,
                                                                                  keepalives_count=5)
                except Exception as e:
                    print(e)
        return PostgresSql._instance

    def getConnect(self):
        conn = self.connectPool.getconn()
        cursor = conn.cursor()
        return conn, cursor

    def closeConnect(self, conn, cursor):
        cursor.close()
        self.connectPool.putconn(conn)

    def closeAll(self):
        self.connectPool.closeall()

    # 执行增删改
    def execute(self, sql, vars=None):
        conn, cursor = self.getConnect()
        try:
            cursor.execute(sql, vars)
            conn.commit()
            self.closeConnect(conn, cursor)
        except Exception as e:
            conn.rollock()
            raise e

    def selectOne(self, sql):
        conn, cursor = self.getConnect()
        cursor.execute(sql)
        result = cursor.fetchone()
        self.closeConnect(conn, cursor)
        return result

    def selectAll(self, sql):
        conn, cursor = self.getConnect()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.closeConnect(conn, cursor)
        return result


if __name__ == '__main__':
    test = PostgresSql()
    sql = 'SELECT * FROM sirius.md_goods_lot_info where goods_id =321'
    a = test.selectAll(sql)
    print(a)
