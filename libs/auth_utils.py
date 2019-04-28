from libs.encrypt import prpcrypt
from libs.errors import ApiLoginError
from libs.yaml_parse import ConfigParser
import requests
from libs.logs import log
from libs.db_cil import redis_cli


def login(u):
    u_name = 'u'
    token = redis_cli().get(u)
    if token:
        return token
    uri = '/live/index/login'
    key = '1234567890654321'
    iv = '1234567890123456'
    data = {
        u_name: prpcrypt(key, iv).encrypt(u)
    }
    url = ConfigParser().api_host.rstrip('/') + '/' + uri.lstrip('/')
    try:
        response = requests.post(url, data=data)
        token = response.headers.get("Token")
        if token:
            log.info("[{}]登录成功,token[{}]".format(u, token))
            redis_cli().set(u, token, ex=3600)
        return token
    except Exception:
        log.error('[{}]登录失败'.format(u))
        raise ApiLoginError

