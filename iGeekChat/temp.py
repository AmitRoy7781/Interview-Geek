from datetime import datetime,date,timedelta

a = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
print(a)