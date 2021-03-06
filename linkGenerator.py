import os
import base64
import datetime
import json


def b_encode(string, do_strip=False):
    result = base64.urlsafe_b64encode(string.encode('utf-8')).decode('utf-8')
    if do_strip is True:
        result = result.strip('=')
    return result


# v2ray code
datestr = '-{:0>2}{:0>2}'.format(datetime.datetime.now().month,
                                 datetime.datetime.now().day)
links = []
proxies = []
with open('ip_list', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if len(line) == 0 or line.startswith('#'):
            continue
        item_list = line.split()
        if len(item_list) != 8:
            continue
        j_ps, j_add, j_port, j_aid, j_method, j_host, j_path, j_id = item_list
        if '/' in j_ps:
            j_ps = j_ps[0:j_ps.find('/')].strip()
        index = j_ps.find('(')
        if index == -1:
            j_ps += datestr
        else:
            j_ps = j_ps[0:index] + datestr + j_ps[index:]
        v2rayNobject = {
            'v': '2',
            'ps': j_ps,
            'add': j_add,
            'port': j_port,
            'id': j_id,
            'aid': j_aid,
            'net': j_method,
            'type': 'none',
            'host': j_host if j_host == j_add else '',
            'path': j_path if j_path and j_method != 'tcp' else '',
            'tls': 'tls' if j_method != 'tcp' else 'none'
        }
        v2rayNjson = json.dumps(v2rayNobject, ensure_ascii=False, indent=2)
        # print(v2rayNjson)
        v2rayNlink = 'vmess://{}'.format(b_encode(v2rayNjson, False))
        links.append(v2rayNlink)
        proxies.append(v2rayNobject)

with open('link', 'w+', encoding='utf-8') as file:
    file.write(b_encode('\n'.join(links), False))
with open('raw_link', 'w+', encoding='utf-8') as file:
    file.write('\n'.join(links))

from clash import toClash
with open('clash', 'w+', encoding='utf-8') as file:
    file.write(toClash(proxies))

# ssr code
# # port = '2333'
# protocol = 'origin'
# smethod = 'aes-256-cfb'
# obfs = 'plain'
# group = b_encode('zmgay')
# password = b_encode('qawsedrftgyh')
# datestr = '-{:0>2}{:0>2}'.format(datetime.datetime.now().month, datetime.datetime.now().day)
# links = []
# with open('ip_list','r',encoding='utf-8') as file:
# 	for line in file:
# 		line = line.strip()
# 		if len(line) == 0 or line.startswith('#'):
# 			continue
# 		item_list = line.split()
# 		if len(item_list)!=3:
# 			continue
# 		nodeName, ipAddr, port = item_list
# 		index = nodeName.find('(')
# 		if index == -1:
# 			nodeName += datestr
# 		else:
# 			nodeName = nodeName[0:index] + datestr + nodeName[index:]
# 		if len(ipAddr) == 0:
# 			continue
# 		remarks = b_encode(nodeName)
# 		ssrLink = '{}:{}:{}:{}:{}:{}/?obfsparam=&protoparam=&remarks={}&group={}'.format(ipAddr, port, protocol, smethod, obfs, password, remarks, group)
# 		# print(ssrLink)
# 		ssrLink = 'ssr://{}'.format(b_encode(ssrLink, True))
# 		links.append(ssrLink)
# with open('link_list', 'w+', encoding='utf-8') as file:
# 	file.write(b_encode('\n'.join(links), False))
