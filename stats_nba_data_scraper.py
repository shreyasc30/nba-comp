from datetime import datetime, timedelta

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from CONST_season_start_end_dates import SEASON_START_END_DATES

import pandas as pd

# URL and parsing method could break at any time due to web scraping being used #
CONST_URL = "https://www.nba.com/stats/gamebooks/?Date="

opts = Options()
# toggle the below to see / not see the browser carrying out transactions -- makes things longer if off, but good for testing
#opts.headless = True
browser = Firefox(options=opts)

def iterate_single_season(season_string, df):
    if season_string not in SEASON_START_END_DATES.keys():
        raise ValueError("Specified year start/end dates could not be found: " + season_string)
    (start_date, end_date) = SEASON_START_END_DATES.get(season_string)

    curr_date = start_date

    print(curr_date.strftime('%d'))

    while curr_date < end_date:
        # do some actions with the current date
        # %Y to get the year as an integer
        # %d for zero padded day
        # %m for zero padded month
        url = CONST_URL + curr_date.strftime('%m') + "%2F" + curr_date.strftime('%d') + "%2F" + curr_date.strftime('%Y')

        # business logic happens here
        df = iterate_single_gameday(season_string, url, df)
        

        # increment the day
        curr_date += timedelta(days = 1)

# preconditions
# url is valid, add check in iterate_single_season
# df is dataframe to which we want to add each data entry
# single gameday refers to a single date

def iterate_single_gameday(season_string, url, df):
    browser.get(url)
    # nba table is always before G league table on the page
    # in order to ensure it is NBA games, we use the SELECT feature to select a specific value in the league dropdown (avoids g league etc.)
    select = Select(browser.find_element_by_name("LeagueID"))
    select.select_by_visible_text('NBA')

    # wait for the table to reload since otherwise we get a NoSuchElementException from selenium when looking for table

    # try:
    #     element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.name, "nba-stat-table__overflow"))
    #     )
    # finally:
    #     browser.quit()
    #     raise Exception("Driver timeout and quit due to table not being found on page after 10 seconds")

    # above was resolved, was an issue with my understanding of the HTML DOM elements. This remains as a tutorial if necessary for future work
    
        
    l = browser.find_element_by_xpath("//a[contains(@ng-href, 'box-score')]").text

    print(l)

df = pd.DataFrame()
iterate_single_season('2011-12', df)
