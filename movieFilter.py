#! /usr/bin/env python
# coding=utf-8
import os, json, platform
from collections import OrderedDict

filehome = os.getcwd()
if (platform.system() == "Linux"):
    filehome = '/mnt/file/doubanMovie'

input = raw_input('Please input the NO or part of name: ')
os.chdir(filehome)
files = os.listdir(filehome)
for file in files:
    if (file.find('-') >= 0):
        with open(filehome + '/' + file, 'r') as f:
            for line in f:
                if len(line.strip()) > 0:
                    item = json.loads(line, 'utf-8', object_pairs_hook=OrderedDict)
                    if item['no'] == input or item['name'].find(input) >= 0:
                        print json.dumps(item, ensure_ascii=False)
