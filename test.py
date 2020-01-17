#!/usr/bin/python
# encoding:utf-8


from login_device import *


def h3c_6800(ip):
    # 使用生成器功能调用h3c的登录方法登录设备
    @devopstools.h3c_login_device(ip, 720)
    # show_ip_interf函数中定义要执行的命令及反馈结果
    def show_ip_interf():
        try:
            # 登陆设备后，执行命令display ip interface brief
            output = devopstools.h3c_cli('display ip int brief')
            print output
        except Exception:
            # 如果出错打印出错原因
            print('Some errors occurred when execute command on %s.' % ip)
            print(traceback.format_exc())
    show_ip_interf()


def cisco_3560(ip):
    @devopstools.cisco_login_device(ip, 720)
    def show_ip_interf():
        try:
            output = devopstools.cisco_cli(['show ip interface brief', 'show arp'])
            print output
        except Exception:
            print('Some errors occurred when execute command on %s.' % ip)
            print(traceback.format_exc())
    show_ip_interf()


def huawei_6865(ip):
    @devopstools.huawei_login_device(ip, 30)
    def show_ip_interf():
        try:
            output = devopstools.huawei_cli(['display ip interface brief', 'display cu'])
            print output
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
    # 根据设备的厂商与型号选择相应的操作函数
    for device in devicelist:
        if device['vendor'] == 'h3c' and device['model'] == 'S6800':
            h3c_6800(device['ip'])
        elif device['vendor'] == 'cisco' and device['model'] == 'C3560':
            cisco_3560(device['ip'])
        elif device['vendor'] == 'huawei' and device['model'] == 'CE6865':
            huawei_6865(device['ip'])
        else:
            pass

if __name__ == '__main__':
    main(device_list)

