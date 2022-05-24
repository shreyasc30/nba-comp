from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from CONST_season_start_end_dates import SEASON_START_END_DATES

browser = Firefox(options=Options().set_headless())

def iterate_single_season(season_string):
    (start_date, end_date) = SEASON_START_END_DATES.get(season_string, "Season " + season_string + " dates not found")

    curr_date = start_date

    print(curr_date.strftime('%d'))

    while curr_date.day <= end_date.day and curr_date.year <= end_date.year:
        # do some actions with the current date
        # business logic happens here

        #increment the day
        pass
        # %Y to get the year as an integer
        # %d for zero padded day
        # %m for zero padded month

iterate_single_season('2010-11')
