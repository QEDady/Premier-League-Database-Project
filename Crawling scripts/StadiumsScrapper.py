import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from unicodedata import name
import re

#put the geckodriver in the enviornment path to work
driver = webdriver.Firefox()
driver.get('https://www.premierleague.com/')
time.sleep(10)
accept_cookies = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()


df_stadiums_links = pd.read_csv(r'output/stadiumsLinks.csv')
stadiums_links = df_stadiums_links.to_dict('records')
# Now, it is on the form
# {'StadiumName': 'Emirates Stadium', 'StadiumLink': 'https://www.premierleague.com/clubs/1/Arsenal/stadium'}

stadiums_list = []

for stadium in stadiums_links:
    stadium_link = stadium["StadiumLink"]
    #stadium_link = "https://www.premierleague.com/clubs/2/Aston-Villa/stadium"

    while True:
        try:
            driver.get(stadium_link)
            time.sleep(5)

            try :
                stadium_info_button = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div/ul/li[2]')
                stadium_info_button.click()
                stadium_info = driver.find_element(By.CLASS_NAME, 'articleTabContent').find_element(By.CLASS_NAME, 'active').find_elements(By.TAG_NAME, 'p')
                print("On the right page", stadium["StadiumName"])
                stadium_dict = {}
                for cur_data in stadium_info:
                    try:
                        print("check")
                        label = cur_data.find_element(By.TAG_NAME, 'strong').text.strip()
                        value = cur_data.text.split(':')[-1].strip()
                        print(label, value)
                        # Sometimes, it is not capacity: 
                        # for exammple Tottenham Hotspur Stadium capacity: 62,062
                        if 'capacity' in label or 'Capacity' in label:
                            value = value.replace(',', '')
                            stadium_dict['Capacity'] = value
                        elif label == 'Built:' or label == 'Opened:':
                            stadium_dict['BuildingDate'] = value
                        elif label == 'Record PL attendance:':
                            value= value.replace(',', '')
                            stadium_dict['RecordLeagueAttendance'] = re.split(' ', value)[0].strip()
                        elif label == 'Pitch size:':
                            value = re.split('x', value)
                            value[0] = value[0].strip()
                            value[1]= value[1].strip()
                            stadium_dict['LengthMeter']= value[0][:-1]
                            stadium_dict['WidthMeter'] = value[1][:-1]
                        elif label == 'Stadium address:':
                            value  = value.replace(u'\xa0', u' ')
                            value = re.split(',', value)
                            # According to my observation, 
                            # The last is the postcodde
                            # The one before last is the city
                            # The remaining is the area
                            stadium_dict['Area'] = ', '.join(value[:-2])
                            stadium_dict['City'] =  value[-2].strip()
                            stadium_dict['PostCode'] = value[-1].strip()
                        
                    except:
                        #we have exausted all elements with strong tag, so we stop
                        print("exhaused all strong")
                        break
                print(stadium_dict)
                final_stadium_dict = {}
                final_stadium_dict['Name'] = stadium['StadiumName']
                final_stadium_dict['Area'] = stadium_dict.get('Area','')
                final_stadium_dict['City'] = stadium_dict.get('City','')
                final_stadium_dict['PostCode'] =  stadium_dict.get('PostCode','')
                final_stadium_dict['BuildingDate'] = stadium_dict.get('BuildingDate','')
                final_stadium_dict['Capacity'] = stadium_dict.get('Capacity','')
                final_stadium_dict['RecordLeagueAttendance'] = stadium_dict.get('RecordLeagueAttendance','')
                final_stadium_dict['LengthMeter'] = stadium_dict.get('LengthMeter','')
                final_stadium_dict['WidthMeter']= stadium_dict.get('WidthMeter','')

                print("Done", final_stadium_dict)
                stadiums_list.append(final_stadium_dict)
                break
            except:
                print("could not find the information page for",  stadium["StadiumName"])
                break
        except:
            print("Could not open url for", stadium["StadiumName"], "trying again")
    
# Create 
stadiumsDf = pd.DataFrame(stadiums_list)
stadiumsDf.to_csv(r'output/stadiumsTable.csv',index=False)

driver.close()