from datetime import datetime, timedelta
from time import sleep

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

from CONST_season_start_end_dates import SEASON_START_END_DATES
from CONST_team_names_since_2011 import TEAM_NAMES

import pandas as pd

# URL and parsing method could break at any time due to web scraping being used #
CONST_URL = "https://www.nba.com/stats/gamebooks/?Date="

opts = Options()
# toggle the below to see / not see the browser carrying out transactions -- makes things longer if off, but good for testing
opts.headless = True
browser = Firefox(options=opts)

def iterate_single_season(season_string, df):
    game_urls = []
    if season_string not in SEASON_START_END_DATES.keys():
        raise ValueError("Specified year start/end dates could not be found: " + season_string)
    (start_date, end_date) = SEASON_START_END_DATES.get(season_string)

    curr_date = start_date

    # print(curr_date.strftime('%d'))

    while curr_date < end_date:
        # do some actions with the current date
        # %Y to get the year as an integer
        # %d for zero padded day
        # %m for zero padded month
        url = CONST_URL + curr_date.strftime('%m') + "%2F" + curr_date.strftime('%d') + "%2F" + curr_date.strftime('%Y')

        # business logic happens here
        game_urls = get_single_gameday_urls(season_string, url, game_urls, curr_date)

        # increment the day
        curr_date += timedelta(days = 1)

    # now we have a list of all the game URLs for an entire season
    # we want to go through these games and populate 2 data entries per game (winning team, losing team)
    # once the dataframe is fully populated, we are done iterating through an entire season. So we can return the df

    missing_ = []
    for (url, date) in game_urls:
        # print(url)
        (errcode, df) = analyze_single_game_url(season_string, url, df, date, 5)
        # remove all star game
        if errcode != 1 and not (("est" in url) and ("wst" in url)):
            missing_.append((errcode, url))
    
    start_wait = 10
    new_missing = []
    while (len(missing_) > 0):
        while start_wait <= 60:
            entry = missing_[0]
            (errcode, df) = analyze_single_game_url(season_string, entry[1], df, date, start_wait)
            if errcode != 1:
                new_missing.append((errcode, entry[1]))
            start_wait += 5
        missing_ = new_missing
        if start_wait > 60:
            print("Waited 60 seconds for " + entry[1] + " and no luck")
            missing_ = missing_[1:]
                

    print(missing_)
    with open('missing.txt', 'w') as f:
        for item in missing_:
            f.write(item + "\n")
    return df


# preconditions
# url is valid, add check in iterate_single_season
# df is dataframe to which we want to add each data entry
# single gameday refers to a single date

def get_single_gameday_urls(season_string, url, game_urls, curr_date):
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
    
    # simplistic wait for page to render. Otherwise, links not visible (table has to populate) 
    # TODO: improve sleep mechanism to be dynamic similar to the above to cut down wasted time
    sleep(5)

    # TODO: save the date to add to the return value of this function
    # unique index of each example will be date.1, date.2 etc.

    interactive_box_score_elements = browser.find_elements_by_partial_link_text("Interactive Box Score")

    for elem in interactive_box_score_elements:
        link = elem.get_attribute('href')
        if "gleague" not in link:
            game_urls.append((link, curr_date))
    return game_urls

def analyze_single_game_url(season_string, url, df, date, wait_time):
    # TODO: implement me !
    try :
        browser.get(url)
    except (TimeoutException):
        return ((-1, df))

    print(url)
    # simplistic sleep because of intermittent error -- find a way too streamline this process
    sleep(wait_time)
    try :
        two_tables_parent = browser.find_elements_by_class_name(name="MaxWidthContainer_mwc__2OXc5")[1]

    except (IndexError):
        return ((-1, df))

    team_names_player_names_data = two_tables_parent.find_elements_by_class_name('block')
    
    # use the below to see what information is available to you with this one line
    # this method can be changed / overridden to extract individual player statistics at the time of writing
    # using the below / changing from here on out
    # for team_name in team_names_player_names_data:
    #     print(team_name.text)
    
    try:
        home_team_name = team_names_player_names_data[0].text
        away_team_name = team_names_player_names_data[4].text


        home_team_data_dump = team_names_player_names_data[1].text
        away_team_data_dump = team_names_player_names_data[5].text
    
    except(IndexError):
        return ((-3, df))

    # if the away team data is not in the most common spot, we have to find it
    # we know the team data is the entry right after the name, so we can look for the name
    away_team_idx = 2
    while away_team_name.upper() not in TEAM_NAMES:
        away_team_name = team_names_player_names_data[away_team_idx].text
        if away_team_idx == len(team_names_player_names_data):
            print("Could not find away team name, example skipped: " + url)
            return (-2, df)
        away_team_idx += 1
        try:
            away_team_data_dump = team_names_player_names_data[away_team_idx].text
        except(IndexError):
            return (-4, df)


    # for tnpnd in team_names_player_names_data:
    #     print(tnpnd.text)
    #     print("\n\n")

    # if you want individual player data, redirect some logic here to grab it from the above variables
    # TODO: add support (perhaps with a flag / full CLI support) for extracting player data
    
    home_team_data_dump = home_team_data_dump.replace('/n', ',')
    away_team_data_dump = away_team_data_dump.replace('/n', ',')
    home_totals_only = home_team_data_dump[home_team_data_dump.rfind("TOTALS"):].split()

    # the below logic was created to handle tests for several special cases documented and dealt with above
    away_totals_found = away_team_data_dump.rfind("TOTALS")
    away_totals_only = away_team_data_dump[away_totals_found:].split()
    home_totals_only[0], away_totals_only[0] = home_team_name, away_team_name

    home_totals_only.append(season_string)
    home_totals_only.append(date)
    away_totals_only.append(season_string)
    away_totals_only.append(date)


    # print(away_team_data_dump)
    #print(away_totals_only)

    # print(season_string + " " + home_team_name + " vs. " + away_team_name + " link:" + url)
    len_df = len(df)
    df.loc[len_df] = home_totals_only
    df.loc[len_df + 1] = away_totals_only

    return (1, df)



    
    

df = pd.DataFrame(columns=["name", "fgm", "fga", "fgperc", "3pm", "3pa", "3pperc", "ftm", "fta", "ftperc", "oreb", "dreb", "reb", "asst", "stl", "block", "to", "fouls", "pts", "plus-minus", "season", "date"])

for season_name in SEASON_START_END_DATES.keys():    
    df = iterate_single_season(season_name, df)
    df.to_csv(season_name + "_NBA_season_team_game_data.csv")
    df = df.head(0)

# for url in urls:
#     df = analyze_single_game_url('2011-12', url, df)


# analyze_single_game_url('2011-12', 'https://www.nba.com/game/cle-vs-uta-0021100139/box-score', df)