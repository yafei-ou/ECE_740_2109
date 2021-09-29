import pymysql as sql
import datetime
import time

db = sql.connect(host='127.0.0.1',user = "root",passwd = "Ouyafei4869",db = "correctorDB")
cursor = db.cursor()

date = datetime.datetime.now().strftime("%Y-%m-%d")
startTime = datetime.datetime.now()
startTimeStr = datetime.datetime.now().strftime("%H%M%S")
time.sleep(2)
endTime = datetime.datetime.now()
endTimeStr = datetime.datetime.now().strftime("%H%M%S")
timeSpan = (endTime-startTime).total_seconds()
hours, remainder = divmod(timeSpan, 3600)
minutes, seconds = divmod(remainder, 60)
hours, minutes, seconds = int(hours), int(minutes), int(seconds)
timeSpanStr = '%s%s%s' % (hours, minutes, seconds)

cursor.execute("insert into UserUsage (Date,StartTime,EndTime,TimeSpan,NumHeadTilt,NumBodyTilt)\
     values (str_to_date(%s, '%%Y-%%m-%%d'), %s, %s, %s, %s, %s)",
     (date, startTimeStr, endTimeStr, timeSpanStr, 1, 1))
db.commit()
db.close()

print(startTimeStr, endTimeStr, timeSpanStr)
print(db)