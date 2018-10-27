proxies = list()
with open('proxy.txt') as pr:
    for i in pr:
        if i.count('.') == 3:
            x = i.split()
            y = 'https://' + x[0] + ':' + x[1]
            proxies.append(y)
print(proxies)
