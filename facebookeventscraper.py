from selenium import webdriver
from selenium.webdriver.chrome.options import  Options
from random import seed
from random import random
from time import process_time, sleep, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import csv
import os
import re
from openpyxl import load_workbook
import urllib.request
from datetime import datetime
from urllib.request import urlopen


# headers for csv 
header=['Index','title','Description','Cetegory','tag_list','Limit age & group size','People Range','Age Range','Date & Time','TBD Text','Start Date','start Time','End Time','Durations','Repeat Every','End Date','Online Event?','locations','Cost','Price($)','ticket (change to Other)','website',' Type','Other Image Urls','img_src (rename to Default Image)','Auto Accept','Profile Video','Video Url','Link to page']




with open('output2.csv', 'w', encoding='UTF8') as f:  #  creatinfg csv 
    writer = csv.writer(f)

    writer.writerow(header)
 

header=['index',"urls"]
with open('envent_link.csv', 'w', encoding='UTF8') as f:  #  creatinfg csv 
    writer = csv.writer(f)

    writer.writerow(header)
city_name="new york"    
# city_name="ottawa"
driver=webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://www.facebook.com/events/search/?q={}'.format(city_name))
driver.maximize_window()
link_list=[]
data_list=[]

for _ in range(1):
    try:
        actions = ActionChains(driver)
        actions.send_keys(Keys.SPACE).perform()                # moving slider

        time.sleep(3)
        soup=BeautifulSoup(driver.page_source,'html.parser')
        div_of_event_list=soup.find('div',{'class':'fjf4s8hc tu1s4ah4 f7vcsfb0 k3eq2f2k d2edcug0 rq0escxv'}) 
        single_event_div=div_of_event_list.find_all('div',{'class':'rq0escxv l9j0dhe7 du4w35lb hybvsw6c io0zqebd m5lcvass fbipl8qg nwvqtn77 k4urcfbm ni8dbmo4 stjgntxs sbcfpzgs'})
        for sigle_event in single_event_div:
        
            event_link=sigle_event.find('a')
            if 'https://www.facebook.com'+event_link.get('href') not in link_list :

                link_list.append('https://www.facebook.com'+event_link.get('href'))
                data_frame=pd.DataFrame(['https://www.facebook.com'+event_link.get('href')])

                df_read=data_frame.to_csv('envent_link.csv',mode="a" ,header=False) 
    except:
        pass


df=pd.read_csv('envent_link.csv')            # readnig csv for link of every event 
for event_link in df['urls'].values.tolist():
    try:
       
       
            driver.get(event_link)    # hiting the link for every event 
            time.sleep(5)
            print(event_link,"url:")
            soup=BeautifulSoup(driver.page_source,'html.parser')              # getting html of every page 
            title=soup.find('h1',{'data-testid':'event-permalink-event-name'})
            # print(title.text)
            try:
                description_div=soup.find('div',{'id':'reaction_units'})
                description=description_div.find('div',{'class':'_63ew'}).text
            except:
                description="No Description given "
                    
            tags=soup.find_all('li',{'class':'_63ep _63eq'})


            tag_list=[]
            for t in tags:
                tag_list.append(t.text)
             
            location_ul_list=soup.find('ul',{'class','uiList _4kg _4ks'})
            timeinfosection=location_ul_list.find('li')
            timeinfo=timeinfosection.find('div',{'class':'_2ycp _5xhk'})

            if 'from' in timeinfo.text :
                startdate=timeinfo.text.split('from')[0]
                if startdate[0].isnumeric() :
                    startdate=timeinfo.text.split('from')[0]
                else:    
                    startdate=timeinfo.text.split('from')[0].split(',')[1]

                enddate="NO"
                starttime=timeinfo.text.split('from')[1].split("-")[0][0:5]
                endtime=timeinfo.text.split('from')[1].split("-")[1][0:5]
                durtation="NO"
                
            else:
                try:
                    startdate=timeinfo.text.split("at")[0]
                    if startdate[0].isnumeric() :
                        startdate=timeinfo.text.split("at")[0]

                    else:
                        startdate=timeinfo.text.split('from')[0]
                    enddate=timeinfo.text.split("at")[1].split()[2]+timeinfo.text.split("at")[1].split()[3]+timeinfo.text.split("at")[1].split()[4]
                    starttime=timeinfo.text.split("at")[1].split()[0][0:5]
                    endtime=timeinfo.text.split("at")[2][0:5]
                    durtation="Yes"
                except:
                    startdate=timeinfo.text.split("at")[-2]
                    if startdate[0].isnumeric() :
                        startdate=timeinfo.text.split("at")[-2]
                        
                    else:
                        startdate=timeinfo.text.split("at")[-2].split(',')[1]
                        
                    enddate="No"
                    starttime=timeinfo.text.split("at")[-1][0:5]
                    endtime="NO"
                    durtation="No"


            location=location_ul_list.find_all('li')
            ticket=soup.find('li',{'data-testid':'event_ticket_link'})         # getting ticket  info 
            if ticket is not None:
                
                ticket=ticket.find('div',{'class':'_5xhp fsm fwn fcg'}).text

            else:
                ticket="No ticket info"

            if location is  not None :                                          # getting location and website link info
                if ".com" in location[1].text or "https" in location[1].text:
                    website=location[1]
                    website=location[1].find('div',{'class':'_98dl fsm fwn fcg'})
                    if website is not None:
                        website=website.text
                    else:
                        website="No website given" 
                    locations="No location"
                            
                else:
                    locations=location[1]
                    locations=location[1].find('div',{'class':'_4dpf _phw'})
                    if locations is not None:
                        locations=locations.text
                    else:
                        locations="No location given"   
                    website="No website link"
            
            if "Online event" in location[1].text :
                online= "YES"
            else:
                online=locations



            image_div=soup.find('div',{'id':'event_header_primary'})        # getting  Image url 
            try:
                img_src=image_div.find('img').get('src')
            except:
                img_src="NO Image Url "     
            
            # appending data into arrays 
            # header=['Index','title','Description','Cetegory','tag_list','Limit age & group size','People Range','Age Range','Date & Time','TBD Text','Start Date','start Time','End Time','Durations','Repeat Every','End Date','Online Event?','locations','Cost','Price($)','ticket (change to Other)','website',' Type','Other Image Urls','img_src (rename to Default Image)','Auto Accept','Profile Video','Video Url','Link to page']

            data_list.append(title.text)

            data_list.append(description)
            data_list.append(' ')

            data_list.append(tag_list)
            data_list.append(' ')  # limit age $ group size 
            data_list.append(' ')  # people range 
            data_list.append(' ')  #  age range 
            data_list.append(' ')  # date and  time 
            data_list.append(' ')  # TBD

            data_list.append(startdate)
            data_list.append(starttime)
            data_list.append(endtime)
            data_list.append(durtation)
            data_list.append(' ')  # repeat every 

            data_list.append(enddate)  
            data_list.append(online)
            data_list.append(locations)
            data_list.append(' ')  # cost
            data_list.append(' ')   #Price

            data_list.append(ticket)
            data_list.append(website)
            data_list.append(' ')  # type 
            data_list.append(' ') #other image url



            data_list.append(img_src)
            data_list.append(' ') # autto accept 
            data_list.append(' ') # profile video 
            data_list.append(' ') # video url

            data_list.append(driver.current_url)
            data_frame=pd.DataFrame([data_list])

            df_read=data_frame.to_csv('output2.csv',mode="a" ,header=False)   # saving data into csv 
            data_list.clear()
            tag_list.clear()
        
        # driver.close()
    except:
        pass
# os.remove('envent_link.csv')

    