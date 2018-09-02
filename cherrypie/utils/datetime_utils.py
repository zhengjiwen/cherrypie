# -*- coding:utf-8 -*-
from datetime import datetime
from datetime import timedelta
import arrow
from functools import partial
import calendar

now = arrow.now

utcnow = arrow.utcnow

prc_tz = 'prc'


def prcnow():
    utcnow().to(prc_tz)


def prctoday():
    return prcnow().date()


def span_range(start, end, frame, tz=None):
    return arrow.Arrow.span_range(frame, start, end, tz=tz)


def time_range(start, end, frame, tz=None):
    return arrow.Arrow.range(frame, start, end, tz=tz)


span_range_by_minute = partial(span_range, frame='minute')
span_range_by_hour = partial(span_range, frame='hour')
span_range_by_day = partial(span_range, frame='day')

prc_span_range_by_minute = partial(span_range, frame='minute', tz=prc_tz)
prc_span_range_by_hour = partial(span_range, frame='hour', tz=prc_tz)
prc_span_range_by_day = partial(span_range, frame='day', tz=prc_tz)

prc_range_by_minute = partial(time_range, frame='minute', tz=prc_tz)
prc_range_by_hour = partial(time_range, frame='hour', tz=prc_tz)
prc_range_by_day = partial(time_range, frame='day', tz=prc_tz)


def utc_today_int():
    return int(datetime.utcnow().strftime('%Y%m%d'))


def utc_from_today_int(date_int):
    return arrow.Arrow.strptime(str(date_int), '%Y%m%d%H%M')


def timestamp(is_float=False):
    if is_float:
        return arrow.utcnow().float_timestamp
    else:
        return arrow.utcnow().timestamp


def utc_from_timestamp(ts):
    return arrow.Arrow.utcfromtimestamp(ts)


def add_zero(year, month, day):
    # year, month , day =  zfc.split(spl)
    if int(month) < 10:
        month = "0%s" % month
    if int(day) < 10:
        day = "0%s" % day

    return "%s-%s-%s" % (year, month, day)


def int_time_period(start, end):
    if start == end:
        return [int(end.replace("-", ''))]
    start_time = start
    end_time = end
    st = start_time.split('-')
    et = end_time.split('-')
    date_list = []
    s_year, s_month, s_day = int(st[0]), int(st[1]), int(st[2])
    e_year, e_month, e_day = int(et[0]), int(et[1]), int(et[2])

    if s_month + s_year == (e_month + e_year):
        if s_month < 10:
            s_month = "0%s" % s_month
        for i in range(s_day, e_day + 1):
            if i < 10:
                i = "0%s" % i

            date_list.append(int("%s%s%s" % (s_year, s_month, i)))

    else:
        s_end = calendar.monthrange(s_year, s_month)[1]
        if s_month < 10:
            month = "0%s" % s_month
        else:
            month = s_month
        for i in range(s_day, s_end + 1):
            if i < 10:
                i = "0%s" % i
            date_list.append(int("%s%s%s" % (s_year, month, i)))

        if s_year == e_year:
            for i in range(s_month + 1, e_month):
                end = calendar.monthrange(s_year, i)[1]
                if i < 10:
                    i = "0%s" % i
                for b in range(1, end + 1):
                    if b < 10:
                        b = "0%s" % b
                    date_list.append(int("%s%s%s" % (s_year, i, b)))
        else:
            for i in range(s_month + 1, 13):
                end = calendar.monthrange(s_year, i)[1]
                if i < 10:
                    i = "0%s" % i
                for b in range(1, end + 1):
                    if b < 10:
                        b = "0%s" % b
                    date_list.append(int("%s%s%s" % (s_year, i, b)))

            for i in range(1, e_month):
                end = calendar.monthrange(e_year, i)[1]
                if i < 10:
                    i = "0%s" % i
                for b in range(1, end + 1):
                    if b < 10:
                        b = "0%s" % b
                    date_list.append(int("%s%s%s" % (s_year, i, b)))

        if e_month < 10:
            month = "0%s" % e_month
        else:
            month = e_month
        for i in range(1, e_day + 1):
            if i < 10:
                i = "0%s" % i
            date_list.append(int("%s%s%s" % (e_year, month, i)))

    return date_list


def get_work_time(date):
    ret = datetime.strptime(str(date), "%Y%m%d")
    return datetime(ret.year, ret.month, ret.day, 9)


def get_local_time(timenow):
    return timenow + timedelta(hours=8)


def get_first_day_of_month():
    today_date = datetime.today()
    year = today_date.year
    month = today_date.month
    res = str(datetime(year, month, 1))
    return res.split(' ')[0]


def get_last_day(year, month):
    last_day = calendar.monthrange(year, month)[1]
    if month > 9:
        return "%s-%s-%s" % (year, month, last_day)
    else:
        return "%s-0%s-%s" % (year, month, last_day)


def get_month_list():
    first_day = get_first_day_of_month()
    year, month, day = first_day.split('-')
    last_day = get_last_day(int(year), int(month))
    return int_time_period(first_day, last_day)


if __name__ == "__main__":
    pass
