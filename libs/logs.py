import logging
import coloredlogs
import config
import os
import sys
from .yaml_parse import ConfigParser

logger = logging.getLogger(__name__)

log_level = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

log_formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

log_set_level = ConfigParser().log_level


coloredlogs.install(stream=sys.stdout,
                    level=log_level[log_set_level],
                    fmt='%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s')


class AtLogSet(object):

    DebugLogFile = 'debug.log'

    def __init__(self, log_path=None):
        self.log_path = log_path

    def _set_logging(self):
        logger.setLevel(log_level[log_set_level])
        if self.log_path:
            if not os.path.exists(self.log_path):
                os.makedirs(self.log_path)
            log_file_path = os.path.join(self.log_path, self.DebugLogFile)
            if not logger.handlers:
                # 创建一个handler，用于写入日志文件
                fh = logging.FileHandler(log_file_path,
                                         'a',
                                         encoding='utf-8')
                fh.setFormatter(log_formatter)
                # 再创建一个handler，用于输出到控制台   因为使用了coloredlogs所以屏蔽了控制台日志输出
                # ch = logging.StreamHandler(sys.stdout)
                # ch.setLevel(logging.DEBUG)
                # 定义handler的输出格式
                fh.setFormatter(log_formatter)
                # ch.setFormatter(log_formatter)

                # 给logger添加handler
                logger.addHandler(fh)
                # logger.addHandler(ch)
        return logger

    def debug(self, message):
        return self._set_logging().debug(message)

    def info(self, message):
        return self._set_logging().info(message)

    def warning(self, message):
        return self._set_logging().warning(message)

    def error(self, message):
        return self._set_logging().error(message)

    def critical(self, message):
        return self._set_logging().error(message)


log_dir = ConfigParser(config.evn).log_path
log = AtLogSet(log_dir)