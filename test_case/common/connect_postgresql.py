import pymysql
import psycopg2

'''
pip install psycopg2-binary==2.8.5
'''
import psycopg2


# 数据库连接参数
class DbConnect():
    def __init__(self):
        # 打开数据库连接
        self.conn = psycopg2.connect(database="sirius_test",
                                     user="sirius_test",
                                     password="123456",
                                     host="192.168.10.253",
                                     port="5432")
        self.cur = self.conn.cursor()

    def select(self, sql):
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows

    def execute(self, sql):
        # SQL 删除、提交、修改语句
        # sql = "DELETE FROM EMPLOYEE WHERE AGE > %s" % (20)
        # 执行SQL语句
        try:
            self.cur.execute(sql)
            # 提交修改
            self.conn.commit()
        except:
            self.conn.rollback()


def select_sql(select_sql):
    db = DbConnect()
    result = db.select(select_sql)
    db.cur.close()
    db.conn.commit()
    db.conn.close()
    return result


def execute_sql(sql):
    '''执行SQL语句'''
    # cur.execute("DELETE FROM Employee WHERE name='Gopher'")
    db = DbConnect()
    db.execute(sql)
    db.cur.close()
    db.conn.commit()
    db.conn.close()


if __name__ == '__main__':
    sql = "SELECT * FROM sirius.md_user where id =77"
    a = select_sql(sql)
    print(a)
    # sql = ' DELETE FROM sirius.md_user WHERE id = 49 '
    # execute_sql(sql)
