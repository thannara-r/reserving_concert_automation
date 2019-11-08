from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from time import sleep

chrome_option = Options()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome()
base_url="https://www.thaiticketmajor.com/concert/"
userdetail_file="userdetail.json"

with open(userdetail_file, 'r') as f:
    user = json.load(f)
email=user["email"]
password=user["pwd"]
zone=user["zone"]
concert=user["concert"]
seat=int(user["seats"])

def setUp():
    driver.maximize_window()
    driver.get(base_url)
    driver.implicitly_wait(30)

def Login():
    driver.find_element_by_xpath("//*[@class='btn-signin item d-none d-lg-inline-block']").click()
    sleep(1)
    username = driver.find_element_by_id("username")
    username.send_keys(email)
    pwd = driver.find_element_by_id("password")
    pwd.send_keys(password)
    driver.find_element_by_xpath("//button[@class='btn-red btn-signin']").click()
    sleep(2)
    driver.implicitly_wait(50)
    cur_url=driver.current_url
    while cur_url == base_url:
        driver.find_element_by_partial_link_text(f"{concert}").click()
        driver.implicitly_wait(30)
        cur_url=driver.current_url
    driver.implicitly_wait(30)

def SelectShow():
    row=len(driver.find_elements_by_xpath("//div[@class='box-event-list']/div[2]/div"))
    driver.implicitly_wait(30)
    
    show=int(user["show"])
    if show<=row:
        driver.find_element_by_xpath(f"//div[@class='box-event-list']/div[2]/div[{show}]/div[2]/span[1]/a[1]").click()
        driver.implicitly_wait(30)
        
    else:
        show_new=int(input(f"please input round of show({1}-{row}): "))
        driver.find_element_by_xpath(f"//div[@class='box-event-list']/div[2]/div[{show_new}]/div[2]/span[1]/a[1]").click()
        driver.implicitly_wait(30)
        

def SelectZone():
    list_zone=driver.find_elements_by_xpath("//div[@class='select-zone']/div[1]/font[2]/map[1]/area")
    row=len(list_zone)
    index=0
    for i in range(1,row+1):
        result=find(zone,list_zone[i-1].get_attribute("href"))
        if result:
            index=i
            break
    driver.find_element_by_xpath(f"//div[@class='select-zone']/div[1]/font[2]/map[1]/area[{index}]").click()
    driver.implicitly_wait(30)

def find(msg,link):
    get_zone=link.split('#')
    if msg == get_zone[2]:
        return True
    else:
        return False

def SelectSeat(number=seat):
    count=0
    row=len(driver.find_elements_by_xpath("//*[@id='tableseats']/tbody[1]/tr"))
    for i in range(1,row+1):
        column=len(driver.find_elements_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td"))
        for j in range(2,column+1):
            text=driver.find_element_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]").text
            nrow=driver.find_element_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j-1}]").text
            if text=="":
                print(f"seats:{nrow}{j} not available")
            if text!="" and count<number:
                driver.find_element_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]").click()
                count+=1
            if count==number:
                break
        if count==number:
                break
    driver.find_element_by_id("booknow").click()
    driver.implicitly_wait(30)

def confirm_ticketprotect():
    driver.find_element_by_xpath("//div[@class='confirm-ticketprotect button']/a[1]").click(30) 
    driver.implicitly_wait(30)

 

setUp()
Login()
SelectShow()
SelectZone()
SelectSeat()
confirm_ticketprotect()