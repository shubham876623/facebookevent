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
import re
from openpyxl import load_workbook
import urllib.request
from datetime import datetime
from urllib.request import urlopen



header=['Index','title','Description','tag_list','Start Date','start Time','End Time','End Date','Durations','Online Event?','locations','website','ticket','img_src','Link to page']



with open('output.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    writer.writerow(header)
city_name="ottawa"
driver=webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://www.facebook.com/events/search/?q={}'.format(city_name))
driver.maximize_window()
link_list=[]
data_list=[]
# for _ in range(5):
actions = ActionChains(driver)
actions.send_keys(Keys.SPACE).perform()  # moving slider

# time.sleep(1)  
time.sleep(5)
soup=BeautifulSoup(driver.page_source,'html.parser')
div_of_event_list=soup.find('div',{'class':'fjf4s8hc tu1s4ah4 f7vcsfb0 k3eq2f2k d2edcug0 rq0escxv'})
single_event_div=div_of_event_list.find_all('div',{'class':'rq0escxv l9j0dhe7 du4w35lb hybvsw6c io0zqebd m5lcvass fbipl8qg nwvqtn77 k4urcfbm ni8dbmo4 stjgntxs sbcfpzgs'})

# for sigle_event in single_event_div:
for i in range (1,10):
    try:
        sigle_event=single_event_div[i]
        event_link=sigle_event.find('a')
        driver=webdriver.Chrome(ChromeDriverManager().install())
        
        driver.get('https://www.facebook.com'+event_link.get('href'))
        time.sleep(5)
        print('https://www.facebook.com'+event_link.get('href'),"uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
        soup=BeautifulSoup(driver.page_source,'html.parser')
        title=soup.find('h1',{'data-testid':'event-permalink-event-name'})
        # print(title.text)
        try:
            description_div=soup.find('div',{'id':'reaction_units'})
            description=description_div.find('div',{'class':'_63ew'}).text
        except:
            description="No Description given "
                
        # print(description.text)
        tags=soup.find_all('li',{'class':'_63ep _63eq'})


        tag_list=[]
        for t in tags:
            tag_list.append(t.text)
        
        location_ul_list=soup.find('ul',{'class','uiList _4kg _4ks'})
        timeinfo=location_ul_list.find('li')
        # print(timeinfo.text,"time info fffffffffffffffffffffffffffffff")
        if 'from' in timeinfo.text :
            startdate=timeinfo.text.split('from')[0].replace('clock','')
            enddate="NO"
            starttime=timeinfo.text.split('from')[1].split("-")[0]
            endtime=timeinfo.text.split('from')[1].split("-")[1]
            durtation="NO"
            # print(timeinfo.text,'from is there ')
            
        else:
            try:
                startdate=timeinfo.text.split("at")[0].replace('clock','')
                enddate=timeinfo.text.split("at")[1].split()[2]+timeinfo.text.split("at")[1].split()[3]+timeinfo.text.split("at")[1].split()[4]
                starttime=timeinfo.text.split("at")[1].split()[0]
                endtime=timeinfo.text.split("at")[2]
                durtation="Yes"
            except:
                startdate=timeinfo.text.split("at")[-2]
                enddate="No"
                starttime=timeinfo.text.split("at")[-1]
                endtime="NO"
                durtation="Yes"

            # print(timeinfo.text,"Not from is there ")  
        print(startdate)
        print(enddate)
        print(starttime)
        print(endtime)
        print(durtation)


        location=location_ul_list.find_all('li')
        ticket=soup.find('li',{'data-testid':'event_ticket_link'})
        if ticket is not None:
            
            ticket=ticket.find('div',{'class':'_5xhp fsm fwn fcg'}).text

        else:
            ticket="No ticket info"



     


    # for webiste 
        if location is  not None :
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







        image_div=soup.find('div',{'id':'event_header_primary'})  
        try:
            img_src=image_div.find('img').get('src')
        except:
            img_src="NO Image Url "     
        

        data_list.append(title.text)
        data_list.append(description)
        data_list.append(tag_list)
        data_list.append(startdate)
        data_list.append(starttime)
        data_list.append(endtime)
        data_list.append(enddate)
        data_list.append(durtation)
        data_list.append(online)
        data_list.append(locations)
        data_list.append(website)
        data_list.append(ticket)
        data_list.append(img_src)
        data_list.append(driver.current_url)
        # print(data_list)
        data_frame=pd.DataFrame([data_list])

        df_read=data_frame.to_csv('output.csv',mode="a" ,header=False)
        data_list.clear()
        tag_list.clear()
        driver.close()
    except:
        pass


    