import json
import time
from bs4 import BeautifulSoup
from collections import OrderedDict
from doubanMovie_py3 import getHtml, getTime, filehome

if __name__ == '__main__':
    print('cbo running')
    filehome += 'cbo/'
    with open(filehome + 'cbolog.txt', 'a') as log:
        log.write('Retrieve Start at ' + getTime() + '\n')
        try:
            timestamp = time.time()
            url = 'www.cbooo.cn/BoxOffice/GetHourBoxOffice?d=%d' % timestamp
            html = getHtml(url, log, True, False)
            items = json.loads(html)  # , object_pairs_hook=OrderedDict)
            lst = []
            infos = OrderedDict()
            timestr = getTime(timestamp)
            item = OrderedDict()
            item['name'] = 'sum'
            item['sum'] = items['data1'][0]['sumBoxOffice']
            item['time'] = timestr
            lst.append(item)
            for l in items['data2']:
                item = OrderedDict()
                item['name'] = l['MovieName']
                item['boxoffice'] = l['BoxOffice']
                item['boxper'] = l['boxPer']
                item['day'] = l['movieDay']
                item['sum'] = l['sumBoxOffice']
                item['time'] = timestr
                lst.append(item)
            infos['list'] = lst
            log.write('Start to record\n')
            filename = getTime()
            filename = filename[:filename.find(' ')] + '.txt'
            with open(filehome + filename, 'a') as f:
                for i in lst:
                    f.write(json.dumps(i, ensure_ascii=False) + '\n')
                f.write('\n')
            log.write('Record success\n')

        except requests.exceptions.ConnectionError as e:
            log.write('Error: Network Connection Error. ' + getTime() + '\n')
            print(e)
        log.write('Retrieve Finish at ' + getTime() + '\n\n')
    print(getTime())
    print()
