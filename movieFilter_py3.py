import os, json, platform, sys
from collections import OrderedDict

# reload(sys)
# sys.setdefaultencoding('utf-8')
filehome = os.getcwd()
if platform.system() == "Linux":
    filehome = '/mnt/file/'
    if raw_input('Please input the dir(doubanMovie as 1 and cbo as 2): ').strip() == '1':
        filehome = filehome + 'doubanMovie'
    else:
        filehome = filehome + 'cbo'

input = raw_input('Please input the NO or part of name: ')
os.chdir(filehome)
files = os.listdir(filehome)
files.sort()
output = []
for f in files:
    if f.find('-') >= 0:
        with open(filehome + '/' + f, 'r') as f:
            for line in f:
                if len(line.strip()) > 0:
                    item = json.loads(line, 'utf-8', object_pairs_hook=OrderedDict)
                    if (input.isdigit() and item.has_key('no') and item['no'] == input) \
                            or (item.has_key('name') and isinstance(item['name'], basestring) and item['name'].find(
                                input) >= 0):
                        output.append(json.dumps(item, ensure_ascii=False))
                        print output[-1]
if len(output) > 0:
    filename = raw_input('Please input the filename to archive(-1 to cancel): ')
    if filename != '-1':
        with open(filename, 'w') as f:
            for o in output:
                f.write(o + '\n')
else:
    print input + ' not found.'
