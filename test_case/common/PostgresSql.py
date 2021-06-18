import threading
import time

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
                                                                                  user="sirius_test", password='123456',
                                                                                  database='sirius_int',
                                                                                  options='-c search_path={schema}'.format(
                                                                                      schema='sirius'),
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
    pass
    test = PostgresSql()
    sql = 'SELECT storage_location_id from wms_goods_stock  where goods_id= 259 ORDER BY storage_location_id limit 1 ;'
    a = test.selectOne(sql)
    print(str(a))
    # # sql = 'SELECT id FROM  sirius.md_goods  limit 10'
    # sql = "SELECT id FROM  md_goods where name like '锁定%' limit 10"
    # # sql1 = "SELECT name FROM  md_goods where id = c"
    # a = test.selectAll(sql)
    # b = (a[0][0])
    # idList = []
    # for i in a:
    #     j = i[0]
    #     ttt = (i[0], 57, 57, 13, 'put_on_shelf', 43, 'f', 59, str(time.time()))
    #     idList.append(j)
    # sql2 = """INSERT INTO sirius.wms_goods_stock
    #             ( goods_id, goods_lot_info_id, quantity, warehouse_id, status, version,
    #             is_packaged, storage_location_id, unique_code )
    #             VALUES {}""".format(*idList)
    #
    # sql3 = """UPDATE sirius.wms_goods_stock SET quantity = 10 where goods_id in {}""".format(tuple(idList))
    # test.execute(sql3)
