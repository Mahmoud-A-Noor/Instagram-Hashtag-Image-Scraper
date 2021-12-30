import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains as AC
import urllib.request


### Get Images Links by Hashtag ###
def getImagesLinks(tag, numberOfPagesToScroll, Insta_Username, Insta_Password):
    driver = webdriver.Edge("msedgedriver.exe")
    driver.get("https://www.instagram.com")

    Links = set()

    ### Login Section ###

    time.sleep(3)
    username_field = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    username_field.send_keys(Insta_Username)

    password_field = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    password_field.send_keys(Insta_Password)
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    time.sleep(5)

    ### Scraping Section ###

    link = "https://www.instagram.com/explore/tags/" + tag
    driver.get(link)
    time.sleep(5)
    for i in range(numberOfPagesToScroll):
        for c in range(5):
            AC(driver).send_keys(Keys.PAGE_DOWN).perform()  # scrolls Down the page
            time.sleep(0.2)
        time.sleep(1.5)
        row = driver.find_elements_by_class_name("FFVAD")
        for element in row:
            Links.add(element.get_attribute("src"))
    time.sleep(3)
    driver.close()
    return Links


### Save Links To Download Later ###


def saveLinksToFile(links, filename):
    with open(filename, "w") as f:
        for link in links:
            f.write(link + "\n")


### Load Links To Download ###

def loadLinksFromFile(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()


### Download Images ###

def downloadImages(links, foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    if foldername is not None:
        foldername += "\\"

    for index, link in enumerate(links):
        urllib.request.urlretrieve(link, f".\\{foldername}{index}.jpg")


### Main ###


imagesLinks = getImagesLinks(tag="dog", numberOfPagesToScroll=3, Insta_Username="Your_Username",
                             Insta_Password="Your_Password")
saveLinksToFile(links=imagesLinks, filename="dog.txt")
imagesLinks = loadLinksFromFile("dog.txt")
downloadImages(imagesLinks, foldername="dog")
