# -*- coding: utf-8 -*- 
# @Time : 2022/6/14 21:42 
# @Author : junjie
# @File : aes_utils.py

import base64, hmac
from Crypto.Cipher import AES
from app.constants import constants
from hashlib import sha256

class AesUtils(object):

    @classmethod
    def add_to_16(cls, value):
        """不足16位补0"""
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes


    @classmethod
    def encrypt(cls, text):
        """
        AES加密
        :param text: 待加密明文
        :return:
        """
        # 初始化加密器
        aes = AES.new(cls.add_to_16(constants.AES_KEY), AES.MODE_CBC, cls.add_to_16(constants.AES_IV))
        bs = AES.block_size
        pad2 = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)  # PKS7
        encrypt_aes = aes.encrypt(pad2(text).encode())
        # 用base64转成字符串形式
        # 执行加密并转码返回bytes
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        # 和js的 结果相同 http://tool.chacuo.net/cryptaes
        return encrypted_text.replace('\n', '')  # 去除换行符

    @classmethod
    def decrypt(cls, text):
        """
        AES解密
        :param text: 待解密密文
        :return:
        """
        # 初始化解密器
        # 偏移量 16个0
        aes = AES.new(cls.add_to_16(constants.AES_KEY), AES.MODE_CBC, cls.add_to_16(constants.AES_IV))
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
        # 执行解密并转码返回str
        decrypted_text = aes.decrypt(base64_decrypted).decode()
        unpad = lambda s: s[0:-ord(s[-1])]
        return unpad(decrypted_text)


class Sha256(object):

    @classmethod
    def encrypt(cls, timestamp: str):
        secret = constants.SECRET
        data = f"{timestamp}\n{secret}"
        sign = base64.b64encode(
            hmac.new(secret.encode('utf-8'), data.encode('utf-8'), digestmod=sha256).digest()).decode()
        return sign

if __name__ == '__main__':
    # 加密
    encrypt_data = AesUtils.encrypt('fang')
    print(encrypt_data)
    # 解密
    decrypt_data = AesUtils.decrypt(encrypt_data)
    print(decrypt_data)