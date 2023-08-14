# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      crypt_pwd
   Description:
   Author:          LinZhengTian
   date：           2018/5/24
-------------------------------------------------
   Change Activity:
                    2018/5/24:
-------------------------------------------------
"""
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_v1_5
import uuid
import os
from django.core.cache import cache


class CryptPwd:
    """
    用于加密和解密密码,
    """

    def __init__(self):
        self.key = "juren"
        self.mode = AES.MODE_ECB

    @staticmethod
    def add_to_16(value):
        """
        要加密的数据和使用的key的字节数必须是16位，这里不足16位的用'\n'填充，方便后面解密使用rstrip
        :param value: 要加长的内容
        :return: bytes类型的数据
        :type value: str
        :rtype: bytes
        """
        while len(value) % 16 != 0:
            value += '\n'
        return value.encode('utf-8')

    def encrypt_pwd(self, pwd):
        """
        对密码进行加密
        :param pwd: 密码
        :return: 加密后的密码
        :type pwd: str
        :rtype: str
        """
        aes = AES.new(self.add_to_16(self.key), self.mode)
        encrypt_aes = aes.encrypt(self.add_to_16(pwd))
        encrypted_pwd = str(base64.b64encode(encrypt_aes), encoding='utf-8')
        return encrypted_pwd

    def decrypt_pwd(self, encrypted_pwd):
        """
        对密码进行解密
        :param encrypted_pwd: 加密后的密码，必须是使用同一种方式加密的密码
        :return: 解密后的密码，字符串类型
        :type encrypted_pwd: str
        :rtype: str
        """
        aes = AES.new(self.add_to_16(self.key), self.mode)
        decrypt_base64 = base64.b64decode(encrypted_pwd.encode('utf-8'))
        decrypt_pwd = str(aes.decrypt(decrypt_base64), encoding='utf-8')
        return decrypt_pwd.rstrip()

    @property
    def gen_pri_pub_key(self):
        rsa = RSA.generate(1024)
        private_key = rsa.exportKey().decode('utf8')
        if not os.path.exists('pri'):
            os.mkdir('pri')
        id = str(uuid.uuid1()).replace('-','')
        with open(os.path.join('pri', id+'.pem'), 'w') as f:
            f.write(private_key)
        public_key = rsa.publickey().exportKey().decode('utf8')
        return { 'id': id, 'value': public_key}

    @staticmethod
    def gen_pri_pub_key_cache():
        rsa = RSA.generate(1024)
        private_key = rsa.exportKey().decode('utf8')
        public_key = rsa.publickey().exportKey().decode('utf8').replace("-----BEGIN PUBLIC KEY-----\n", "").replace("\n-----END PUBLIC KEY-----", "")
        pid = str(uuid.uuid1()).replace('-', '')
        cache.set("login_private_" + pid, private_key, 1800)
        return {"pid": pid, "key": public_key}

    @staticmethod
    def de_js_encrypt_cache(en_pwd, pid):
        """
        解密非对称加密密钥
        """
        private_key = cache.get("login_private_" + pid, "")
        if private_key:
            rsakey = RSA.importKey(private_key)  # 导入私钥
            cipher = PKCS1_v1_5.new(rsakey)  # 生成对象
            missing_padding = len(en_pwd) % 4
            if missing_padding:
                en_pwd += '=' * (4 - missing_padding)
            decode_data = base64.b64decode(en_pwd.encode('utf8'))
            text = cipher.decrypt(decode_data, "ERROR")  # 将密文解密成明文，返回的是一个bytes类型数据，需要自己转换成str
            return text.decode('utf-8')
        else:
            return ""

    @staticmethod
    def de_js_encrypt(en_pwd, id):
        """
        解密通过jsencrypt.js文件加密的密码
        :param en_pwd:
        :return:
        """
        with open(os.path.join('pri', id+'.pem')) as f:
            private_key = f.read()
        rsakey = RSA.importKey(private_key)  # 导入私钥
        cipher = PKCS1_v1_5.new(rsakey)  # 生成对象

        missing_padding = len(en_pwd) % 4
        if missing_padding:
            en_pwd += '=' * (4 - missing_padding)
        decode_data = base64.b64decode(en_pwd.encode('utf8'))

        text = cipher.decrypt(decode_data, "ERROR")  # 将密文解密成明文，返回的是一个bytes类型数据，需要自己转换成str
        return text.decode('utf-8')
