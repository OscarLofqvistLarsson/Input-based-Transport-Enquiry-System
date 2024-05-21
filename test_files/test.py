import datetime

current_time = datetime.datetime.now().time().replace(microsecond=0)


print(current_time)