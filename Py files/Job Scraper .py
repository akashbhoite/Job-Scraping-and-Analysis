
#Importing the necessary libraries

from selenium import webdriver
import pandas as pd 
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
driver = webdriver.Chrome("/Users/akashbhoite/Downloads/chromedriver")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "/Users/akashbhoite/Downloads/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.linkedin.com/jobs/search?keywords=Data%20Science&location=United%20States&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0")
time.sleep(3)
close = driver.find_element_by_xpath("/html/body/div[3]/button")
close.click()

SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
           
        break
    last_height = new_height
    
for i in range(100):
    see_more = driver.find_element_by_xpath("//*[@id='main-content']/div/section/button").click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #print("for ::   ",i)
    time.sleep(2)

    

all_jobs = driver.find_elements_by_xpath("//*[@id='main-content']/div/section/ul/li")
    
for job in all_jobs: 
    title1 = job.find_element_by_tag_name("h3").text
    company = job.find_element_by_tag_name("h4").text
    location = job.find_element_by_class_name("job-result-card__location").text
    try:
        link = job.find_element_by_class_name("result-card__full-card-link").click()
    except:
        continue
    time.sleep(1)
    try:
        show_more = driver.find_element_by_xpath("//button[@aria-label='Show more']").click()
    except:
        continue
    time.sleep(1)
    try:
        desc2 = driver.find_element_by_xpath("//div[@class='show-more-less-html__markup']").text.replace("\n","").strip()
    except:
        desc2 = driver.find_element_by_xpath("//*[@id='main-content']/section/div[2]/section[2]/div/section/div").text.replace("\n","").strip()
    df = df.append({"Title":title1, "Company":company, "Location":location,"Description":desc2},ignore_index=True)
        
#Saving the scraped data to a csv file

df.to_csv("linkedin.csv",index=False)

