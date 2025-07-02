import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

import time



#"""
import helperFunctionsDir.helperFunctions as helperFunctions
import helperFunctionsDir.productCategories as productCategories
#import helperFunctions
#"""

"""
#forTesting
import Projects.ScrapingFood.helperFunctionsDir.helperFunctions as helperFunctions
"""
#

def scrapeMaxima(driver, category, linkCount, key):
    
    NAME_ID = "fti-product-title-category-page-"
    ALL_PRICES_ID = "fti-product-price-category-page-"

    name = []
    priceSmall = []
    priceBig = []

    for i in range(0, 52):
        #print(i)
        try:
            nameHtml = driver.find_element(By.ID, NAME_ID+str(i))
        except selenium.common.exceptions.NoSuchElementException:
            print(i)
            print("scrapeMaxima -> no more items in the page (scraped or cant find)")
            break
        
        priSep = list()
        priceForKg = ""
        try:
            priceHtml = driver.find_element(By.ID, ALL_PRICES_ID+str(i))
            
            try:
                DISCOUNT_PRICE_PATH = ".//div[@data-testid='promoColouredContainer']"
                prices = priceHtml.find_element(By.XPATH, DISCOUNT_PRICE_PATH).text
                
                ##! if only product and big forKG
                #priSep = prices.split("\n")
                #priSep[0] = priSep[0]+"."
                #priceForProduct = "".join(priSep[:3]) 
                #priceForKg = priSep[3]
                ###^
            except:
                prices = priceHtml.text
                ##! if only product and big forKG
                #priSep = prices.split("\n")
                #priSep[0] = priSep[0]+"."
                #priceForProduct = "".join(priSep[:3]) 
                #priceForKg = priSep[3]
                #print("exception reading: ", i)
                ###^
            finally:
                priSep = prices.split("\n")
                priceForKg = str(priSep[3])

            priceBig.append(str(priceForKg))
            name.append(nameHtml.text)

            
        except selenium.common.exceptions.NoSuchElementException:
            print(i)
            print("scrapeMaxima -> no more items in the page (scraped or cant find)")
            break

        #print(i)
        time.sleep(0.05)


    ## ! Saving and writing to .xlsx file
    website = "Maxima"
    try:
        linkCount = helperFunctions.saveCSV_File(website, category, linkCount, name, priceBig, key)
    except:
        linkCount = helperFunctions.saveXLSX_File(website, category, linkCount, name, priceBig, key)
        print("ScrapeMaxima -> cannot save in CSV, trying to save in XLSX")
    ### ^ 

    return driver, linkCount+1


def scrapeRimi(driver, category, linkCount, key):
    name = []
    priceSmall = []
    priceBig = []


    PRICE_WITH_CARD = "/div/div[2]/div/div[1]/div[2]/div[2]"
    CARD_CLASS = "price-per-unit"

    PRICE_WITH_REDNBLACK = "/div/div[2]/div/div[1]/div[2]/div[2]"
    BLACK_RED_CLASS = "card__price-per"


    PROD_NAME = ".//div/div[3]/p[2]"
    PROD_NAME_CLASS = "card__name"

    for i in range(1, 81):
        PROD_LOCATION = "/html/body/main/section/div[1]/div/div[2]/div[1]/div/div[2]/ul/li["+str(i)+"]"
        try:
            currentProduct = driver.find_element(By.XPATH, PROD_LOCATION)
        except:
            print(i)
            print("scrapeRimi -> no more items in the page (scraped or cant find)")
            break

        ## ! Getting product Names
        nameHtml = ""
        try:
            nameHtml = currentProduct.find_element(By.CLASS_NAME, PROD_NAME_CLASS).text
        except selenium.common.exceptions.NoSuchElementException:
            print(i)
            print("scrapeRimi -> no more items in the page (scraped or cant find)")
            break
        
        ## ! Getting product Cost
        price = ""
        try:
            price = currentProduct.find_element(By.CLASS_NAME, CARD_CLASS).text
        except:
            try:
                price = currentProduct.find_element(By.CLASS_NAME, BLACK_RED_CLASS).text
            except:
                print(i)
                print("scrapeRimi -> could not scrape price")


        name.append(nameHtml)
        priceBig.append(price)



    ## ! Saving and writing to .xlsx file
    website = "Rimi"
    try:
        linkCount = helperFunctions.saveCSV_File(website, category, linkCount, name, priceBig, key)
    except:
        linkCount = helperFunctions.saveXLSX_File(website, category, linkCount, name, priceBig, key)
        print("ScrapeRimi -> cannot save in CSV, trying to save in XLSX")
    ### ^ 

    return driver, linkCount+1


def scrapeLats(driver, category, linkCount, key):
    NAME_CLASS = "-oTitle"
    PRICE_CLASS = "-ePerUnit"
    name = []
    priceBig = []

    for i in range(1, 41):
        PROD_LOCATION = "/html/body/div[2]/div[5]/div[2]/div/div/div[1]/div/div["+str(i)+"]"
        try:
            currentProduct = driver.find_element(By.XPATH, PROD_LOCATION)
        except:
            print(i)
            print("scrapeLats -> no more items in the page (scraped or cant find)")
            break

        ## ! Getting product Names
        nameHtml = ""
        try:
            nameHtml = currentProduct.find_element(By.CLASS_NAME, NAME_CLASS).text
        except selenium.common.exceptions.NoSuchElementException:
            print(i)
            print("scrapeLats -> no more items in the page (scraped or cant find)")
            break
        
        ## ! Getting product Cost
        price = ""
        try:
            price = currentProduct.find_element(By.CLASS_NAME, PRICE_CLASS).text
        except:
            print("scrapeLats -> could not scrape price")
        name.append(nameHtml)
        priceBig.append(price)

    ## ! Saving and writing to .xlsx file
    website = "Lats"
    try:
        linkCount = helperFunctions.saveCSV_File(website, category, linkCount, name, priceBig, key)
    except:
        linkCount = helperFunctions.saveXLSX_File(website, category, linkCount, name, priceBig, key)
        print("ScrapeLats -> cannot save in CSV, trying to save in XLSX")
    ### ^ 

    return driver, linkCount+1

    pass

def scrapeElvi(driver, category, linkCount, key):
    NAME_AND_BIGPRICE_CLASS = "title"
    SMALL_PRICE_CLASS = "col.discount"
    name = []
    priceBig = []
    
    for i in range(1, 81):
        try:
            PROD_LOCATION = "/html/body/div[8]/div/ul/li["+str(i)+"]"
            currentProduct = driver.find_element(By.XPATH, PROD_LOCATION)
        except:
            print(i)
            print("scrapeElvi -> no more items in the page (scraped or cant find)")
            break
        
        nameHtml = ""
        try:
            nameNprice = currentProduct.find_element(By.CLASS_NAME, NAME_AND_BIGPRICE_CLASS).text
        except:
            print("scrapeElvi -> could no scrape name and price")
        finally:
            mutatedNameNPrice = nameNprice.split("\\n")
            nameHtml = mutatedNameNPrice[0]
            if not (";" in mutatedNameNPrice[1]):
                price = currentProduct.find_element(By.CLASS_NAME, SMALL_PRICE_CLASS).text
            else:
                price = (mutatedNameNPrice[1].split(";"))[1]
                price = price.trim()

        priceBig.append(price)
        name.append(nameHtml)



    ## ! Saving and writing to .xlsx file
    website = "Elvi"
    try:
        linkCount = helperFunctions.saveCSV_File(website, category, linkCount, name, priceBig, key)
    except:
        linkCount = helperFunctions.saveXLSX_File(website, category, linkCount, name, priceBig, key)
        print("ScrapeLats -> cannot save in CSV, trying to save in XLSX")
    ### ^ 
    return driver, linkCount+1
