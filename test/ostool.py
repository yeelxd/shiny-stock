import time;

epoch = int(time.mktime(time.strptime('2018-01-30', '%Y-%m-%d'))) - time.timezone
print(epoch)

today_epoch = time.time()
print(today_epoch)
