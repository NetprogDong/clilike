# clilike

clilike是一款基于python语言实现与终端设备交互的工具。对于配置、交互手段不丰富、不灵活的设备，如：路由器、交换机等，此工具不失为一方良药。

顾名思义，clilike的使用就像工程师以cli方式登陆对设备进行操作一样方便、可控。除此之外，clilike支持批量、并行化操作，将此工具运用到大规模网络运维工作中，能够大大提高运维效率，减少误操作率。

clilike使用pexpect模块，可模拟telnet、ssh等多种设备登陆方式。当前版本clilike仅支持telnet登陆方式，且仅支持h3c、huawei、cisco设备。

### 环境参数

该工具需要先设置环境参数，用以适应你的网络环境。该环境参数的设置文件为profile.py，需要设置的参数以python字典的形式存放，字典中每个key代表一类参数，每个key对应的value即为需要设置的参数值，参数值均为字符串。

```python
env_parameter = {
                  'log_dir' : '/Users/dong/Desktop/clilikelog/',
                  'aaa_user' : 'aaa_username',
                  'aaa_passwd' : 'aaa_userpassword',
                  'local_user' : 'local_username',
                  'local_passwd' : 'local_userpassowrd',
                  'enable_passwd_cisco' : 'enable_password',
                  'hostname_format_h3c' : '\r\n(<|\[)([^\n]+(-|\.|_)){3}[^\n]+(>|\])',
                  'hostname_format_cisco1' : '\r\n([^\n]+(-|\.|_)){3}[^\n]+#',
                  'hostname_format_cisco2' : '\r\n([^\n]+(-|\.|_)){3}[^\n]+>',

                  }
```

下面我会一一列举需要设置的参数并加以解释：  
* log存放路径  
clilike每次登陆操作设备都会自动创建log文件，用来记录所有的操作，便于后续查阅、溯源及排障。对应的key为'log_dir'，例子中的log路径为'/Users/dong/Desktop/clilikelog/'，意思是在该服务器上的所有clilike发起的登录及后续操作产生的log文件都会存储在该log路径下。  
* 登录用户名&密码  
  - 登录用户分为aaa用户和本地用户，执行逻辑为顺序尝试登录，即优先使用aaa用户登录，如果登录失败再使用local用户登录。
  - 若你的网络运维环境中只存在上述一种用户，那么另外一种用户及密码值可忽略。
  - key为'enable_passwd_cisco'的值为思科设备的enable密码，如果网络中不存在思科设备或不需要enable密码进行登录的可忽略。
* 行匹配符  
clilike工具需要被操作端的返回信息来做成功执行命令的判断，因此需要一个特定且每次执行命令都会返回的一串固定的字符串，这里叫做行匹配符。  
行匹配符分为两种：
  - 设备登陆过程的行匹配符：该类行匹配符均已在底层写好，用户无需关注。
  - 设备执行命令过程的行匹配符：该类行匹配符需要用户根据自身网络设备命名来自行编写。  
    该类行匹配符由网络设备的hostname/sysname与特定的字符共同组成。  
    对应的key为'hostname_format_h3c','hostname_format_cisco1','hostname_format_cisco2'。

### 举例

* 华三、华为设备，sysname为LEAF1.P1.G1.YF，那么要匹配的回显行字符串包括但不限于如下  
```
"<LEAF1.P1.G1.YF>"或
"[LEAF1.P1.G1.YF]"或
"[LEAF1.P1.G1.YF-Ten-GigabitEthernet1/0/45]"或
"[LEAF1.P1.G1.YF-bgp-default]"等等。
```
本工具使用正则表达式来做行匹配符，那么只要你的网络设备的sysname满足如下条件，即可直接使用代码中提供的'hostname_format_h3c'对应的value，如果不满足如下条件，需要自行编写行匹配符。  
  - 条件1  
  sysname满足至少有3个'.'字符。  
  例如：LEAF1.P1.G1.YF  
  - 条件2  
  sysname满足至少有3个'-'字符。  
  例如：LEAF1-P1-G1-YF  
  - 条件3  
  sysname满足至少有3个'\_'字符。  
  例如：LEAF1\_P1\_G1\_YF  
* 思科设备  
思科有两个行匹配符，也使用正则表达式来匹配行匹配符，区别仅在于最后一位字符是'>'还是'#'。  
只要你的网络设备的hostname满足如下条件，即可直接使用代码中提供的'hostname_format_cisco1'和'hostname_format_cisco2'对应的value，如果不满足如下条件，需要自行编写行匹配符。  
  - 条件1  
  hostname满足至少有3个'.'字符。  
  例如：LEAF1.P1.G1.YF  
  - 条件2  
  hostname满足至少有3个'-'字符。  
  例如：LEAF1-P1-G1-YF  
  - 条件3  
  hostname满足至少有3个'\_'字符。  
  例如：LEAF1\_P1\_G1\_YF  

### 方法&功能  
clilike提供了设备登陆方法以及执行命令方法：  
* 设备登陆方法  
提供了h3c、cisco、huawei3种设备的telnet登陆方法。  
即调用装饰器函数  
```python
@devopstools.h3c_login_device(’10.100.100.1‘, 720)
@devopstools.cisco_login_device(’10.100.100.1‘, 720)
@devopstools.huawei_login_device(’10.100.100.1‘, 720)
```
其中，两个参数  
1)'10.100.100.1'：数据类型为字符串，即为所要登陆的设备ip。  
2)720：数据类型为整数，即为该session的超时时间，单位为秒，超时后session中断并返回超时提醒。
tips:  
由于登陆方法通过装饰器函数实现，因此登陆后对设备进行的一切执行命令的过程全部放在装饰器函数所要装饰的函数中。见test.py中的show_ip_interf()函数。
```python
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
```
* 设备执行命令方法  
提供了h3c、cisco、huawei3种设备执行命令的方法  
例如：
```python
devopstools.h3c_cli('display ip int brief')
devopstools.cisco_cli(['show ip interface brief', 'show arp'])
devopstools.huawei_cli(['display ip interface brief', 'display cu'])
```
执行的命令即为传入的参数，其中参数为列表的会依次执行列表中的元素，用以实现一次执行多条命令。  
该方法还会返回执行命令后的设备回显，返回回显信息数据类型为字符串。  
```python
output = devopstools.h3c_cli('display ip int brief')
print output
```

### 差错控制
* session超时  
  - 引起session超时的原因：  
    1)设备不可达  
    2)回显始终未匹配到行匹配符  
  - 差错控制机制  
    超时后，会在终端打印相关错误信息，并结束该session。
* 设备拒绝登陆  
  - 引起拒绝登陆的原因：  
    1)设备由于安全策略或自身配置导致拒绝登陆  
    2)用户名或密码错误
  - 差错控制机制  
    拒绝登陆出现后，会在终端打印相关错误信息，并结束该session。
* 执行命令错误  
执行命令一旦返回报错回显信息，有两种动作，通过执行命令方法的参数strict控制：  
  - strict = 'True'，默认值  
  只要出现命令错误提示回显，则立即结束该session，并且在终端打印错误信息。  
  - strict = 'False'  
  出现命令错误提示回显后，只在终端打印错误信息，并继续执行程序。
  ```python
  output = devopstools.h3c_cli('display ip int brief', strict = True)
  output = devopstools.cisco_cli(['show ip interface brief', 'show arp'], strict = False)
  ```

### 异步并行  
通过multiprocessing模块进行异步并行操作，主体思路就是先定义好登陆设备后的操作设备的函数方法，最后通过异步函数p.apply_async()调用设备操作函数。  
详见例子代码：test_async.py  


### 简易实践  
详见如下文件：  
* test.py
* test_async.py


  
