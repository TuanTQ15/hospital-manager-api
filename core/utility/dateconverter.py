from datetime import datetime

def convertDateTimeToLong(dateString):
    try:
        dt_obj = datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S.%f')
        millisec = dt_obj.timestamp() * 1000
        return millisec
    except:
        return 0

def convertDateToLong(dateString):
    try:
        dt_obj = datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
        millisec = dt_obj.timestamp() * 1000
        return millisec
    except:
        return 0
def convertLongToDateTime(millisencond:int):
    timestamp=datetime.fromtimestamp(millisencond/1000.0)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')

def convertLongToDate(millisencond:int,pattern):
    timestamp=datetime.fromtimestamp(millisencond/1000.0)
    return timestamp.strftime(pattern)