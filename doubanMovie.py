#! /usr/bin/env python
# coding=utf-8
import urllib2, sys, re, json, time, ssl, platform
from collections import OrderedDict


def getTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


# reload(sys)
# sys.setdefaultencoding('utf-8')
filehome = ''
if (platform.system() == "Linux"):
    filehome = '/mnt/file/doubanMovie/'
while True:
    with open(filehome + 'log.txt', 'a') as log:
        log.write('Retrieve Start at ' + getTime() + '\n')


        def getHtml(url):
            'get html from url and write log'
            host = url.find('/')
            if host > 0:
                host = url[:host]
            else:
                host = url
            req_header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'Accept-Charset': 'utf-8',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'host': host,
                'Referer': None
            }

            req_timeout = 5
            req = urllib2.Request('https://' + url, None, req_header)
            for times in range(5):
                try:
                    time.sleep(0.1)
                    log.write('Try to connect ' + url + ' : ')
                    resp = urllib2.urlopen(req, None, req_timeout)
                    log.write('success.\n')
                    break
                except (urllib2.URLError, ssl.SSLError) as e:
                    log.write('failed.\n')
                    print e
            else:
                raise urllib2.URLError, '5 timeout'
            html = resp.read().strip()
            return html


        try:
            p1 = re.compile(r'<li class="title">[\s\S]*?</li>')
            movies = p1.findall(getHtml('movie.douban.com'))
            movie = []
            for m in movies:
                p = re.compile(r'(?<=subject/)\d+')
                movie.append(p.findall(m)[0])
            infos = []
            for m in movie:
                html = getHtml('movie.douban.com/subject/' + m)
                p = re.compile(r'<h1>\s*<span property="v:itemreviewed">[\s\S]*?<div id="interest_sect_level"')
                item = p.findall(html)[0]
                p = re.compile(r'property="v:average">.*?</')
                p1 = re.compile(r'\d')
                ttt=p.findall(item)
                if len(p1.findall(ttt[0])) > 0:
                    info = OrderedDict()
                    info['no'] = m
                    p = re.compile(r'<h1>[\s\S]*?</h1>')
                    item1 = p.findall(item)[0]
                    p1 = re.compile(r'(?<=.">)[\s\S]*?(?=</)')
                    result = p1.findall(item1)
                    aaaaa = result[0]
                    print aaaaa
                    info['name'] = result[0]
                    info['year'] = result[1][1:-1]
                    p = re.compile(r'<span property="v:initialReleaseDate"[\s\S]*?</span><br/>')
                    temp = p1.findall(p.findall(item)[0])
                    item1 = '/'.join(temp)
                    info['release'] = item1
                    p = re.compile(r'<div id="interest_sectl">[\s\S]*?<div id="interest_sect_level"')
                    item = p.findall(item)[0]
                    p = re.compile(r'average">.*?<')
                    p1 = re.compile(r'\d+\.\d+')
                    info['average'] = p1.findall(p.findall(item)[0])[0]
                    p = re.compile(r'votes">\d*?<')
                    p1 = re.compile(r'\d+')
                    info['sum'] = p1.findall(p.findall(item)[0])[0]
                    p = re.compile(r'<span class="stars5[\s\S]*?<br />\s*</div>')
                    item = p.findall(item)[0]
                    p = re.compile(r'\d+\.\d+%')
                    info['rate_level'] = p.findall(item)
                    info['time'] = getTime()
                    infos.append(info)
            log.write('Start to record\n')
            filename = getTime()
            filename = filename[:filename.find(' ')] + '.txt'
            with open(filehome + filename, 'a') as f:
                for i in infos:
                    f.write(json.dumps(i, ensure_ascii=False) + '\n')
                f.write('\n')
        except IndexError as e:
            log.write('Error: Regex Format Wrong. ' + getTime() + '\n')
            print e
        except urllib2.URLError as e:
            log.write('Error: Network Connection Error. ' + getTime() + '\n')
            print e
        log.write('Retrieve Finish at ' + getTime() + '\n\n')
    time.sleep(3600)
