import time
import random
ips = [line.split()[0] for line in open('ip_list', 'r', encoding='utf-8')
       if line.startswith('#') is not True]
# print(ips)
forbidden_ports = {8080, 3129, 8081, 9098, 1080,
                   9080, 9090, 3389, 1521, 1158, 2100, 1433, 1434}
starts = 1024
ends = 65535
for ip in ips:
    while True:
        time.sleep(random.random()*3)
        times = time.ctime()
        hashing = hash(ip+times)
        port = starts + hashing % (ends-starts)
        print('The hash value of ip[{}] at {} is {}. \nTo the port {}'.format(
            ip, times, hashing, port))
        if port in forbidden_ports:
            print('The port is in forbidden list. Try again...\n')
        else:
            print()
            break
