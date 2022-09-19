import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from unicodedata import name


#put the geckodriver in the environment path to work
driver = webdriver.Firefox()


url='https://www.premierleague.com/clubs'
driver.get(url)


# Accept on Cookies
time.sleep(10) # Wait to load page

accept_cookies = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()

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

# Get all clubs
clubs = driver.find_elements(By.XPATH,'/html/body/main/div[2]/div/div/div[3]/div/table/tbody/tr')
print("Number of Clubs",len(clubs))

clubs_list_premiere_url = []
stadiums_links = []

#loop on every club
for club in clubs:
    attr = club.find_elements(By.TAG_NAME,'td')
    [team, stadium] = attr #Object Destruction

    #Stadiums
    stadium_url = stadium.find_element(By.TAG_NAME, 'a')
    stadium_dict = {
        'StadiumName' : stadium.text,
        'StadiumLink' : stadium_url.get_attribute('href')
        }
    print(stadium_dict)
    stadiums_links.append(stadium_dict) 
    
    #premiereLeaguURL of the club
    premiere_url = team.find_element(By.TAG_NAME, 'a').get_attribute('href')
    club_dict = {
        "Name": team.text,
        "Website": premiere_url,
        "StadiumName": stadium.text
        }

    clubs_list_premiere_url.append(club_dict)

# Club_list now has the clubs with their premiere league links
# We loop over them and put the official website instead

club_list_official_url = []
for club in clubs_list_premiere_url:
    premiere_url = club["Website"]
    while True:
        try:
            driver.get(premiere_url)
            time.sleep(3)#load the page
            
            try:
                official_website = driver.find_element(By.CLASS_NAME, 'website')
                official_website_url = official_website.find_element(By.TAG_NAME, 'a').get_attribute('href')
               
                club_list_official_url.append(club)
                club_list_official_url[-1]["Website"] = official_website_url
                print(club_list_official_url[-1])
                print('Found official website for', club["Name"])
            except:
                print('no website for ', club['Name'])
            break
            
        except:
            print("Could not open", club["Name"], "premiere url")


# Create 
clubsDf = pd.DataFrame(club_list_official_url)
clubsDf.to_csv(r'output/clubsTable.csv',index=False)

StadiumsLinksDf = pd.DataFrame(stadiums_links)
StadiumsLinksDf.to_csv(r'output/stadiumsLinks.csv',index=False)

driver.close()