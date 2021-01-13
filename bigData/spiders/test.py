import json
import os
import sys
import time

# import winrm #pywinrm
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import  threading
import paramiko
import wmi  #WMI
import base64,codecs
import socket
# 如果text不足16位的倍数就用空格补足为16位
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')

# 加密函数
def encrypt(text):
    key = '0CoJUm6Qyw8W8jud'.encode('utf-8')
    mode = AES.MODE_CBC
    iv = b'0102030405060708'
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)

# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text):
    key = '0CoJUm6Qyw8W8jud'.encode('utf-8')
    iv = b'0102030405060708'
    mode = AES.MODE_CBC
    print(text.__len__())
    print(text.__len__()%16
          )
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')

iplis=[]
def sys_version(ipaddress,user,password):
    try:
        print(ipaddress)
        # time.sleep(10)
        conn=wmi.WMI(computer=ipaddress,user=user,password=password)
        print(conn)

    except Exception as e:
        print(e)
        ex=str(e)
        if ex.find("拒绝访问")>-1:
            iplis.append(ipaddress)
        # print(e.__dict__.get("com_error"))
        pass

class Client:
    def __init__(self,ip):
        self.ip=ip
    def connet(self):
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error as e:
            print(e)
            sys.exit()

        try:
            for i in range(255):
                re = "192.168.142." + str(i)
                s.connect((re,80))
                message=b"GET / HTTP/1.1\r\n\r\n"
                s.sendall(message)
                reply=s.recv(4096)
                print(reply)
                s.close()
        except socket.error:
            print("shibai"+self.ip)
            sys.exit()
        print(self.ip)

if __name__ == '__main__':
    # sys_version("192.168.142.200","KS\mei_qing","Ks#2020")
    # host=socket.gethostbyname(socket.gethostname())
    # os.system("arp -a>temp.txt")
    # with open("temp.txt") as fp:
    #     for line in fp:
    #         line=line.split()[:2]
    #         if line and line[0].startswith(host[:4]) and (not line[0].endswith("255")):
    #             print(":".join(line))
    # cl=Client("")
    # cl.connet()
    print(time.time())
    pass




   # client=paramiko.SSHClient()
   # client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
   # client.connect("192.168.142.1",port=22,username="KS\liu_hfei",password="Ks#2020")
   # stdin,stdout,stderr=client.exec_command("hostname")
   # result=stdout.read().decode("utf-8")
   # print(result)