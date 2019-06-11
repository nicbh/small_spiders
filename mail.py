import os, time, platform
platform_info = platform.platform()
if 'Linux' in platform_info:
    platform_info = 'linux'
elif 'Darwin' in platform_info:
    platform_info = 'macos'
print('start at {}'.format(time.asctime(time.localtime(time.time()))))
ip_list = []
ip_name = {}
with open('ip_list', 'r', encoding='utf-8') as file:
    for line in file:
        line=line.strip()
        if len(line)==0 or line.startswith('#'):
            continue
        if '#' in line:
            line=line[0:line.find('#')].strip()
        name, ip, port = line.split()[0:3]
        hostname = '{} {}'.format(ip,port)
#        if '#' in line:
#            ip = line[0:line.find('#')].strip()
#            name = line[line.find('#') + 1:].strip()
#            name = name[0:name.find('/')].strip()
        ip_name[hostname] = name
        ip_list.append(hostname)
lost_list = []
for hostname in ip_list:
    ip, port = hostname.split()
    response = os.system("nc -w 1 -z -v {} {}".format(ip, port))
    if response != 0:
        lost_list.append(hostname)
ip_list = lost_list
lost_list = []
for hostname in ip_list:
    ip, port = hostname.split()
    for i in range(3):
        response = os.system("nc -w 20 -z -v {} {}".format(ip, port))
        if response == 0:
            break
    if response != 0:
        lost_list.append(hostname)
print('lost ip list: ', lost_list)
# lost_list = []
# acc_list=['34.83.227.169 46736','172.96.244.152 29312','104.238.149.58 14309']
# tmp=set(lost_list).difference(acc_list)
# acc_list=set(acc_list).difference(lost_list)
# lost_list=tmp

if len(lost_list) > 0: # or len(acc_list)!=0:
    txt = 'ip {} is unconnected at {}'.format(', '.join(["{}({})".format(ip, ip_name[ip]) for ip in lost_list]), time.asctime(time.localtime(time.time())))
    from email import encoders
    from email.header import Header
    from email.mime.text import MIMEText
    from email.utils import parseaddr, formataddr
    import smtplib

    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    from_addr = '642374509@qq.com' 
    apuwtdh = 'nmxtrhcsdxthbcch'
    to_addr = '642374509@qq.com'
    smtp_server = 'smtp.qq.com'

    msg = MIMEText(txt, 'plain', 'utf-8')
    msg['From'] = 'Ping_Robot <%s>' % from_addr
    msg['To'] = 'Admin <%s>' % to_addr
    msg['Subject'] = 'ip ping warning'

    server = smtplib.SMTP_SSL(smtp_server)
    server.login(from_addr, apuwtdh)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
print('end at {}'.format(time.asctime(time.localtime(time.time()))))
print('------------------------')
