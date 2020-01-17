#!/usr/bin/python
# encoding:utf-8
import pexpect
import time
import traceback
from profile import *




class devopstools:
    @classmethod
    def h3c_login_device(cls, ip, logintime):
        try:
            # 创建telnet登录设备的句柄
            cls.child = pexpect.spawn('telnet %s' % ip, timeout=logintime)
            cls.child.setwinsize(34, 124)
            # 创建一个log文件，记录telnet句柄内所有操作信息
            clock = time.strftime("%Y-%m-%d-%X")
            cls.f = open('%s%s_%s_telnet.log' % (env_parameter['log_dir'], clock, ip), 'w')
            cls.child.logfile_read = cls.f
            index = cls.child.expect(['ogin:|sername:', pexpect.TIMEOUT, pexpect.EOF])
            if index != 0:
                cls.f.close()
                cls.child.close()
                if index == 1:
                    raise Exception('%s: telnet login failed, timeout when logging.' % ip)
                else:
                    raise Exception('%s: telnet login failed, refused by remote when logging.' % ip)
            else:
                cls.child.sendline(env_parameter['aaa_user'])
                index = cls.child.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
                if index != 0:
                    cls.f.close()
                    cls.child.close()
                    raise Exception('%s: telnet login failed, timeout when typing username [%s].' % (ip, env_parameter['aaa_user']))
                else:
                    cls.child.sendline(env_parameter['aaa_passwd'])
                    time.sleep(1)
                    index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], 'ogin:|sername:', pexpect.TIMEOUT, pexpect.EOF])
                    if index != 0:
                        if index == 1:
                            print('%s: user %s is wrong, trying user %s.' % (ip, env_parameter['aaa_user'], env_parameter['local_user']))
                            cls.child.sendline('%s' % env_parameter['local_user'])
                            index = cls.child.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
                            if index != 0:
                                cls.f.close()
                                cls.child.close()
                                raise Exception('%s: telnet login failed, timeout when typing username [%s].' % (ip, env_parameter['local_user']))
                            else:
                                cls.child.sendline('%s' % env_parameter['local_passwd'])
                                time.sleep(1)
                                index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], 'ogin:|sername:', pexpect.TIMEOUT, pexpect.EOF])
                                if index != 0:
                                    if index == 1:
                                        cls.f.close()
                                        cls.child.close()
                                        raise Exception('%s: telnet login failed, wrong username or password, please check it.' % ip)
                                    else:
                                        cls.f.close()
                                        cls.child.close()
                                        raise Exception('%s: telnet login failed, timeout when typing [%s] password.' % (ip, env_parameter['local_user']))
                        else:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('%s :telnet login failed, timeout when typing [%s] password.' % (ip, env_parameter['aaa_user']))

                    cls.child.sendline('undo terminal monitor')
                    index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT, pexpect.EOF])
                    if index != 0:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('%s: telnet login failed, timeout when typing initial cmd.' % ip)
                    cls.child.sendline('screen-length disable')
                    index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT, pexpect.EOF])
                    if index != 0:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('%s: telnet login failed, timeout when typing initial cmd.' % ip)


                    def decorator(func):
                        def wrapper(*args, **kw):
                            return func(*args, **kw)

                        return wrapper

                    return decorator

                    cls.f.close()
                    cls.child.close()
        except Exception:
            print traceback.format_exc()


    @classmethod
    def cisco_login_device(cls, ip, logintime):
        try:
            # 创建telnet登录设备的句柄
            cls.child = pexpect.spawn('telnet %s' % ip, timeout=logintime)
            # 创建一个log文件，记录telnet句柄内所有操作信息
            clock = time.strftime("%Y-%m-%d-%X")
            cls.f = open('%s%s_%s_telnet.log' % (env_parameter['log_dir'], clock, ip), 'w')
            cls.child.logfile_read = cls.f
            index = cls.child.expect(['ogin:|sername:', pexpect.TIMEOUT, pexpect.EOF])
            if index != 0:
                cls.f.close()
                cls.child.close()
                if index == 1:
                    raise Exception('%s: telnet login failed, timeout when logging.' % ip)
                else:
                    raise Exception('%s: telnet login failed, refused by remote when logging.' % ip)
            else:
                cls.child.sendline('%s' % env_parameter['aaa_user'])
                index = cls.child.expect(['assword:', 'sername:', pexpect.TIMEOUT, pexpect.EOF])
                if index != 0:
                    if index != 1:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('%s: telnet login failed, timeout when typing username [%s].' % (ip, env_parameter['aaa_user']))
                    else:
                        print('%s :user zhaodong3 is wrong, trying user %s.' % (ip, env_parameter['local_user']))
                        cls.child.sendline('%s' % env_parameter['local_user'])
                        time.sleep(1)
                        index = cls.child.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
                        if index != 0:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('%s: telnet login failed, timeout when typing username [%s].' % (ip, env_parameter['local_user']))
                        else:
                            cls.child.sendline('%s' % env_parameter['local_passwd'])
                            time.sleep(1)
                            index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'],
                                                      '%s' % env_parameter['hostname_format_cisco2'],
                                                      'ogin:|sername:', pexpect.TIMEOUT, pexpect.EOF])
                            if index != 0:
                                if index == 1:
                                    cls.child.sendline('enable')
                                    index = cls.child.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
                                    if index != 0:
                                        cls.f.close()
                                        cls.child.close()
                                        raise Exception('%s: telnet login failed, timeout when typing enable.' % ip)
                                    else:
                                        cls.child.sendline('%s' % env_parameter['enable_passwd_cisco'])
                                        index = cls.child.expect(
                                            ['%s' % env_parameter['hostname_format_cisco1'],
                                             'denied|incorrect|error', pexpect.TIMEOUT, pexpect.EOF])
                                        if index != 0:
                                            if index == 1:
                                                cls.f.close()
                                                cls.child.close()
                                                raise Exception('%s: telnet login failed, wrong enable password.' % ip)
                                            else:
                                                cls.f.close()
                                                cls.child.close()
                                                raise Exception(
                                                    '%s: telnet login failed, timeout when typing enable password.' % ip)
                                elif index == 2:
                                    cls.f.close()
                                    cls.child.close()
                                    raise Exception(
                                        '%s: telnet login failed, wrong username or password, please check it.' % ip)
                                else:
                                    cls.f.close()
                                    cls.child.close()
                                    raise Exception(
                                        '%s: telnet login failed, timeout when typing [%s] password.' % (ip, env_parameter['local_user']))
                else:
                    cls.child.sendline('%s' % env_parameter['aaa_passwd'])
                    time.sleep(1)
                    index = cls.child.expect(
                        ['%s' % env_parameter['hostname_format_cisco1'], '%s' % env_parameter['hostname_format_cisco2'],'ogin:|sername:', pexpect.TIMEOUT, pexpect.EOF])
                    if index != 0:
                        if index == 1:
                            cls.child.sendline('enable')
                            index = cls.child.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
                            if index != 0:
                                cls.f.close()
                                cls.child.close()
                                raise Exception('%s: telnet login failed, timeout when typing enable.' % ip)
                            else:
                                cls.child.sendline('%s' % env_parameter['enable_passwd_cisco'])
                                index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'], 'denied|incorrect|error', pexpect.TIMEOUT, pexpect.EOF])
                                if index != 0:
                                    if index == 1:
                                        cls.f.close()
                                        cls.child.close()
                                        raise Exception('%s: telnet login failed, wrong enable password.' % ip)
                                    else:
                                        cls.f.close()
                                        cls.child.close()
                                        raise Exception('%s: telnet login failed, timeout when typing enable password.' % ip)
                        elif index == 2:
                            print('%s :user %s is wrong, trying user %s.' % (ip, env_parameter['aaa_user'], env_parameter['local_user']))
                            cls.child.sendline('%s' % env_parameter['local_user'])
                            time.sleep(1)
                            index = cls.child.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
                            if index != 0:
                                cls.f.close()
                                cls.child.close()
                                raise Exception('%s: telnet login failed, timeout when typing username [%s].' % (ip, env_parameter['local_user']))
                            else:
                                cls.child.sendline('%s' % env_parameter['local_passwd'])
                                time.sleep(1)
                                index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'],'%s' % env_parameter['hostname_format_cisco2'], 'ogin:|sername:', pexpect.TIMEOUT, pexpect.EOF])
                                if index != 0:
                                    if index == 1:
                                        cls.child.sendline('enable')
                                        index = cls.child.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
                                        if index != 0:
                                            cls.f.close()
                                            cls.child.close()
                                            raise Exception('%s: telnet login failed, timeout when typing enable.' % ip)
                                        else:
                                            cls.child.sendline('%s' % env_parameter['enable_passwd_cisco'])
                                            index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'], 'denied|incorrect|error', pexpect.TIMEOUT, pexpect.EOF])
                                            if index != 0:
                                                if index == 1:
                                                    cls.f.close()
                                                    cls.child.close()
                                                    raise Exception('%s: telnet login failed, wrong enable password.' % ip)
                                                else:
                                                    cls.f.close()
                                                    cls.child.close()
                                                    raise Exception('%s: telnet login failed, timeout when typing enable password.' % ip)
                                    elif index == 2:
                                        cls.f.close()
                                        cls.child.close()
                                        raise Exception('%s: telnet login failed, wrong username or password, please check it.' % ip)
                                    else:
                                        cls.f.close()
                                        cls.child.close()
                                        raise Exception('%s: telnet login failed, timeout when typing [%s] password.' % (ip, env_parameter['local_user']))

                # 调节设备输出行、列参数，保证抓取信息的准确性
                cls.child.sendline('terminal length 0')
                index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'], pexpect.TIMEOUT, pexpect.EOF])
                if index != 0:
                    cls.f.close()
                    cls.child.close()
                    raise Exception('%s: telnet login failed, timeout when typing initial cmd.' % ip)
                cls.child.sendline('terminal width 0')
                index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'], pexpect.TIMEOUT, pexpect.EOF])
                if index != 0:
                    cls.f.close()
                    cls.child.close()
                    raise Exception('%s: telnet login failed, timeout when typing initial cmd.' % ip)

                # 嵌套具体功能脚本、函数
                def decorator(func):
                    def wrapper(*args, **kw):
                        return func(*args, **kw)

                    return wrapper

                return decorator

                # 脚本执行完毕，关闭log文件
                cls.f.close()
                cls.child.close()
        except Exception:
            print traceback.format_exc()
            print('%s: Some errors occurred when execute command.' % ip)


    @classmethod
    def huawei_login_device(cls, ip, logintime):
        try:
            # 创建telnet登录设备的句柄
            cls.child = pexpect.spawn('telnet %s' % ip, timeout=logintime)
            # 创建一个log文件，记录telnet句柄内所有操作信息
            clock = time.strftime("%Y-%m-%d-%X")
            cls.f = open('%s%s_%s_telnet.log' % (env_parameter['log_dir'], clock, ip), 'w')
            cls.child.logfile_read = cls.f
            index = cls.child.expect(['ogin:|sername:', pexpect.TIMEOUT, pexpect.EOF])
            if index != 0:
                cls.f.close()
                cls.child.close()
                if index == 1:
                    raise Exception('%s: telnet login failed, timeout when login.' % ip)
                else:
                    raise Exception('%s: telnet login failed, refused by remote when logging.' % ip)
            else:
                cls.child.sendline('%s' % env_parameter['aaa_user'])
                index = cls.child.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
                if index != 0:
                    cls.f.close()
                    cls.child.close()
                    raise Exception('%s: telnet login failed, timeout when typing username [%s].' % (ip, env_parameter['aaa_user']))
                else:
                    cls.child.sendline('%s' % env_parameter['aaa_passwd'])
                    time.sleep(1)
                    index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], 'ogin:|sername:', pexpect.TIMEOUT, pexpect.EOF])
                    if index != 0:
                        if index == 1:
                            print('%s :user %s is wrong, trying user netpm.' % (ip, env_parameter['aaa_user']))
                            cls.child.sendline('%s' % env_parameter['local_user'])
                            index = cls.child.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
                            if index != 0:
                                cls.f.close()
                                cls.child.close()
                                raise Exception('%s: telnet login failed, timeout when typing username [%s].' % (ip, env_parameter['local_user']))
                            else:
                                cls.child.sendline('%s' % env_parameter['local_passwd'])
                                time.sleep(1)
                                index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], 'ogin:|sername:', pexpect.TIMEOUT, pexpect.EOF])
                                if index != 0:
                                    if index == 1:
                                        cls.f.close()
                                        cls.child.close()
                                        raise Exception('%s: telnet login failed, wrong username or password, please check it.' % ip)
                                    else:
                                        cls.f.close()
                                        cls.child.close()
                                        raise Exception('%s: telnet login failed, timeout when typing [%s] password.' % (ip, env_parameter['local_user']))
                        else:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('%s :telnet login failed, timeout when typing [%s] password.' % (ip, env_parameter['aaa_user']))

                    cls.child.sendline('undo terminal monitor')
                    index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT, pexpect.EOF])
                    if index != 0:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('%s: telnet login failed, timeout when typing initial cmd.' % ip)
                    cls.child.sendline('screen-length 0 temporary')
                    index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT, pexpect.EOF])
                    if index != 0:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('%s: telnet login failed, timeout when typing initial cmd.' % ip)

                    def decorator(func):
                        def wrapper(*args, **kw):
                            return func(*args, **kw)

                        return wrapper

                    return decorator

                    cls.f.close()
                    cls.child.close()
        except Exception:
            print traceback.format_exc()
            print('%s: Some errors occurred when execute command.' % ip)



    @classmethod
    def h3c_cli(cls, command, style='simple', strict=True):
        output = ''
        if strict == True:
            if type(command) == str or type(command) == unicode:
                cls.child.sendline(command)
                index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'],
                                          'Wrong parameter|System is busy|Unrecognized command|Invalid input|Invalid command|Invalid parameter|Failed to pass the authorization|Too many parameters|syntax error|unknown command|Unrecognized host or address',
                                          'Y/N|y/n', pexpect.TIMEOUT])
                if index != 0:
                    if index == 1:
                        cls.f.close()
                        cls.child.close()
                        raise Exception("Wrong command, kill the progress.")
                    elif index == 2:
                        cls.child.sendline('y')
                        index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT])
                        if index != 0:
                            cls.f.close()
                            cls.child.close()
                            raise Exception("Execute cmd failed, timeout!")
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                            return output
                        else:
                            output1 = cls.child.before
                            if '\r\r\n' in output1:
                                output2 = output1.split('\r\r\n')
                                del output2[0]
                                output2[-1] = output2[-1].strip('\r')
                                for line in output2:
                                    output = output + line + '\r\n'
                                return output
                            else:
                                output2 = output1.split('\r\n')
                                del output2[0]

                                for line in output2:
                                    output = output + line + '\r\n'
                                return output
                    else:
                        cls.f.close()
                        cls.child.close()
                        raise Exception("Execute cmd failed, timeout!")
                else:
                    if style == 'verbose':
                        output1 = cls.child.before
                        output2 = cls.child.after
                        output = output + output1 + output2
                        return output
                    else:
                        output1 = cls.child.before
                        if '\r\r\n' in output1:
                            output2 = output1.split('\r\r\n')
                            del output2[0]
                            output2[-1] = output2[-1].strip('\r')
                            for line in output2:
                                output = output + line + '\r\n'
                            return output
                        else:
                            output2 = output1.split('\r\n')
                            del output2[0]

                            for line in output2:
                                output = output + line + '\r\n'
                            return output
            elif type(command) == list:
                for each in command:
                    cls.child.sendline(each)
                    # time.sleep(1)
                    index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'],
                                              'Wrong parameter|System is busy|Unrecognized command|Invalid input|Invalid command|Invalid parameter|Failed to pass the authorization|Too many parameters|syntax error|unknown command|Unrecognized host or address',
                                              'Y/N|y/n', pexpect.TIMEOUT])
                    if index != 0:
                        if index == 1:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('Wrong command, kill the progress.')
                        elif index == 2:
                            cls.child.sendline('y')
                            index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT])
                            if index != 0:
                                cls.f.close()
                                cls.child.close()
                                raise Exception('Execute cmd failed, timeout!')
                            if style == 'verbose':
                                output1 = cls.child.before
                                output2 = cls.child.after
                                output = output + output1 + output2
                            else:
                                output1 = cls.child.before
                                if '\r\r\n' in output1:
                                    output2 = output1.split('\r\r\n')
                                    del output2[0]
                                    output2[-1] = output2[-1].strip('\r')
                                    for line in output2:
                                        output = output + line + '\r\n'
                                else:
                                    output2 = output1.split('\r\n')
                                    del output2[0]

                                    for line in output2:
                                        output = output + line + '\r\n'
                        else:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('Execute cmd failed, timeout!')
                    else:
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                        else:
                            output1 = cls.child.before
                            if '\r\r\n' in output1:
                                output2 = output1.split('\r\r\n')
                                del output2[0]
                                output2[-1] = output2[-1].strip('\r')
                                for line in output2:
                                    output = output + line + '\r\n'
                            else:
                                output2 = output1.split('\r\n')
                                del output2[0]

                                for line in output2:
                                    output = output + line + '\r\n'
                return output
            else:
                cls.f.close()
                cls.child.close()
                raise Exception('Wrong command, kill the progress.')
        else:
            if type(command) == str or type(command) == unicode:
                cls.child.sendline(command)
                # time.sleep(1)
                index = cls.child.expect(
                    ['%s' % env_parameter['hostname_format_h3c'], 'Y/N|y/n', pexpect.TIMEOUT])
                if index != 0:
                    if index == 1:
                        cls.child.sendline('y')
                        cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT])
                        if index != 0:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('Execute cmd failed, timeout!')
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                            return output
                        else:
                            output1 = cls.child.before
                            if '\r\r\n' in output1:
                                output2 = output1.split('\r\r\n')
                                del output2[0]
                                output2[-1] = output2[-1].strip('\r')
                                for line in output2:
                                    output = output + line + '\r\n'
                                return output
                            else:
                                output2 = output1.split('\r\n')
                                del output2[0]

                                for line in output2:
                                    output = output + line + '\r\n'
                                return output
                    else:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('Execute failed, timeout!')
                else:
                    if style == 'verbose':
                        output1 = cls.child.before
                        output2 = cls.child.after
                        output = output + output1 + output2
                        return output
                    else:
                        output1 = cls.child.before
                        if '\r\r\n' in output1:
                            output2 = output1.split('\r\r\n')
                            del output2[0]
                            output2[-1] = output2[-1].strip('\r')
                            for line in output2:
                                output = output + line + '\r\n'
                            return output
                        else:
                            output2 = output1.split('\r\n')
                            del output2[0]

                            for line in output2:
                                output = output + line + '\r\n'
                            return output
            elif type(command) == list:
                for each in command:
                    cls.child.sendline(each)
                    # time.sleep(1)
                    index = cls.child.expect(
                        ['%s' % env_parameter['hostname_format_h3c'], 'Y/N|y/n', pexpect.TIMEOUT])
                    if index != 0:
                        if index == 1:
                            cls.child.sendline('y')
                            index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT])
                            if index != 0:
                                cls.f.close()
                                cls.child.close()
                                raise Exception('Execute cmd failed, timeout!')
                            if style == 'verbose':
                                output1 = cls.child.before
                                output2 = cls.child.after
                                output = output + output1 + output2
                            else:
                                output1 = cls.child.before
                                if '\r\r\n' in output1:
                                    output2 = output1.split('\r\r\n')
                                    del output2[0]
                                    output2[-1] = output2[-1].strip('\r')
                                    for line in output2:
                                        output = output + line + '\r\n'
                                else:
                                    output2 = output1.split('\r\n')
                                    del output2[0]

                                    for line in output2:
                                        output = output + line + '\r\n'
                        else:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('Execute failed, timeout!')
                    else:
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                        else:
                            output1 = cls.child.before
                            if '\r\r\n' in output1:
                                output2 = output1.split('\r\r\n')
                                del output2[0]
                                output2[-1] = output2[-1].strip('\r')
                                for line in output2:
                                    output = output + line + '\r\n'
                            else:
                                output2 = output1.split('\r\n')
                                del output2[0]

                                for line in output2:
                                    output = output + line + '\r\n'
                return output
            else:
                cls.f.close()
                cls.child.close()
                raise Exception('Wrong command, kill the progress')

    @classmethod
    #命令行的参数有两种：
    # 1）单个命令使用str形式传参
    # 2）多个命令使用list形式传参
    #执行命令后返回的回显信息有两种：
    # 1）simple，只返回回显内容
    # 2）verbose，返回回显内容为完整内容，带命令行和hostname#
    #执行命令后报错的处理方式有两种：
    # 1）True，一旦执行命令报错，立即返回错误信息，并结束该句柄
    # 2）False，执行命令报错后，只返回错误信息，继续执行句柄内容
    def cisco_cli(cls, command, style='simple', strict=True):
        output = ''
        # True模式
        if strict == True:
            # 单命令传参模式
            if type(command) == str or type(command) == unicode:
                cls.child.sendline(command)
                # time.sleep(1)
                index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'],
                                          'Wrong parameter|System is busy|Unrecognized command|Invalid input|Invalid command|Invalid parameter|Failed to pass the authorization|Too many parameters|syntax error|unknown command|Unrecognized host or address',
                                          'Y/N|y/n', pexpect.TIMEOUT])
                if index != 0:
                    # 输入命令报错直接关闭log文件，返回错误消息
                    if index == 1:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('Wrong command, kill the progress')
                    # 如果需要选择交互，默认选择Y
                    elif index == 2:
                        cls.child.sendline('y')
                        index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'], pexpect.TIMEOUT])
                        if index != 0:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('Execute cmd failed, timeout!')
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                            return output
                        else:
                            output1 = cls.child.before
                            output2 = output1.split('\r\n')
                            del output2[0]

                            for line in output2:
                                output = output + line + '\r\n'
                            return output
                    # 出现超时后，直接关闭log文件，返回错误消息
                    else:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('execute failed, timeout!')
                # 执行命令后一切正常
                else:
                    # verbose模式
                    if style == 'verbose':
                        output1 = cls.child.before
                        output2 = cls.child.after
                        output = output + output1 + output2
                        return output
                    # simple模式
                    else:
                        output1 = cls.child.before
                        output2 = output1.split('\r\n')
                        del output2[0]

                        for line in output2:
                            output = output + line + '\r\n'
                        return output
            # 多命令传参模式
            elif type(command) == list:
                for each in command:
                    cls.child.sendline(each)
                    # time.sleep(1)
                    index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'],
                                              'Wrong parameter|System is busy|Unrecognized command|Invalid input|Invalid command|Invalid parameter|Failed to pass the authorization|Too many parameters|syntax error|unknown command|Unrecognized host or address',
                                              'Y/N|y/n', pexpect.TIMEOUT])
                    if index != 0:
                        if index == 1:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('Wrong command, kill the progress')
                        elif index == 2:
                            cls.child.sendline('y')
                            index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'], pexpect.TIMEOUT])
                            if index != 0:
                                cls.f.close()
                                cls.child.close()
                                raise Exception('Execute cmd failed, timeout!')
                            if style == 'verbose':
                                output1 = cls.child.before
                                output2 = cls.child.after
                                output = output + output1 + output2
                            else:
                                output1 = cls.child.before
                                output2 = output1.split('\r\n')
                                del output2[0]

                                for line in output2:
                                    output = output + line + '\r\n'
                        else:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('Execute failed, timeout!')
                    else:
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                        else:
                            output1 = cls.child.before
                            output2 = output1.split('\r\n')
                            del output2[0]

                            for line in output2:
                                output = output + line + '\r\n'
                return output
            else:
                cls.f.close()
                cls.child.close()
                raise Exception('Wrong command, kill the progress')
        # False模式
        else:
            if type(command) == str or type(command) == unicode:
                cls.child.sendline(command)
                # time.sleep(1)
                index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'], 'Y/N|y/n', pexpect.TIMEOUT])
                if index != 0:
                    if index == 1:
                        cls.child.sendline('y')
                        index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'], pexpect.TIMEOUT])
                        if index != 0:
                            cls.f.close()
                            cls.child.close()
                            raise Exception("Execute cmd failed, timeout!")
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                            return output
                        else:
                            output1 = cls.child.before
                            output2 = output1.split('\r\n')
                            del output2[0]

                            for line in output2:
                                output = output + line + '\r\n'
                            return output
                    else:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('Execute failed, timeout!')
                else:
                    if style == 'verbose':
                        output1 = cls.child.before
                        output2 = cls.child.after
                        output = output + output1 + output2
                        return output
                    else:
                        output1 = cls.child.before
                        output2 = output1.split('\r\n')
                        del output2[0]

                        for line in output2:
                            output = output + line + '\r\n'
                        return output
            elif type(command) == list:
                for each in command:
                    cls.child.sendline(each)
                    # time.sleep(1)
                    index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'], 'Y/N|y/n', pexpect.TIMEOUT])
                    if index != 0:
                        if index == 1:
                            cls.child.sendline('y')
                            index = cls.child.expect(['%s' % env_parameter['hostname_format_cisco1'], pexpect.TIMEOUT])
                            if index != 0:
                                cls.f.close()
                                cls.child.close()
                                raise Exception("Execute cmd failed, timeout!")
                            if style == 'verbose':
                                output1 = cls.child.before
                                output2 = cls.child.after
                                output = output + output1 + output2
                            else:
                                output1 = cls.child.before
                                output2 = output1.split('\r\n')
                                del output2[0]

                                for line in output2:
                                    output = output + line + '\r\n'
                        else:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('Execute failed, timeout!')
                    else:
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                        else:
                            output1 = cls.child.before
                            output2 = output1.split('\r\n')
                            del output2[0]

                            for line in output2:
                                output = output + line + '\r\n'
                return output
            else:
                cls.f.close()
                cls.child.close()
                raise Exception('Wrong command, kill the progress')

    @classmethod
    def huawei_cli(cls, command, style='simple', strict=True):
        output = ''
        if strict == True:
            if type(command) == str or type(command) == unicode:
                cls.child.sendline(command)
                # time.sleep(1)
                index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'],
                                          'Wrong parameter|System is busy|Unrecognized command|Invalid input|Invalid command|Invalid parameter|Failed to pass the authorization|Too many parameters|syntax error|unknown command|Unrecognized host or address',
                                          'Y/N|y/n', pexpect.TIMEOUT])
                if index != 0:
                    if index == 1:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('Wrong command, kill the progress')
                    elif index == 2:
                        cls.child.sendline('y')
                        index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT])
                        if index != 0:
                            cls.f.close()
                            cls.child.close()
                            raise Exception("Execute cmd failed, timeout!")
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                            return output
                        else:
                            output1 = cls.child.before
                            output2 = output1.split('\r\n')
                            del output2[0]

                            for line in output2:
                                output = output + line + '\r\n'
                            return output
                    else:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('Execute failed, timeout!')
                else:
                    if style == 'verbose':
                        output1 = cls.child.before
                        output2 = cls.child.after
                        output = output + output1 + output2
                        return output
                    else:
                        output1 = cls.child.before
                        output2 = output1.split('\r\n')
                        del output2[0]

                        for line in output2:
                            output = output + line + '\r\n'
                        return output
            elif type(command) == list:
                for each in command:
                    cls.child.sendline(each)
                    # time.sleep(1)
                    index = cls.child.expect(['%s' % env_parameter['hostname_format_h3c'],
                                              'Wrong parameter|System is busy|Unrecognized command|Invalid input|Invalid command|Invalid parameter|Failed to pass the authorization|Too many parameters|syntax error|unknown command|Unrecognized host or address',
                                              'Y/N|y/n', pexpect.TIMEOUT])
                    if index != 0:
                        if index == 1:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('Wrong command, kill the progress')
                        elif index == 2:
                            cls.child.sendline('y')
                            index = cls.child.expect(
                                ['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT])
                            if index != 0:
                                cls.f.close()
                                cls.child.close()
                                raise Exception("Execute cmd failed, timeout!")
                            if style == 'verbose':
                                output1 = cls.child.before
                                output2 = cls.child.after
                                output = output + output1 + output2
                            else:
                                output1 = cls.child.before
                                output2 = output1.split('\r\n')
                                del output2[0]

                                for line in output2:
                                    output = output + line + '\r\n'
                        else:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('Execute failed, timeout!')
                    else:
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                        else:
                            output1 = cls.child.before
                            output2 = output1.split('\r\n')
                            del output2[0]

                            for line in output2:
                                output = output + line + '\r\n'
                return output
            else:
                cls.f.close()
                cls.child.close()
                raise Exception('Wrong command, kill the progress')

        else:
            if type(command) == str or type(command) == unicode:
                cls.child.sendline(command)
                index = cls.child.expect(
                    ['%s' % env_parameter['hostname_format_h3c'], 'Y/N|y/n', pexpect.TIMEOUT])
                if index != 0:
                    if index == 1:
                        cls.child.sendline('y')
                        index = cls.child.expect(
                            ['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT])
                        if index != 0:
                            cls.f.close()
                            cls.child.close()
                            raise Exception("Execute cmd failed, timeout!")
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                            return output
                        else:
                            output1 = cls.child.before
                            output2 = output1.split('\r\n')
                            del output2[0]

                            for line in output2:
                                output = output + line + '\r\n'
                            return output
                    else:
                        cls.f.close()
                        cls.child.close()
                        raise Exception('Execute failed, timeout!')
                else:
                    if style == 'verbose':
                        output1 = cls.child.before
                        output2 = cls.child.after
                        output = output + output1 + output2
                        return output
                    else:
                        output1 = cls.child.before
                        output2 = output1.split('\r\n')
                        del output2[0]

                        for line in output2:
                            output = output + line + '\r\n'
                        return output
            elif type(command) == list:
                for each in command:
                    cls.child.sendline(each)
                    # time.sleep(1)
                    index = cls.child.expect(
                        ['%s' % env_parameter['hostname_format_h3c'], 'Y/N|y/n', pexpect.TIMEOUT])
                    if index != 0:
                        if index == 1:
                            cls.child.sendline('y')
                            index = cls.child.expect(
                                ['%s' % env_parameter['hostname_format_h3c'], pexpect.TIMEOUT])
                            if index != 0:
                                cls.f.close()
                                cls.child.close()
                                raise Exception("Execute cmd failed, timeout!")
                            if style == 'verbose':
                                output1 = cls.child.before
                                output2 = cls.child.after
                                output = output + output1 + output2
                            else:
                                output1 = cls.child.before
                                output2 = output1.split('\r\n')
                                del output2[0]

                                for line in output2:
                                    output = output + line + '\r\n'
                        else:
                            cls.f.close()
                            cls.child.close()
                            raise Exception('Execute failed, timeout!')
                    else:
                        if style == 'verbose':
                            output1 = cls.child.before
                            output2 = cls.child.after
                            output = output + output1 + output2
                        else:
                            output1 = cls.child.before
                            output2 = output1.split('\r\n')
                            del output2[0]

                            for line in output2:
                                output = output + line + '\r\n'
                return output
            else:
                cls.f.close()
                cls.child.close()
                raise Exception('Wrong command, kill the progress')

