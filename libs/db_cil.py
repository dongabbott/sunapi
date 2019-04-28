from libs.yaml_parse import ConfigParser
from libs.logs import log
from sqlalchemy import create_engine
from redis import StrictRedis, ConnectionPool


class MySQLCil(object):
    """利用sqlalchemy进行数据库操作"""
    def __init__(self,  sql):
        self.sql = sql
        self.pool = ConfigParser().sql_con_pool
        self.engine = create_engine(self.pool)

    def _run(self):
        log.debug("运行SQL语句:{}".format(self.sql))
        result = self.engine.execute(self.sql)
        try:
            data = result.fetchall()
            log.debug("执行结果:{}".format(data))
            return data
        except Exception as e:
            log.error(e)
            return None

    @property
    def result(self):
        return self._run()


def redis_cli():
    """创建redis连接"""
    redis_config = ConfigParser().redis_option
    redis_pool = ConnectionPool(**redis_config)
    redis_connect = StrictRedis(connection_pool=redis_pool)
    return redis_connect


def mysql_select(sql):
    """mysql查询"""
    return MySQLCil(sql).result