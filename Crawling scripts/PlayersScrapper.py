import time
from unicodedata import name
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
# accept_cookies = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[5]/button[1]')
# accept_cookies.click()

players_links_df =  pd.read_csv(r'output/playerLinks.csv')
players_links = players_links_df['0'].tolist()
#players_links = ['https://www.premierleague.com/players/8163/', 'https://www.premierleague.com/players/5178', 'https://www.premierleague.com/players/24334', 'https://www.premierleague.com/players/66590']

players_list = []
for player_url in players_links:
    while True:
        try:
            driver.get(player_url)
            time.sleep(4)

            playerId = player_url.split('/')[-2]
            playerName = driver.find_elements(By.CLASS_NAME,'t-colour')[-1].text
            #print('passed 0')
            
            nationality = ''
            # some players do not have nationality like
            # https://www.premierleague.com/players/90666
            try:
                nationality = driver.find_element(By.CLASS_NAME, 'playerCountry').text
            except:
                #print('No Country for ', player_url)
                pass

            #print("passed 1")
            BirthDate = ''
            #some players do not have birthates or height like
            # https://www.premierleague.com/players/66590
            try:
                BirthDate = driver.find_element(By.XPATH, '/html/body/main/div[3]/div/div/div[1]/section/div/ul[2]/li/div[2]').text.split(' ')[0]
            except:
                #print('No Bdate for ', player_url)
                pass
            
           # print("passed 2")
            Height=''
            try:
                Height = driver.find_element(By.XPATH, '/html/body/main/div[3]/div/div/div[1]/section/div/ul[3]/li/div[2]').text[:-2]
            except:
                #print('No Height for ', player_url)
                pass

            #print("passed 3")
            position = ''
            side_information = driver.find_element(By.CLASS_NAME, 'playerIntro').find_elements(By.TAG_NAME, 'div')
            for i in range(len(side_information)-1):
                if side_information[i].text == 'Position':
                    position = side_information[i+1].text
                    break
            
            #print("passed 4")
            weight = ''
            try:
                weight = driver.find_element(By.CLASS_NAME, 'u-hide').find_element(By.CLASS_NAME, 'info')
                weight = (weight.get_attribute('innerHTML'))[:-2]
            except:
                #print('No weight for ', player_url)
                pass

           # print("passed 5")
            player_dict = {
                'ID': playerId,
                'FullName': playerName,
                'Nationaility':nationality,
                'Position' : position,
                'BirthDate': BirthDate,
                'Height': Height,
                'Weight':weight
            }

            print(player_dict)
            
            players_list.append(player_dict)
            break
        except:
            print("Trying to scrap", player_url)

playersDf = pd.DataFrame(players_list)
playersDf.to_csv(r'output/playersTable.csv',index=False)

driver.close()