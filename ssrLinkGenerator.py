import os, base64, datetime
def b_encode(string, do_strip=True):
	result = base64.urlsafe_b64encode(string.encode('utf-8')).decode('utf-8')
	if do_strip is True:
		result = result.strip('=')
	return result
# port = '2333'
protocol = 'origin'
smethod = 'aes-256-cfb'
obfs = 'plain'
group = b_encode('zmgay')
password = b_encode('qawsedrftgyh')
datestr = '{:0>2}{:0>2}'.format(datetime.datetime.now().month, datetime.datetime.now().day)
links = []
with open('ip_list','r',encoding='utf-8') as file:
	for line in file:
		line = line.strip()
		ipAddr = line
		nodeName = ''
		if '#' in line:
			ipAddr = line[0:line.find('#')].strip()
			if len(ipAddr) == 0:
				continue
			ipAddr, port = ipAddr.split()
			nodeName = line[line.find('#') + 1:].strip()
			if '/' in nodeName:
				nodeName = nodeName[0:nodeName.find('/')].strip()
		index = nodeName.find('(')
		if index == -1:
			nodeName += datestr
		else:
			nodeName = nodeName[0:index] + datestr + nodeName[index:]
		if len(ipAddr) == 0:
			continue
		remarks = b_encode(nodeName)
		ssrLink = '{}:{}:{}:{}:{}:{}/?obfsparam=&protoparam=&remarks={}&group={}'.format(ipAddr, port, protocol, smethod, obfs, password, remarks, group)
		# print(ssrLink)
		ssrLink = 'ssr://{}'.format(b_encode(ssrLink))
		links.append(ssrLink)
with open('link_list', 'w+', encoding='utf-8') as file:
	file.write(b_encode('\n'.join(links), False))
 		
