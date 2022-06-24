import calendar
import datetime

year = datetime.datetime.now().year
cal = calendar.TextCalendar(calendar.SUNDAY)
for m in range(1, 13):
    print(cal.formatmonth(year, m, 0, 0))
