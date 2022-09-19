import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

#put the geckodriver in the enviornment path to work
driver = webdriver.Firefox()
driver.get('https://www.premierleague.com/')
time.sleep(10)
# accept_cookies = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[5]/button[1]')
# accept_cookies.click()

# Seasons
seasonToUrls = {
    "2021/22" : "https://www.premierleague.com/results?co=1&se=418&cl=-1",
    "2020/21" : "https://www.premierleague.com/results?co=1&se=363&cl=-1",
    "2019/20": "https://www.premierleague.com/results?co=1&se=274&cl=-1", 
    "2018/19"  : "https://www.premierleague.com/results?co=1&se=210&cl=-1"}

seasonToMatches = {}

# for check
all_match_urls = []
for season, seasonUrl in seasonToUrls.items():
    while True:
        try:
            driver.get(seasonUrl)
            time.sleep(5)
#
            # Scroll down
            current_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 	# Scroll step
                time.sleep(3) 	# Wait to load page
                try:
                    new_height = driver.execute_script("return document.body.scrollHeight") # Calculate new scroll height
                except:
                    print("Failed: ", new_height)
                if new_height == current_height: # Compare with last scroll height
                    break
                current_height = new_height
        
            print("scorlled till",current_height)
            time.sleep(5)

            #mathces = driver.find_elements(BY, "div.fixture")
            matches = driver.find_elements(By.CLASS_NAME, 'postMatch')
            matches_urls = []
            for match in matches:
                matches_urls.append('https:'+ match.get_attribute('data-href'))
            #for check
            print(season, " has ", len(matches_urls), " matches")
            seasonToMatches[season] = matches_urls

            #for check
            all_match_urls.extend(matches_urls)
            break
        
        except:
            print("Failed to open season", season, "page. Trying again")

#for check
print("We have", len(all_match_urls), "matches")
matchesUrlsDf = pd.DataFrame(all_match_urls)
matchesUrlsDf.to_csv(r'output/matchesUrlsNotNeed.csv',index=False)


matches_list = []
#check
counter = 1
for season, urls in seasonToMatches.items():
    for matchUrl in urls:
        while True:
            try:
                driver.get(matchUrl)
                time.sleep(10)

                stats_button = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div[2]/div[2]/div[1]/div/div/ul/li[3]')
                stats_button.click()
                time.sleep(3)

                HomeTeamName = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div[2]/section/div[3]/div/div/div[1]/div[1]/a[2]/span[1]').text
                AwayTeamName = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div[2]/section/div[3]/div/div/div[1]/div[3]/a[2]/span[1]').text
                Date = driver.find_element(By.CLASS_NAME, "matchDate").text
                StadiumName = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div[2]/section/div[1]/div/div[1]/div[3]').text.split(',')[0]
                score = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div[2]/section/div[3]/div/div/div[1]/div[2]/div/div').text.split('-')

                # We get all stats. Each stat is a tr class with 3 td's inside it 
                stats = driver.find_elements(By.XPATH, '/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr')

                stats_dict = {}
                for stat in stats:
                    stat_name = stat.find_elements(By.TAG_NAME, 'td')[1].text
                    home = stat.find_elements(By.TAG_NAME, 'td')[0].text
                    away = stat.find_elements(By.TAG_NAME, 'td')[2].text
                    stats_dict[stat_name] = (home, away)
                
                    match_dict ={
                    'Season':season,
                    'HomeTeamName': HomeTeamName,
                    'AwayTeamName': AwayTeamName,
                    'Date': Date,
                    'HomePossession' : stats_dict['Possession %'][0],
                    'HomeYellowCards': stats_dict.get('Yellow cards', [0, 0])[0],
                    'HomeRedCards': stats_dict.get('Red cards', [0, 0])[0],
                    'HomeFouls' : stats_dict.get('Fouls conceded', [0, 0])[0],
                    'HomeShots' : stats_dict.get('Shots', [0, 0])[0],
                    'HomeGoals' : score[0],
                    'AwayYellowCards': stats_dict.get('Yellow cards', [0, 0])[1],
                    'AwayRedCards': stats_dict.get('Red cards', [0, 0])[1],
                    'AwayFouls' : stats_dict.get('Fouls conceded', [0, 0])[1],
                    'AwayShots' : stats_dict.get('Shots', [0, 0])[1],
                    'AwayGoals' : score[1],
                    'StadiumName' : StadiumName
                }

                print("Match Done Number ",counter, match_dict)
                counter +=1
                matches_list.append(match_dict)
                break
                
            except:
                print("Falied to open match ", matchUrl, "trying again")

matchesDf = pd.DataFrame(matches_list)
matchesDf.to_csv(r'output/matchesTable.csv',index=False)

driver.close()