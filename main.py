import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import pytesseract
import os
import wget
from PIL import Image
import pytesseract
from io import BytesIO
try:
    path = os.getcwd()
    path = os.path.join(path, "images")
    #create the directory
    os.mkdir(path)
except Exception:
    pass

search_query = input("Enter your search query: ")
driver = webdriver.Chrome() # without headless
driver.get("https://olx.in")
driver.maximize_window()
time.sleep(3)
driver.find_element(By.XPATH,"*//div/input[@data-aut-id='searchBox']").send_keys(search_query)
driver.find_element(By.XPATH,"*//div/input[@data-aut-id='searchBox']").send_keys(Keys.RETURN)

def randomdelay(min, max):
    time.sleep(random.randint(min, max))

def extract_text_from_image(image_url, name=None):
    # Create the "images" directory if it doesn't exist
    images_dir = 'images'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    if name is not None:
        save_as = os.path.join(path, name + '.jpg')
        wget.download(image_url, save_as)
    image = Image.open(save_as)
    extracted_text = pytesseract.image_to_string(image,config=r"--psm 6 --oem 3")
    return extracted_text

# Example usage:
# image_url = 'https://apollo-singapore.akamaized.net/v1/files/yb90nhk47umd3-IN/image;s=300x600;q=60'
# text = extract_text_from_image(image_url, name='my_image')
# print("\n",text)

load= int(input("Enter the number of time you want load : "))

for i in range(0, load):
    try:
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '*//button[@type="button"]/span[text() = "load more"]')))
        element.click()
        print(f"{i} times clicked load more")
        randomdelay(1, 3)
    except:
        continue

### Get all the card links

Datalist = driver.find_elements(By.XPATH,'*//li[@data-aut-id="itemBox"]')
AdUrlList=[]

for data in Datalist:
    anchor_tag = data.find_element(By.XPATH, './/a')
    url = anchor_tag.get_attribute('href')
    AdUrlList.append(url)
print(AdUrlList)


def get_formatted_date(Datedata):
    today = datetime.now().date()

    if Datedata == "Today":
        return today.strftime("%b %d, %Y")
    elif Datedata == "Yesterday":
        yesterday = today - timedelta(days=1)
        return yesterday.strftime("%b %d, %Y")
    elif Datedata == "Tomorrow":
        tomorrow = today + timedelta(days=1)
        return tomorrow.strftime("%b %d, %Y")
    elif len(Datedata) > 0:
        return Datedata + ", " + str(today.year)
    else:
        return None
#     else:
#         try:
#             date_obj = datetime.strptime(datedata, "%b %d")
#             date_with_year = date_obj.replace(year=today.year).strftime("%b %d, %Y")
#             return date_with_year
#         except ValueError:
#             print(ValueError)
#             return None

columHeader=['name', 'Salary from', 'Position Type', 'Salary period', 'Salary to','posted','imageText','imageUrl','address', 'Description']
df = pd.DataFrame(columns=columHeader)
data_list = []
print("Number of ads are :", len(AdUrlList))
imageName=1
imageText=""
for addUrl in AdUrlList:
    print(addUrl)
    driver.get(addUrl)
    name_ower="*//div[@class='eHFQs']"
    sdetils = "*//span[@data-aut-id='value_salary_from']"
    jtypeDetails = "*//span[@data-aut-id='value_job_type']"
    mperiodDetails = "*//span[@data-aut-id='value_salary_period']"
    SToPeriodDetails = "*//span[@data-aut-id='value_salary_to']"
    Description = "*//div[@data-aut-id='itemDescriptionContent']"
    date_of_post="*//div[@data-aut-id='itemCreationDate']"
    adrees="*//div//span[@class='_1RkZP']"
    
    try:
        owerdata=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,name_ower))).text
        datedata=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, date_of_post))).text
        addressdata=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,adrees))).text
        sdata=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, sdetils))).text
    #     sdata = driver.find_element(By.XPATH, sdetils).text
        jdata=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, jtypeDetails))).text
    #     jdata = driver.find_element(By.XPATH, jtypeDetails).text
        mdata=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, mperiodDetails))).text
    #     mdata = driver.find_element(By.XPATH, mperiodDetails).text
        Stopdata=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, SToPeriodDetails))).text
    #     Stopdata = driver.find_element(By.XPATH, SToPeriodDetails).text
        Descdata=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, Description))).text
        datedata= str(get_formatted_date(datedata)) # read these code understand here change into string 
        try:
            image_url=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "*//div//figure/img"))).get_attribute('src')
            imageText=extract_text_from_image(image_url, name=str(imageName))
            imageName+=1
        except:
            image_url="not found"
            imageText="not found"
        print(datedata,"image text : " ,imageText)
    except:
        print("add is not related to hdfcank it is another type need to make logic according it data field")
        continue
#   Descdata = driver.find_element(By.XPATH, Description).text
    randomdelay(1, 3)
    saveData={
        'name':owerdata,
        'Salary from': sdata,
        'Position Type': jdata,
        'Salary period': mdata,
        'Salary to': Stopdata,
        'posted':datedata,
        'imageText':imageText,
        'imageUrl':image_url,
        'adress':addressdata,
        'Description': Descdata
    }
    print(saveData)
    data_list.append(saveData)
    randomdelay(2, 3)
    # below colum keys must match which updated now
    df = pd.DataFrame(data_list, columns=columHeader)
    df.to_excel('output.xlsx', index=False)
