import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_experimental_option("detach",True)

driver = webdriver.Chrome(options=options)

driver.get("https://www.smartprix.com/mobiles")
time.sleep(1)

driver.find_element(by=By.XPATH, value="/html/body/div[1]/main/aside/div/div[6]/div[2]/label[1]/span").click()
time.sleep(1)

driver.find_element(by=By.XPATH, value = "/html/body/div[1]/main/aside/div/div[5]/div[2]/label[2]/span").click()
time.sleep(1)

old_height = driver.execute_script("return document.body.scrollHeight")

while True:

    driver.find_element(by=By.XPATH,value="/html/body/div[1]/main/div[1]/div[2]/div[3]").click()
    time.sleep(1)

    new_height = driver.execute_script("return document.body.scrollHeight")

    print(old_height)
    print(new_height)

    if new_height == old_height:
        break

    old_height = new_height

html = driver.page_source

with open(r"D:\Projects\smartprix\smartprix.html","w",encoding="utf-8") as f:
    f.write(html)
