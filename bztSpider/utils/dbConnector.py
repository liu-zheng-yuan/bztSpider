import pymysql
import configparser
import time
from queue import Queue
import threading
import settings

start = time.time()


class dbConnector:
    _instance = None  # 单例模式 只能有一个dbConnector
    _instance_lock = threading.Lock()

    def __init__(
        self,
        host=None,
        port=None,
        user=None,
        passwd=None,
        db=None,
        charset=None,
        maxconn=5,
    ):
        cf = configparser.ConfigParser()
        cf.read("D:\Code\Python\DigitalStar\\bztSpider\\bztSpider\\utils\dbconfig.ini")
        self.host = settings.MYSQL_host if host == None else host
        self.user = settings.MYSQL_user if user == None else user
        self.passwd = settings.MYSQL_password if passwd == None else passwd
        self.db = settings.MYSQL_db if db == None else db
        self.port = int(settings.MYSQL_port) if port == None else port
        self.maxconn = maxconn
        self.pool = Queue(maxconn)
        for i in range(maxconn):
            try:
                conn = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    passwd=self.passwd,
                    db=self.db,
                    charset="utf8"
                )
                conn.autocommit(True)
                # self.cursor=self.conn.cursor(cursor=pymysql.cursors.DictCursor)
                self.pool.put(conn)
            except Exception as e:
                raise IOError(e)

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance == None:  # 多线程时先判断有无 只要有 就不需要下面加锁操作
            with cls._instance_lock:
                if cls._instance == None:  # 只有真正有可能错判要新建对象时 才真正加锁
                    cls._instance = dbConnector(*args, **kwargs)
        return cls._instance

    def exec_sql(self, sql, operation=None):
        """
            执行无返回结果集的sql，主要有insert update delete
        """
        try:
            conn = self.pool.get()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            response = (
                cursor.execute(sql, operation) if operation else cursor.execute(sql)
            )
        except Exception as e:
            print(e)
            cursor.close()
            self.pool.put(conn)
            return None
        else:
            cursor.close()
            self.pool.put(conn)
            return response

    def exec_sql_feach(self, sql, operation=None):
        """
            执行有返回结果集的sql,主要是select
        """
        try:
            conn = self.pool.get()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            response = (
                cursor.execute(sql, operation) if operation else cursor.execute(sql)
            )
        except Exception as e:
            print(e)
            cursor.close()
            self.pool.put(conn)
            return None, None
        else:
            data = cursor.fetchall()
            cursor.close()
            self.pool.put(conn)
            # return response, data
            # 不要返回完整的response 返回结果集就可以了
            return data

    def exec_sql_many(self, sql, operation=None):
        """
            执行多个sql，主要是insert into 多条数据的时候
        """
        try:
            conn = self.pool.get()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            response = (
                cursor.executemany(sql, operation)
                if operation
                else cursor.executemany(sql)
            )
        except Exception as e:
            print(e)
            cursor.close()
            self.pool.put(conn)
        else:
            cursor.close()
            self.pool.put(conn)
            return response

    def close_conn(self):
        for i in range(self.maxconn):
            self.pool.get().close()


# 测试10个线程每个插入十万条的时间 9秒
# conn = dbConnector.get_instance(maxconn = 10)
# def test_func(num):
#     data = (("title" + str(i)) for i in range(num))
#     sql = "insert into collection(title) values(%s)"
#     print(conn.exec_sql_many(sql, data))
# job_list = []
# for i in range(10):
#     t = threading.Thread(target=test_func, args=(100000,))
#     t.start()
#     job_list.append(t)
# for j in job_list:
#     j.join()
# conn.close_conn()
# print("totol time:", time.time() - start)

# #测试一个线程插入100w的时间 7秒 = =
# conn = pymysql.connect(host="localhost",port=3306,user="root",passwd="123456",db="bztspider",charset="utf8")
# conn.autocommit(True)  # 设置自动commit
# cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 设置返回的结果集用字典来表示，默认是元祖
# data = (("title" + str(i)) for i in range(1000000))
# sql = "insert into collection(title) values(%s)"
# cursor.executemany(sql,data)
# cursor.close()
# conn.close()
# print("totol time:", time.time() - start)
