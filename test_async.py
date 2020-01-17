#!/usr/bin/python
# encoding:utf-8

from multiprocessing import Pool
from login_device import *
import traceback
import time
import os


def h3c_6800(ip):
    # 使用生成器功能调用h3c的登录方法登录设备
    @devopstools.h3c_login_device(ip, 720)
    # show_ip_interf函数中定义要执行的命令及反馈结果
    def show_ip_interf():
        try:
            starttime = time.asctime(time.localtime(time.time()))
            print('h3c_6800 login start from %s' % starttime)
            # 登陆设备后，执行命令display current-configuration
            output = devopstools.h3c_cli('dis cu')
            endtime = time.asctime(time.localtime(time.time()))
            print('h3c_6800 login end to %s' % endtime)
        except Exception:
            # 如果出错打印出错原因
            print('Some errors occurred when execute command on %s.' % ip)
            print(traceback.format_exc())
    show_ip_interf()


def cisco_3560(ip):
    @devopstools.cisco_login_device(ip, 720)
    def show_ip_interf():
        try:
            starttime = time.asctime(time.localtime(time.time()))
            print('cisco_3560 login start from %s' % starttime)
            output = devopstools.cisco_cli('show run')
            endtime = time.asctime(time.localtime(time.time()))
            print('cisco_3560 login end to %s' % endtime)
        except Exception:
            print('Some errors occurred when execute command on %s.' % ip)
            print(traceback.format_exc())
    show_ip_interf()


def huawei_6865(ip):
    @devopstools.huawei_login_device(ip, 720)
    def show_ip_interf():
        try:
            starttime = time.asctime(time.localtime(time.time()))
            print('huawei_6865 login start from %s' % starttime)
            output = devopstools.huawei_cli('dis cu')
            endtime = time.asctime(time.localtime(time.time()))
            print('huawei_6865 login end to %s' % endtime)
        except Exception:
            print('Some errors occurred when execute command on %s.' % ip)
            print(traceback.format_exc())
    show_ip_interf()


# 添加3台交换机基础信息，包括ip、产商名称、型号等，正式环境请使用数据库
device_list = [
    {
        'ip' : '10.110.1.254',
        'vendor' : 'h3c',
        'model' : 'S6800'
    },
    {
        'ip' : '10.73.254.48',
        'vendor' : 'cisco',
        'model' : 'C3560'
    },
    {
        'ip' : '10.100.1.15',
        'vendor' : 'huawei',
        'model' : 'CE6865'
    }]


def main(devicelist):
    print('Parent process id is %s' % os.getpid())
    p = Pool(20)
    for device in devicelist:
        if device['vendor'] == 'h3c' and device['model'] == 'S6800':
            p.apply_async(h3c_6800, args=(device['ip'], ))
        elif device['vendor'] == 'cisco' and device['model'] == 'C3560':
            p.apply_async(cisco_3560, args=(device['ip'], ))
        elif device['vendor'] == 'huawei' and device['model'] == 'CE6865':
            p.apply_async(huawei_6865, args=(device['ip'], ))
        else:
            pass
    p.close()
    p.join()

if __name__ == '__main__':
    main(device_list)
