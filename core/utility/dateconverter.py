from datetime import datetime

def convertDateToLong(dateString):
    dt_obj = datetime.strptime(dateString,'%Y-%m-%d %H:%M:%S.%f')
    millisec = dt_obj.timestamp() * 1000
    print(millisec)
    return millisec
def convertLongToDate(millisencond):
    return datetime.datetime.fromtimestamp(millisencond).strftime('%Y-%m-%d %H:%M:%S')