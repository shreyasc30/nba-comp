from datetime import datetime, timedelta
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from CONST_season_start_end_dates import SEASON_START_END_DATES

# URL and parsing method could break at any time due to web scraping being used #
CONST_URL = "https://www.nba.com/stats/gamebooks/?Date="

opts = Options()
# toggle the below to see / not see the browser carrying out transactions -- makes things longer if off, but good for testing
opts.headless = True
browser = Firefox(options=opts)

def iterate_single_season(season_string):
    if season_string not in SEASON_START_END_DATES.keys():
        raise ValueError("Specified year start/end dates could not be found: " + season_string)
    (start_date, end_date) = SEASON_START_END_DATES.get(season_string)

    curr_date = start_date

    print(curr_date.strftime('%d'))

    while curr_date < end_date:
        # do some actions with the current date
        url = CONST_URL + curr_date.strftime('%m') + "%2F" + curr_date.strftime('%d') + "%2F" + curr_date.strftime('%Y')
        print(url)
        break
        # business logic happens here
        # %Y to get the year as an integer
        # %d for zero padded day
        # %m for zero padded month
        print(curr_date)

        #increment the day
        curr_date += timedelta(days = 1)

iterate_single_season('2011-12')
