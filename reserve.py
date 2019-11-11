from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from time import sleep
import sys
chrome_option = Options()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome()
base_url="https://www.thaiticketmajor.com/concert/"
userdetail_file="userdetail.json"
count=0
with open(userdetail_file, 'r') as f:
    user = json.load(f)
email=user["email"]
password=user["pwd"]
zone=user["zone"]
concert=user["concert"]
seat=int(user["seats"])
zone_list=0
show=int(user["show"])
next_zone_index=1

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
    if show<=row:
        driver.find_element_by_xpath(f"//div[@class='box-event-list']/div[2]/div[{show}]/div[2]/span[1]/a[1]").click()
        driver.implicitly_wait(30)
        
    else:
        show_new=int(input(f"please input round of show({1}-{row}): "))
        driver.find_element_by_xpath(f"//div[@class='box-event-list']/div[2]/div[{show_new}]/div[2]/span[1]/a[1]").click()
        driver.implicitly_wait(30)
    selected=driver.find_element_by_xpath(f"//*[@id='rdId']/option[1]").text
    
    if  selected=="เลือกรอบการแสดง / Select round":
        driver.find_element_by_id("rdId").click()
        driver.implicitly_wait(30)
        driver.find_element_by_xpath(f"//*[@class='select-date fix-me']/option[{show+1}]").click()
        driver.implicitly_wait(30)


def SelectZone(zone=zone):    
    global zone_list
    list_zone=driver.find_elements_by_xpath(f"//*[@class='select-zone']/div[1]/map[1]/area")
    row=zone_list=len(list_zone)
    index=0
    cur_url=nextUrl=driver.current_url
    print(f"Zone:{zone}")
    for i in range(1,row+1):
        result=find(zone,list_zone[i-1].get_attribute("href"))
        if result:
            index=i
            break
    while cur_url == nextUrl:
        driver.find_element_by_xpath(f"//*[@class='select-zone']/div[1]/map[1]/area[{index}]").click()
        driver.implicitly_wait(30)
        nextUrl=driver.current_url

def find(msg,link):
    get_zone=link.split('#')
    if msg == get_zone[2]:
        return True
    else:
        return False


        

def SelectSeat(number=seat):
    global count
    row=len(driver.find_elements_by_xpath("//*[@id='tableseats']/tbody[1]/tr"))
    for i in range(1,row+1):
        column=len(driver.find_elements_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td"))
        for j in range(2,column+1):
            text=driver.find_element_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]").text
            nrow=driver.find_element_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]").get_attribute("title")
            if text==" ":
                print(f"seats:{nrow} not available")
            if text!=" " and count<number and text!="":
                driver.find_element_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]").click()
                count+=1
            if count==number:
                break
        if count==number:
                break
    if count!=0:
        confirm_ticketprotect()

def go_to_next_zone():
    global next_zone_index
    while next_zone_index<=zone_list:
        driver.find_element_by_partial_link_text("ย้อนกลับ / Back").click()
        driver.implicitly_wait(40)
        driver.find_element_by_partial_link_text("ที่นั่งว่าง / Seats Available").click()
        driver.implicitly_wait(30)
        for j in range(2,zone_list+1):
            amount=driver.find_element_by_xpath(f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{j}]/td[2]").text
            i=driver.find_element_by_xpath(f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{j}]/td[1]").text
            if amount!="0" or amount=="Available":
                SelectZone(i)
                SelectSeat()
            next_zone_index+=1
    if count==0:
        print(f"Sorry, this concert don't have any seat for you.")
        sys.exit()


    

def confirm_ticketprotect():
    driver.find_element_by_partial_link_text("ยืนยันที่นั่ง / Book Now").click()
    driver.implicitly_wait(50)
    nextUrl=driver.current_url

    driver.find_element_by_partial_link_text("Continue").click()
    driver.implicitly_wait(40)
        

 

setUp()
Login()
SelectShow()
SelectZone(zone)
SelectSeat()
if count==0:
    go_to_next_zone()
