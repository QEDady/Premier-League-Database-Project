#This script will scrape the data required for the table PlayersInClubs
# It will also save links for each indvidual player for playersScrapper to scrape them

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options


driver = webdriver.Firefox()
driver.get('https://www.premierleague.com/')
time.sleep(10)
accept_cookies = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()


# Seasons
seasonToUrls = {
    "2021/22" : "https://www.premierleague.com/players?se=418&cl=-1",
    "2020/21" : "https://www.premierleague.com/players?se=363&cl=-1",
    "2019/20": "https://www.premierleague.com/players?se=274&cl=-1",
    "2018/19"  : "https://www.premierleague.com/players?se=210&cl=-1"}


all_players_urls = set()
player_in_club_list =[]

for season, seasonUrl in  seasonToUrls.items():
    while True:
        try:
            driver.get(seasonUrl)
            time.sleep(10)
           
            idToClub = {}
            clubs = driver.find_elements(By.XPATH, "/html/body/main/div[2]/div[1]/div/section/div[2]/ul/li")
          
            for club in clubs:
                if club.get_attribute('data-option-id')!= '-1':
                    idToClub[club.get_attribute('data-option-id')] = club.get_attribute('data-option-name')
            
            print("\n\n\n", season, " has ", len(idToClub), " clubs")

            for clubId, club in idToClub.items():
                club_players_url=seasonUrl[:-2]
                club_players_url += clubId
                
                print ("started to scrap ", club, " players")
                while True:
                    try:
                        driver.get(club_players_url)
                        time.sleep(3)

                        #scroll
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


                        players = driver.find_elements(By.CLASS_NAME, "playerName")
                        #check
                        print("Club ", club, " has ", len(players), "players")
                        for player in players:
                            player_url = player.get_attribute("href")
                            player_url_parsed = ''

                            foundDigit = 0
                            playerId = ''
                            #I will parse the link to get the id and to stop once I get the id
                            # As some links have weird characters after the id, so it is 
                            # better to just stop after the id, and the link would work fine
                            for ch in player_url:
                                player_url_parsed += ch
                                if ch.isdigit(): 
                                    foundDigit = 1
                                    playerId +=ch
                                if ch == '/' and foundDigit:
                                    break
                            
                            all_players_urls.add(player_url_parsed)

                            player_in_club_dict = {
                                'PlayerID': playerId,
                                'Season':season,
                                'ClubName': club
                            }
                            print(player_in_club_dict)

                            player_in_club_list.append(player_in_club_dict)

                        break
                    except:
                        print("Trying club players again: ", club_players_url)
                    
               

            break
        except:
            print("trying", season, "clubs again")
    

playersInClubsDf = pd.DataFrame(player_in_club_list)
playersInClubsDf.to_csv(r'output/playersInClubsTable.csv',index=False)

playerLinksDF = pd.DataFrame(all_players_urls)
playerLinksDF.to_csv(r'output/playerLinks.csv', index=False)

driver.close()