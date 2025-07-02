from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import time

#"""
import helperFunctionsDir.prepareDriver as prepareDriver
import helperFunctionsDir.productCategories as productCategories
import helperFunctionsDir.scrapeWebsites as scrapeWebsites
import helperFunctionsDir.helperFunctions as helperFunctions
#import helperFunctionsDir.helperFunctions as helperFunctions
#"""

"""
#for testing
import Projects.ScrapingFood.helperFunctionsDir.prepareDriver as prepareDriver
import Projects.ScrapingFood.helperFunctionsDir.productCategories as productCategories
import Projects.ScrapingFood.helperFunctionsDir.scrapeWebsites as scrapeWebsites
import Projects.ScrapingFood.helperFunctionsDir.helperFunctions as helperFunctions
"""


def main():
    
    ## ! Set up driver
    driver = initializeDriver()
    ###^

    ## ! Get website names
    websites = set()
    websites = userInputsWebsites()
    ###^
    

    for website in websites:
        ## ! checks if folder exists if not creates
        helperFunctions.doesFolderExist(website)
        ###^

        ## ! user chooses which food categories to scrape from a website
        categoryNames = set()
        categoryNames = userInputsFoodCategory()
        ###^

        ## ! detects if category has already been scraped
        newCategoryNames = set()
        newCategoryNames = helperFunctions.areCategoriesScraped(website, categoryNames)
        ###^

        ## ! for every food category
        for category in newCategoryNames:
            
            mainScraping(driver, website, category)
            helperFunctions.scrapedCategory(website, category)
        ###^
        
    
    ### Maxima Only
def initializeDriver():
    
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def userInputsWebsites():
    websites = set()
    print("What websites you want to get info from?")
    msg = """
    Maxima: m
    Rimi: r
    to quit write: q
    """
    
    toQuit = input(msg)
    while toQuit != "q" and toQuit != "Q":
        if toQuit == "m" or toQuit == "r":
            websites.add(toQuit)
        toQuit = input(msg)

    return websites


def userInputsFoodCategory():
    categoryNames = set()
    msg = """
        Bekeleja: b
        Piens: p
        Augļi: a
        Maize: m
        Gaļa: g
        Dzērieni: d
        to quit write: q
        """
    toQuit = input(msg)
    categoryNames.add(toQuit)
    
    while toQuit != "q" and toQuit != "Q":

        toQuit = input(msg)
        if toQuit == 'b' or toQuit == 'p' or toQuit == 'a' or toQuit == 'm' or toQuit == 'g' or toQuit == 'd':
            # in this loop we do not add category URLS, because thats a lot of URLS for a variable
            categoryNames.add(toQuit)
        elif toQuit == "q":
            pass
        else:
            print("not correct information")

    return categoryNames


def mainScraping(driver, website, category):
    ## ! 1. we get links from category 
    ## ! 2. for each url we open site and prepare site and then scrape it
    match website:
        case "m":
            print(website)
            urls = productCategories.getCategoryUrl(category, website)
            linkcount = 0
            for key in urls:
                for url in urls[key]:
                    print(url)
                    driver.get(url)
                    time.sleep(5)
                    
                    driver = prepareDriver.prepareMaxima(driver)
                    
                    driver, linkcount = scrapeWebsites.scrapeMaxima(driver, category, linkcount, key)

        case "r":
            print(website)
            urls = productCategories.getCategoryUrl(category, website)
            linkcount = 0
            for key in urls:
                for url in urls[key]:
                    print(url)
                    driver.get(url)
                    time.sleep(5)
                    
                    driver = prepareDriver.prepareRimi(driver)
                    
                    driver, linkcount = scrapeWebsites.scrapeRimi(driver, category, linkcount, key)
            
        case "p":
            return
            urls = productCategories.getCategoryUrl(category, website)
            for url in urls:
                driver.get(url)
                driver = prepareDriver.preparePromo(driver)
                scrapeWebsites.scrapePromo(driver)
                print("maxima")
            

        case "l":
            print(website)
            urls = productCategories.getCategoryUrl(category, website)
            linkcount = 0
            for key in urls:
                for url in urls[key]:
                    print(url)
                    driver.get(url)
                    time.sleep(5)
                    
                    driver = prepareDriver.prepareLats(driver)
                    
                    driver, linkcount = scrapeWebsites.scrapeLats(driver, category, linkcount, key)
        case "e":
            print(website)
            urls = productCategories.getCategoryUrl(category, website)
            linkcount = 0
            for key in urls:
                for url in urls[key]:
                    print(url)
                    driver.get(url)
                    time.sleep(5)
                    
                    driver = prepareDriver.prepareElvi(driver)
                    
                    driver, linkcount = scrapeWebsites.scrapeElvi(driver, category, linkcount, key)

        case "t":
            return #Top has no products to scrape
            print(website)
            urls = productCategories.getCategoryUrl(category, website)
            linkcount = 0
            for key in urls:
                for url in urls[key]:
                    print(url)
                    driver.get(url)
                    time.sleep(5)
                    
                    driver = prepareDriver.prepareElvi(driver)
                    
                    driver, linkcount = scrapeWebsites.scrapeElvi(driver, category, linkcount, key)
    ### ^


main()
