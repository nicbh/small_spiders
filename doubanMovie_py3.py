import requests
import json
import re
import time
import traceback
import platform
from bs4 import BeautifulSoup
from collections import OrderedDict

filehome = ""
if platform.system() == "Linux":
    filehome = "/root/data/files/"


def getTime(timestamp=time.time()):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


def getHtml(url, log, isjson=False, isssl=True):
    "get html from url and write log"
    host = url.find("/")
    if host > 0:
        host = url[:host]
    else:
        host = url
    req_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Accept-Charset": "utf-8",
        "Accept": "text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Accept-Encoding": "gzip",
        "Connection": "keep-alive",
        "host": host,
        "Referer": null
    }

    req_timeout = 20
    if isssl:
        url = "https://" + url
    else:
        url = "http://" + url
    if isjson:
        req_header["X-Requested-With"] = "XMLHttpRequest"
    for times in range(8):
        try:
            time.sleep(0.8)
            log.write("Try to connect " + url + " : ")
            resp = requests.get(url, headers=req_header, timeout=req_timeout)
            log.write("success.\n")
            html = resp.text
            break
        except requests.exceptions.ConnectionError as e:
            log.write("failed.\n")
            time.sleep(times)
            print(e)
            # traceback.print_exc()
    else:
        raise requests.exceptions.ConnectionError("5 timeout")
    return html


def getSoup(url, log, isjson=False, isssl=True):
    "get BeautifulSoup from url and write log"
    html = getHtml(url, log, isjson=isjson, isssl=isssl)
    return BeautifulSoup(html, "html.parser")

if __name__ == "__main__":
    print("dm running")

    filehome += "doubanMovie/"
    with open(filehome + "log.txt", "a") as log:
        log.write("Retrieve Start at " + getTime() + "\n")

        try:
            soup = getSoup("movie.douban.com", log)
            movies = [x.a["href"] for x in soup.find_all("li", class_="title")]
            movie = []
            for m in movies:
                p = re.compile(r"(?<=subject/)\d+")
                movie.append(p.findall(m)[0])
            infos = []
            for m in movie:
                soup = getSoup("movie.douban.com/subject/" +
                               m, log).find(id="content")
                info = OrderedDict()
                info["no"] = m
                info["name"] = soup.find(
                    "span", property="v:itemreviewed").text
                info["year"] = soup.find("span", class_="year").text[1:-1]
                info["release"] = "/".join(
                    [x.text for x in soup.find_all("span", property="v:initialReleaseDate")])

                interest = soup.find(id="interest_sectl")
                average = interest.find(property="v:average")
                summ = interest.find(property="v:votes")
                level = interest.find_all(class_="rating_per")
                info["average"] = average.text if average is not null else null
                info["sum"] = summ.text if summ is not null else null
                info["rate_level"] = [x.text for x in level]
                info["time"] = getTime()
                infos.append(info)
                print(info["no"], info["name"])
            log.write("Start to record\n")
            filename = getTime()
            filename = filename[:filename.find(" ")] + ".txt"
            with open(filehome + filename, "a") as f:
                for i in infos:
                    f.write(json.dumps(i, ensure_ascii=False) + "\n")
                f.write("\n")
            log.write("Record success\n")
        except IndexError as e:
            log.write("Error: Regex Format Wrong. " + getTime() + "\n")
            print(e)
        except requests.exceptions.ConnectionError as e:
            log.write("Error: Network Connection Error. " + getTime() + "\n")
            print(e)
        log.write("Retrieve Finish at " + getTime() + "\n\n")
    print(getTime())
    print()
