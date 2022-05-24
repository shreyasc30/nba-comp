import datetime
# NBA timings inclusive of opening and closing days
# necessary due to multiple lockout
SEASON_START_END_DATES = {

    '1996-97': (datetime.date(1996, 11, 1), datetime.date(1997, 4, 20)),
    '1997-98': (datetime.date(1997, 10, 31), datetime.date(1998, 4, 19)),
    '1998-99': (datetime.date(1999, 2, 5), datetime.date(1999, 5, 5)),
    '1999-00': (datetime.date(1999, 11, 2), datetime.date(2000, 4, 19)),
    '2000-01': (datetime.date(2000, 10, 31), datetime.date(2001, 4, 18)),
    '2001-02': (datetime.date(2001, 10, 30), datetime.date(2002, 4, 17)),
    '2002-03': (datetime.date(2002, 10, 29), datetime.date(2003, 4, 16)),
    '2003-04': (datetime.date(2003, 10, 28), datetime.date(2004, 4, 14)),
    '2004-05': (datetime.date(2004, 11, 2), datetime.date(2005, 4, 20)),
    '2005-06': (datetime.date(2005, 11, 1), datetime.date(2006, 4, 19)),
    '2006-07': (datetime.date(2006, 10, 31), datetime.date(2007, 4, 18)),
    '2007-08': (datetime.date(2007, 10, 30), datetime.date(2008, 4, 16)),
    '2008-09': (datetime.date(2008, 10, 28), datetime.date(2009, 4, 16)),
    '2009-10': (datetime.date(2009, 10, 27), datetime.date(2010, 4, 14)),
    '2010-11': (datetime.date(2010, 10, 26), datetime.date(2011, 4, 13)),
    '2011-12': (datetime.date(2011, 12, 25), datetime.date(2012, 4, 26)),
    '2012-13': (datetime.date(2012, 10, 30), datetime.date(2013, 4, 17)),
    '2013-14': (datetime.date(2013, 10, 29), datetime.date(2014, 4, 16)),
    '2014-15': (datetime.date(2014, 10, 28), datetime.date(2015, 4, 15)),
    '2015-16': (datetime.date(2015, 10, 27), datetime.date(2016, 4, 13)),
    '2016-17': (datetime.date(2016, 10, 25), datetime.date(2017, 4, 12)),
    '2017-18': (datetime.date(2017, 10, 17), datetime.date(2018, 4, 11)),
    '2018-19': (datetime.date(2018, 10, 16), datetime.date(2019, 4, 10))

}
