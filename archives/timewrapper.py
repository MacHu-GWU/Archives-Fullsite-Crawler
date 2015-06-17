##encoding=UTF8

"""
Copyright (c) 2015 by Sanhe Hu
------------------------------
    Author: Sanhe Hu
    Email: husanhe@gmail.com
    Lisence: LGPL


Module description
------------------
    This module provide syntactic sugar and useful functions which standard datetime and dateutil
    doesn't have
    
        TimeWrapper.str2date(datestr), TimeWrapper.str2datetime(datetimestr)
            parse arbitrary format date string/datetime string to python date/datetime object.
            automatically detect format.
        
        TimeWrapper.dtime_range(start, end, freq)
            a powerful datetime series generator
            
        TimeWrapper.randdate(start, end), TimeWrapper.randdatetime(start, end)
            a simple random date and datetime generator
            
        TimeWrapper.day_interval(year, month, day, mode = "str")
        TimeWrapper.month_interval(year, month, mode = "str")
        TimeWrapper.year_interval(year, mode = "str")
            generate day, month, year interval start, end datetime string for SQL BETWEEN query.


Keyword
-------
    date, datetime
    
    
Compatibility
-------------
    Python2: Yes
    Python3: Yes
    

Prerequisites
-------------
    None


Import Command
--------------
    from archives.timewrapper import timewrapper
"""

from __future__ import print_function
from datetime import datetime as dt, date as date, timedelta as td
import itertools
import random
import sys

is_py2 = (sys.version_info[0] == 2)
if is_py2:
    range = xrange


##############
# Exceptions #
##############


class ModeError(Exception):
    """used in TimeWrapper.day_interval, TimeWrapper.month_interval, TimeWrapper.year_interval
    for wrong mode str.
    """
    def __init__(self, mode_name):
        self.mode_name = mode_name

    def __str__(self):
        return "mode has to be 'str' or 'datetime', default 'str'. You are using '%s'." % self.mode_name

class NoMatchingTemplateError(Exception):
    """used in TimeWrapper.str2date, TimeWrapper.str2datetime
    """
    def __init__(self, pattern):
        self.pattern = pattern
        
    def __str__(self):
        return "None template matching '%s'" % self.pattern

class TimeWrapper(object):
    """时间包装器 是一个智能处理多种日期, 时间日期格式的转换器
    """
    def __init__(self):
        self.date_templates = list()
        self.datetime_templates = list()
        
        # add some datetime.date templates here
        self.date_templates.append("%Y-%m-%d") # 2014-09-20
        self.date_templates.append("%m-%d-%Y") # 09-20-2014
        self.date_templates.append("%m/%d/%Y") # 09/20/2014
        self.date_templates.append("%d/%m/%Y") # 20/09/2014
        self.date_templates.append("%Y/%m/%d") # 2014/09/20
        self.date_templates.append("%B %d, %Y") # September 20, 2014
        self.date_templates.append("%b %d, %Y") # Sep 20, 2014
        self.date_templates.append("%Y%m%d") # 20140920
        
        # add some datetime.datetime templates here
        self.datetime_templates.append("%Y-%m-%d %H:%M:%S") # "2014-01-15 17:58:31"
        self.datetime_templates.append("%Y-%m-%d %H:%M:%S.%f") # "2014-01-15 17:58:31.1234"
        self.datetime_templates.append("%Y-%m-%dT%H:%M:%S") # "2014-01-15T17:58:31"
        self.datetime_templates.append("%Y-%m-%dT%H:%M:%S.%f") # "2014-01-15T17:58:31.1234"
        
        self.datetime_templates.append("%m/%d/%Y %H:%M") # "2014-01-15 14:05"
        self.datetime_templates.append("%Y-%m-%d %I:%M:%S %p") # 2014-01-15 5:58:31 PM
        self.datetime_templates.append("%m/%d/%Y %I:%M:%S %p") # 1/15/2014 5:58:31 PM
        self.datetime_templates.append("%d/%m/%Y %I:%M:%S %p") # 15/01/2014 5:58:31 PM

        self.datetime_templates.append("%Y-%m-%d") # 2014-09-20
        self.datetime_templates.append("%m-%d-%Y") # 09-20-2014
        self.datetime_templates.append("%m/%d/%Y") # 09/20/2014
        self.datetime_templates.append("%d/%m/%Y") # 20/09/2014
        self.datetime_templates.append("%Y/%m/%d") # 2014/09/20
        self.datetime_templates.append("%B %d, %Y") # September 20, 2014
        self.datetime_templates.append("%b %d, %Y") # Sep 20, 2014
        self.datetime_templates.append("%Y%m%d") # 20140920

        self.default_date_template = "%Y-%m-%d"                  # 日期默认模板
        self.iso_dateformat = "%Y-%m-%d"                         # 国际标准模板
        self.default_datetime_templates = "%Y-%m-%d %H:%M:%S"    # 日期时间默认模板
        self.iso_datetimeformat = "%Y-%m-%d %H:%M:%S"            # 国际标准模板
    
    def add_date_template(self, template):
        """manually add a date format template so TimeWrapper can recognize it.
        A better way is to edit the source code and add it.
        """
        self.default_date_template.append(template)
        
    def add_datetime_template(self, template):
        """manually add a datetime format template so TimeWrapper can recognize it.
        A better way is to edit the source code and add it.
        """
        self.default_datetime_templates.append(template)
        
    ### ====== date manipulate ======
    def reformat(self, dtstring, before, after):
        """将dtstring从原来的#before格式转换成#after格式"""
        DT = dt.strptime(dtstring, before)
        return dt.strftime(DT, after)
    
    def str2date(self, datestr):
        """Try strip date string from our 108 date_templates and convert to ISO date format
         If None template matching datestr matching, then raise Error
         
        [Args]
        ------
            datestr: a date str
            
        [Returns]
        ---------
            DATE: a datetime.date object
        
        每次解析时, 先尝试这个默认模板, 如果失败了, 再重新对所有模板进行尝试; 一旦尝试成功, 这将
        当前成功的模板保存为默认模板。
        """
        try:
            return dt.strptime(datestr, self.default_date_template).date()
        except: # 如果默认的模板不匹配, 则重新尝试所有的模板
            pass
        
        for template in self.date_templates: # 对每个template进行尝试, 如果都不成功, 抛出异常
            try:
                DATETIME = dt.strptime(datestr, template) # 如果成功了
                self.default_date_template = template # 保存index到iso_dateformat
                return DATETIME.date()
            except:
                pass
        raise NoMatchingTemplateError(datestr)

    def str2datetime(self, datetimestr):
        """Try strip date string from our 2 datetime_templates and convert to ISO datetime format
         If None template matching datetimestr matching, then raise Error
         
        [Args]
        ------
            datetimestr: a datetime str
            
        [Returns]
        ---------
            DATETIME: a datetime.datetime object
        
        每次解析时, 先尝试这个默认模板, 如果失败了, 再重新对所有模板进行尝试; 一旦尝试成功, 这将
        当前成功的模板保存为默认模板。
        """
        try:
            return dt.strptime(datetimestr, self.default_datetime_templates)
        except: # 如果默认的模板不匹配, 则重新尝试所有的模板
            pass
        
        for template in self.datetime_templates: # 对每个template进行尝试, 如果都不成功, 抛出异常
            try:
                DATETIME = dt.strptime(datetimestr, template) # 如果成功了
                self.default_datetime_templates = template # 保存index到iso_dateformat
                return DATETIME
            except:
                pass
        raise NoMatchingTemplateError(datetimestr)
    
    def isodatestr(self, datestr):
        return str(self.str2date(datestr))

    def isodatetimestr(self, datetimestr):
        return str(self.str2datetime(datetimestr))
    
    """
    在数据库中, 我们经常需要使用:
        SELECT * FROM tablename WHERE create_datetime BETWEEN 'start' and 'end';
    为了方便, 我们提供了day_interval, month_interval, year_interval三个函数能够方便的生成start和end
    日期字符串。例如: month_interval(2014, 3) returns:
        start = "2014-03-01 00:00:00", end = "2014-03-31 23:59:59"
    
    [Notice]
    --------
        生成等间距的datetime序列, 可以使用pandas.date_range函数, 请参考pandas.date_range的部分
    """
    
    @staticmethod
    def day_interval(year, month, day, mode = "str"):
        """ example:
        day_interval(2014, 3, 1, "str") returns: "2014-03-01 00:00:00", "2014-03-01 23:59:59"
        
        str mode return pair of datetime str
        dt mode return pair of datetime object
        """
        start, end = dt(year, month, day), dt(year, month, day) + td(days=1) - td(seconds=1)
        if mode == "datetime":
            return start, end
        elif mode == "str":
            return str(start), str(end)
        else:
            raise ModeError(mode)
    
    @staticmethod
    def month_interval(year, month, mode = "str"):
        """ example:
        month_interval(2014, 12, "str") returns: "2014-12-01 00:00:00", "2014-12-31 23:59:59"
        
        str mode return pair of datetime str
        dt mode return pair of datetime object
        """
        if month == 12:
            start, end = dt(year, month, 1), dt(year+1, 1, 1) - td(seconds=1)
        else:
            start, end = dt(year, month, 1), dt(year, month+1, 1) - td(seconds=1)
        if mode == "datetime":
            return start, end
        elif mode == "str":
            return str(start), str(end)
        else:
            raise ModeError(mode)
        
    @staticmethod
    def year_interval(year, mode = "str"):
        """ example:
        year_interval(2014, "str") returns: "2014-01-01 00:00:00", "2014-12-31 23:59:59"
        
        str mode return pair of datetime str
        dt mode return pair of datetime object
        """
        start, end = dt(year, 1, 1), dt(year+1, 1, 1) - td(seconds=1)
        if mode == "datetime":
            return start, end
        elif mode == "str":
            return str(start), str(end)
        else:
            raise ModeError(mode)
        
    def _freq_parser(self, freq):
        """
        day, hour, min, sec,
        """
        try:
            if "day" in freq:
                freq = freq.replace("day", "")
                return td(days=int(freq))
            elif "hour" in freq:
                freq = freq.replace("hour", "")
                return td(hours=int(freq))
            elif "min" in freq:
                freq = freq.replace("min", "")
                return td(minutes=int(freq))
            elif "seconds" in freq:
                freq = freq.replace("seconds", "")
                return td(seconds=int(freq))
            else:
                raise Exception("%s is invalid format. use day, hour, min, sec." % freq)
        except:
            raise Exception("%s is invalid format. use day, hour, min, sec." % freq)
        
    def dtime_range(self, start=None, end=None, periods=None, freq="1day", normalize=False):
        """a pure Python implementation of pandas.date_range()
        given 2 of start, end, periods and freq, generate a series of datetime object.
        
        [Args]
        ------
            start : string or datetime-like, default None
                Left bound for generating dates
            end : string or datetime-like, default None
                Right bound for generating dates
            periods : integer or None, default None
                If None, must specify start and end
            freq : string, default ‘1day’ (calendar daily)
                Available mode are day, hour, min, sec
                Frequency strings can have multiples, e.g. ‘5hour
            normalize : bool, default False
                Normalize start/end dates to midnight before generating date range
        """
        def normalize_datetime_to_midnight(dtime):
            """normalize a datetime %Y-%m-%d %H:%M:%S to %Y-%m-%d 00:00:00
            """
            return dt(dtime.year, dtime.month, dtime.day)
        
        def not_normalize(dtime):
            """do not normalize
            """
            return dtime
        
        if (bool(start) + bool(end) + bool(periods)) == 2: # if two of start, end, or periods exist
            if normalize:
                converter = normalize_datetime_to_midnight
            else:
                converter = not_normalize
            
            interval = self._freq_parser(freq)
            
            if (bool(start) & bool(end)): # start and end
                if isinstance(start, str): # if str, convert to datetime
                    start = self.str2datetime(start)
                elif not isinstance(start, dt): 
                    raise Exception("start has to be datetime str or datetime")
                if isinstance(end, str): # if str, convert to datetime
                    end = self.str2datetime(end)
                elif not isinstance(end, dt): 
                    raise Exception("end has to be datetime str or datetime")
                if start > end: # if start time later than end time, raise error
                    raise Exception("start time has to be eariler and equal than end time")
                start = start - interval
                while 1:
                    start += interval
                    if start <= end:
                        yield converter(start)
                    else:
                        break
            elif (bool(start) & bool(periods)): # start and periods
                if isinstance(start, str): # if str, convert to datetime
                    start = self.str2datetime(start)
                elif not isinstance(start, dt): 
                    raise Exception("start has to be datetime str or datetime")
                start = start - interval
                for _ in range(periods):
                    start += interval
                    yield converter(start)
            elif (bool(end) & bool(periods)): # end and periods
                if isinstance(end, str): # if str, convert to datetime
                    end = self.str2datetime(end)
                elif not isinstance(end, dt): 
                    raise Exception("end has to be datetime str or datetime")
                start = end - interval * periods
                for _ in range(periods):
                    start += interval
                    yield converter(start)              
        else:
            raise Exception("Must specify two of start, end, or periods")

    ##########################################
    # timestamp, toordinary method extension #
    ##########################################
    def totimestamp(self, datetime_object):
        """Because in python2 datetime doesn't have timestamp() method,
        so we have to implement in a python2,3 compatible way.
        """
        return (datetime_object - dt(1969, 12, 31, 20, 0)).total_seconds()
    
    def fromtimestamp(self, timestamp):
        """because python doesn't support negative timestamp to datetime
        so we have to implement my own method
        """
        if timestamp >= 0:
            return dt.fromtimestamp(timestamp)
        else:
            return dt(1969, 12, 31, 20, 0) + td(seconds=timestamp)


    ###################################
    # random datetime, date generator #
    ###################################
    def randdate(self, start=date(1970,1,1), end=date.today()):
        """generate a random date between start to end

        [Args]
        ------
            start : string or date-like, Left bound for generating date
            end : string or date-like, Right bound for generating dates

        [Returns]
        ---------
            a datetime.date object
        """
        if isinstance(start, str):
            start = self.str2date(start)
        if isinstance(end, str):
            end = self.str2date(end)
        if start > end:
            raise Exception("start must be smaller than end! your start=%s, end=%s" % (start, end))
        return date.fromordinal(random.randint(start.toordinal(), end.toordinal()))

    def randdatetime(self, start=dt(1970,1,1), end=dt.now()):
        """generate a random datetime between start to end

        [Args]
        ------
            start : string or datetime-like, Left bound for generating date
            end : string or datetime-like, Right bound for generating dates

        [Returns]
        ---------
            a datetime.datetime object
        """
        if isinstance(start, str):
            start = self.str2datetime(start)
        if isinstance(end, str):
            end = self.str2datetime(end)
        if start > end:
            raise Exception("start must be smaller than end! your start=%s, end=%s" % (start, end))
        return dt.fromtimestamp(random.randint(self.totimestamp(start), self.totimestamp(end)))

timewrapper = TimeWrapper()

if __name__ == "__main__":
    import unittest
    
    class TimeWrapperUnittest(unittest.TestCase):
        def test_reformat(self):
            self.assertEqual(timewrapper.reformat("2014-01-05", "%Y-%m-%d", "%d/%m/%Y"),
                             "05/01/2014")
            self.assertEqual(timewrapper.reformat("2014-01-05 19:45:32", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"),
                             "2014/01/05")
            
        def test_day_month_year_interval(self):
            # day_interval
            self.assertTupleEqual(timewrapper.day_interval(2014, 3, 5), # with no mode argument
                ("2014-03-05 00:00:00", "2014-03-05 23:59:59")
                )
            self.assertTupleEqual(timewrapper.day_interval(2014, 12, 31, mode="datetime"), # datetime mode
                (dt(2014,12,31,0,0,0), dt(2014,12,31,23,59,59))
                )
            self.assertRaises(ModeError, timewrapper.day_interval, 2014, 12, 31, mode="good") # wrong mode
        
            # month_interval
            self.assertTupleEqual(timewrapper.month_interval(2014, 3),
                ("2014-03-01 00:00:00", "2014-03-31 23:59:59")
                )
            self.assertTupleEqual(timewrapper.month_interval(2014, 12, mode="datetime"),
                (dt(2014,12,1,0,0,0), dt(2014,12,31,23,59,59))
                )
            self.assertRaises(ModeError, timewrapper.month_interval, 2014, 12, mode="good")
            
            # year interval
            self.assertTupleEqual(timewrapper.year_interval(2014),
                ("2014-01-01 00:00:00", "2014-12-31 23:59:59")
                )
            self.assertTupleEqual(timewrapper.year_interval(2014, mode="datetime"),
                (dt(2014,1,1,0,0,0), dt(2014,12,31,23,59,59))
                )
            self.assertRaises(ModeError, timewrapper.year_interval, 2014, mode="good")
        
        def test_str2date(self):
            self.assertEqual(timewrapper.isodatestr("05/01/2014"), "2014-05-01")
            self.assertEqual(timewrapper.isodatestr("September 20, 2014"), "2014-09-20")
            self.assertEqual(timewrapper.isodatestr("Sep 20, 2014"), "2014-09-20")
            self.assertRaises(NoMatchingTemplateError, timewrapper.isodatestr, "[2014][05][01]")
        
        def test_str2datetime(self):
            self.assertEqual(timewrapper.isodatetimestr("2014-07-03 8:12:34"), "2014-07-03 08:12:34")
            self.assertEqual(timewrapper.isodatetimestr("2014-07-03 8:12:34 PM"), "2014-07-03 20:12:34")
            self.assertRaises(NoMatchingTemplateError, timewrapper.isodatetimestr, "[2014][07][03]")
        
        def test_dtime_range(self):
            # test start + end
            self.assertListEqual([dt(2014,1,1,3,0,0), dt(2014,1,1,3,5,0), dt(2014,1,1,3,10,0)],
                list(timewrapper.dtime_range(start="2014-01-01 03:00:00", 
                                    end="2014-01-01 03:10:00", 
                                    freq="5min"))
                )
            # test start + periods
            self.assertListEqual([dt(2014,1,1,3,0,0), dt(2014,1,1,3,5,0), dt(2014,1,1,3,10,0)],
                list(timewrapper.dtime_range(start="2014-01-01 03:00:00", 
                                    periods=3, 
                                    freq="5min"))
                )
            # test end + periods
            self.assertListEqual([dt(2014,1,1,3,0,0), dt(2014,1,1,3,5,0), dt(2014,1,1,3,10,0)],
                list(timewrapper.dtime_range(end="2014-01-01 03:10:00",
                                    periods=3,
                                    freq="5min"))
                )
            # test take datetime as input
            self.assertListEqual([dt(2014,1,1,3,0,0), dt(2014,1,1,3,5,0), dt(2014,1,1,3,10,0)],
                list(timewrapper.dtime_range(start=dt(2014,1,1,3,0,0), 
                                    end=dt(2014,1,1,3,10,0), 
                                    freq="5min"))
                )
        
        def test_totimestamp_fromtimestamp(self):
            a_datetime = dt(1997, 7, 7, 12, 0, 0)
            try:
                self.assertEqual(a_datetime.timestamp(), timewrapper.totimestamp(a_datetime))
                self.assertEqual(dt.fromtimestamp(123456789), timewrapper.fromtimestamp(123456789))
            except:
                self.assertEqual(868291200, timewrapper.totimestamp(a_datetime))
                self.assertEqual(dt.fromtimestamp(123456789), timewrapper.fromtimestamp(123456789))
                
            a_datetime = dt(1924, 2, 19, 12, 0, 0)
            try:
                self.assertEqual(a_datetime.timestamp(), timewrapper.totimestamp(a_datetime))
                self.assertEqual(dt.fromtimestamp(-123456789), timewrapper.fromtimestamp(-123456789))
            except:
                self.assertEqual(-1447401600, timewrapper.totimestamp(a_datetime))
                self.assertEqual(dt(1966, 2, 1, 22, 26, 51), timewrapper.fromtimestamp(-123456789))
        
        def test_randdate_randdatetime(self):
            # test random date is between the boundary
            a_date = timewrapper.randdate("2014-01-01", date(2014, 1, 31))
            self.assertGreaterEqual(a_date, date(2014, 1, 1))
            self.assertLessEqual(a_date, date(2014, 1, 31))

            # test random datetime is between the boundary
            a_datetime = timewrapper.randdatetime("2014-01-01", dt(2014, 1, 31, 23, 59, 59))
            self.assertGreaterEqual(a_datetime, dt(2014, 1, 1, 0, 0, 0))
            self.assertLessEqual(a_datetime, dt(2014, 1, 31, 23, 59, 59))


    unittest.main()
    