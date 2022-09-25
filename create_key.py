# -*- coding: utf-8 -*- 
# @Time : 2022/6/26 22:39 
# @Author : junjie
# @File : create_key.py

import paramiko
import os

def generate_ssh_key() -> None:
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/commons/settings/keys')
    if not os.path.isdir(key_path): os.mkdir(key_path)
    rsa_pri_key = os.path.join(key_path, 'rsa_pri_key')
    ras_pub_key = os.path.join(key_path, 'rsa_pub_key')
    key = paramiko.RSAKey.generate(4096)
    # 私钥生成
    key.write_private_key_file(rsa_pri_key)
    # 公钥生成
    pub_key = f"{key.get_name()} {key.get_base64()} FunDataFactory"
    with open(ras_pub_key, 'w') as f:
        f.write(pub_key)

if __name__ == '__main__':
    generate_ssh_key()