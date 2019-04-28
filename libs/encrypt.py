from Crypto.Cipher import AES
from base64 import b64decode
from base64 import b64encode


def add_to_16(text):
    while len(text) % 16 != 0:
        text += '\0'
    return str.encode(text)


class prpcrypt(object):

    def __init__(self, key, iv):
        """
        :param key:AES　加密key
        :return:
        """
        self.key = key
        self.iv = iv
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self, text):
        """
        :param text:需要加密的字符串
        :return: 加密后的base64编码字符串
        """

        raw = add_to_16(text)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return str(b64encode(cipher.encrypt(raw)), encoding="utf-8")

    def decrypt(self, text):
        """
        :param text: 需要解密的字符串
        :return: 解密后的base64编码字符串
        """
        enc = b64decode(text)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return str(cipher.decrypt(enc), encoding='utf-8')