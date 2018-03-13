
import os, time
ip_list = []
with open('ip_list', 'r', encoding='utf-8') as file:
	for line in file:
		ip_list.append(line.strip())
lost_list = []
for hostname in ip_list:
	response = os.system("ping -c 1 " + hostname)
	if response != 0:
		lost_list.append(hostname)
ip_list = lost_list
lost_list = []
for hostname in ip_list:
	response = os.system("ping -c 5 " + hostname)
	if response != 0:
		lost_list.append(hostname)
print('lost ip list: ', lost_list)
if len(lost_list) > 0:
	txt = 'ip {} is unconnected at {}'.format(', '.join(["'{}'".format(ip) for ip in lost_list]), time.asctime(time.localtime(time.time())))
	from email import encoders
	from email.header import Header
	from email.mime.text import MIMEText
	from email.utils import parseaddr, formataddr
	import smtplib

	def _format_addr(s):
	    name, addr = parseaddr(s)
	    return formataddr((Header(name, 'utf-8').encode(), addr))

	from_addr = '18085133818@163.com' 
	auth = 'wangyi163'
	to_addr = '642374509@qq.com'
	smtp_server = 'smtp.163.com'

	msg = MIMEText(txt, 'plain', 'utf-8')
	msg['From'] = _format_addr('Ping Robot <%s>' % from_addr)
	msg['To'] = _format_addr('Admin <%s>' % to_addr)
	msg['Subject'] = Header('ip ping warning', 'utf-8').encode()

	server = smtplib.SMTP(smtp_server, 25)
	server.set_debuglevel(1)
	server.login(from_addr, auth)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()