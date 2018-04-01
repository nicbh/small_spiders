import os, base64
def b_encode(string):
	return base64.urlsafe_b64encode(string.encode('utf-8')).decode('utf-8').strip('=')
port = '2333'
protocol = 'origin'
smethod = 'aes-256-cfb'
obfs = 'plain'
password = b_encode('qawsedrftgyh')

links = []
with open('ip_list','r',encoding='utf-8') as file:
	for line in file:
		line = line.strip()
		ipAddr = line
		nodeName = ''
		if '#' in line:
			ipAddr = line[0:line.find('#')].strip()
			nodeName = line[line.find('#') + 1:].strip()
		if len(ipAddr) == 0:
			continue
		remarks = b_encode(nodeName)
		ssrLink = '{}:{}:{}:{}:{}:{}/?obfsparam=&protoparam=&remarks={}&group='.format(ipAddr, port, protocol, smethod, obfs, password, remarks)
		ssrLink = 'ssr://{}'.format(b_encode(ssrLink))
		links.append(ssrLink)
with open('link_list', 'w+', encoding='utf-8') as file:
	file.write('\n'.join(links))
 		